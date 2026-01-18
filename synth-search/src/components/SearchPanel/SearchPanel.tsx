import styles from './SearchPanel.module.sass'
import SearchBar from '@/components/SearchBar/SearchBar'
import clsx from 'clsx'

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
            <div className={styles.toggleWrapper}>
                <div className={clsx(styles.slider, activeSource === 'secrets' && styles.right)} />
                <button
                    className={clsx(styles.toggleButton, activeSource === 'cookbook' && styles.active)}
                    onClick={() => onSourceChange('cookbook')}
                >
                    Cookbook
                </button>
                <button
                    className={clsx(styles.toggleButton, activeSource === 'secrets' && styles.active)}
                    onClick={() => onSourceChange('secrets')}
                >
                    Secrets
                </button>
            </div>

            <SearchBar
                query={query}
                onQueryChange={onQueryChange}
                modelReady={modelReady}
            />
        </div>
    )
}
