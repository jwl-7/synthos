import styles from './AppController.module.sass'
import { useEffect, useState } from 'react'
import { useSemanticSearch } from '@/hooks/useSemanticSearch'
import SearchPanel from '@/components/SearchPanel/SearchPanel'
import SearchResults from '@/components/SearchResults/SearchResults'
import clsx from 'clsx'

export default function AppController() {
    const [query, setQuery] = useState<string>('')
    const [activeKb, setActiveKb] = useState<string>('cookbook')
    const [kbData, setKbData] = useState<KbData[]>([])
    const [isLoadingData, setIsLoadingData] = useState(false)

    useEffect(() => {
        const loadKb = async () => {
            setIsLoadingData(true)
            const fileName = activeKb === 'cookbook' ? 'synth-cookbook.json' : 'synth-secrets.json'
            try {
                const response = await fetch(`data/${fileName}`)
                const data = await response.json()
                setKbData(data)
            } catch (e) {
                console.error('Failed to load knowledge base:', e)
            } finally {
                setIsLoadingData(false)
            }
        }
        loadKb()
    }, [activeKb])

    const { answer, results, isSearching, modelReady } = useSemanticSearch(query, kbData)
    const isActive = query.length > 0
    const isKbReady = modelReady && !isLoadingData

    return (
        <div className={clsx(styles.appWrapper, isActive && styles.active)}>
            <div className={styles.contentWrapper}>
                <SearchPanel
                    query={query}
                    onQueryChange={setQuery}
                    isKbReady={isKbReady}
                    activeSource={activeKb}
                    onSourceChange={setActiveKb}
                />
                <SearchResults
                    answer={answer}
                    results={results}
                    isSearching={isSearching}
                />
            </div>
        </div>
    )
}
