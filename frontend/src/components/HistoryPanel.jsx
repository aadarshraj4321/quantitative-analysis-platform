import React, { useState, useEffect } from 'react';
import { getJobsHistory } from '../services/api';
import { History, LoaderCircle } from 'lucide-react';

function HistoryPanel({ onSelectJob }) {
  const [history, setHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const fetchHistory = () => {
    setIsLoading(true);
    getJobsHistory()
      .then(response => {
        setHistory(response.data.filter(job => job.status === 'SUCCESS' || job.status === 'FAILED'));
      })
      .catch(error => console.error("Failed to fetch history:", error))
      .finally(() => setIsLoading(false));
  };

  const togglePanel = () => {
    const newIsOpen = !isOpen;
    setIsOpen(newIsOpen);
    if (newIsOpen) {
      fetchHistory();
    }
  };

  const handleSelect = (job) => {
    onSelectJob(job);
    setIsOpen(false);
  }

  return (
    <>
      <button 
        onClick={togglePanel}
        className="fixed bottom-6 right-6 bg-green-600 hover:bg-green-700 text-white p-4 rounded-full shadow-lg z-50 transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-green-400"
        aria-label="Toggle analysis history"
      >
        <History className="w-8 h-8" />
      </button>

      {isOpen && <div onClick={() => setIsOpen(false)} className="fixed inset-0 bg-black/50 z-30 transition-opacity"></div>}

      <div className={`fixed top-0 right-0 h-full bg-gray-900 border-l border-gray-700 shadow-2xl z-40 transition-transform duration-500 ease-in-out ${isOpen ? 'translate-x-0' : 'translate-x-full'} w-full md:w-96`}>
        <div className="p-4 border-b border-gray-700 flex justify-between items-center">
          <h2 className="text-xl font-bold">Analysis History</h2>
          <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-white text-3xl">&times;</button>
        </div>
        <div className="p-4 overflow-y-auto h-[calc(100%-4rem)]">
          {isLoading ? (
            <div className="flex justify-center items-center h-full pt-20">
              <LoaderCircle className="w-8 h-8 animate-spin text-green-400" />
            </div>
          ) : history.length === 0 ? (
            <div className="text-center pt-20">
              <p className="text-gray-500">No past analyses found.</p>
              <p className="text-xs text-gray-600 mt-2">Complete an analysis to see it here.</p>
            </div>
          ) : (
            <ul className="space-y-3">
              {history.map(job => (
                <li 
                  key={job.id} 
                  onClick={() => handleSelect(job)}
                  className="p-3 bg-gray-800 rounded-md cursor-pointer hover:bg-green-800/50 border border-transparent hover:border-green-400/50 transition-all"
                >
                  <p className="font-bold text-white">{job.ticker}</p>
                  <div className="flex justify-between text-xs text-gray-400 mt-1">
                    <span>{new Date(job.created_at).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}</span>
                    <span className={`font-semibold px-2 py-0.5 rounded-full ${job.status === 'SUCCESS' ? 'bg-green-900/50 text-green-300' : 'bg-red-900/50 text-red-300'}`}>{job.status}</span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </>
  );
}

export default HistoryPanel;