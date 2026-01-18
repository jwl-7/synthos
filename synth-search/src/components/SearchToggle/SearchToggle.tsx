import styles from './SearchToggle.module.sass'
import clsx from 'clsx'

interface SearchToggleProps {
    activeSource: string
    onSourceChange: (source: string) => void
}

export default function SearchToggle({ activeSource, onSourceChange }: SearchToggleProps) {
    return (
        <div className={styles.searchToggleWrapper}>
            <div className={clsx(styles.searchToggleSlider, activeSource === 'secrets' && styles.right)} />
            <button
                className={clsx(styles.searchToggleButton, activeSource === 'cookbook' && styles.active)}
                onClick={() => onSourceChange('cookbook')}
            >
                Cookbook
            </button>
            <button
                className={clsx(styles.searchToggleButton, activeSource === 'secrets' && styles.active)}
                onClick={() => onSourceChange('secrets')}
            >
                Secrets
            </button>
        </div>
    )
}
