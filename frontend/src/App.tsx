import { useState } from "react";

type Movie = {
  id: number;
  original_title: string;
};

type Recommendation = {
  original_title: string;
  similarity: number;
};

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Movie[]>([]);
  const [selected, setSelected] = useState<Movie[]>([]);
  const [recommended, setRecommended] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSearch() {
    const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
    if (!res.ok) throw new Error(`Request Failed: ${res.status}`);
    const data = (await res.json()) as Movie[];
    console.log(data);
    setResults(data);
  }

  function handleSelection(movie: Movie) {
    if (selected.some((m) => m.id === movie.id)) return;
    setSelected((prev) => [...prev, movie]);
  }

  function removeSelection(movie: Movie) {
    const updatedItems = selected.filter(
      (selected) => selected.id !== movie.id,
    );
    setSelected(updatedItems);
  }

  async function handleRecommendation(selected: Movie[]) {
    setLoading(true);
    setError(null);

    try {
      const ids = selected.map((sel) => sel.id);

      const res = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(ids),
      });

      if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(
          text
            ? `Request Failed (${res.status}): ${text}`
            : `Request Failed: ${res.status} `,
        );
      }
      const data = (await res.json()) as Recommendation[];
      setRecommended(data);
    } catch (e: unknown) {
      const message =
        e instanceof Error
          ? e.message
          : "Something went wrong while fetching recommendations";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setQuery("");
    setRecommended([]);
    setResults([]);
    setSelected([]);
    setError(null);
  }

  return (
    <div style={{ padding: 40 }}>
      <h1>Search</h1>
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type Something"
      />

      <button
        onClick={handleSearch}
        disabled={!query.trim() || loading}
        style={{ marginLeft: 8 }}
      >
        Search
      </button>

      <ul>
        {results.map((res) => (
          <li key={res.id} onClick={() => handleSelection(res)}>
            {res.original_title}
          </li>
        ))}
      </ul>

      <h1>Selected Movies</h1>
      <ul>
        {selected.map((sel) => (
          <li key={sel.id}>
            {sel.original_title}{" "}
            <button onClick={() => removeSelection(sel)}>X</button>
          </li>
        ))}
      </ul>

      <button
        onClick={() => handleRecommendation(selected)}
        disabled={selected.length === 0 || loading}
      >
        {loading ? "Loading..." : "Get Recommendation"}
      </button>

      <ul>
        {recommended.map((rec) => (
          <li key={rec.original_title}>
            Name: {rec.original_title} Similarity: {rec.similarity.toFixed(2)}
          </li>
        ))}
      </ul>
      <button
        onClick={handleReset}
        disabled={
          selected.length === 0 &&
          recommended.length === 0 &&
          query.trim().length === 0 &&
          results.length === 0
        }
      >
        Reset
      </button>
    </div>
  );
}
