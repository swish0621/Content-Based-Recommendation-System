import type { Movie } from "../types";

type Props = {
  movies: Movie[];
  onSelect: (movie: Movie) => void;
};

export default function SearchResults({ movies, onSelect }: Props) {
  return (
    <ul>
        {movies.map((movie) => (
          <li key={movie.id} onClick={() => onSelect(movie)}>
            {movie.original_title}
          </li>
        ))}
      </ul>
  )
}
