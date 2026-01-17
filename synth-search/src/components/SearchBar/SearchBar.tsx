import styles from './SearchBar.module.sass'

interface SearchBarProps {
    query: string
    onQueryChange: (query: string) => void
    modelReady: boolean
}

export default function SearchBar({ query, onQueryChange, modelReady }: SearchBarProps) {
    return (
        <div className={styles.searchBar}>
            <input
                type="text"
                placeholder="Search"
                autoFocus
                value={query}
                onChange={(e) => onQueryChange(e.target.value)}
                disabled={!modelReady}
            />
        </div>
    )
}
