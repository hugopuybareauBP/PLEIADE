// frontend/src/components/BookDetails/AnalysisTab.tsx

import React, { useEffect, useState } from 'react';
import { CheckCircle2, XCircle } from 'lucide-react';

interface Chapter {
    title: string;
    summary: string;
  }
  
  interface Character {
    group: string;
    description: string;
  }
  
  interface AnalysisData {
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
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/analysis_marketing`);
                const json = await res.json();
                setData(json.analysis);
            } catch (err) {
                console.error("Failed to load analysis", err);
            } finally {
                setLoading(false);
            }
        };
        fetchAnalysis();
    }, [bookId]);

    if (loading || !data) {
        return <p className="text-white">Generating analysis...</p>;
    }

    return (
        <div className="space-y-6">
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
                        console.log("CHAPTER", chapter),
                        <div key={index} className="flex items-start space-x-4">
                            <span className="w-8 h-8 bg-white/10 rounded-full flex items-center justify-center">
                                {index + 1}
                            </span>
                            <div>
                                <h4 className="font-medium">{chapter.title}</h4>
                                <p className="text-white/70 text-sm mt-1">{chapter.summary}</p>
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
                            <h4 className="font-medium mb-2">{character.group}</h4>
                            <p className="text-white/70">{character.description}</p>
                        </div>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default AnalysisTab;