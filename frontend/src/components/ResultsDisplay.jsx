import React from 'react';
import { Bot, Newspaper, LineChart, Share2, TrendingUp, TrendingDown, ChevronsUp, ChevronsDown, Landmark, Building2, User, ArrowUp, ArrowDown, Minus } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import HistoricalChart from './HistoricalChart';

const SectionTitle = ({ icon, title, subtitle }) => (
  <div className="mb-8">
    <div className="flex items-center space-x-4 mb-2">
      <div className="p-2 bg-gradient-to-r from-green-500/20 to-emerald-500/20 rounded-lg border border-green-500/30">
        {icon}
      </div>
      <h2 className="text-3xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent tracking-wide">
        {title}
      </h2>
    </div>
    {subtitle && (
      <p className="text-gray-400 ml-16 text-sm leading-relaxed">{subtitle}</p>
    )}
  </div>
);

const MetricCard = ({ title, value, subtitle, trend }) => {
  const getTrendIcon = () => {
    if (trend > 0) return <ArrowUp className="w-4 h-4 text-green-400" />;
    if (trend < 0) return <ArrowDown className="w-4 h-4 text-red-400" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  const getTrendColor = () => {
    if (trend > 0) return 'text-green-400';
    if (trend < 0) return 'text-red-400';
    return 'text-gray-400';
  };

  return (
    <div className="group relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 to-emerald-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl"></div>
      <div className="relative bg-gray-800/60 backdrop-blur-sm p-6 rounded-xl border border-gray-700/50 hover:border-green-500/30 transition-all duration-300 hover:shadow-lg hover:shadow-green-500/10 hover:-translate-y-1">
        <div className="flex items-center justify-between mb-2">
          <p className="text-sm font-medium text-gray-400 uppercase tracking-wide">{title}</p>
          {trend !== undefined && getTrendIcon()}
        </div>
        <p className="text-2xl font-bold text-white mb-1 leading-tight">{value}</p>
        {subtitle && (
          <p className={`text-xs font-medium ${getTrendColor()} flex items-center space-x-1`}>
            <span>{subtitle}</span>
          </p>
        )}
      </div>
    </div>
  );
};

const NewsCard = ({ item, index }) => (
  <a 
    href={item.url} 
    target="_blank" 
    rel="noopener noreferrer" 
    className="group block relative overflow-hidden bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm rounded-xl border border-gray-700/50 hover:border-green-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-green-500/10 hover:-translate-y-2"
  >
    <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 to-emerald-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
    <div className="relative p-6">
      <div className="flex items-start justify-between mb-4">
        <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold ${
          item.sentiment === 'Positive' 
            ? 'bg-green-900/60 text-green-300 border border-green-500/30' 
            : item.sentiment === 'Negative' 
            ? 'bg-red-900/60 text-red-300 border border-red-500/30' 
            : 'bg-yellow-900/60 text-yellow-300 border border-yellow-500/30'
        }`}>
          {item.sentiment}
        </span>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-xs text-gray-500">Live</span>
        </div>
      </div>
      
      <h3 className="font-bold text-gray-100 mb-3 line-clamp-3 leading-snug text-base group-hover:text-green-300 transition-colors">
        {item.title}
      </h3>
      
      <div className="flex justify-between items-center text-xs text-gray-400 pt-4 border-t border-gray-700/50">
        <span className="font-semibold bg-gray-700/50 px-2 py-1 rounded-md">{item.source}</span>
        <span className="opacity-70">Click to read</span>
      </div>
    </div>
  </a>
);

function ResultsDisplay({ result }) {
  if (!result) return null;

  const { 
    company_name, 
    current_price, 
    previous_close, 
    day_high, 
    day_low, 
    fifty_two_week_high, 
    fifty_two_week_low, 
    market_cap, 
    pe_ratio, 
    sector, 
    industry, 
    ceo, 
    intelligence_briefing, 
    llm_analysis 
  } = result;

  const price_change = current_price - previous_close;
  const price_change_percent = ((price_change / previous_close) * 100);
  const advisorReportText = llm_analysis?.llm_report;

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: `${company_name} Analysis`,
        text: `Check out this comprehensive analysis of ${company_name}`,
        url: window.location.href,
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      alert('Analysis link copied to clipboard!');
    }
  };

  return (
    <div className="mt-12 animate-fade-in">
      
      <div className="relative overflow-hidden bg-gradient-to-br from-gray-800/60 to-gray-900/60 backdrop-blur-sm p-8 rounded-2xl border border-gray-700/50 mb-12">
        <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 to-emerald-500/5"></div>
        <div className="relative flex flex-col lg:flex-row justify-between items-start">
          <div className="flex-1">
            <div className="flex items-center space-x-4 mb-4">
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-sm font-medium text-green-400 uppercase tracking-wider">Live Analysis</span>
            </div>
            
            <h1 className="text-5xl lg:text-6xl font-extrabold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-4 leading-tight">
              {company_name}
            </h1>
            
            <div className="flex flex-wrap items-center gap-6 text-gray-400">
              <span className="flex items-center space-x-2 bg-gray-700/50 px-3 py-2 rounded-lg">
                <Building2 className="w-4 h-4 text-green-400" /> 
                <span className="font-medium">{sector}</span>
              </span>
              <span className="flex items-center space-x-2 bg-gray-700/50 px-3 py-2 rounded-lg">
                <Landmark className="w-4 h-4 text-green-400" /> 
                <span className="font-medium">{industry}</span>
              </span>
              <span className="flex items-center space-x-2 bg-gray-700/50 px-3 py-2 rounded-lg">
                <User className="w-4 h-4 text-green-400" /> 
                <span className="font-medium">CEO: {ceo}</span>
              </span>
            </div>
          </div>
          
          <button 
            onClick={handleShare} 
            className="mt-6 lg:mt-0 flex-shrink-0 group relative overflow-hidden bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 hover:shadow-lg hover:shadow-green-500/25 hover:-translate-y-1"
          >
            <div className="absolute inset-0 bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div className="relative flex items-center space-x-2">
              <Share2 className="w-5 h-5" />
              <span>Share Analysis</span>
            </div>
          </button>
        </div>
      </div>

      <div className="mb-16">
        <SectionTitle 
          icon={<TrendingUp className="w-8 h-8 text-green-400" />} 
          title="Key Metrics" 
          subtitle="Real-time financial indicators and performance metrics"
        />
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
          <MetricCard 
            title="Current Price" 
            value={`₹${current_price?.toFixed(2)}`} 
            subtitle={`${price_change >= 0 ? '+' : ''}₹${price_change.toFixed(2)} (${price_change_percent >= 0 ? '+' : ''}${price_change_percent.toFixed(2)}%)`}
            trend={price_change}
          />
          <MetricCard 
            title="Market Cap" 
            value={`₹${(market_cap / 10000000).toFixed(2)} Cr`} 
          />
          <MetricCard 
            title="P/E Ratio" 
            value={pe_ratio?.toFixed(2)} 
            subtitle="Price to Earnings"
          />
          <MetricCard 
            title="Today's Range" 
            value={`₹${day_low?.toFixed(2)}`}
            subtitle={`High: ₹${day_high?.toFixed(2)}`}
          />
          <MetricCard 
            title="52W Range" 
            value={`₹${fifty_two_week_low?.toFixed(2)}`}
            subtitle={`High: ₹${fifty_two_week_high?.toFixed(2)}`}
          />
        </div>
      </div>

      <div className="mb-16">
        <SectionTitle 
          icon={<LineChart className="w-8 h-8 text-green-400" />} 
          title="Price Movement" 
          subtitle="Historical price action over the last 100 trading days"
        />
        
        <div className="relative overflow-hidden bg-gradient-to-br from-gray-800/40 to-gray-900/40 backdrop-blur-sm p-8 rounded-2xl border border-gray-700/50">
          <div className="absolute inset-0 bg-gradient-to-br from-green-500/3 to-emerald-500/3"></div>
          <div className="relative">
            <HistoricalChart ticker={result.ticker} />
          </div>
        </div>
      </div>

      {advisorReportText && (
        <div className="mb-16">
          <SectionTitle 
            icon={<Bot className="w-8 h-8 text-green-400" />} 
            title="AI Analyst Report"
            subtitle="Comprehensive analysis powered by advanced AI models and real-time market data"
          />
          
          <div className="relative overflow-hidden bg-gradient-to-br from-gray-800/40 to-gray-900/40 backdrop-blur-sm rounded-2xl border border-gray-700/50">
            <div className="absolute inset-0 bg-gradient-to-br from-green-500/3 to-emerald-500/3"></div>
            <div className="relative p-8">
              <div className="flex items-center space-x-3 mb-6 pb-4 border-b border-gray-700/50">
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-green-400 uppercase tracking-wider">AI Generated</span>
                <span className="text-xs text-gray-500">•</span>
                <span className="text-xs text-gray-500">Powered by AI</span>
              </div>
              
              <div className="prose prose-invert prose-lg max-w-none text-gray-300 prose-headings:text-green-400 prose-strong:text-white prose-p:leading-relaxed prose-li:leading-relaxed">
                <ReactMarkdown
                  components={{
                    h1: ({node, ...props}) => <h2 className="text-2xl font-bold mt-8 mb-4 text-green-400" {...props} />,
                    h2: ({node, ...props}) => <h3 className="text-xl font-bold mt-6 mb-3 text-green-300" {...props} />,
                    h3: ({node, ...props}) => <h4 className="text-lg font-semibold mt-4 mb-2 text-green-200" {...props} />,
                    ul: ({node, ...props}) => <ul className="list-disc pl-6 space-y-2 my-4" {...props} />,
                    ol: ({node, ...props}) => <ol className="list-decimal pl-6 space-y-2 my-4" {...props} />,
                    li: ({node, ...props}) => <li className="leading-relaxed text-gray-300" {...props} />,
                    p: ({node, ...props}) => <p className="mb-4 leading-relaxed text-gray-300" {...props} />,
                    strong: ({node, ...props}) => <strong className="font-semibold text-white" {...props} />,
                    blockquote: ({node, ...props}) => (
                      <blockquote className="border-l-4 border-green-500/50 pl-4 italic text-gray-400 my-4" {...props} />
                    ),
                  }}
                >
                  {advisorReportText}
                </ReactMarkdown>
              </div>
            </div>
          </div>
        </div>
      )}
      
      <div className="mb-16">
        <SectionTitle 
          icon={<Newspaper className="w-8 h-8 text-green-400" />} 
          title="Market Intelligence" 
          subtitle="Latest news and sentiment analysis from multiple sources"
        />
        
        {intelligence_briefing?.articles?.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
            {intelligence_briefing.articles.slice(0, 9).map((item, index) => (
              <NewsCard key={index} item={item} index={index} />
            ))}
          </div>
        ) : (
          <div className="text-center py-16 bg-gray-800/30 rounded-2xl border border-gray-700/50">
            <Newspaper className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400 text-lg">No news articles found for this symbol.</p>
            <p className="text-gray-500 text-sm mt-2">Try checking back later or verify the ticker symbol.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ResultsDisplay;