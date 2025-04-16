import { Clock, User } from 'lucide-react';

interface BookCardProps {
    book: {
        id: string;
        title: string;
        cover: string;
        author: string;
        uploadDate: string;
        progress: number;
    };
    hasDetails: boolean;
    onClick: () => void;
}

const BookCard = ({ book, hasDetails, onClick }: BookCardProps) => {
    return (
        <div
            className="relative bg-white/10 rounded-lg overflow-hidden cursor-pointer transform hover:scale-105 transition-transform duration-200 group"
            onClick={onClick}
        >
            {/* Book cover with optional progress bar */}
            <div className="aspect-[3/4] relative">
                <img
                    src={`${import.meta.env.VITE_API_URL}${book.cover}`}
                    alt={book.title}
                    className="w-full h-full object-cover"
                />
            </div>

            {/* Book meta info */}
            <div className="p-3">
                <h3 className="text-sm font-semibold text-white mb-1 truncate">{book.title}</h3>
                <div className="flex items-center text-white/70 text-xs mb-1">
                    <User className="h-3 w-3 mr-1" />
                    <span className="truncate">{book.author}</span>
                </div>
                <div className="flex items-center text-white/70 text-xs">
                    <Clock className="h-3 w-3 mr-1" />
                    <span>{new Date(book.uploadDate).toLocaleDateString()}</span>
                </div>
            </div>

            {/* 🔘 Hover-only overlay if book details not generated */}
            {!hasDetails && (
                <div className="absolute inset-0 bg-gray-900/70 text-white text-sm font-medium items-center justify-center hidden group-hover:flex">
                    Click to generate book details
                </div>
            )}
        </div>
    );
};

export default BookCard;
