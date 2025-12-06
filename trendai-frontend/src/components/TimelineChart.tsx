import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export function TimelineChart() {
  const data = [
    { time: '00:00', fet: 245, agix: 189, rndr: 98, tao: 156 },
    { time: '04:00', fet: 298, agix: 267, rndr: 134, tao: 178 },
    { time: '08:00', fet: 389, agix: 323, rndr: 178, tao: 201 },
    { time: '12:00', fet: 534, agix: 478, rndr: 234, tao: 267 },
    { time: '16:00', fet: 612, agix: 545, rndr: 298, tao: 312 },
    { time: '20:00', fet: 778, agix: 612, rndr: 356, tao: 289 },
    { time: '23:59', fet: 856, agix: 689, rndr: 423, tao: 334 },
  ];

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1E222D" />
        <XAxis 
          dataKey="time" 
          stroke="#6B7280"
          style={{ fontSize: '12px' }}
        />
        <YAxis 
          stroke="#6B7280"
          style={{ fontSize: '12px' }}
        />
        <Tooltip 
          contentStyle={{
            backgroundColor: '#11141A',
            border: '1px solid #1E222D',
            borderRadius: '8px',
            color: '#fff',
          }}
        />
        <Legend 
          wrapperStyle={{ fontSize: '12px' }}
        />
        <Line 
          type="monotone" 
          dataKey="fet" 
          stroke="#3B82F6" 
          strokeWidth={2}
          name="FET"
          dot={{ fill: '#3B82F6', r: 3 }}
        />
        <Line 
          type="monotone" 
          dataKey="agix" 
          stroke="#8B5CF6" 
          strokeWidth={2}
          name="AGIX"
          dot={{ fill: '#8B5CF6', r: 3 }}
        />
        <Line 
          type="monotone" 
          dataKey="rndr" 
          stroke="#10B981" 
          strokeWidth={2}
          name="RNDR"
          dot={{ fill: '#10B981', r: 3 }}
        />
        <Line 
          type="monotone" 
          dataKey="tao" 
          stroke="#EF4444" 
          strokeWidth={2}
          name="TAO"
          dot={{ fill: '#EF4444', r: 3 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}