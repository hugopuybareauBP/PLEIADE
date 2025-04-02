import React, { useState } from 'react';
import { Upload, Loader2 } from 'lucide-react';

interface UploadAreaProps {
    onUploadSuccess: () => void;
}

const UploadArea: React.FC<UploadAreaProps> = ({ onUploadSuccess }) => {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);

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
        setIsUploading(true);
    
        const file = e.dataTransfer.files?.[0];
        if (!file) {
            setIsUploading(false);
            return;
        }
    
        const formData = new FormData();
        formData.append("file", file);
    
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/upload`, {
                method: "POST",
                body: formData,
            });
    
            if (!response.ok) {
                throw new Error("Upload failed");
            }
    
            const data = await response.json();
            console.log("Upload success:", data);
    
            // Optional: Show fake progress bar while processing
            for (let i = 0; i <= 100; i += 10) {
                setUploadProgress(i);
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            onUploadSuccess?.();
    
        } catch (error) {
            console.error("Error uploading file:", error);
        } finally {
            setIsUploading(false);
            setUploadProgress(0);
        }
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

                    <input
                        type="file"
                        id="fileInput"
                        className="hidden"
                        onChange={(e) => {
                            const file = e.target.files?.[0];
                            if (file) {
                                const fakeEvent = {
                                    preventDefault: () => { },
                                    dataTransfer: { files: [file] },
                                } as unknown as React.DragEvent;
                                handleDrop(fakeEvent);
                            }
                        }}
                    />

                    <label htmlFor="fileInput">
                        <button className="mt-4 px-6 py-2 bg-white text-[#6c03a8] rounded-lg font-medium hover:bg-white/90 transition-colors">
                            Choose File
                        </button>
                    </label>
                </>
            )}
        </div>
    );
      
}

export default UploadArea;