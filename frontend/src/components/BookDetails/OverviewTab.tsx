import React, { useEffect, useState } from 'react';
import {
    Clock, FileText, BookOpen, BarChart2, Users, MapPin,
    Calendar, BookType, MessageCircle, Tag
} from 'lucide-react';

interface OverviewTabProps {
    bookId: string;
}

type BookWithCover = {
    title: string;
    author: string;
    note: string;
    coverUrl: string | null;
    isbn: string | null;
};

const OverviewTab = ({ bookId }: OverviewTabProps) => {
    const [data, setData] = useState<any | null>(null);
    const [loading, setLoading] = useState(true);
    const [similarBooks, setSimilarBooks] = useState<BookWithCover[]>([]);
    const [selectedCover, setSelectedCover] = useState<string | null>(null);

    useEffect(() => {
        const fetchDetails = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/details`);
                const details = await res.json();
                setData(details.overview);

                if (details.overview?.comparison?.length > 0) {
                    const enriched = await Promise.all(
                        details.overview.comparison.map(async (book: any) => {
                            const query = `intitle:${encodeURIComponent(book.title)}+inauthor:${encodeURIComponent(book.author)}`;
                            const url = `https://www.googleapis.com/books/v1/volumes?q=${query}`;

                            try {
                                const res = await fetch(url);
                                const json = await res.json();
                                const info = json.items?.[0]?.volumeInfo;

                                const coverUrl = info?.imageLinks?.thumbnail ?? null;

                                // Extract first ISBN-13 or fallback to ISBN-10
                                const isbn = info?.industryIdentifiers?.find(
                                    (id: { type: string; identifier: string }) =>
                                        id.type === "ISBN_13" || id.type === "ISBN_10"
                                )?.identifier ?? null;

                                return { ...book, coverUrl, isbn };
                            } catch {
                                return { ...book, coverUrl: null, isbn: null };
                            }
                        })
                    );
                    setSimilarBooks(enriched);
                }
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
                        <OverviewItem icon={<BookOpen />} label="Estimated number of pages" value={data.keyData.pages} />
                        <OverviewItem icon={<BarChart2 />} label="Number of Chapters" value={data.keyData.chapters} />
                        <OverviewItem icon={<Users />} label="Number of Characters" value={data.keyData.mainCharacters} />
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
                    {/* <div>
                        <dt className="text-white/50">Qualifiers</dt>
                        <dd className="space-y-1 mt-1">
                            {data.classification.qualifiers.map((q: string, idx: number) => (
                                <div key={idx} className="flex items-center space-x-2">
                                    <span className="px-2 py-1 bg-white/10 rounded-full text-sm text-white">{q}</span>
                                </div>
                            ))}
                        </dd>
                    </div> */}
                </dl>
            </div>

            {/* Book Comparison with Covers */}
            {similarBooks.length > 0 && (
                <div className="bg-white/5 rounded-lg p-6">
                    <h3 className="text-lg font-semibold mb-3">Suggestions for similar Books</h3>
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                        {similarBooks.map((book, idx) => (
                            <div
                                key={idx}
                                className="cursor-pointer transform hover:scale-105 transition-transform duration-200 bg-white/10 rounded-lg overflow-hidden"
                                onClick={() =>
                                    setSelectedCover(
                                        book.coverUrl ?? `${import.meta.env.VITE_API_URL}/covers/no_cover.png`
                                    )
                                }
                            >
                                <div className="aspect-[3/4] relative">
                                    <img
                                        src={book.coverUrl ?? `${import.meta.env.VITE_API_URL}/covers/no_cover.png`}
                                        alt={`${book.title} cover`}
                                        className="w-full h-full object-cover"
                                    />
                                </div>
                                <div className="p-3 text-center">
                                    <h3 className="text-sm font-semibold text-white mb-1 truncate">
                                        {book.title}
                                    </h3>
                                    <p className="text-white/70 text-xs truncate">{book.author}</p>
                                    <p className="text-white/50 text-xs mt-1">{book.note}</p>
                                    {book.isbn && (
                                        <p className="text-white/40 text-[11px] mt-1">ISBN: {book.isbn}</p>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Enlarged Cover Modal */}
                    {selectedCover && (
                        <div
                            className="fixed inset-0 bg-black/80 flex items-center justify-center z-50"
                            onClick={() => setSelectedCover(null)}
                        >
                            <img
                                src={selectedCover}
                                alt="Full cover"
                                className="max-w-full max-h-full object-contain shadow-lg rounded-lg"
                            />
                        </div>
                    )}
                </div>
            )}

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
