import React, { useState } from "react";
import "./MainPage.css";
import SummaryStream from "./SummaryStream";

export default function MainPage() {
    const [file, setFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState("");
    const [isDragOver, setIsDragOver] = useState(false);
    const [textData, setTextData] = useState({ full_text: "", filename: "", chunks: []});
    const [summaries, setSummaries] = useState([]);
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
            const url = `http://localhost:8000/${endpoint}`;
            console.log(`Payload to backend : `, textData)
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

    async function handleStreamedSummary() {
        setSummaries([]); // reset previous summaries
          
        const response = await fetch("http://localhost:8000/summarize/stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(textData),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        let buffer = "";

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            const parts = buffer.split("\n\n");
            buffer = parts.pop(); // keep the last part in buffer

            for (const part of parts) {
                if (part.startsWith("data: ")) {
                    const jsonData = JSON.parse(part.replace("data: ", ""));
                    setSummaries((prev) => [...prev, jsonData]);
                }
            }
        }
    }

    return (
        <div className="App">
            <div className="bearing-point">BearingPoint</div>
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
                                <button onClick={handleStreamedSummary}>📝 Summarize (Streamed) </button>
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

                    {summaries.length > 0 && (
                        <div className="stats-container">
                            <h2>📝 Summaries for: <code>{textData.filename}</code></h2>
                            {summaries.map((chunk) => (
                                <div key={chunk.chunk_id} style={{ marginBottom: "20px" }}>
                                    <h4>Chunk {chunk.chunk_id}</h4>
                                    <div className="stream-wrapper"><SummaryStream text={chunk.summary}/></div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );  
}

