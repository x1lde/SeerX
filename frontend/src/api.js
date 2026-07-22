const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

async function get(path) { 
    const res = await fetch(`${API_URL}${path}`);
    if (!res.ok) throw new Error(`Request failed: ${res.status}`);
    return res.json();
}

export const fetchPortfolio = () => get("/portfolio");
export const fetchPredictions = () => get("/predictions");
export const fetchTrades = () => get("/trades");