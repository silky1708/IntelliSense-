import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'

// import Editor from '@monaco-editor/react'
import axios from 'axios'
import './App.css'

import React from "react";
// import MonacoEditor from "./MonacoEditor";
import MinimalCodeEditor from './MinimalCodeEditor'
import CodeEditorWithSuggestions from './CodeEditorwithSuggestions'

const App = () => {
    return (
        <div>
            {/* <h1>Python Code Editor with Custom IntelliSense</h1> */}
            <CodeEditorWithSuggestions />
        </div>
    );
};

export default App;







// function App() {
//   function handleEditorChange(value, event) {
//     console.log('here is the current code:', value);
//   }
//   return (
//     <div className='App'>
//        <Editor 
//         height="90vh"
//         width="100%"
//         theme="vs-dark"
//         defaultLanguage='python'
//         onChange={handleEditorChange}
//         saveViewState={true}
//        />
//     </div>
//   )
// }

// export default App
