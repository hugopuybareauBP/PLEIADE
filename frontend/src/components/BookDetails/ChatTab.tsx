import React, { useState } from 'react';
import { SendHorizonal, Loader2 } from 'lucide-react';

interface ChatTabProps {
    bookId: string;
}

const ChatTab = ({ bookId }: ChatTabProps) => {
    const [question, setQuestion] = useState('');
    const [loading, setLoading] = useState(false);
    const [history, setHistory] = useState<{ q: string; a: string }[]>([]);
    const [currentAnswer, setCurrentAnswer] = useState<string | null>(null);

    const handleAsk = () => {
        if (!question.trim()) return;
        setLoading(true);
        setCurrentAnswer('');

        const source = new EventSource(
            `${import.meta.env.VITE_API_URL}/chat/stream?question=${encodeURIComponent(question)}&book_id=${encodeURIComponent(bookId)}`
        );

        let streamedAnswer = '';

        const finalize = () => {
            source.close();
            setHistory((prev) => [...prev, { q: question, a: streamedAnswer }]);
            setQuestion('');
            setLoading(false);
            setCurrentAnswer(null);
        };

        source.onmessage = (event) => {
            // ✅ Clean SSE prefix if present (safety net)
            const cleanChunk = event.data.replace(/^data:\s*/, '');
            streamedAnswer += cleanChunk;
            setCurrentAnswer(streamedAnswer);
        };

        // source.onerror = (err) => {
        //     console.error('Streaming error:', err);
        //     finalize();
        // };

        // Optional timeout to avoid hanging connections
        setTimeout(() => {
            finalize();
        }, 30000);
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && !loading) {
            handleAsk();
        }
    };

    return (
        <div className="space-y-6">
            <div className="bg-white/5 rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-4">Ask a question about the book</h3>
                <div className="flex space-x-2">
                    <input
                        type="text"
                        className="flex-grow rounded-lg p-3 bg-white/10 text-white placeholder-white/50"
                        placeholder="e.g. What happens in chapter 5?"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        onKeyDown={handleKeyPress}
                        disabled={loading}
                    />
                    <button
                        onClick={handleAsk}
                        className="bg-white/20 hover:bg-white/30 p-3 rounded-lg text-white"
                        disabled={loading}
                    >
                        {loading ? <Loader2 className="animate-spin" /> : <SendHorizonal />}
                    </button>
                </div>
            </div>

            <div className="bg-white/5 rounded-lg p-6 space-y-4">
                <h3 className="text-lg font-semibold mb-4">Conversation</h3>
                {history.length === 0 && !currentAnswer ? (
                    <p className="text-white/50 italic">No questions asked yet.</p>
                ) : (
                    <>
                        {history.map((item, idx) => (
                            <div key={idx} className="space-y-2">
                                <div className="text-white font-semibold">Q: {item.q}</div>
                                <div className="text-white/80 bg-white/10 rounded-md p-3">A: {item.a}</div>
                            </div>
                        ))}
                        {currentAnswer && (
                            <div className="space-y-2">
                                <div className="text-white font-semibold">Q: {question}</div>
                                <div className="text-white/80 bg-white/10 rounded-md p-3">A: {currentAnswer}</div>
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
};

export default ChatTab;
