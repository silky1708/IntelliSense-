from flask import Flask, jsonify, render_template, url_for, request
from flask_cors import CORS

import sys
sys.path.insert(0, 'quac/quac')
from main import type_inference

import json
import ast
import re


app = Flask(__name__)
cors = CORS(app, origins='*')


K = 3      # how many suggestions to display??


@app.route("/")
def index():
    return "server is up and running!"


def strip_non_alphanumeric(s):
    return re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', s)


def parse_global_imports(code):
    global_imports = {}
    for line in code.splitlines():
        words = list(filter(lambda x: not x == '', line.split(' ')))
        if "import" in words and not words[0].startswith('#'):
            import_idx = words.index("import")
            module = words[import_idx+1] if import_idx+1 < len(words) else None
            module = module.split('.')[-1]  # [TODO] torchvision.transforms -- should store as torchvision.transforms or transforms?
            alias = module
            # alias present
            if 'as' in words:
                as_idx = words.index('as')
                alias = words[as_idx+1] if as_idx+1 < len(words) else None

            assert not module is None, f"{line} -> imported module not defined!"
            assert not alias is None, f"{line} -> alias not defined!" 
            global_imports[module] = alias
    
    return global_imports


def parse_global_variables(code):
    tree = ast.parse(code)
    global_variables = {}

    for node in ast.walk(tree):
        # Check for assignment statements (ast.Assign)
        if isinstance(node, ast.Assign):
            # Global variables are those assigned at the module level
            for target in node.targets:
                if isinstance(target, ast.Name):  # Ensure it's a variable
                    var_name = target.id
                    var_value = node.value

                    # Determine the type of the assigned value
                    if isinstance(var_value, ast.Constant):  # For constants
                        value = var_value.value
                        var_type = type(value).__name__
                    elif isinstance(var_value, ast.Name):  # For other variables
                        value = var_value.id
                        var_type = "variable"  # Just refer to another variable
                    elif isinstance(var_value, ast.Call):  # Function call (e.g., list, dict)
                        value = f"Function call: {ast.dump(var_value)}"
                        var_type = "call"
                    else:
                        value = "Unknown"
                        var_type = "unknown"
                    
                    # Add to the globals_info dictionary
                    global_variables[var_name] = {'type': var_type, 'value': value}

    return global_variables


def parse_quac_output(quac_dict, params_db):
    fn_name_to_return_types = {}
    temp_preds = quac_dict.get("temp", {})
    global_fn_types = temp_preds.get("global", {})
    for fname,v in global_fn_types.items():
        return_types = v["return"]
        return_types = [strip_non_alphanumeric(ret.split('.')[-1]) for ret in return_types] # builtins.int -> int
        if len(return_types) == 1:
            return_types = return_types[0]
        fn_name_to_return_types[fname] = return_types

        # support for local advanced intellisense -- add global functions to database
        params_db[fname] = {fname: []}
        for param_name,param_type in v.items():
            if param_name == "return":
                continue
            param_type = [strip_non_alphanumeric(ret.split('.')[-1]) for ret in param_type]
            if len(param_type) == 1:
                param_type = param_type[0]
            
            params_db[fname][fname].append({
                "name": param_name,
                "type": param_type
            })

    return fn_name_to_return_types


def resolve_nonliteral_variables(global_variables, global_functions):
    resolved_global_variables = {}
    for var_name,v in global_variables.items():
        if v['type'] == 'variable':  # variable assignment, for e.g., a = b; b = z so on
            rhs_var = v['value']
            while global_variables[rhs_var]['type'] == 'variable':
                rhs_var = global_variables[rhs_var]['value']
            rhs_var_value = global_variables[rhs_var]
            resolved_global_variables[var_name] = rhs_var_value['type']

        elif v['type'] == 'call': # function call e.g., a = sum(...)
            rhs_fn = v['value']   # "Function call: Call(func=Name(id='add', ctx=Load()), args=[Constant(value=3), Constant(value=4)], keywords=[])"
            rhs_fn = rhs_fn.split('id=')[-1].split("'")[1]  # add, fib
            fn_type = global_functions.get(rhs_fn, "Unknown")
            resolved_global_variables[var_name] = fn_type

        else:
            resolved_global_variables[var_name] = v['type']

    return resolved_global_variables


def get_module_and_function(code_context):
    # which function does the user need help with? last line, last word
    func_call = strip_non_alphanumeric(code_context.split('\n')[-1].split(' ')[-1])  # hopefully, get one of [linspace, np.linspace, numpy.linspace,]
    modules_and_funcs = func_call.split('.')
    assert len(modules_and_funcs) > 0, f"can't parse the function from {code_context}"

    module = None
    if len(modules_and_funcs) > 2:
        raise Exception(f"{func_call} not yet supported :(")
    elif len(modules_and_funcs) == 2:
        module = modules_and_funcs[0]
        func = modules_and_funcs[1]
    else:
        func = modules_and_funcs[0]

    return module, func


def get_parameters_metadata(module, func, global_imports, params_db):
    if module is not None:
        for imported,alias in global_imports.items():
            if alias == module:
                return params_db[imported][func]
    
    for k,v in params_db.items():
        if func in v:
            return v[func]
    
    return None


@app.route("/suggest", methods=['GET', 'POST'])
def get_suggestion():
    if request.method == 'POST':
        data = request.json  # Parses the body as JSON
        code_context = data.get('code_context', '')
        print('code received!\n', code_context)

        global_imports = parse_global_imports(code_context)
        with open('params_db.json', 'r') as fp:
            params_db = json.load(fp)
        module, func = get_module_and_function(code_context)
        
        code_context_wo_last_line = '\n'.join(code_context.split('\n')[:-1])
        global_variables = parse_global_variables(code_context_wo_last_line)

        print('Global imports:\n', global_imports)
        print('Global variables:\n', global_variables)
        # run type inference -- quac is decent for global functions. drop the last (malformed) line (since it might give compile error with Quac)
        quac_output_dict = type_inference(code_context_wo_last_line)
        print("****** Quac predictions: \n", quac_output_dict)
        global_functions = parse_quac_output(quac_output_dict, params_db)

        print('global vars:', global_variables)
        resolved_global_variables = resolve_nonliteral_variables(global_variables, global_functions)
        print('resolved_global_vars:', resolved_global_variables)
        
        # candidates = global_functions | resolved_global_variables  # merge two dicts
        print('candidates:\n', global_functions | resolved_global_variables)
        suggestions = []
        param_metadata = get_parameters_metadata(module, func, global_imports, params_db)

        if not param_metadata is None:
            for param in param_metadata:
                name = param.get("name", "")
                typeParam = param.get("type", "")
                default_value = param.get("default_value", "")
                description = param.get("description", "")

                # take max K from each of variables and functions
                suggestionsList = list(filter(lambda k: resolved_global_variables[k] in typeParam, resolved_global_variables.keys()))[-K:]
                suggestionsList += list(filter(lambda k: global_functions[k] in typeParam, global_functions.keys()))[-K:]
                suggestions.append({
                    "name": name,
                    "type": typeParam,
                    "default_value": default_value,
                    "description": description,
                    "suggestions": suggestionsList
                })

        output_dict = {
            "message": "OK",
            "suggestions": suggestions
        }

        response = jsonify(output_dict)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response



if __name__=="__main__":
    app.run(debug=True, use_reloader=False)