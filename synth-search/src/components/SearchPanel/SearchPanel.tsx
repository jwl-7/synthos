import styles from './SearchPanel.module.sass'
import SearchBar from '@/components/SearchBar/SearchBar'
import SearchToggle from '@/components/SearchToggle/SearchToggle'
import ThemeToggle from '@/components/ThemeToggle/ThemeToggle'

interface SearchPanelProps {
    query: string
    isKbReady: boolean
    activeSource: string
    onQueryChange: (query: string) => void
    onSourceChange: (source: string) => void
}

export default function SearchPanel({
    query,
    isKbReady,
    activeSource,
    onQueryChange,
    onSourceChange
}: SearchPanelProps) {
    return (
        <div className={styles.searchPanel}>
            <h1 className={styles.title}>Synthos</h1>
            <ThemeToggle />
            <SearchToggle
                activeSource={activeSource}
                onSourceChange={onSourceChange}
            />
            <SearchBar
                query={query}
                onQueryChange={onQueryChange}
                isKbReady={isKbReady}
            />
        </div>
    )
}
