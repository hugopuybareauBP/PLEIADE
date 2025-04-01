import React, { useState } from 'react';
import { Upload, Loader2 } from 'lucide-react';

const UploadArea = () => {
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

        // Simulate upload progress
        for (let i = 0; i <= 100; i += 10) {
            setUploadProgress(i);
            await new Promise(resolve => setTimeout(resolve, 200));
        }

        setIsUploading(false);
        setUploadProgress(0);
    };

    return (
        <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${isDragging
                ? 'border-white bg-white/10'
                : 'border-white/50 hover:border-white hover:bg-white/5'
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
                    <p className="text-white text-lg">Analyzing your book... {uploadProgress}%</p>
                </div>
            ) : (
                <>
                    <Upload className="h-12 w-12 text-white mx-auto mb-4" />
                    <p className="text-white text-lg mb-2">
                        Drag and drop your manuscript here
                    </p>
                    <p className="text-white/70">or</p>
                    <button className="mt-4 px-6 py-2 bg-white text-[#6c03a8] rounded-lg font-medium hover:bg-white/90 transition-colors">
                        Choose File
                    </button>
                </>
            )}
        </div>
    );
}

export default UploadArea;