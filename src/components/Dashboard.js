import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [portfolio, setPortfolio] = useState(null);
  const [trades, setTrades] = useState([]);
  const [symbol, setSymbol] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    try {
      const [p, t] = await Promise.all([axios.get('/api/portfolio'), axios.get('/api/trades')]);
      setPortfolio(p.data);
      setTrades(t.data);
    } catch (e) {}
  };

  useEffect(() => { fetchData(); }, []);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post(`/api/analyze/${symbol.toUpperCase()}`);
      fetchData();
    } catch (e) {}
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>AI Trading Dashboard</h1>
      <div style={{ marginBottom: '20px', padding: '15px', border: '1px solid #ccc' }}>
        <h2>Portfolio: ${portfolio?.balance?.toFixed(2) || '0.00'}</h2>
      </div>
      <form onSubmit={handleAnalyze} style={{ marginBottom: '20px' }}>
        <input value={symbol} onChange={e => setSymbol(e.target.value)} placeholder="Symbol (e.g. TSLA)" />
        <button disabled={loading}>{loading ? 'Analyzing...' : 'Analyze'}</button>
      </form>
      <table border="1" cellPadding="5" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr><th>Symbol</th><th>Action</th><th>Price</th><th>Status</th><th>PNL</th></tr>
        </thead>
        <tbody>
          {trades.map(t => (
            <tr key={t.id}><td>{t.symbol}</td><td>{t.action}</td><td>{t.price}</td><td>{t.status}</td><td>{t.pnl}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;
