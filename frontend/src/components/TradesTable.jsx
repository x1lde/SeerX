export default function TradesTable({ trades }) {
    return (
        <div className="card">
            <h2>Trade history</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Symbol</th>
                        <th>Side</th>
                        <th>Qty</th>
                    </tr>
                </thead>
                <tbody>
                    {trades.map((t) => (
                        <tr key={t.id}>
                            <td>{t.date}</td>
                            <td>{t.symbol}</td>
                            <td className={t.side === "buy" ? "positive" : "negative"}>{t.side}</td>
                            <td>{t.qty}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}