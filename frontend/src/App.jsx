import {useEffect, useState } from 'react'
import {fetchPortfolio, fetchPredictions, fetchTrades} from "./api";
import PortfolioSummary from "./components/PortfolioSummary"
import PredictionsTable from './components/PredictionsTable';
import TradesTable from './components/TradesTable';
import './App.css'

export default function App(){
  const [portfolio, setPortfolio] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [trades, setTrades] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData(){
      try {
      const [portfolioData, predictionsData, tradesData] = await Promise.all([
        fetchPortfolio(),
        fetchPredictions(),
        fetchTrades(),
      ]);
      setPortfolio(portfolioData);
      setPredictions(predictionsData);
      setTrades(tradesData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <div className='status'>Loading dashboard...</div>;
  if (error) return <div className='status error'>Failed to load data: {error}</div>

  return (
    <div className='app'>
      <h1>SeerX</h1>
      <PortfolioSummary portfolio={portfolio} />
      <div className="grid">
        <PredictionsTable predictions={predictions} />
        <TradesTable trades={trades}/>
      </div>
    </div>
  )
}