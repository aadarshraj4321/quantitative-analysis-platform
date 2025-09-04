import React from 'react';
import { LoaderCircle, CheckCircle2, XCircle, FileClock, Database, Search, Bot } from 'lucide-react';

function JobStatusCard({ job }) {
  const getStatusInfo = (status) => {
    const statusMap = {
      'PENDING': {
        icon: <FileClock className="w-8 h-8 text-yellow-400" />,
        text: 'Your analysis is in the queue.',
        bgColor: 'bg-yellow-900/50 border-yellow-400/30',
      },
      'DATA_FETCHING': {
        icon: <Database className="w-8 h-8 text-blue-400 animate-pulse" />,
        text: 'Agent 1: Data Agent is fetching fundamentals...',
        bgColor: 'bg-blue-900/50 border-blue-400/30',
      },
      'INTELLIGENCE_GATHERING': {
        icon: <Search className="w-8 h-8 text-blue-400 animate-pulse" />,
        text: 'Agent 2: Intelligence Agent is scanning news...',
        bgColor: 'bg-blue-900/50 border-blue-400/30',
      },
      'ANALYZING': {
        icon: <Bot className="w-8 h-8 text-blue-400 animate-spin" />,
        text: 'Agent 3: Analyst Agent is generating a report with Gemini...',
        bgColor: 'bg-blue-900/50 border-blue-400/30',
      },
      'SUCCESS': {
        icon: <CheckCircle2 className="w-8 h-8 text-green-400" />,
        text: 'All agents have completed their tasks!',
        bgColor: 'bg-green-900/50 border-green-400/30',
      },
      'FAILED': {
        icon: <XCircle className="w-8 h-8 text-red-400" />,
        text: `Analysis failed. See error below.`,
        bgColor: 'bg-red-900/50 border-red-400/30',
      }
    };
    
    return statusMap[status] || {
        icon: <FileClock className="w-8 h-8 text-gray-400" />,
        text: 'Waiting for status...',
        bgColor: 'bg-gray-800 border-gray-600',
    };
  };

  const statusInfo = getStatusInfo(job.status);

  return (
    <div className="my-8">
      <div className={`p-6 rounded-lg border flex items-center space-x-4 transition-all duration-500 ${statusInfo.bgColor}`}>
        <div className="flex-shrink-0">
          {statusInfo.icon}
        </div>
        <div>
          <p className="font-bold text-lg text-gray-200">
            Analysis for {job.ticker}
          </p>
          <p className="text-gray-400">{statusInfo.text}</p>
        </div>
      </div>
    </div>
  );
}

export default JobStatusCard;