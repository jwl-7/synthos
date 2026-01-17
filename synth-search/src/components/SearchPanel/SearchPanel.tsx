import styles from './SearchPanel.module.sass'
import SearchBar from '@/components/SearchBar/SearchBar'

interface SearchPanelProps {
    query: string
    onQueryChange: (query: string) => void
    modelReady: boolean
}

export default function SearchPanel({ query, onQueryChange, modelReady }: SearchPanelProps) {
    return (
        <div className={styles.searchPanel}>
            <h1 className={styles.title}>Synthos</h1>
            <h4 className={styles.tagline}>AI-Assistant for Sound Design</h4>
            <SearchBar
                query={query}
                onQueryChange={onQueryChange}
                modelReady={modelReady}
            />
        </div>
    )
}
