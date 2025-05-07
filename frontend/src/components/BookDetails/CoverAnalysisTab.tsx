import React, { useEffect, useState } from 'react';
import classNames from 'classnames';

interface CoverElement {
    category: string;
    title: string;
    description: string;
    icon?: string;
}

interface Props {
    bookId: string;
    cover: string;
}

const emojiColorMap: Record<string, string> = {
    "🔥": "border-orange-500",
    "❤️": "border-red-500",
    "🧠": "border-pink-500",
    "✍️": "border-yellow-500",
    "🎭": "border-blue-500",
    "🌌": "border-indigo-500",
    "💻": "border-gray-500",
    "⚖️": "border-neutral-500",
};

const CoverAnalysisTab: React.FC<Props> = ({ bookId, cover }) => {
    const [data, setData] = useState<CoverElement[] | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCoverAnalysis = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/cover_analysis_tab/${bookId}`);
                const analysis = await res.json();
                setData(analysis);
            } catch (err) {
                console.error("Failed to load cover analysis", err);
            } finally {
                setLoading(false);
            }
        };
        fetchCoverAnalysis();
    }, [bookId]);

    if (loading || !data) {
        return <p className="text-white animate-pulseSlow">Analyzing cover...</p>;
    }

    return (
        <div className="flex flex-col md:flex-row gap-6 animate-fadeIn">
            {/* Cover side (33%) */}
            <div className="md:w-1/3 w-full flex justify-center">
                <div className="rounded-2xl shadow-xl overflow-hidden transition-transform duration-300 hover:scale-105">
                    <img
                        src={`${import.meta.env.VITE_API_URL}${cover}`}
                        alt="Book cover"
                        className="max-h-[600px] object-contain"
                    />
                </div>
            </div>

            {/* Comments side (66%) */}
            <div className="md:w-2/3 w-full space-y-6">
                {data.map((item, i) => {
                    const borderColor = item.icon && emojiColorMap[item.icon] ? emojiColorMap[item.icon] : "border-white/20";
                    return (
                        <div
                            key={i}
                            className={classNames(
                                "rounded-lg border-l-4 p-4 bg-white/5 transform transition-all duration-300 hover:scale-[1.02] hover:bg-white/10 opacity-0 animate-fadeIn",
                                borderColor
                            )}
                            style={{ animationDelay: `${i * 100}ms`, animationFillMode: "forwards" }}
                        >
                            <div className="flex items-center gap-2 mb-2">
                                {item.icon && <span className="text-xl">{item.icon}</span>}
                                <h3 className="text-lg font-semibold text-white/90">{item.category}</h3>
                            </div>
                            <p className="text-white text-md font-medium mb-1">"{item.title}"</p>
                            <p className="text-white/70">{item.description}</p>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default CoverAnalysisTab;
