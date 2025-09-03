import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';

// A more reliable public CORS proxy
const PROXY_URL = 'https://api.allorigins.win/raw?url=';

const fetchHistoricalData = async (ticker) => {
    const yahooUrl = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?range=100d&interval=1d`;
    const encodedUrl = encodeURIComponent(yahooUrl);
    
    try {
        const response = await axios.get(PROXY_URL + encodedUrl);
        const data = response.data.chart.result[0];
        const timestamps = data.timestamp;
        const prices = data.indicators.quote[0].close;

        // Filter out any null price points which can crash the chart
        return timestamps
            .map((ts, i) => ({
                date: new Date(ts * 1000).toLocaleDateString('en-IN', {day: 'numeric', month: 'short'}),
                price: prices[i] ? prices[i].toFixed(2) : null,
            }))
            .filter(point => point.price !== null);

    } catch (error) {
        console.error("Failed to fetch historical data for chart:", error);
        return [];
    }
};

function HistoricalChart({ ticker }) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (ticker) {
            setLoading(true);
            fetchHistoricalData(ticker).then(chartData => {
                setData(chartData);
                setLoading(false);
            });
        }
    }, [ticker]);

    if (loading) return <div className="h-[300px] flex items-center justify-center"><p className="text-gray-400">Loading Chart Data...</p></div>;
    if (data.length === 0) return <div className="h-[300px] flex items-center justify-center"><p className="text-gray-400">Could not load chart data.</p></div>;

    return (
        <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
                <LineChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
                    <XAxis dataKey="date" stroke="#9CA3AF" tick={{ fontSize: 12 }} />
                    <YAxis stroke="#9CA3AF" tick={{ fontSize: 12 }} domain={['auto', 'auto']} />
                    <Tooltip 
                        contentStyle={{ backgroundColor: '#1F2937', border: '1px solid #374151' }}
                        labelStyle={{ color: '#F3F4F6' }}
                    />
                    <Line type="monotone" dataKey="price" stroke="#34D399" strokeWidth={2} name="Close Price" dot={false} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}

export default HistoricalChart;