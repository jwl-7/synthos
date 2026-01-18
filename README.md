<div align="center">
    <img alt="Demo" width="400" src="https://github.com/user-attachments/assets/f1122d51-ceef-4145-86ee-a026ea562b93" />
</div>

# 🔍 synthos
AI-Assistant for Sound Design

## 🧠 How It Works
This project implements a local [RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)-esque pipeline to provide fast, accurate search results without the need for a backend server.

#### Vectorization (Offline)
The python [pre-processor](./pre-processor/) uses
[pymupdf](https://github.com/pymupdf/PyMuPDF) to extract the text from a `.pdf` file. The text content is split into sentence-based chunks and sanitized. The chunks are processed by [sentence-transformers](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) to then fully convert the `.pdf` -> vector embeddings (`.json`).

#### Semantic Retrieval (Client-Side)
The frontend [synth-search](./synth-search/) uses [Transformers.js](https://huggingface.co/docs/transformers.js/en/index) to perform local inference. When a user searches, the query is vectorized in-browser using the AI model [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2). A cosine similarity calculation is performed against the local index to find the most contextually relevant matches.

#### Semantic Processing (Client-Side)
The semantic data matched from the user query is sanitized and processed as a prompt to the AI model [Flan-T5 Base](https://huggingface.co/Xenova/flan-t5-base). The text-to-text generation is cleaned and sent to the user.

## Data Sources
- [Synth Secrets](https://www.soundonsound.com/series/synth-secrets-sound-sound) by Sound On Sound
- [Welsh's Synthesizer Cookbook](https://synthesizer-cookbook.com/) by Fred Welsh

## ⚖️ License
This project is released under the GNU GPL License - see the [LICENSE](LICENSE) file for details
