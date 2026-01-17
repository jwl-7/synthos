import styles from './SearchLoader.module.sass'

export default function SearchLoader() {
    return (
        <div className={styles.searchLoader}>
            <div className={styles.ripple}>
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
    )
}
