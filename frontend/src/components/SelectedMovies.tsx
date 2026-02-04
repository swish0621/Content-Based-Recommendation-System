import type { Movie } from "../types";

type Props = {
    selected: Movie[];
    onRemove: (movie: Movie) => void;
};

export default function SelectedMovies({ selected, onRemove }: Props) {
    return (
        <ul>
        {selected.map((movie) => (
          <li key={movie.id}>
            {movie.original_title}
            <button onClick={() => onRemove(movie)}>X</button>
          </li>
        ))}
      </ul>
    );
}
