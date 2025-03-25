import React, { useState } from "react";
import "./UploadPage.css";

export default function UploadPage() {
    const [file, setFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState("");
    const [isDragOver, setIsDragOver] = useState(false);
    const [textData, setTextData] = useState({ full_text: "", filename: "" });
    const [result, setResult] = useState(null);

    function handleDragOver(e) {
        e.preventDefault();
        setIsDragOver(true);
    }

    function handleDragLeave(e) {
        e.preventDefault();
        setIsDragOver(false);
    }

    function handleDrop(e) {
        e.preventDefault();
        setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        setFile(e.dataTransfer.files[0]);
        setUploadStatus("");
        }
    }

    function handleFileChange(e) {
        setFile(e.target.files[0]);
        setUploadStatus("");
    }

    async function handleUpload() {
        if (!file) {
            setUploadStatus("No file selected.");
            return;
        }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://localhost:8000/upload", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        setTextData(data);
        setUploadStatus(`Upload successful: ${data.filename}`);
    } catch (err) {
            console.error(err);
            setUploadStatus(`Error: ${err.message}`);
        }
    }

    async function handleAnalysis(endpoint) {
        if (!textData.full_text) {
            setUploadStatus("Please upload a file first.");
            return;
        }

    try {
        // const url = `http://localhost:8000/${endpoint}`;
        const url = `http://localhost:8000/spacy-stats`;
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(textData),
        });

        const data = await response.json();
        console.log("[DEBUG] Full result from backend:", data);
        setResult(data);

    } catch (err) {
            console.error("[ERROR] Request failed", err);
            setResult({ error: "Analysis failed." });
        }
    }

    return (
        <div className="App">
            <h1 className="app-title">Pleiade</h1>
            <div className="container-boarder">
            <div className="container">
                <h1>📚 Manuscript Analyzer</h1>
            <div
                className={`drag-drop-zone ${isDragOver ? "drag-over" : ""}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
            >
                <h3>Drag and drop your file here, or click to select.</h3>
                <input type="file" onChange={handleFileChange} />
            </div>

            <button onClick={handleUpload}>Upload File</button>

            {file && <p>📄 Selected File: {file.name}</p>}
            {uploadStatus && <p>{uploadStatus}</p>}

            {textData.full_text && (
            <div style={{ marginTop: "20px" }}>
                <h3>Choose Analysis:</h3>
                <button onClick={() => handleAnalysis("spacy-stats")}>🔍 Spacy Stats</button>{" "}
                <button onClick={() => handleAnalysis("sentiment")}>😊 Sentiment Analysis</button>{" "}
                <button onClick={() => handleAnalysis("summary")}>📝 Summarize</button>
            </div>
            )}

            {result && result.features && (
                <div className="stats-container">
                    <h2>SpaCy Stats for: <code>{result.filename}</code></h2>
                    <table className="stats-table">
                        <thead>
                            <tr>
                                <th>Feature</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            {Object.entries(result.features).map(([key, value]) => (
                                <tr key={key}>
                                    <td>{key}</td>
                                    <td>{typeof value === 'number' ? value.toFixed(2) : value}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* {result && (
                <div className="result">
                    <h3>📊 Result:</h3>
                    <pre>{JSON.stringify(result, null, 2)}</pre>
                </div>
            )} */}
            </div>
            </div>
        </div>
    );  
}
