import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import JobForm from './components/JobForm';
import JobStatusCard from './components/JobStatusCard';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSkeleton from './components/LoadingSkeleton';
import HistoryPanel from './components/HistoryPanel';
import { createJob, getJob } from './services/api';
import { XCircle } from 'lucide-react'; 

function App() {
  const [job, setJob] = useState(null);
  const [isLoading, setIsLoading] = useState(false); 
  const [isPolling, setIsPolling] = useState(false); 
  const [error, setError] = useState(null);

  const handleAnalysisRequest = async (ticker) => {
    setIsLoading(true);
    setIsPolling(true);
    setError(null);
    setJob(null);
    try {
      const response = await createJob(ticker);
      setJob(response.data);
    } catch (err) {
      setError('Failed to create job. Please check the API server and try again.');
      setIsLoading(false);
      setIsPolling(false);
    }
  };

  const handleSelectHistoryJob = (historyJob) => {
    setIsLoading(false);
    setIsPolling(false);
    setError(null);
    setJob(historyJob);
  }

  useEffect(() => {
    if (!job?.id || !isPolling) return;

    if (job.status !== 'PENDING') {
      setIsLoading(false);
    }

    const intervalId = setInterval(async () => {
      try {
        const response = await getJob(job.id);
        const updatedJob = response.data;
        setJob(updatedJob);

        if (updatedJob.status === 'SUCCESS' || updatedJob.status === 'FAILED') {
          clearInterval(intervalId);
          setIsPolling(false);
        }
      } catch (err) {
        setError('Failed to poll job status.');
        clearInterval(intervalId);
        setIsPolling(false);
      }
    }, 3000);

    return () => clearInterval(intervalId);
  }, [job, isPolling]);

  return (
    <div className="min-h-screen bg-gray-900 text-white font-sans">
      <Header />
      <HistoryPanel onSelectJob={handleSelectHistoryJob} />
      
      <main className="container mx-auto p-4 md:p-8">
        <div className="max-w-4xl mx-auto">
          <p className="text-lg text-gray-400 mb-8 text-center">
            Enter an Indian stock ticker to receive a comprehensive, AI-powered analysis.
          </p>
          
          <JobForm onAnalyze={handleAnalysisRequest} isLoading={isLoading || isPolling} />
          
          {error && <div className="my-6 p-4 bg-red-900/50 rounded-lg text-red-300 text-center">{error}</div>}
          
          {isLoading && !job && <LoadingSkeleton />}
          
          {job && !isLoading && <JobStatusCard job={job} />}

          {job?.status === 'SUCCESS' && job.result && (
            <ResultsDisplay result={job.result} />
          )}

          {job?.status === 'FAILED' && job.result?.error && (
             <div className="mt-8 p-6 bg-gray-800/30 border border-red-500/30 rounded-lg text-center animate-fade-in">
               <XCircle className="w-16 h-16 text-red-400 mx-auto mb-4" />
               <h2 className="text-2xl font-bold text-red-300 mb-2">Analysis Failed</h2>
               <p className="text-gray-400 max-w-lg mx-auto">
                 We couldn't complete the analysis for <strong className="text-white">{job.ticker}</strong>.
                 This usually means the stock symbol is incorrect or not listed.
               </p>
               <p className="text-xs text-gray-500 mt-4">Please double-check the ticker (e.g., RELIANCE.NS) and try again.</p>
               
               <details className="mt-6 text-left w-full max-w-lg mx-auto">
                 <summary className="cursor-pointer text-xs text-gray-500 hover:text-gray-400 focus:outline-none">Show technical details</summary>
                 <pre className="mt-2 bg-gray-900 p-4 rounded-md text-gray-400 text-xs whitespace-pre-wrap font-mono">
                   {job.result.error}
                 </pre>
               </details>
             </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;





