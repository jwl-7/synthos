import styles from './AppController.module.sass'
import { useState } from 'react'
import { useSemanticSearch } from '@/hooks/useSemanticSearch'
import SearchPanel from '@/components/SearchPanel/SearchPanel'
import SearchResults from '@/components/SearchResults/SearchResults'
import clsx from 'clsx'
import pdfKbData from '@/data/pdf_kb.json'

export default function AppController() {
    const [query, setQuery] = useState<string>('')
    const kbData = pdfKbData as KBEntry[]
    const { answer, results, isSearching, modelReady } = useSemanticSearch(query, kbData)
    const isActive = query.length > 0

    return (
        <div className={clsx(styles.appWrapper, isActive && styles.active)}>
            <div className={styles.contentWrapper}>
                <SearchPanel
                    query={query}
                    onQueryChange={setQuery}
                    modelReady={modelReady}
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
