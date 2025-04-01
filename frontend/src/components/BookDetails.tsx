import React, { useState } from 'react';
import {
    ArrowLeft,
    BookOpen,
    BarChart2,
    Share2,
    MessageSquare,
    Headphones,
    Loader2,
    Copy,
    Download,
    Image as ImageIcon,
    Send,
    CheckCircle2,
    XCircle,
    Twitter,
    Instagram,
    Video,
    Clock,
    FileText,
    Users,
    MapPin,
    Calendar,
    BookType,
    MessageCircle,
    Tag
} from 'lucide-react';

interface BookDetailsProps {
    book: {
        id: string;
        title: string;
        cover: string;
        author: string;
        uploadDate: string;
        synopsis: string;
    };
    onBack: () => void;
}

const tabs = [
    { id: 'overview', label: 'Content Overview', icon: BookOpen },
    { id: 'analysis', label: 'Detailed Analysis', icon: BarChart2 },
    { id: 'marketing', label: 'Marketing', icon: Share2 },
    { id: 'chat', label: 'AI Chat', icon: MessageSquare },
    { id: 'audio', label: 'Audio', icon: Headphones },
];

const socialMediaPosts = {
    twitter: [
        {
            content: "🚀 'The Future of AI' by @SarahJohnson is your essential guide to understanding artificial intelligence. From current applications to future possibilities, this book demystifies AI for everyone. Available now! #AIBook #TechReads",
            metrics: { likes: 156, retweets: 42 }
        },
        {
            content: "🤖 \"AI isn't just changing technology—it's reshaping our world.\" Dive into @SarahJohnson's fascinating exploration of how AI is transforming industries and our daily lives. #FutureOfAI #TechTrends",
            metrics: { likes: 203, retweets: 67 }
        }
    ],
    instagram: [
        {
            image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&auto=format&fit=crop&q=60",
            caption: "📚 Unlock the secrets of AI with 'The Future of AI' by Sarah Johnson. A mind-expanding journey through the technology that's shaping our tomorrow. 🤖✨\n\n#AIBook #TechBooks #Innovation #ArtificialIntelligence #FutureOfTech",
            metrics: { likes: 892, comments: 45 }
        },
        {
            image: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&auto=format&fit=crop&q=60",
            caption: "🌟 'The future belongs to those who understand AI.' - Sarah Johnson\n\nDive into the most comprehensive guide on artificial intelligence and its impact on our world. Available now! 📚\n\n#AITechnology #BookRecommendations #TechInnovation",
            metrics: { likes: 1247, comments: 73 }
        }
    ],
    tiktok: [
        {
            thumbnail: "https://images.unsplash.com/photo-1674027444485-cec3da58eef0?w=800&auto=format&fit=crop&q=60",
            caption: "POV: You're discovering how AI will change your future 🤖 #AIBook #BookTok #TechTok",
            metrics: { views: "126.5K", likes: "18.2K" }
        },
        {
            thumbnail: "https://images.unsplash.com/photo-1676299081847-5c7fe8b15015?w=800&auto=format&fit=crop&q=60",
            caption: "5 mind-blowing AI predictions from 'The Future of AI' 🤯 #LearnOnTikTok #AITechnology",
            metrics: { views: "203.8K", likes: "25.4K" }
        }
    ]
};

const BookDetails = ({ book, onBack }: BookDetailsProps) => {
    const [activeTab, setActiveTab] = useState('overview');
    const [isLoading] = useState(false);
    const [chatMessage, setChatMessage] = useState('');
    const [chatHistory] = useState([
        { role: 'user', content: 'Can you write a 100-word synopsis of this book?' },
        { role: 'assistant', content: '"The Future of AI" is a groundbreaking exploration of artificial intelligence and its transformative impact on society. Sarah Johnson masterfully breaks down complex AI concepts, making them accessible to both tech enthusiasts and general readers. The book covers current AI applications across industries, ethical considerations, and potential future developments. Through expert interviews and case studies, Johnson presents a balanced view of AI\'s possibilities and challenges. She particularly emphasizes how AI will reshape work, healthcare, and daily life, while addressing concerns about automation and privacy. The book concludes with practical insights for preparing for an AI-driven future.' },
        { role: 'user', content: 'What are the main themes discussed in the book?' },
        { role: 'assistant', content: 'The main themes include:\n\n1. AI\'s current state and evolution\n2. Impact on various industries\n3. Ethical considerations and challenges\n4. Future predictions and possibilities\n5. Human-AI collaboration\n6. Privacy and security concerns\n7. Economic implications\n8. Societal transformation' },
        { role: 'user', content: 'Who would benefit most from reading this book?' },
        { role: 'assistant', content: 'This book is valuable for:\n\n- Business leaders looking to understand AI\'s impact on their industries\n- Technology professionals seeking a broader perspective\n- Students and educators in tech-related fields\n- Policy makers interested in AI governance\n- General readers wanting to understand AI\'s role in shaping our future\n\nThe accessible writing style makes it suitable for both technical and non-technical audiences.' }
    ]);

    const renderSocialMediaPost = (platform: 'twitter' | 'instagram' | 'tiktok', post: any, index: number) => {
        switch (platform) {
            case 'twitter':
                return (
                    <div className="bg-white/10 rounded-lg p-4">
                        <div className="flex items-start space-x-3">
                            <Twitter className="h-5 w-5 text-[#1DA1F2] flex-shrink-0 mt-1" />
                            <div className="flex-1">
                                <p className="text-white/90 text-sm">{post.content}</p>
                                <div className="flex items-center space-x-4 mt-2 text-white/50 text-sm">
                            <span>❤️ {post.metrics.likes}</span>
                            <span>🔄 {post.metrics.retweets}</span>
                        </div>
                    </div>
                </div>
          </div>
        );
      
            case 'instagram':
                return (
                    <div className="bg-white/10 rounded-lg overflow-hidden">
                        <img src={post.image} alt="Instagram post" className="w-full aspect-square object-cover" />
                        <div className="p-4">
                            <div className="flex items-center space-x-2 mb-2">
                                <Instagram className="h-5 w-5 text-[#E1306C]" />
                                <span className="text-white/90 font-medium">Instagram</span>
                            </div>
                            <p className="text-white/90 text-sm whitespace-pre-line">{post.caption}</p>
                            <div className="flex items-center space-x-4 mt-2 text-white/50 text-sm">
                                <span>❤️ {post.metrics.likes}</span>
                                <span>💬 {post.metrics.comments}</span>
                            </div>
                        </div>
                    </div>
                );
      
            case 'tiktok':
                return (
                    <div className="bg-white/10 rounded-lg overflow-hidden">
                        <div className="relative">
                            <img src={post.thumbnail} alt="TikTok thumbnail" className="w-full aspect-[9/16] object-cover" />
                            <div className="absolute inset-0 flex items-center justify-center">
                                <Video className="h-12 w-12 text-white/80" />
                            </div>
                        </div>
                        <div className="p-4">
                            <div className="flex items-center space-x-2 mb-2">
                                <span className="text-white/90 font-medium">TikTok</span>
                            </div>
                            <p className="text-white/90 text-sm">{post.caption}</p>
                            <div className="flex items-center space-x-4 mt-2 text-white/50 text-sm">
                                <span>👁️ {post.metrics.views}</span>
                                <span>❤️ {post.metrics.likes}</span>
                            </div>
                        </div>
                    </div>
                );
        }
    };

    const renderTabContent = () => {
        switch (activeTab) {
        case 'overview':
            return (
            <div className="space-y-6">
                <div className="bg-white/5 rounded-lg p-6">
                    <h3 className="text-xl font-semibold mb-4">Synopsis</h3>
                    <p className="text-white/70">{book.synopsis}</p>
                </div>
            
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="bg-white/5 rounded-lg p-6">
                                <h3 className="text-lg font-semibold mb-4">Key Data</h3>
                                <div className="space-y-4">
                                    <div className="flex items-center space-x-3">
                                        <Clock className="h-5 w-5 text-white/50" />
                                        <div>
                                            <dt className="text-white/50">Estimated Reading Time</dt>
                                            <dd className="text-white font-medium">8 hours 30 minutes</dd>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <FileText className="h-5 w-5 text-white/50" />
                                        <div>
                                            <dt className="text-white/50">Word Count</dt>
                                            <dd className="text-white font-medium">85,000 words</dd>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <BookOpen className="h-5 w-5 text-white/50" />
                                        <div>
                                            <dt className="text-white/50">Number of Pages</dt>
                                            <dd className="text-white font-medium">320 pages</dd>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <BarChart2 className="h-5 w-5 text-white/50" />
                                        <div>
                                            <dt className="text-white/50">Number of Chapters</dt>
                                            <dd className="text-white font-medium">12 chapters</dd>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <Users className="h-5 w-5 text-white/50" />
                                        <div>
                                            <dt className="text-white/50">Main Characters</dt>
                                            <dd className="text-white font-medium">15 industry experts</dd>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <MapPin className="h-5 w-5 text-white/50" />
                                        <div>
                                            <dt className="text-white/50">Key Locations</dt>
                                            <dd className="text-white font-medium">8 tech hubs worldwide</dd>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-white/5 rounded-lg p-6">
                                <h3 className="text-lg font-semibold mb-4">Content Analysis</h3>
                                <div className="space-y-4">
                                    <div className="flex items-center space-x-3">
                                        <Calendar className="h-5 w-5 text-white/50" />
                                        <div>
                                            <dt className="text-white/50">Time Period</dt>
                                            <dd className="text-white font-medium">Present day to 2035</dd>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <BookType className="h-5 w-5 text-white/50" />
                                        <div>
                                            <dt className="text-white/50">Genres</dt>
                                            <dd className="text-white font-medium">Technology, Business, Future Studies</dd>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-3">
                                        <MessageCircle className="h-5 w-5 text-white/50" />
                                        <div>
                                            <dt className="text-white/50">Overall Tone</dt>
                                            <dd className="text-white font-medium">Informative, Optimistic, Balanced</dd>
                                        </div>
                                    </div>
                                    <div className="flex items-start space-x-3">
                                        <Tag className="h-5 w-5 text-white/50 mt-1" />
                                        <div>
                                            <dt className="text-white/50">Key Words</dt>
                                            <dd className="text-white font-medium">
                                                <div className="flex flex-wrap gap-2 mt-1">
                                                    {['Artificial Intelligence', 'Machine Learning', 'Digital Transformation', 'Innovation', 'Ethics', 'Future of Work', 'Technology Impact', 'Automation'].map((keyword) => (
                                                        <span key={keyword} className="px-2 py-1 bg-white/10 rounded-full text-sm">
                                                            {keyword}
                                                        </span>
                                                    ))}
                                                </div>
                                            </dd>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-white/5 rounded-lg p-6">
                                <h3 className="text-lg font-semibold mb-3">Classification</h3>
                                <dl className="space-y-3">
                                    <div>
                                        <dt className="text-white/50">Primary Thema Code</dt>
                                        <dd className="text-white">UB (Information & communication technology)</dd>
                                    </div>
                                    <div>
                                        <dt className="text-white/50">Secondary Thema Codes</dt>
                                        <dd className="space-y-1 mt-1">
                                            <div className="flex items-center space-x-2">
                                                <span className="px-2 py-1 bg-white/10 rounded-full text-sm text-white">UBJ (Social networking)</span>
                                                <span className="text-white/70 text-sm">Impact of AI on social connections</span>
                                            </div>
                                            <div className="flex items-center space-x-2">
                                                <span className="px-2 py-1 bg-white/10 rounded-full text-sm text-white">KJM (Management & management techniques)</span>
                                                <span className="text-white/70 text-sm">AI in business strategy</span>
                                            </div>
                                            <div className="flex items-center space-x-2">
                                                <span className="px-2 py-1 bg-white/10 rounded-full text-sm text-white">PDR (Impact of science & technology on society)</span>
                                                <span className="text-white/70 text-sm">Societal implications</span>
                                            </div>
                                        </dd>
                                    </div>
                                    <div>
                                        <dt className="text-white/50">Qualifiers</dt>
                                        <dd className="space-y-1 mt-1">
                                            <div className="flex items-center space-x-2">
                                                <span className="px-2 py-1 bg-white/10 rounded-full text-sm text-white">4SP (For professional/vocational reference)</span>
                                            </div>
                                            <div className="flex items-center space-x-2">
                                                <span className="px-2 py-1 bg-white/10 rounded-full text-sm text-white">4G (Research & development)</span>
                                            </div>
                                        </dd>
                                    </div>
                                </dl>
                            </div>
                        </div>
                    </div>
                );

            case 'analysis':
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
                                        {[
                                            'Clear and engaging writing style that makes complex concepts accessible',
                                            'Well-researched with current industry examples and case studies',
                                            'Balanced perspective on AI\'s potential benefits and challenges',
                                            'Strong technical foundation with practical applications',
                                            'Effective use of diagrams and illustrations'
                                        ].map((strength, index) => (
                                            <li key={index} className="flex items-start">
                                                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-2 mr-2"></span>
                                                <span className="text-white/70">{strength}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                                <div>
                                    <div className="flex items-center mb-3">
                                        <XCircle className="h-5 w-5 text-red-400 mr-2" />
                                        <h4 className="text-lg font-medium">Areas for Improvement</h4>
                                    </div>
                                    <ul className="space-y-3">
                                        {[
                                            'Could include more international perspectives on AI adoption',
                                            'Some technical sections may need additional context for beginners',
                                            'More real-world examples would strengthen certain arguments',
                                            'Consider expanding the ethical implications discussion',
                                            'Additional future scenarios could enhance long-term relevance'
                                        ].map((weakness, index) => (
                                            <li key={index} className="flex items-start">
                                                <span className="w-1.5 h-1.5 rounded-full bg-red-400 mt-2 mr-2"></span>
                                                <span className="text-white/70">{weakness}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div className="bg-white/5 rounded-lg p-6">
                            <h3 className="text-xl font-semibold mb-4">Character Profiles</h3>
                            <div className="space-y-4">
                                {['Expert Researchers', 'Industry Leaders', 'AI Practitioners'].map((character) => (
                                    <div key={character} className="border-b border-white/10 pb-4">
                                        <h4 className="font-medium mb-2">{character}</h4>
                                        <p className="text-white/70">Key stakeholders discussing AI's impact and future directions.</p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="bg-white/5 rounded-lg p-6">
                            <h3 className="text-xl font-semibold mb-4">Chapter Breakdown</h3>
                            <div className="space-y-4">
                                {[
                                    'Introduction to AI',
                                    'Historical Development',
                                    'Current Applications',
                                    'Future Prospects'
                                ].map((chapter, index) => (
                                    <div key={chapter} className="flex items-start space-x-4">
                                        <span className="w-8 h-8 bg-white/10 rounded-full flex items-center justify-center">
                                            {index + 1}
                                        </span>
                                        <div>
                                            <h4 className="font-medium">{chapter}</h4>
                                            <p className="text-white/70 text-sm mt-1">
                                                Chapter summary and key points will be displayed here.
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                );

            case 'marketing':
                return (
                    <div className="space-y-6">
                        <div className="bg-white/5 rounded-lg p-6">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-xl font-semibold">E-commerce Content</h3>
                                <button className="p-2 hover:bg-white/10 rounded-lg transition-colors">
                                    <Copy className="h-5 w-5" />
                                </button>
                            </div>
                            <div className="space-y-4">
                                <div className="bg-white/10 rounded-lg p-4">
                                    <h4 className="font-medium mb-2">Amazon Description</h4>
                                    <div className="space-y-4 text-white/70">
                                        <p className="text-lg font-semibold">Unlock the Secrets of Artificial Intelligence and Shape Your Future</p>

                                        <p>In "The Future of AI," renowned tech expert Sarah Johnson delivers a compelling and accessible exploration of artificial intelligence's revolutionary impact on our world. This groundbreaking book demystifies complex AI concepts, offering readers a clear roadmap to understanding and preparing for an AI-driven future.</p>

                                        <div className="pl-4 border-l-2 border-white/20 my-4">
                                            <p className="italic">"A masterful guide that bridges the gap between technical complexity and practical understanding." - Tech Review Weekly</p>
                                        </div>

                                        <p>You'll discover:</p>
                                        <ul className="list-disc pl-6 space-y-2">
                                            <li>How AI is transforming industries from healthcare to finance</li>
                                            <li>Practical insights for businesses and professionals</li>
                                            <li>Expert predictions about AI's future developments</li>
                                            <li>Ethical considerations and societal impacts</li>
                                            <li>Strategies for adapting to an AI-enhanced world</li>
                                        </ul>

                                        <p className="mt-4">Perfect for business leaders, technology enthusiasts, and anyone seeking to understand how AI will shape our future. Sarah Johnson combines deep expertise with engaging storytelling to create an essential guide for navigating the AI revolution.</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="bg-white/5 rounded-lg p-6">
                            <h3 className="text-xl font-semibold mb-4">Social Media Content</h3>
                            <div className="space-y-6">
                                <div>
                                    <h4 className="text-lg font-medium mb-3">Twitter Posts</h4>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {socialMediaPosts.twitter.map((post, index) => renderSocialMediaPost('twitter', post, index))}
                                    </div>
                                </div>

                                <div>
                                    <h4 className="text-lg font-medium mb-3">Instagram Posts</h4>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {socialMediaPosts.instagram.map((post, index) => renderSocialMediaPost('instagram', post, index))}
                                    </div>
                                </div>

                                <div>
                                    <h4 className="text-lg font-medium mb-3">TikTok Posts</h4>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        {socialMediaPosts.tiktok.map((post, index) => renderSocialMediaPost('tiktok', post, index))}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="bg-white/5 rounded-lg p-6">
                            <h3 className="text-xl font-semibold mb-4">Visual Content</h3>
                            <div className="grid grid-cols-2 gap-4">
                                {[1, 2, 3, 4].map((i) => (
                                    <div key={i} className="aspect-video bg-white/10 rounded-lg flex items-center justify-center">
                                        <ImageIcon className="h-8 w-8 text-white/50" />
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                );

            case 'chat':
                return (
                    <div className="h-[600px] flex flex-col">
                        <div className="flex-1 overflow-y-auto p-4 space-y-4">
                            {chatHistory.map((message, index) => (
                                <div
                                    key={index}
                                    className={`flex ${message.role === 'assistant' ? 'justify-start' : 'justify-end'}`}
                                >
                                    <div
                                        className={`max-w-[80%] rounded-lg p-3 ${message.role === 'assistant'
                                                ? 'bg-white/10'
                                                : 'bg-white/20'
                                            }`}
                                    >
                                        <p className="text-white whitespace-pre-line">{message.content}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                        <div className="p-4 bg-white/5">
                            <div className="flex space-x-2">
                                <input
                                    type="text"
                                    value={chatMessage}
                                    onChange={(e) => setChatMessage(e.target.value)}
                                    placeholder="Ask a question about the book..."
                                    className="flex-1 bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white placeholder-white/50 focus:outline-none focus:border-white/40"
                                />
                                <button className="p-2 bg-white/10 rounded-lg hover:bg-white/20 transition-colors">
                                    <Send className="h-5 w-5" />
                                </button>
                            </div>
                        </div>
                    </div>
                );

            case 'audio':
                return (
                    <div className="space-y-6">
                        <div className="bg-white/5 rounded-lg p-6">
                            <h3 className="text-xl font-semibold mb-4">Audio Samples</h3>
                            <div className="space-y-4">
                                {['Introduction', 'Chapter 1', 'Chapter 2'].map((section) => (
                                    <div key={section} className="bg-white/10 rounded-lg p-4">
                                        <div className="flex items-center justify-between mb-2">
                                            <h4 className="font-medium">{section}</h4>
                                            <button className="p-2 hover:bg-white/10 rounded-full">
                                                <Headphones className="h-4 w-4" />
                                            </button>
                                        </div>
                                        <div className="h-2 bg-white/20 rounded-full">
                                            <div className="h-2 bg-white/60 rounded-full w-1/3"></div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="bg-white/5 rounded-lg p-6">
                            <h3 className="text-xl font-semibold mb-4">Voice Settings</h3>
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium mb-2">Voice Style</label>
                                    <select className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white">
                                        <option>Natural</option>
                                        <option>Professional</option>
                                        <option>Casual</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium mb-2">Speaking Rate</label>
                                    <input
                                        type="range"
                                        className="w-full"
                                        min="0.5"
                                        max="2"
                                        step="0.1"
                                        defaultValue="1"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                );

            default:
                return null;
        }
    };

    return (
        <div className="bg-white/10 rounded-lg p-6">
            <button
                onClick={onBack}
                className="flex items-center text-white mb-6 hover:text-white/80 transition-colors"
            >
                <ArrowLeft className="h-5 w-5 mr-2" />
                Back to Books
            </button>

            <div className="flex flex-col md:flex-row gap-8 mb-8">
                <div className="w-full md:w-1/3 lg:w-1/4">
                    <img
                        src={book.cover}
                        alt={book.title}
                        className="w-full rounded-lg shadow-lg"
                    />
                </div>
                <div className="flex-1">
                    <h1 className="text-3xl font-bold text-white mb-2">{book.title}</h1>
                    <p className="text-white/70 text-lg mb-4">by {book.author}</p>
                </div>
            </div>

            <div className="border-b border-white/20 mb-6">
                <div className="flex space-x-4 overflow-x-auto">
                    {tabs.map((tab) => {
                        const Icon = tab.icon;
                        return (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`flex items-center px-4 py-2 text-sm font-medium whitespace-nowrap ${activeTab === tab.id
                                        ? 'text-white border-b-2 border-white'
                                        : 'text-white/70 hover:text-white'
                                    }`}
                            >
                                <Icon className="h-4 w-4 mr-2" />
                                {tab.label}
                            </button>
                        );
                    })}
                </div>
            </div>

            <div className="min-h-[400px]">
                {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                        <Loader2 className="h-8 w-8 text-white animate-spin" />
                    </div>
                ) : (
                    <div className="text-white">
                        {renderTabContent()}
                    </div>
                )}
            </div>
        </div>
    );
}

export default BookDetails;