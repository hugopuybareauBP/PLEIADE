import React, { useEffect, useState } from 'react';
import { CheckCircle2, XCircle } from 'lucide-react';

interface Chapter {
    chapter_name: string;
    raw_output: string;
}

interface Character {
    character_name: string;
    description: string;
}

interface AnalysisData {
    synopsis: string;
    impact: {
        strengths: string[];
        weaknesses: string[];
    };
    characters: Character[];
    chapters: Chapter[];
}

interface Props {
    bookId: string;
}

const AnalysisTab: React.FC<Props> = ({ bookId }) => {
    const [data, setData] = useState<AnalysisData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAnalysis = async () => {
            setLoading(true);

            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/details`);
                const details = await res.json();
                setData(details.analysis);
            } catch (err) {
                console.error("Failed to load analysis", err);
            } finally {
                setTimeout(() => setLoading(false), 300);
            }
        };

        fetchAnalysis();
    }, [bookId]);

    if (loading || !data) {
        return (
            <div className="text-white">
                <p>Generating analysis...</p>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {data.synopsis && (
                <div className="bg-white/5 rounded-lg p-6 mb-6">
                    <h3 className="text-xl font-semibold mb-4">Synopsis</h3>
                    <p className="text-white/70">{data.synopsis}</p>
                </div>
            )}

            <div className="bg-white/5 rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-4">Impact Analysis</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <div className="flex items-center mb-3">
                            <CheckCircle2 className="h-5 w-5 text-emerald-400 mr-2" />
                            <h4 className="text-lg font-medium">Strengths</h4>
                        </div>
                        <ul className="space-y-3">
                            {data.impact.strengths.map((point, idx) => (
                                <li key={idx} className="text-white/70">• {point}</li>
                            ))}
                        </ul>
                    </div>
                    <div>
                        <div className="flex items-center mb-3">
                            <XCircle className="h-5 w-5 text-red-400 mr-2" />
                            <h4 className="text-lg font-medium">Areas for Improvement</h4>
                        </div>
                        <ul className="space-y-3">
                            {data.impact.weaknesses.map((point, idx) => (
                                <li key={idx} className="text-white/70">• {point}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>

            <div className="bg-white/5 rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-4">Chapter Breakdown</h3>
                <ul className="space-y-3">
                    {data.chapters.map((chapter, index) => (
                        <div key={index} className="flex items-start space-x-4">
                            <span className="w-8 h-8 bg-white/10 rounded-full flex items-center justify-center">
                                {index + 1}
                            </span>
                            <div>
                                <h4 className="font-medium">{chapter.chapter_name}</h4>
                                <p className="text-white/70 text-sm mt-1">{chapter.raw_output}</p>
                            </div>
                        </div>
                    ))}
                </ul>
            </div>

            <div className="bg-white/5 rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-4">Character Profiles</h3>
                <ul className="space-y-3">
                    {data.characters.map((character, index) => (
                        <div key={index} className="border-b border-white/10 pb-4">
                            <h4 className="font-medium mb-2">{character.character_name}</h4>
                            <p className="text-white/70">{character.description}</p>
                        </div>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default AnalysisTab;
