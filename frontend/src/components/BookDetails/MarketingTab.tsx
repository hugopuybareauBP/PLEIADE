// frontend/src/components/BookDetails/AnalysisTab.tsx

import React, { useEffect, useState } from 'react';
import { Copy, Instagram, Twitter, Video, Image as ImageIcon } from 'lucide-react';

interface TikTokSegment {
    start: number;
    end: number;
    narration: string;
    visuals: string;
    sound: string;
}

interface TikTokScript {
    title: string;
    segments: TikTokSegment[];
    call_to_action: string;
}

interface MarketingData {
    ecommerce: {
        description: string[];
        bullets: string[];
        closing: string;
    };
    social: {
        twitter: { content: string; metrics: { likes: number; retweets: number } }[];
        instagram: { image: string; caption: string; metrics: { likes: number; comments: number } }[];
        tiktok: TikTokScript[]; // Array of structured TikTok scripts
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
                const res = await fetch(`${import.meta.env.VITE_API_URL}/books/${bookId}/details`);
                const details = await res.json();
                setData(details.marketing);
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

                    {/* TikTok */}
                    <div>
                        <h4 className="text-lg font-medium mb-3 flex items-center gap-2">
                            <Video className="h-5 w-5 text-white" /> TikTok Script
                        </h4>
                        <div className="bg-white/5 rounded-lg overflow-hidden p-4 space-y-4 animate-fade-in">
                            <h5 className="text-xl font-semibold text-white/90">
                                {data.social.tiktok[0]?.title ?? 'TikTok Video'}
                            </h5>
                            <div className="relative border-l-2 border-white/20 pl-4 space-y-6">
                                {data.social.tiktok[0]?.segments?.map((seg, i) => (
                                    <div
                                        key={i}
                                        className="relative group transition-all hover:bg-white/5 p-3 rounded-md"
                                        style={{ animationDelay: `${i * 100}ms` }}
                                    >
                                        <div className="absolute -left-2 top-2 h-3 w-3 bg-white border border-white/40 rounded-full group-hover:scale-110 transition-transform" />
                                        <p className="text-sm text-white/50 mb-1">
                                            ⏱ {seg.start}s – {seg.end}s
                                        </p>
                                        <p className="text-white/90 font-medium mb-1">🎙 {seg.narration}</p>
                                        <p className="text-white/70 italic">🎬 {seg.visuals}</p>
                                        <p className="text-white/60 mt-1">🔊 {seg.sound}</p>
                                    </div>
                                ))}
                            </div>
                            <div className="mt-6 text-center text-lg font-semibold text-white/90">
                                🎯 {data.social.tiktok[0]?.call_to_action}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MarketingTab;
