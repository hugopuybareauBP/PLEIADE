import { useState, useEffect } from 'react';
import { BookOpen, UserCircle } from 'lucide-react';
import BookCard from './components/BookCard';
import UploadArea from './components/UploadArea';
import BookDetails from './components/BookDetails/BookDetails';

interface Book {
    id: string;
    title: string;
    cover: string;
    author: string;
    uploadDate: string;
    progress: number;
    synopsis: string;
    full_text: string;
    chunks: [];
    hasDetails: boolean;
}

function App() {
    const [selectedBook, setSelectedBook] = useState<Book | null>(null);
    const [books, setBooks] = useState<Book[]>([]);

    useEffect(() => {
        fetchBooks();
    }, []);

    const fetchBooks = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/books`);
            const data = await response.json();
            setBooks(data);
            console.log("Books fetched:", data);
        } catch (error) {
            console.error("Error fetching books:", error);
        }
    };

    const handleBookClick = (book: Book) => {
        setSelectedBook(book);
    };

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
                    <BookDetails
                        book={selectedBook}
                        onBack={() => {
                            setSelectedBook(null);
                            fetchBooks();
                        }}
                    />
                ) : (
                    <>
                        <UploadArea onUploadSuccess={fetchBooks} />

                        <div className="mt-12">
                            <h2 className="text-2xl font-semibold text-white mb-6">Your Books</h2>
                            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
                                {books.map((book) => (
                                    <BookCard
                                        key={book.id}
                                        book={book}
                                        hasDetails={book.hasDetails}
                                        onClick={() => handleBookClick(book)}
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
