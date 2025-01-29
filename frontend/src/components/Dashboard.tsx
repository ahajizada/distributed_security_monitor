import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

interface LogData {
  timestamp: string;
  count: number;
}

interface AlertData {
  id: string;
  severity: string;
  message: string;
  timestamp: string;
}

const Dashboard: React.FC = () => {
  const [logData, setLogData] = useState<LogData[]>([]);
  const [alerts, setAlerts] = useState<AlertData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [logResponse, alertResponse] = await Promise.all([
        fetch('/api/logs/stats'),
        fetch('/api/alerts')
      ]);
      
      const logs = await logResponse.json();
      const alertsData = await alertResponse.json();
      
      setLogData(logs);
      setAlerts(alertsData);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center">Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Log Volume</h2>
        <LineChart width={800} height={300} data={logData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="count" stroke="#2563eb" />
        </LineChart>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Recent Alerts</h2>
        <div className="space-y-4">
          {alerts.map((alert) => (
            <Alert key={alert.id}>
              <AlertTitle className="text-lg font-semibold">
                {alert.severity} Alert
              </AlertTitle>
              <AlertDescription>
                {alert.message}
                <div className="text-sm text-gray-500 mt-1">
                  {new Date(alert.timestamp).toLocaleString()}
                </div>
              </AlertDescription>
            </Alert>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
