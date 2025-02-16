import { FC } from 'react';
import ReactMarkdown from 'react-markdown';

interface Reference {
    verse: string;
    text: string;
}

interface ChatResponseProps {
    summary?: string;
    explanation?: string;
    references?: Reference[];
    error?: boolean;
}

const ChatResponse: FC<ChatResponseProps> = ({ summary, explanation, references, error }) => {
    if (error) {
        return (
            <div className="max-w-4xl mx-auto">
                <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden border border-red-200 dark:border-red-800">
                    <div className="p-6 flex items-center space-x-3">
                        <div className="h-10 w-10 bg-red-100 dark:bg-red-900/50 rounded-full flex items-center justify-center">
                            <span className="text-xl">⚠️</span>
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-red-600 dark:text-red-400">Response Error</h2>
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                                I apologize, but I encountered an error processing the response. Please try again.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden border border-gray-200 dark:border-gray-700">
                {/* Assistant Header */}
                <div className="border-b border-gray-100 dark:border-gray-700">
                    <div className="px-6 py-4 flex items-center space-x-3">
                        <div className="flex-shrink-0">
                            {/* <div className="h-10 w-10 bg-indigo-100 dark:bg-indigo-900/50 rounded-full flex items-center justify-center"> */}
                                <span className="text-xl">🤖</span>
                            {/* </div> */}
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Assistant</h2>
                            <p className="text-sm text-gray-500 dark:text-gray-400">Spiritual Guide</p>
                        </div>
                    </div>
                </div>
                
                {/* Main Content */}
                <div className="px-6 py-6 space-y-8">
                    {/* Summary Section */}
                    {summary && (
                        <div className="animate-fade-in">
                            <div className="flex items-center space-x-2 mb-4">
                                {/* <div className="h-8 w-8 bg-amber-100 dark:bg-amber-900/50 rounded-lg flex items-center justify-center"> */}
                                    <span className="text-lg">⭐</span>
                                {/* </div> */}
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Summary</h3>
                            </div>
                            <div className="bg-amber-50 dark:bg-amber-900/20 rounded-xl p-5 border border-amber-100 dark:border-amber-800">
                                <div className="prose dark:prose-invert prose-amber prose-sm sm:prose-base max-w-none">
                                    <ReactMarkdown>
                                        {summary}
                                    </ReactMarkdown>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Detailed Answer Section */}
                    {explanation && (
                        <div className="animate-fade-in">
                            <div className="flex items-center space-x-2 mb-4">
                                {/* <div className="h-8 w-8 bg-blue-100 dark:bg-blue-900/50 rounded-lg flex items-center justify-center"> */}
                                    <span className="text-lg">📚</span>
                                {/* </div> */}
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Detailed Explanation</h3>
                            </div>
                            <div className="bg-blue-50 dark:bg-blue-900/20 rounded-xl p-5 border border-blue-100 dark:border-blue-800">
                                <div className="prose dark:prose-invert prose-blue prose-sm sm:prose-base max-w-none">
                                    <ReactMarkdown>
                                        {explanation}
                                    </ReactMarkdown>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* References Section */}
                    {references && references.length > 0 && (
                        <div className="animate-fade-in">
                            <div className="flex items-center space-x-2 mb-4">
                                {/* <div className="h-8 w-8 bg-purple-100 dark:bg-purple-900/50 rounded-lg flex items-center justify-center"> */}
                                    <span className="text-lg">💬</span>
                                {/* </div> */}
                                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">References</h3>
                            </div>
                            <div className="space-y-4">
                                {references.map((reference, index) => (
                                    <div key={index} 
                                        className="group bg-white dark:bg-gray-800 rounded-xl p-5 
                                                 border border-gray-200 dark:border-gray-700 
                                                 hover:border-purple-200 dark:hover:border-purple-700 
                                                 transition-all duration-300 hover:shadow-md"
                                    >
                                        <div className="flex items-center justify-between mb-2">
                                            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium 
                                                           bg-purple-100 dark:bg-purple-900/50 
                                                           text-purple-800 dark:text-purple-300"
                                            >
                                                <span className="mr-2">📖</span>
                                                {reference.verse}
                                            </span>
                                        </div>
                                        <p className="text-gray-600 dark:text-gray-300 italic">
                                            {reference.text}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ChatResponse; 