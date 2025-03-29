import React, { useRef, forwardRef, useImperativeHandle } from "react";
import Editor from "@monaco-editor/react";

const MonacoEditor = forwardRef((props, ref) => {
    const editorRef = useRef(null);

    useImperativeHandle(ref, () => ({
        setValue: (value) => {
            if (editorRef.current) {
                editorRef.current.setValue(value);
            }
        }
    }));

    function handleEditorDidMount(editor, monaco) {
        editorRef.current = editor;

        // Register Monkey Language
        monaco.languages.register({ id: "monkey" });

        // Define syntax highlighting
        monaco.languages.setMonarchTokensProvider("monkey", {
            keywords: ["let", "fn", "return", "if", "else", "true", "false"],
            operators: ["=", "+", "-", "*", "/", "==", "!=", ">", "<"],
            symbols: /[=><!~?:&|+\-*\/\^%]+/,
            tokenizer: {
                root: [
                    [/\b(let|fn|return|if|else|true|false)\b/, "keyword"],
                    [/\b[a-zA-Z_]\w*(?=\()/, "function"],
                    [/\b[a-zA-Z_]\w*\b/, "identifier"],
                    [/\b\d+\b/, "number"],
                    [/@symbols/, "operator"],
                    [/".*?"/, "string"],
                    [/\/\/.*/, "comment"],
                    [/\/\*/, "comment", "@comment"],
                ],
                comment: [
                    [/\*\//, "comment", "@pop"],
                    [/./, "comment"],
                ],
            },
        });

        // Auto-closing brackets and indentation rules
        monaco.languages.setLanguageConfiguration("monkey", {
            autoClosingPairs: [
                { open: "{", close: "}" },
                { open: "(", close: ")" },
                { open: "[", close: "]" },
                { open: '"', close: '"' },
            ],
            surroundingPairs: [
                { open: "{", close: "}" },
                { open: "(", close: ")" },
                { open: "[", close: "]" },
                { open: '"', close: '"' },
            ],
            brackets: [["{", "}"], ["(", ")"], ["[", "]"]],
            indentationRules: {
                increaseIndentPattern: /{\s*$/,
                decreaseIndentPattern: /^}/,
            },
        });

        // Define custom black theme
        monaco.editor.defineTheme("black-theme", {
            base: "vs-dark",
            inherit: true,
            rules: [
                { token: "", foreground: "ffffff", background: "000000" },
                { token: "comment", foreground: "808080" },
                { token: "string", foreground: "00ff00" },
                { token: "keyword", foreground: "ff00ff" },
                { token: "number", foreground: "ffcc00" }
            ],
            colors: {
                "editor.background": "#000000",
                "editor.foreground": "#ffffff",
                "editorCursor.foreground": "#ffffff",
                "editorLineNumber.foreground": "#888888",
                "editorLineNumber.activeForeground": "#ffffff",
                "editor.selectionBackground": "#333333",
                "editor.inactiveSelectionBackground": "#222222"
            }
        });

        // Apply custom theme
        monaco.editor.setTheme("black-theme");
    }

    return (
        <div style={{ width: "100%", height: "700px" }}>
            <Editor
                height="100%"
                width="100%"
                defaultLanguage="monkey"
                defaultValue={props.value || ""}
                theme="black-theme"
                onMount={handleEditorDidMount}
                onChange={props.onChange}
                options={{
                    fontSize: 18,
                    automaticLayout: true,
                    minimap: { enabled: false },
                }}
            />
        </div>
    );
});

export default MonacoEditor;
