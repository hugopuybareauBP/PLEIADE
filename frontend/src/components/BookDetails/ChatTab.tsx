import React, { useState, useRef, useEffect } from 'react';
import { SendHorizonal, Loader2 } from 'lucide-react';

interface ChatTabProps {
    bookId: string;
}

const ChatTab = ({ bookId }: ChatTabProps) => {
    const [question, setQuestion] = useState('');
    const [loading, setLoading] = useState(false);
    const [history, setHistory] = useState<{ q: string; a: string }[]>([]);
    const [currentAnswer, setCurrentAnswer] = useState<string | null>(null);
    const bottomRef = useRef<HTMLDivElement | null>(null);
    const streamedAnswerRef = useRef<string>('');
    const hasEnded = useRef(false);

    const finalize = () => {
        if (hasEnded.current) return;
        hasEnded.current = true;

        setHistory((prev) => [...prev, { q: question, a: streamedAnswerRef.current }]);
        setCurrentAnswer(streamedAnswerRef.current);

        setTimeout(() => {
            setCurrentAnswer(null);
        }, 100);

        setQuestion('');
        setLoading(false);
        streamedAnswerRef.current = '';
    };

    const handleAsk = () => {
        if (!question.trim()) return;

        hasEnded.current = false;
        setLoading(true);
        setCurrentAnswer('');
        streamedAnswerRef.current = '';

        const source = new EventSource(
            `${import.meta.env.VITE_API_URL}/chat/stream?question=${encodeURIComponent(question)}&book_id=${bookId}`
        );

        source.onmessage = (event) => {
            streamedAnswerRef.current += event.data;
            setCurrentAnswer(streamedAnswerRef.current);
        };

        source.addEventListener('done', () => {
            console.log("✅ Stream done");
            source.close();
            finalize();
        });

        source.onerror = (event) => {
            console.error('❌ Streaming error', event);
            source.close();
            finalize();
        };

        setTimeout(() => {
            if (!hasEnded.current) {
                console.warn("⚠️ Timeout - closing stream");
                source.close();
                finalize();
            }
        }, 30000);
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && !loading) {
            handleAsk();
        }
    };

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [currentAnswer, history]);

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="bg-white/5 rounded-lg p-6">
                <h3 className="text-xl font-semibold mb-4">Ask a question about the book</h3>
                <div className="flex space-x-2">
                    <input
                        autoFocus
                        type="text"
                        className="flex-grow rounded-full px-4 py-3 bg-white/10 text-white placeholder-white/50 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white/30 transition"
                        placeholder="e.g. What happens in chapter 5?"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        onKeyDown={handleKeyPress}
                        disabled={loading}
                    />
                    <button
                        onClick={handleAsk}
                        className="bg-white/20 hover:bg-white/30 p-3 rounded-full text-white transition"
                        disabled={loading}
                    >
                        {loading ? <Loader2 className="animate-spin" /> : <SendHorizonal />}
                    </button>
                </div>
            </div>

            {/* Chat area */}
            <div className="bg-white/5 rounded-lg p-6 space-y-4 max-h-[550px] overflow-y-auto">
                {history.length === 0 && !currentAnswer && !loading ? (
                    <p className="text-white/50 italic text-center">
                        Ask anything about the story. Characters, plot, hidden meanings...
                    </p>
                ) : (
                    <>
                        {history.map((item, idx) => (
                            <div key={idx} className="space-y-4">
                                {/* User Message */}
                                <div className="flex justify-end items-start space-x-2">
                                    <div className="max-w-lg bg-white/20 text-white rounded-xl px-4 py-2">
                                        {item.q}
                                    </div>
                                    <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center text-white text-sm">👤</div>
                                </div>

                                {/* Assistant Message */}
                                <div className="flex justify-start items-start space-x-2">
                                    <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-white text-sm">🤖</div>
                                    <div className="max-w-lg bg-white/10 text-white/80 rounded-xl px-4 py-2 whitespace-pre-line">
                                        {item.a}
                                    </div>
                                </div>
                            </div>
                        ))}

                        {currentAnswer && (
                            <div className="space-y-4">
                                <div className="flex justify-end items-start space-x-2">
                                    <div className="max-w-lg bg-white/20 text-white rounded-xl px-4 py-2">
                                        {question}
                                    </div>
                                    <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center text-white text-sm">👤</div>
                                </div>
                                <div className="flex justify-start items-start space-x-2">
                                    <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-white text-sm">🤖</div>
                                    <div className="max-w-lg bg-white/10 text-white/80 rounded-xl px-4 py-2 whitespace-pre-line">
                                        {currentAnswer}
                                    </div>
                                </div>
                            </div>
                        )}

                        {loading && !currentAnswer && (
                            <div className="flex items-center text-white/50 text-sm italic space-x-2">
                                <span>Thinking</span>
                                <span className="animate-pulse">.</span>
                                <span className="animate-pulse delay-100">.</span>
                                <span className="animate-pulse delay-200">.</span>
                            </div>
                        )}
                        <div ref={bottomRef} />
                    </>
                )}
            </div>
        </div>
    );
};

export default ChatTab;
