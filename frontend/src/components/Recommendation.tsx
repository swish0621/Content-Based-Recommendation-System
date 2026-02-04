import type {Recommendation} from "./../types"


type Props = {
    recommended: Recommendation[];
};

export default function Recommendations({recommended}: Props) {
    return (
        <ul>
            {recommended.map((rec) => (
                <li key={rec.original_title}>
                    Name: {rec.original_title} Similarity: {rec.similarity.toFixed(2)}
                </li>
            ))}
        </ul>
    );
}
