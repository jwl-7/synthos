import styles from './SearchResults.module.sass'
import SearchLoader from '../SearchLoader/SearchLoader'

interface SearchResultsProps {
    answer: string
    results: SearchResult[]
    isSearching: boolean
}

export default function SearchResults({ answer, results, isSearching }: SearchResultsProps) {
    if (isSearching) return <SearchLoader />

    const topScoreRaw = results.length > 0 ? results[0].score : 0
    const topScorePercent = (topScoreRaw * 100).toFixed(0)

    const hue = Math.min(Math.max(Number(topScorePercent) * 1.2, 0), 120)
    const scoreColor = `hsl(${hue}, 80%, 45%)`

    return (
        <div className={styles.searchResultsWrapper}>
            <div className={styles.searchResults}>
                {answer && (
                    <div className={styles.card}>
                        <div className={styles.matchScore}>
                            <div className={styles.matchBadge} style={{ borderColor: scoreColor }}>
                                <span className={styles.matchLabel} style={{ color: scoreColor }}>
                                    {topScorePercent}% MATCH
                                </span>
                            </div>
                        </div>

                        <div className={styles.answerContent}>
                            {answer}
                        </div>

                        <div className={styles.debugSources}>
                            <p className={styles.label}>Debug Output</p>
                            {results.slice(0, 3).map((result: any, i: number) => {
                                const scorePercent = (result.score * 100).toFixed(0)
                                const hue = Math.min(Math.max(Number(scorePercent) * 1.2, 0), 120)
                                const scoreColor = `hsl(${hue}, 80%, 45%)`
                                return (
                                    <div key={i} className={styles.sourceItem}>
                                        <span className={styles.matchLabel} style={{ color: scoreColor }}>
                                            {scorePercent}% MATCH
                                        </span>
                                        <p className={styles.text}>
                                            {result.text.substring(0, 120)}...
                                        </p>
                                    </div>
                                )
                            })}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
