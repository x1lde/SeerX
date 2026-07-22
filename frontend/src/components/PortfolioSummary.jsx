export default function PortfolioSummary({ portfolio }) {
    if (!portfolio) return null;
}

return (
    <div classname='card'>
        <h2>Portfolio</h2>
        <div classname="stats">
            <div>
                <span classname='label'>Equity</span>
                <span classname='value'>${portfolio.equity.toLocaleString()}</span>
            </div>
            <div>
                <span classname='label'>Cash</span>
                <span classname='value'>${portfolio.cash.toLocaleString()}</span>
            </div>
            <div>
                <span classname='label'>Buying power</span>
                <span classname='value'>${portfolio.buying_power.toLocaleString()}</span>
            </div>
        </div>

        {portfolio.positions.length > 0 && (
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Qty</th>
                        <th>Market value</th>
                        <th>Unrealized P/L</th>
                    </tr>
                </thead>
                <tbody>
                    {portfolio.positions.map((p)=> (
                        <tr key={p.symbol}>
                            <td>{p.symbol}</td>
                            <td>{p.qty}</td>
                            <td>${p.market_value.toLocaleString()}</td>
                            <td classname={p.unrealized_pl >= 0 ? "positive":"negative"}>
                                ${p.unrealized_pl.toLocaleString()}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        )}
    </div>
);