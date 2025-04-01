import React, { useState } from 'react';
import { BookOpen, Upload, FileText, BarChart, MessageSquare, Headphones, Loader2, UserCircle } from 'lucide-react';
import BookCard from './components/BookCard';
import UploadArea from './components/UploadArea';
import BookDetails from './components/BookDetails';

interface Book {
    id: string;
    title: string;
    cover: string;
    author: string;
    uploadDate: string;
    progress: number;
    synopsis: string;
}

function App() {
    const [selectedBook, setSelectedBook] = useState<Book | null>(null);
    const [books] = useState<Book[]>([
        {
            id: '1',
            title: 'The Future of AI',
            cover: 'https://images.unsplash.com/photo-1655635643532-fa9ba2648cbe?auto=format&fit=crop&w=300&q=80',
            author: 'Sarah Johnson',
            uploadDate: '2024-03-10',
            progress: 100,
            synopsis: "In 'The Future of AI,' Sarah Johnson presents a comprehensive exploration of artificial intelligence's revolutionary potential. Through expert analysis and real-world examples, she illuminates how AI is transforming industries, reshaping society, and redefining human potential in the digital age."
        },
        {
            id: '2',
            title: 'Digital Renaissance',
            cover: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=300&q=80',
            author: 'Michael Chen',
            uploadDate: '2024-03-08',
            progress: 100,
            synopsis: "'Digital Renaissance' explores the convergence of art, technology, and human creativity in the modern era. Michael Chen weaves together stories of digital innovators, artists, and entrepreneurs who are pioneering new forms of expression and business in our connected world."
        },
        {
            id: '3',
            title: 'The Art of Code',
            cover: 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?auto=format&fit=crop&w=300&q=80',
            author: 'Emma Davis',
            uploadDate: '2024-03-07',
            progress: 100,
            synopsis: "Emma Davis's 'The Art of Code' reveals the beauty and creativity behind software development. This groundbreaking work demonstrates how coding is not just a technical skill but a form of artistic expression, blending logical thinking with creative problem-solving."
        },
        {
            id: '4',
            title: 'Quantum Computing',
            cover: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=300&q=80',
            author: 'Robert Zhang',
            uploadDate: '2024-03-05',
            progress: 100,
            synopsis: "A revolutionary guide to the world of quantum computing, Robert Zhang's book demystifies complex concepts for both technical and non-technical readers. From quantum mechanics principles to practical applications, this book charts the future of computing technology."
        },
        {
            id: '5',
            title: 'The Creative Mind',
            cover: 'https://images.unsplash.com/photo-1546074177-ffdda98d214f?auto=format&fit=crop&w=300&q=80',
            author: 'Lisa Anderson',
            uploadDate: '2024-03-03',
            progress: 100,
            synopsis: "Lisa Anderson delves into the science of creativity and innovation in 'The Creative Mind.' Through neuroscience research and practical exercises, she reveals how we can unlock our creative potential and adapt to an increasingly complex world."
        }
    ]);

    return (
        <div className="min-h-screen bg-gradient-to-br from-[#6c03a8] to-[#023B88]">
            <nav className="bg-white/10 backdrop-blur-lg border-b border-white/20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center">
                            <BookOpen className="h-8 w-8 text-white" />
                            <span className="ml-2 text-2xl font-bold text-white">DemandSens</span>
                        </div>
                        <button className="flex items-center space-x-2 text-white hover:text-white/80 transition-colors">
                            <UserCircle className="h-6 w-6" />
                            <span className="text-sm font-medium">My Account</span>
                        </button>
                    </div>
                </div>
            </nav>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {selectedBook ? (
                    <BookDetails book={selectedBook} onBack={() => setSelectedBook(null)} />
                ) : (
                    <>
                        <UploadArea />

                        <div className="mt-12">
                            <h2 className="text-2xl font-semibold text-white mb-6">Your Books</h2>
                            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
                                {books.map((book) => (
                                    <BookCard
                                        key={book.id}
                                        book={book}
                                        onClick={() => setSelectedBook(book)}
                                    />
                                ))}
                            </div>
                        </div>
                    </>
                )}
            </main>
        </div>
    );
}

export default App;