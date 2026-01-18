import styles from './AppController.module.sass'
import { useState } from 'react'
import { useSemanticSearch } from '@/hooks/useSemanticSearch'
import SearchPanel from '@/components/SearchPanel/SearchPanel'
import SearchResults from '@/components/SearchResults/SearchResults'
import cookbookData from '@/data/synth-cookbook.json'
import secretsData from '@/data/synth-secrets.json'
import clsx from 'clsx'

export default function AppController() {
    const [query, setQuery] = useState<string>('')
    const [activeKB, setActiveKB] = useState<string>('cookbook')
    const kbData = activeKB === 'cookbook' ? cookbookData : secretsData
    const { answer, results, isSearching, modelReady } = useSemanticSearch(query, kbData as KBEntry[])
    const isActive = query.length > 0

    return (
        <div className={clsx(styles.appWrapper, isActive && styles.active)}>
            <div className={styles.contentWrapper}>
                <SearchPanel
                    query={query}
                    onQueryChange={setQuery}
                    modelReady={modelReady}
                    activeSource={activeKB}
                    onSourceChange={setActiveKB}
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
