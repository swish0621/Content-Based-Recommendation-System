import { useState } from "react";
import type { Movie, Recommendation } from "./types";
import Recommendations from "./components/Recommendations";
import SelectedMovies from "./components/SelectedMovies";
import SearchResults from "./components/SearchResults";
import "./App.css";

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Movie[]>([]);
  const [selectedMovies, setSelectedMovies] = useState<Movie[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSearch() {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
      await throwIfNotOk(res);
      const data = (await res.json()) as Movie[];
      console.log(data);
      setResults(data);
    } catch (e: unknown) {
      const message =
        e instanceof Error ? e.message : "Something went wrong during search";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function handleSelection(movie: Movie) {
    if (selectedMovies.some((m) => m.id === movie.id)) return;
    setSelectedMovies((prev) => [...prev, movie]);
  }

  function removeSelection(movie: Movie) {
    const updatedItems = selectedMovies.filter(
      (selected) => selected.id !== movie.id,
    );
    setSelectedMovies(updatedItems);
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

      await throwIfNotOk(res);
      const data = (await res.json()) as Recommendation[];
      setRecommendations(data);
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
    setRecommendations([]);
    setResults([]);
    setSelectedMovies([]);
    setError(null);
  }

  async function throwIfNotOk(res: Response) {
    if (res.ok) return;
    const text = await res.text().catch(() => "");
    throw new Error(
      text
        ? `Request Failed (${res.status}): ${text}`
        : `Request Failed: ${res.status}`,
    );
  }

  return (
    <div className="container">
      <h1 className="text-center">Recommendation System</h1>
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      <div className="search-row">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for a movie..."
        />
        <button
          onClick={handleSearch}
          disabled={!query.trim() || loading}
          style={{ marginLeft: 8 }}
        >
          Search
        </button>
      </div>
      <SearchResults movies={results} onSelect={handleSelection} />
      <h1 className="text-center">Selected Movies</h1>
      <SelectedMovies selected={selectedMovies} onRemove={removeSelection} />
      <button
        onClick={() => handleRecommendation(selectedMovies)}
        disabled={selectedMovies.length === 0 || loading}
      >
        {loading ? "Loading..." : "Get Recommendation"}
      </button>
      <Recommendations recommendations={recommendations} />
      <button
        onClick={handleReset}
        disabled={
          selectedMovies.length === 0 &&
          recommendations.length === 0 &&
          query.trim().length === 0 &&
          results.length === 0
        }
      >
        Reset
      </button>
    </div>
  );
}
