import { useState, useEffect } from 'react'
import { pipeline, cos_sim } from '@xenova/transformers'

export function useSemanticSearch(query: string, kbData: KBEntry[]) {
    const [pipelines, setPipelines] = useState<{ extractor: any, generator: any } | null>(null)
    const [answer, setAnswer] = useState<string>('')
    const [results, setResults] = useState<SearchResult[]>([])
    const [isSearching, setIsSearching] = useState(false)

    useEffect(() => {
        async function init() {
            try {
                const extractor = await pipeline('feature-extraction', 'Xenova/all-mpnet-base-v2')
                const generator = await pipeline('text2text-generation', 'Xenova/Flan-T5-base')
                setPipelines({ extractor, generator })
            } catch (e) {
                console.error('Model failed to initialize:', e)
            }
        }
        init()
    }, [])

    useEffect(() => {
        if (!query.trim() || !pipelines) {
            setAnswer('')
            setResults([])
            setIsSearching(false)
            return
        }

        setIsSearching(true)

        const timeoutId = setTimeout(async () => {
            try {
                const { extractor, generator } = pipelines
                const output = await extractor(query, { pooling: 'mean', normalize: true })
                const queryVector = Array.from(output.data) as number[]
                const scored = kbData.map(item => {
                    const vec = item.vector
                    const score = vec && vec.length === queryVector.length ? cos_sim(queryVector, vec) : -1
                    return { ...item, score }
                })

                const topResults = scored
                    .sort((a, b) => b.score - a.score)
                    .slice(0, 5)
                setResults(topResults)

                let contextText = topResults.map(r => r.text).join(' ')
                    .replace(/\s+/g, ' ')
                    .trim()
                if (!contextText) {
                    contextText = topResults.map(r => r.text).join(' ')
                }

                const prompt = `Context: ${contextText}\nQuestion: ${query}\nAnswer:`
                const generatorOutput = await generator(prompt, {
                    max_new_tokens: 120,
                    repetition_penalty: 2.0,
                    temperature: 0.5,
                    do_sample: true
                })
                const cleanAnswer = generatorOutput[0]?.generated_text?.trim() || 'No information found.'
                setAnswer(cleanAnswer)
            } catch (err) {
                console.error('Search failed:', err)
                setAnswer('Failed to process the query.')
            } finally {
                setIsSearching(false)
            }
        }, 600)

        return () => clearTimeout(timeoutId)
    }, [query, pipelines, kbData])

    return {
        answer,
        results,
        isSearching,
        modelReady: !!pipelines
    }
}
