// frontend/src/components/BookDetails/AnalysisTab.tsx

import React, { useEffect, useState } from 'react';
import { Copy, Instagram, Twitter, Video, Image as ImageIcon } from 'lucide-react';

interface MarketingData {
    ecommerce: {
        title: string;
        description: string[];
        bullets: string[];
        closing: string;
    };
    social: {
        twitter: { content: string; metrics: { likes: number; retweets: number } }[];
        instagram: { image: string; caption: string; metrics: { likes: number; comments: number } }[];
        tiktok: { thumbnail: string; caption: string; metrics: { views: string; likes: string } }[];
    };
    visuals: string[];
}

interface Props {
    bookId: string;
}

const MarketingTab: React.FC<Props> = ({ bookId }) => {
    const [data, setData] = useState<MarketingData | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMarketing = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/analysis_marketing`);
                const json = await res.json();
                setData(json.marketing);
            } catch (err) {
                console.error("Failed to load marketing data", err);
            } finally {
                setLoading(false);
            }
        };
        fetchMarketing();
    }, [bookId]);

    if (loading || !data) {
        return <p className="text-white">Generating marketing content...</p>;
    }

    return (
        <div className="space-y-6">
            {/* E-Commerce */}
            <div className="bg-white/5 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold">E-commerce Content</h3>
                    <button className="p-2 hover:bg-white/10 rounded-lg transition-colors">
                        <Copy className="h-5 w-5" />
                    </button>
                </div>
                <div className="space-y-4 text-white/70">
                    <p className="text-lg font-semibold">{data.ecommerce.title}</p>
                    {data.ecommerce.description.map((line, i) => (
                        <p key={i}>{line}</p>
                    ))}
                    <ul className="list-disc pl-6 space-y-2">
                        {data.ecommerce.bullets.map((point, i) => (
                            <li key={i}>{point}</li>
                        ))}
                    </ul>
                    <p className="mt-4">{data.ecommerce.closing}</p>
                </div>
            </div>

            {/* Social Media */}
            <div className="bg-white/5 rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-4">Social Media Content</h3>
                <div className="space-y-6">
                    {/* Twitter */}
                    <div>
                        <h4 className="text-lg font-medium mb-3">Twitter Posts</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {data.social.twitter.map((post, i) => (
                                <div key={i} className="bg-white/10 rounded-lg p-4">
                                    <div className="flex items-start space-x-3">
                                        <Twitter className="h-5 w-5 text-[#1DA1F2]" />
                                        <div>
                                            <p className="text-white/90 text-sm">{post.content}</p>
                                            <div className="flex space-x-4 mt-2 text-white/50 text-sm">
                                                <span>❤️ {post.metrics.likes}</span>
                                                <span>🔁 {post.metrics.retweets}</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Instagram */}
                    <div>
                        <h4 className="text-lg font-medium mb-3">Instagram Posts</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {data.social.instagram.map((post, i) => (
                                <div key={i} className="bg-white/10 rounded-lg overflow-hidden">
                                    <img src={post.image} alt="Instagram" className="w-full aspect-square object-cover" />
                                    <div className="p-4">
                                        <div className="flex items-center space-x-2 mb-2">
                                            <Instagram className="h-5 w-5 text-[#E1306C]" />
                                            <span className="text-white/90 font-medium">Instagram</span>
                                        </div>
                                        <p className="text-white/90 text-sm whitespace-pre-line">{post.caption}</p>
                                        <div className="flex space-x-4 mt-2 text-white/50 text-sm">
                                            <span>❤️ {post.metrics.likes}</span>
                                            <span>💬 {post.metrics.comments}</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* TikTok */}
                    <div>
                        <h4 className="text-lg font-medium mb-3">TikTok Posts</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {data.social.tiktok.map((post, i) => (
                                <div key={i} className="bg-white/10 rounded-lg overflow-hidden">
                                    <div className="relative">
                                        <img src={post.thumbnail} alt="TikTok" className="w-full aspect-[9/16] object-cover" />
                                        <div className="absolute inset-0 flex justify-center items-center">
                                            <Video className="h-12 w-12 text-white/80" />
                                        </div>
                                    </div>
                                    <div className="p-4 text-white/90">
                                        <p className="text-sm">{post.caption}</p>
                                        <div className="flex space-x-4 mt-2 text-white/50 text-sm">
                                            <span>👁️ {post.metrics.views}</span>
                                            <span>❤️ {post.metrics.likes}</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Visuals */}
            <div className="bg-white/5 rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-4">Visual Content</h3>
                <div className="grid grid-cols-2 gap-4">
                    {data.visuals.map((url, i) => (
                        <div key={i} className="aspect-video bg-white/10 rounded-lg overflow-hidden">
                            {url ? (
                                <img src={url} alt={`Visual ${i}`} className="w-full h-full object-cover" />
                            ) : (
                                <div className="flex items-center justify-center h-full">
                                    <ImageIcon className="h-8 w-8 text-white/50" />
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default MarketingTab;