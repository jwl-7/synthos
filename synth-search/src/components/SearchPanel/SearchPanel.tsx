import styles from './SearchPanel.module.sass'
import SearchBar from '@/components/SearchBar/SearchBar'
import SearchToggle from '@/components/SearchToggle/SearchToggle'

interface SearchPanelProps {
    query: string
    modelReady: boolean
    activeSource: string
    onQueryChange: (query: string) => void
    onSourceChange: (source: string) => void
}

export default function SearchPanel({
    query,
    modelReady,
    activeSource,
    onQueryChange,
    onSourceChange
}: SearchPanelProps) {
    return (
        <div className={styles.searchPanel}>
            <h1 className={styles.title}>Synthos</h1>
            <SearchToggle
                activeSource={activeSource}
                onSourceChange={onSourceChange}
            />
            <SearchBar
                query={query}
                onQueryChange={onQueryChange}
                modelReady={modelReady}
            />
        </div>
    )
}
