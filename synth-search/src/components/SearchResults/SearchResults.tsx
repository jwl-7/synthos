import React from 'react'
import styles from './SearchResults.module.sass'
import SearchLoader from '@/components/SearchLoader/SearchLoader'

interface SearchResultsProps {
    answer: string
    results: SearchResult[]
    isSearching: boolean
}

export default function SearchResults({ answer, results, isSearching }: SearchResultsProps) {
    if (isSearching) return <SearchLoader />

    const topScoreRaw = results.length > 0 ? results[0].score : 0

    const renderResult = (result: string, score: number): React.JSX.Element => {
        const scorePercent = (score * 100).toFixed(0)
        const hue = Math.min(Math.max(Number(scorePercent) * 1.2, 0), 120)
        const scoreColor = `hsl(${hue}, 80%, 45%)`
        const scoreFillStyle = {
            width: `${scorePercent}%`,
            backgroundColor: scoreColor,
            color: scoreColor
        }

        return (
            <div className={styles.resultContainer}>
                <div className={styles.scoreContainer}>
                    <div className={styles.scoreBar}>
                        <div className={styles.scoreFill} style={scoreFillStyle}/>
                    </div>
                </div>
                <div className={styles.answerContainer}>
                    <div className={styles.answerWrapper}>
                        {result}
                    </div>
                </div>
            </div>
        )
    }

    const renderTopMatches = () => {
        return (
            <div className={styles.topMatches}>
                <h3 className={styles.topMatchesLabel}>Top Context Matches</h3>
                <div className={styles.topMatchesWrapper}>
                    {results.slice(0, 3).map((result: SearchResult): React.JSX.Element => {
                        return (
                            <div key={result.id} className={styles.topMatchWrapper}>
                                {renderResult(result.text, result.score)}
                            </div>
                        )
                    })}
                </div>
            </div>
        )
    }

    return answer && (
        <div className={styles.searchResults}>
            {renderResult(answer, topScoreRaw)}
            {renderTopMatches()}
        </div>
    )
}
