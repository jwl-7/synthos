interface KbData {
    id: string
    text: string
    vector: number[]
}

interface SearchResult {
    id?: string
    text: string
    score: number
}
