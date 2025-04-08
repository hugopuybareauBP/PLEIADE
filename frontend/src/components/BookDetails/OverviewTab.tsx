import React, { useEffect, useState } from 'react';
import {
    Clock,
    FileText,
    BookOpen,
    BarChart2,
    Users,
    MapPin,
    Calendar,
    BookType,
    MessageCircle,
    Tag
} from 'lucide-react';

interface OverviewTabProps {
    bookId: string;
}

const OverviewTab = ({ bookId }: OverviewTabProps) => {
    const [data, setData] = useState<any | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchDetails = async () => {
            try {
                console.log("Backend URL:", import.meta.env.VITE_API_URL);
                const res = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/details`);
                const details = await res.json();
                setData(details.overview);
            } catch (err) {
                console.error("Error fetching book details:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchDetails();
    }, [bookId]);

    if (loading || !data) {
        return <p className="text-white">Generating overview...</p>;
    }

    return (
        <div className="space-y-6">
            {data?.synopsis && (
                <div className="bg-white/5 rounded-lg p-6 mb-6">
                    <h3 className="text-xl font-semibold mb-4">Synopsis</h3>
                    <p className="text-white/70">{data.synopsis}</p>
                </div>
            )}

            {/* Key Data */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white/5 rounded-lg p-6">
                    <h3 className="text-lg font-semibold mb-4">Key Data</h3>
                    <div className="space-y-4">
                        <OverviewItem icon={<Clock />} label="Estimated Reading Time" value={data.keyData.estimatedReadingTime} />
                        <OverviewItem icon={<FileText />} label="Word Count" value={data.keyData.wordCount} />
                        <OverviewItem icon={<BookOpen />} label="Number of Pages" value={data.keyData.pages} />
                        <OverviewItem icon={<BarChart2 />} label="Number of Chapters" value={data.keyData.chapters} />
                        <OverviewItem icon={<Users />} label="Main Characters" value={data.keyData.mainCharacters} />
                        <OverviewItem icon={<MapPin />} label="Key Locations" value={data.keyData.keyLocations} />
                    </div>
                </div>

                {/* Content Analysis */}
                <div className="bg-white/5 rounded-lg p-6">
                    <h3 className="text-lg font-semibold mb-4">Content Analysis</h3>
                    <div className="space-y-4">
                        <OverviewItem icon={<Calendar />} label="Time Period" value={data.contentAnalysis.timePeriod} />
                        <OverviewItem icon={<BookType />} label="Genres" value={data.contentAnalysis.genres} />
                        <OverviewItem icon={<MessageCircle />} label="Overall Tone" value={data.contentAnalysis.tone} />
                        <div className="flex items-start space-x-3">
                            <Tag className="h-5 w-5 text-white/50 mt-1" />
                            <div>
                                <dt className="text-white/50">Key Words</dt>
                                <dd className="text-white font-medium">
                                    <div className="flex flex-wrap gap-2 mt-1">
                                        {data.contentAnalysis.keywords.map((k: string) => (
                                            <span key={k} className="px-2 py-1 bg-white/10 rounded-full text-sm">{k}</span>
                                        ))}
                                    </div>
                                </dd>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Classification */}
            <div className="bg-white/5 rounded-lg p-6">
                <h3 className="text-lg font-semibold mb-3">Classification</h3>
                <dl className="space-y-3">
                    <div>
                        <dt className="text-white/50">Primary Thema Code</dt>
                        <dd className="text-white">{data.classification.primaryThema}</dd>
                    </div>
                    <div>
                        <dt className="text-white/50">Secondary Thema Codes</dt>
                        <dd className="space-y-1 mt-1">
                            {data.classification.secondaryThema.map((s: any, idx: number) => (
                                <div key={idx} className="flex items-center space-x-2">
                                    <span className="px-2 py-1 bg-white/10 rounded-full text-sm text-white">{s.code}</span>
                                    <span className="text-white/70 text-sm">{s.label}</span>
                                </div>
                            ))}
                        </dd>
                    </div>
                    <div>
                        <dt className="text-white/50">Qualifiers</dt>
                        <dd className="space-y-1 mt-1">
                            {data.classification.qualifiers.map((q: string, idx: number) => (
                                <div key={idx} className="flex items-center space-x-2">
                                    <span className="px-2 py-1 bg-white/10 rounded-full text-sm text-white">{q}</span>
                                </div>
                            ))}
                        </dd>
                    </div>
                </dl>
            </div>
        </div>
    );
};

const OverviewItem = ({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) => (
    <div className="flex items-center space-x-3">
        <div className="text-white/50">{icon}</div>
        <div>
            <dt className="text-white/50">{label}</dt>
            <dd className="text-white font-medium">{value}</dd>
        </div>
    </div>
);

export default OverviewTab;
