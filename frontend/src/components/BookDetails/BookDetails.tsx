import OverviewTab from './OverviewTab';
import AnalysisTab from './AnalysisTab';
import MarketingTab from './MarketingTab';
import ChatTab from './ChatTab';
import DashboardTab from './DashboardTab';

import React, { useState, useEffect } from 'react';
import {
    ArrowLeft,
    BookOpen,
    BarChart2,
    Share2,
    MessageSquare,
    Loader2
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
    { id: 'dashboard', label: 'Dashboard', icon: BarChart2 },
];

const BookDetails = ({ book, onBack }: BookDetailsProps) => {
    const [activeTab, setActiveTab] = useState('overview');
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchDetails = async () => {
            try {
                await fetch(`${import.meta.env.VITE_API_URL}/books/${book.id}/details`);
            } catch (err) {
                console.error("Error generating book details", err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchDetails();
    }, [book.id]);

    const renderTabContent = () => {
        switch (activeTab) {
            case 'overview': return <OverviewTab bookId={book.id} />;
            case 'analysis': return <AnalysisTab bookId={book.id} />;
            case 'marketing': return <MarketingTab bookId={book.id} />;
            case 'chat': return <ChatTab bookId={book.id} />;
            case 'dashboard': return <DashboardTab bookId={book.id} />;
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
                        src={`${import.meta.env.VITE_API_URL}${book.cover}`}
                        alt={book.title}
                        className="w-full rounded-lg shadow-lg"
                    />
                </div>
                <div className="flex-1">
                    <h1 className="text-3xl font-bold text-white mb-2">{book.title}</h1>
                    <p className="text-white/70 text-lg mb-4">by {book.author}</p>
                </div>
            </div>

            {/* Tabs */}
            <div className="border-b border-white/20 mb-6">
                <div className="flex space-x-4 overflow-x-auto">
                    {tabs.map((tab) => {
                        const Icon = tab.icon;
                        return (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`flex items-center px-4 py-2 text-sm font-medium whitespace-nowrap ${
                                    activeTab === tab.id
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

            {/* Tab content */}
            <div className="min-h-[400px]">
                {isLoading ? (
                    <div className="flex items-center justify-center h-full">
                        <Loader2 className="h-8 w-8 text-white animate-spin" />
                        <span className="ml-3 text-white text-lg">Generating book details...</span>
                    </div>
                ) : (
                    <div className="text-white">
                        {renderTabContent()}
                    </div>
                )}
            </div>
        </div>
    );
};

export default BookDetails;
