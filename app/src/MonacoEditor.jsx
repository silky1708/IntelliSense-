import React from "react";
import { Monaco } from "@monaco-editor/react";
import Editor from '@monaco-editor/react'

const MonacoEditor = () => {
    return (
        <div style={{ height: "90vh" }}>
            <Editor
                height="90vh"
                width="100%"
                theme="vs-dark"
                defaultLanguage="python"
                defaultValue="// Start typing here..."
                beforeMount={handleEditorWillMount} // Hook for registering customizations
            />
        </div>
    );
};

// Custom IntelliSense logic
function handleEditorWillMount(monaco) {
    monaco.languages.registerCompletionItemProvider("python", {
        triggerCharacters: [".", '"', "'"], // Characters that trigger suggestions
        provideCompletionItems: (model, position) => {
            // Get the text before the cursor
            const word = model.getWordUntilPosition(position);
            const range = {
                startLineNumber: position.lineNumber,
                startColumn: word.startColumn,
                endLineNumber: position.lineNumber,
                endColumn: word.endColumn,
            };

            // Return suggestions
            return {
                suggestions: [
                    {
                        label: "console.log",
                        kind: monaco.languages.CompletionItemKind.Function,
                        insertText: "console.log(${1:message});",
                        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                        range: range,
                    },
                    {
                        label: "alert",
                        kind: monaco.languages.CompletionItemKind.Function,
                        insertText: "alert(${1:message});",
                        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                        range: range,
                    },
                ],
            };
        },
    });
}

export default MonacoEditor;