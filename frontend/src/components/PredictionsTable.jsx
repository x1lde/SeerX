export default function PredictionsTable({ predictions }) {
    return (
    <div className="card">
        <h2>Predictions</h2>
            <table>
                <thead>
                    <tr>
                    <th>Date</th>
                    <th>Symbol</th>
                    <th>Predicted direction</th>
                    </tr>
                </thead>
                <tbody>
                    {predictions.map((p) => (
                    <tr key={p.id}>
                        <td>{p.date}</td>
                        <td>{p.symbol}</td>
                        <td className={p.predicted_direction === "up" ? "positive" : "negative"}>
                        {p.predicted_direction}
                        </td>
                    </tr>
                    ))}
                </tbody>
            </table>
    </div>
    );
}