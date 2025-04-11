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
    onClick: () => void;
}

const BookCard = ({ book, onClick }: BookCardProps) => {
    return (
        <div
            className="bg-white/10 rounded-lg overflow-hidden cursor-pointer transform hover:scale-105 transition-transform duration-200"
            onClick={onClick}
        >
            <div className="aspect-[3/4] relative">
                <img
                src={book.cover || '/no_cover.png'}
                alt={book.title}
                className="w-full h-full object-cover"
            />
                {book.progress < 100 && (
                <div className="absolute bottom-0 left-0 right-0 bg-black/50 p-2">
                    <div className="w-full bg-white/20 rounded-full h-1.5">
                        <div
                            className="bg-white h-1.5 rounded-full transition-all duration-300"
                            style={{ width: `${book.progress}%` }}
                        ></div>
                    </div>
                </div>
                )}
            </div>
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
        </div>
    );
}

export default BookCard;