import { FC } from 'react';
import ReactMarkdown from 'react-markdown';

interface Reference {
    verse: string;
    text: string;
}

interface ChatResponseProps {
    summary: string;
    explanation: string;
    references: Reference[];
}

const ChatResponse: FC<ChatResponseProps> = ({ summary, explanation, references }) => {
    return (
        <div className="max-w-4xl mx-auto">
            {/* Main Response Card */}
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
                {/* Assistant Header */}
                <div className="border-b border-gray-100">
                    <div className="px-6 py-4 flex items-center space-x-3">
                        <div className="flex-shrink-0">
                            <div className="h-10 w-10 bg-indigo-100 rounded-full flex items-center justify-center">
                                {/* <i className="fas fa-robot text-indigo-600 text-lg"></i> */}
                                <span className="text-indigo-600">🤖</span>
                            </div>
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-gray-900">Assistant</h2>
                            <p className="text-sm text-gray-500">Spiritual Guide</p>
                        </div>
                    </div>
                </div>
                
                {/* Main Content */}
                <div className="px-6 py-6 space-y-8">
                    {/* Summary Section */}
                    <div className="animate-fade-in">
                        <div className="flex items-center space-x-2 mb-4">
                            {/* <div className="h-8 w-8 bg-amber-100 rounded-lg flex items-center justify-center"> */}
                                {/* <i className="fas fa-star-half-alt text-amber-600"></i> */}
                               <span className="text-blue-600">🌟</span>
                            {/* </div> */}
                            <h3 className="text-lg font-semibold text-gray-900">Summary</h3>
                        </div>
                        <div className="bg-amber-50 rounded-xl p-5 border border-amber-100">
                            <div className="prose prose-amber prose-sm sm:prose-base max-w-none">
                                <ReactMarkdown>
                                    {summary}
                                </ReactMarkdown>
                            </div>
                        </div>
                    </div>

                    {/* Detailed Answer Section */}
                    <div className="animate-fade-in">
                        <div className="flex items-center space-x-2 mb-4">
                            {/* <div className="h-8 w-8 bg-blue-100 rounded-lg flex items-center justify-center"> */}
                                {/* <i className="fas fa-book-open text-blue-600"></i> */}
                                <span className="text-blue-600">📚</span>
                            {/* </div> */}
                            <h3 className="text-lg font-semibold text-gray-900">Detailed Explanation</h3>
                        </div>
                        <div className="bg-blue-50 rounded-xl p-5 border border-blue-100">
                            <div className="prose prose-blue prose-sm sm:prose-base max-w-none">
                                <ReactMarkdown>
                                    {explanation}
                                </ReactMarkdown>
                            </div>
                        </div>
                    </div>

                    {/* References Section */}
                    <div className="animate-fade-in">
                        <div className="flex items-center space-x-2 mb-4">
                            {/* <div className="h-8 w-8 bg-purple-100 rounded-lg flex items-center justify-center"> */}
                                {/* <i className="fas fa-quote-left text-purple-600"></i> */}
                                <span className="text-purple-600">💬</span>
                            {/* </div> */}
                            <h3 className="text-lg font-semibold text-gray-900">References</h3>
                        </div>
                        <div className="space-y-4">
                            {references.map((reference, index) => (
                                <div key={index} className="group bg-white rounded-xl p-5 border border-gray-200 hover:border-purple-200 transition-all duration-300 hover:shadow-md">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
                                            {/* <i className="fas fa-book mr-2"></i> */}
                                            <span className="text-purple-600">📖</span> 
                                            &nbsp;{reference.verse}
                                        </span>
                                    </div>
                                    <p className="text-gray-600 italic">
                                        {reference.text}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatResponse; 