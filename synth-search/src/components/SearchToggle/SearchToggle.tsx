import styles from './SearchToggle.module.sass'
import clsx from 'clsx'

interface SearchToggleProps {
    activeSource: string
    onSourceChange: (source: string) => void
}

export default function SearchToggle({ activeSource, onSourceChange }: SearchToggleProps) {
    const isSecrets = activeSource === 'secrets'
    return (
        <button
            className={styles.searchToggleWrapper}
            onClick={() => onSourceChange(isSecrets ? 'cookbook' : 'secrets')}
            type="button"
        >
            <div className={clsx(styles.searchToggleSlider, isSecrets && styles.right)} />
            <span className={clsx(styles.searchToggleButton, !isSecrets && styles.active)}>
                Cookbook
            </span>
            <span className={clsx(styles.searchToggleButton, isSecrets && styles.active)}>
                Secrets
            </span>
        </button>
    )
}
