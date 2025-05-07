// frontend/src/components/ChatTab.tsx

import React, { useState, useRef, useEffect } from 'react';
import { SendHorizonal, Loader2, Trash2 } from 'lucide-react';

interface ChatTabProps {
    bookId: string;
}

interface QA {
    q: string;
    a: string;
}

const ChatTab = ({ bookId }: ChatTabProps) => {
    const [question, setQuestion] = useState('');
    const [loading, setLoading] = useState(false);
    const [history, setHistory] = useState<QA[]>([]);
    const [currentAnswer, setCurrentAnswer] = useState<string | null>(null);
    const bottomRef = useRef<HTMLDivElement | null>(null);
    const streamedAnswerRef = useRef<string>('');
    const hasEnded = useRef(false);

    const queueRef = useRef<string[]>([]);
    const intervalRef = useRef<number | null>(null);

    const startStreaming = () => {
        if (intervalRef.current) return;

        console.log('[⏳] startStreaming...');
        intervalRef.current = window.setInterval(() => {
            if (queueRef.current.length === 0) return;

            const nextChar = queueRef.current.shift();
            if (nextChar !== undefined) {
                streamedAnswerRef.current += nextChar;
                setCurrentAnswer(streamedAnswerRef.current);
                // console.log('[➡️] Char:', nextChar);
            }
        }, 10);
    };

    const stopStreaming = () => {
        if (intervalRef.current) {
            console.log('[🛑] stopStreaming...');
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }
    };

    useEffect(() => {
        const loadHistory = async () => {
            try {
                const res = await fetch(
                    `${import.meta.env.VITE_API_URL}/chat/history?book_id=${bookId}`
                );
                const { history: raw } = (await res.json()) as {
                    history: { role: string; content: string }[];
                };

                const pairs: QA[] = [];
                for (let i = 0; i < raw.length; i++) {
                    if (
                        raw[i].role === 'user' &&
                        raw[i + 1] &&
                        raw[i + 1].role === 'assistant'
                    ) {
                        pairs.push({ q: raw[i].content, a: raw[i + 1].content });
                        i++;
                    }
                }

                console.log('[📜] Loaded history:', pairs);
                setHistory(pairs);
            } catch (err) {
                console.error('Error loading chat history', err);
            }
        };

        loadHistory();
    }, [bookId]);

    const handleClearHistory = async () => {
        if (loading) return;
        try {
            const res = await fetch(
                `${import.meta.env.VITE_API_URL}/chat/history?book_id=${bookId}`,
                { method: 'DELETE' }
            );
            if (!res.ok) throw new Error();
            setHistory([]);
            streamedAnswerRef.current = '';
            setCurrentAnswer(null);
            console.log('[🗑️] History cleared');
        } catch (err) {
            console.error('Error clearing history', err);
        }
    };

    const finalize = () => {
        if (hasEnded.current) return;
        hasEnded.current = true;
        stopStreaming();

        const finalAnswer = streamedAnswerRef.current;
        console.log('[✅] Finalizing answer:', finalAnswer);

        setHistory((prev) => [...prev, { q: question, a: finalAnswer }]);
        setCurrentAnswer(finalAnswer);

        setTimeout(() => {
            setCurrentAnswer(null);
            streamedAnswerRef.current = '';
            console.log('[♻️] Cleared streamed buffer and UI');
        }, 100);

        setQuestion('');
        setLoading(false);
    };

    const handleAsk = () => {
        if (!question.trim()) return;

        hasEnded.current = false;
        setLoading(true);
        setCurrentAnswer('');
        streamedAnswerRef.current = '';
        queueRef.current = [];

        console.log('[🧠] New question:', question);

        const source = new EventSource(
            `${import.meta.env.VITE_API_URL}/chat/stream?question=${encodeURIComponent(
                question
            )}&book_id=${bookId}`
        );

        source.onmessage = (event) => {
            // console.log('[📨] Received chunk:', event.data);
            queueRef.current.push(...event.data);
            startStreaming();
        };

        source.addEventListener('done', () => {
            console.log('[✅] Event: done');
            source.close();
        
            const waitForDrain = setInterval(() => {
                if (queueRef.current.length === 0) {
                    clearInterval(waitForDrain);
                    console.log('[🧹] Queue drained after done → finalizing');
                    finalize();
                } else {
                    console.log('[⌛] Waiting for queue to drain...', queueRef.current.length);
                }
            }, 500); 
        });

        source.onerror = (e) => {
            console.log('[❌] Event: error', e);
            source.close();
            finalize();
        };

        setTimeout(() => {
            if (!hasEnded.current) {
                console.log('[⏰] Timeout triggered');
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
            {/* Header + Ask form */}
            <div className="bg-white/5 rounded-lg p-6">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="text-xl font-semibold text-white">
                        Ask a question about the book
                    </h3>
                    <button
                        onClick={handleClearHistory}
                        disabled={loading}
                        className="flex items-center text-sm text-red-400 hover:text-red-600 disabled:opacity-50"
                    >
                        <Trash2 className="w-4 h-4 mr-1" /> Clear History
                    </button>
                </div>
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
                        className="bg-white/20 hover:bg-white/30 p-3 rounded-full text-white transition disabled:opacity-50"
                        disabled={loading}
                    >
                        {loading ? (
                            <Loader2 className="animate-spin" />
                        ) : (
                            <SendHorizonal />
                        )}
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
                                <div className="flex justify-end items-start space-x-2">
                                    <div className="max-w-lg bg-white/20 text-white rounded-xl px-4 py-2">
                                        {item.q}
                                    </div>
                                    <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center text-white text-sm">
                                        👤
                                    </div>
                                </div>

                                <div className="flex justify-start items-start space-x-2">
                                    <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-white text-sm">
                                        🤖
                                    </div>
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
                                    <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center text-white text-sm">
                                        👤
                                    </div>
                                </div>
                                <div className="flex justify-start items-start space-x-2">
                                    <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-white text-sm">
                                        🤖
                                    </div>
                                    <div className="max-w-lg bg-white/10 text-white/80 rounded-xl px-4 py-2 whitespace-pre-line">
                                        {currentAnswer}
                                        <span className="animate-pulse text-white/50">|</span>
                                    </div>
                                </div>
                            </div>
                        )}

                        {loading && !currentAnswer && (
                            <div className="flex justify-start items-start space-x-2">
                                <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-white text-sm">
                                    🤖
                                </div>
                                <div className="max-w-lg bg-white/10 text-white/80 rounded-xl px-4 py-2">
                                    <span className="inline-block animate-bounce">.</span>
                                    <span className="inline-block animate-bounce delay-150">.</span>
                                    <span className="inline-block animate-bounce delay-300">.</span>
                                </div>
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
