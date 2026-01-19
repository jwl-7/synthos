import styles from './ThemeToggle.module.sass'
import { useState, useEffect } from 'react'
import clsx from 'clsx'
import Moon from './Moon'
import Sun from './Sun'

export default function ThemeToggle() {
    const [theme, setTheme] = useState<string>('light')

    const handleThemeChange = () => {
        if (typeof window === 'undefined') return

        const newTheme = theme === 'light' ? 'dark' : 'light'
        setTheme(newTheme)
        document.documentElement.setAttribute('data-theme', newTheme)
        localStorage.setItem('theme', newTheme)

        window.dispatchEvent(new CustomEvent('themeChange', { detail: { theme: newTheme } }))
    }

    useEffect(() => {
        if (typeof window === 'undefined') return

        const stored = localStorage.getItem('theme')
        const initial = document.documentElement.getAttribute('data-theme')
        const themeChoice = (stored || initial || 'light') as 'light' | 'dark'

        setTheme(themeChoice)
        document.documentElement.setAttribute('data-theme', themeChoice)
    }, [])

    return (
        <button
            className={clsx(styles.themeToggleWrapper, theme === 'dark' && styles.dark)}
            onClick={handleThemeChange}
            type="button"
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
            aria-checked={theme === 'dark'}
            role="switch"
        >
            <div className={styles.themeToggleSlider} />
            <div className={clsx(styles.themeIcon, styles.sun)}>
                <Sun />
            </div>
            <div className={clsx(styles.themeIcon, styles.moon)}>
                <Moon />
            </div>
        </button>
    )
}
