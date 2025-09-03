import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area } from 'recharts';

function PredictionChart({ data }) {
  if (!data || data.length === 0) return null;

  // Format the date for the X-axis
  const formatXAxis = (tickItem) => {
    return new Date(tickItem).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' });
  };
  
  return (
    <div style={{ width: '100%', height: 400 }}>
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#4A5568" />
          <XAxis dataKey="ds" tickFormatter={formatXAxis} stroke="#A0AEC0" />
          <YAxis stroke="#A0AEC0" domain={['dataMin - 5', 'dataMax + 5']} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1A202C', border: '1px solid #4A5568' }}
            labelFormatter={(label) => new Date(label).toLocaleDateString('en-IN')}
          />
          <Legend />
          {/* Confidence Interval Area */}
          <Area type="monotone" dataKey="yhat_upper" fill="#2F855A" stroke="#2F855A" fillOpacity={0.1} name="Upper Confidence" dot={false} />
          <Area type="monotone" dataKey="yhat_lower" fill="#2F855A" stroke="#2F855A" fillOpacity={0.1} name="Lower Confidence" dot={false} />
          
          {/* Forecast Line */}
          <Line type="monotone" dataKey="yhat" stroke="#48BB78" strokeWidth={2} name="Forecast" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default PredictionChart;