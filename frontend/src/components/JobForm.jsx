import React, { useState } from 'react';
import { Search, LoaderCircle } from 'lucide-react';

// The component now receives 'onAnalyze' and 'isLoading' as props
function JobForm({ onAnalyze, isLoading }) {
  const [ticker, setTicker] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!ticker.trim() || isLoading) return;
    onAnalyze(ticker); // Call the function passed down from App.jsx
  };

  return (
    <form onSubmit={handleSubmit} className="mb-12">
      <div className="flex items-center bg-gray-800 border-2 border-gray-600 rounded-lg overflow-hidden focus-within:border-green-400 transition-colors duration-300">
        <span className="pl-4 text-gray-400">
          <Search className="w-6 h-6" />
        </span>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          placeholder="e.g., RELIANCE.NS"
          className="w-full p-4 bg-transparent text-lg text-gray-200 placeholder-gray-500 focus:outline-none"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="bg-green-600 hover:bg-green-700 text-white font-bold py-4 px-6 transition-colors duration-300 disabled:bg-gray-500 disabled:cursor-not-allowed"
          disabled={isLoading}
        >
          {isLoading ? (
            <LoaderCircle className="animate-spin w-6 h-6" />
          ) : (
            'Analyze'
          )}
        </button>
      </div>
    </form>
  );
}

export default JobForm;