import styles from './SearchBar.module.sass'

interface SearchBarProps {
    query: string
    isKbReady: boolean
    onQueryChange: (query: string) => void
}

export default function SearchBar({ query, onQueryChange, isKbReady }: SearchBarProps) {
    return (
        <div className={styles.searchBar}>
            <input
                className={styles.searchInput}
                type="text"
                placeholder="Search"
                autoFocus
                value={query}
                onChange={(e) => onQueryChange(e.target.value)}
                disabled={!isKbReady}
            />
            {!isKbReady && <div className={styles.loadingShimmer} />}
        </div>
    )
}
