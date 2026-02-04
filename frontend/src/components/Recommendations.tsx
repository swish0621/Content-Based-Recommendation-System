import type { Recommendation } from "../types";

type Props = {
  recommendations: Recommendation[];
};

export default function Recommendations({ recommendations }: Props) {
  return (
    <ul>
      {recommendations.map((rec) => (
        <li key={rec.original_title}>
          Name: {rec.original_title} Similarity: {rec.similarity.toFixed(2)}
        </li>
      ))}
    </ul>
  );
}
