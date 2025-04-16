import React, { useState, useRef } from 'react';
import { Upload, Loader2 } from 'lucide-react';

interface UploadAreaProps {
    onUploadSuccess: () => void;
}

const UploadArea: React.FC<UploadAreaProps> = ({ onUploadSuccess }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [title, setTitle] = useState("");
    const [author, setAuthor] = useState("");
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [coverFile, setCoverFile] = useState<File | null>(null);
    const manuscriptInputRef = useRef<HTMLInputElement | null>(null);
    const coverInputRef = useRef<HTMLInputElement | null>(null);

    const handleUpload = async () => {
        if (!selectedFile) return;

        setIsUploading(true);
        const formData = new FormData();
        formData.append("file", selectedFile);
        if (coverFile) formData.append("cover", coverFile);
        formData.append("title", title);
        formData.append("author", author);

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/upload`, {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            console.log("Upload success:", data);
            onUploadSuccess?.();
        } catch (err) {
            console.error("Error uploading:", err);
        } finally {
            setIsUploading(false);
            setUploadProgress(0);
            setSelectedFile(null);
            setCoverFile(null);
            setTitle("");
            setAuthor("");
        }
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = async (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files?.[0];
        if (!file) return;

        setSelectedFile(file);
    };

    return (
        <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${isDragging
                ? "border-white bg-white/10"
                : "border-white/50 hover:border-white hover:bg-white/5"
                }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
        >
            {isUploading ? (
                <div className="space-y-4">
                    <Loader2 className="h-12 w-12 text-white animate-spin mx-auto" />
                    <div className="w-full bg-white/20 rounded-full h-2.5">
                        <div
                            className="bg-white h-2.5 rounded-full transition-all duration-300"
                            style={{ width: `${uploadProgress}%` }}
                        ></div>
                    </div>
                    <p className="text-white text-lg">
                        Analyzing your book... {uploadProgress}%
                    </p>
                </div>
            ) : (
                <>
                    <Upload className="h-12 w-12 text-white mx-auto mb-4" />
                    <p className="text-white text-lg mb-2">
                        Drag and drop your manuscript here
                    </p>
                    <p className="text-white/70">or</p>

                    {/* 👇 Hidden manuscript file input */}
                    <input
                        type="file"
                        id="manuscriptInput"
                        ref={manuscriptInputRef}
                        accept=".txt"
                        className="hidden"
                        onChange={(e) => {
                            const file = e.target.files?.[0];
                            if (file) {
                                setSelectedFile(file);
                            }
                        }}
                    />
                    <label htmlFor="manuscriptInput">
                        <button
                            className="mt-4 px-6 py-2 bg-white text-[#6c03a8] rounded-lg font-medium hover:bg-white/90 transition-colors"
                            onClick={() => manuscriptInputRef.current?.click()}
                        >
                            Choose a manuscript
                        </button>
                    </label>

                    {/* 👇 Form inputs */}
                    <div className="flex flex-col items-center mt-4 gap-2">
                        <input
                            type="text"
                            placeholder="Title"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            className="p-2 rounded w-full max-w-md"
                        />
                        <input
                            type="text"
                            placeholder="Author"
                            value={author}
                            onChange={(e) => setAuthor(e.target.value)}
                            className="p-2 rounded w-full max-w-md"
                        />

                        {/* 👇 Cover input */}
                        <input
                            type="file"
                            accept="image/*"
                            ref={coverInputRef}
                            id="coverInput"
                            className="hidden"
                            onChange={(e) => setCoverFile(e.target.files?.[0] ?? null)}
                        />
                        <label htmlFor="coverInput">
                            <button
                                className="mt-1 px-6 py-2 bg-white text-[#6c03a8] rounded-lg font-medium hover:bg-white/90 transition-colors"
                                onClick={() => coverInputRef.current?.click()}
                            >
                                Add a cover
                            </button>
                        </label>
                    </div>

                    {/* 👇 File + Cover Preview */}
                    {selectedFile && (
                        <div className="text-white mt-4">
                            <p className="font-medium">📘 Selected manuscript:</p>
                            <p className="italic">{selectedFile.name}</p>
                        </div>
                    )}

                    {coverFile && (
                        <div className="text-white mt-4 flex flex-col items-center">
                            {/* <p className="font-medium mb-2">🖼️ Cover preview:</p> */}
                            <img
                                src={URL.createObjectURL(coverFile)}
                                alt="Cover preview"
                                className="rounded-md max-h-40"
                            />
                        </div>
                    )}


                    {selectedFile && (
                        <p className="text-white text-sm mt-2 italic">
                            Ready to upload – don’t forget title, author, and cover!
                        </p>
                    )}

                    {/* 👇 Final upload button */}
                    <button
                        className={`mt-6 px-6 py-2 rounded-lg font-medium transition-colors
                            ${selectedFile
                                ? "bg-white text-[#6c03a8] hover:bg-white/90"
                                : "bg-white/40 text-white cursor-not-allowed"
                            }`}
                        onClick={handleUpload}
                        disabled={!selectedFile}
                    >
                        Upload Book
                    </button>
                </>
            )}
        </div>
    );
};

export default UploadArea;
