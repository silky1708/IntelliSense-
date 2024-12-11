import React, { useState } from "react";
import Editor from "react-simple-code-editor";
import Prism from "prismjs"; // For syntax highlighting
import "prismjs/themes/prism.css"; // Import a Prism theme
import "prismjs/components/prism-javascript"; // Add language support

const MinimalCodeEditor = () => {
    const [code, setCode] = useState("// Write your code here...");

    // Syntax highlighting function
    const highlightCode = (code) =>
        Prism.highlight(code, Prism.languages.javascript, "python");

    return (
        <div style={{ border: "1px solid #ccc", borderRadius: "4px", padding: "10px" }}>
            <Editor
                value={code}
                onValueChange={setCode}
                highlight={highlightCode}
                padding={10}
                style={{
                    fontFamily: "'Fira Code', monospace",
                    fontSize: 14,
                    minHeight: "200px",
                }}
            />
        </div>
    );
};

export default MinimalCodeEditor;
