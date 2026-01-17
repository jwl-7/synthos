"""PDF Pre-Processor

This module pre-processes PDF books -> JSON embeddings for RAG db.
"""

# pylint: disable=multiple-statements

import json
import os
import re
import tkinter
from tkinter import filedialog
from typing import cast

import pymupdf
import pymupdf4llm
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from colors import Color


MODEL_NAME = 'all-mpnet-base-v2'


def select_pdf() -> str|None:
    """Prompt user to select PDF for processing."""
    input(f'Press {Color.ENTER} to select a {Color.PDF} for processing...')

    root = tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_selection = filedialog.askopenfilename(
        title='Select PDF',
        filetypes=[('PDF files', '*.pdf')],
        initialdir=os.getcwd()
    )
    root.destroy()

    if not file_selection:
        print(f'{Color.ERROR} No {Color.PDF} selected.')

    return file_selection

def select_json() -> str|None:
    """Prompt user to select JSON export destination."""
    input(f'Press {Color.ENTER} to select {Color.JSON} export...')

    root = tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_selection = filedialog.asksaveasfilename(
        title='Save Knowledge Base As',
        filetypes=[('JSON files', '*.json')],
        defaultextension='.json',
        initialfile='pdf_kb.json'
    )
    root.destroy()

    if not file_selection:
        print(f'{Color.ERROR} No {Color.JSON} selected.')

    return file_selection

def sanitize_text(text: str) -> str:
    """Sanitizes raw text extracted from PDF."""

    # filter OCR markers and figure captions
    artifacts_pattern = r'(-+\s*End of picture text\s*-+)|(Figure\s+\d+\.?)'
    text = re.sub(artifacts_pattern, '', text, flags=re.IGNORECASE)

    # remove tables and ASCII
    table_noise = r'([|+\-]{3,})|(\|(\s+\|)+)'
    text = re.sub(table_noise, ' ', text)

    # remove table of content lines
    text = re.sub(r'\.{3,}', ' ', text)

    # de-hyphenate words split across lines
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)

    # flatten whitespace
    text = re.sub(r'\s+', ' ', text)

    # remove common PDF ligatures
    ligatures = {'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
    for lig, rep in ligatures.items():
        text = text.replace(lig, rep)

    # text is non-alphanumeric noise
    if not re.search(r'[a-zA-Z0-9]', text): text = ''

    # clean whitespace
    text = text.strip()

    if not text: print(f'{Color.ERROR} No valid content found.')
    return text

def sentence_chunks(text: str) -> list[str]:
    """Split text up into sentence chunks by punctuation."""
    raw_chunks = re.split(r'(?<=[.!?]) +', text)
    chunks = [char.strip() for char in raw_chunks if len(char.strip()) > 30]
    print(f'{Color.INFO} Filtered out {Color.CYAN}{len(raw_chunks) - len(chunks)}{Color.RESET} noise chunks.')

    if not chunks: print(f'{Color.ERROR} No valid content found.')
    return chunks

def vector_embeddings(chunks: list[str], model: SentenceTransformer) -> list[list[float]]:
    """Generates normalized vector embeddings from sentence chunks."""
    print(f'{Color.INFO} Found {Color.CYAN}{len(chunks)}{Color.RESET} chunks. Starting embedding...')
    return [
        model.encode(sentences=chunk, normalize_embeddings=True).tolist()
        for chunk in tqdm(chunks, desc='Encoding', unit='chunk', bar_format='{l_bar}{bar:20}{r_bar}')
    ]

def build_kb(pdf_path: str, json_path: str, model: SentenceTransformer):
    """Converts PDF -> JSON-serialized vector database."""
    knowledge_base = []
    filename = os.path.basename(pdf_path)
    print(f'{Color.INFO} Reading {Color.CYAN}{filename}{Color.RESET}...')

    # extract text from pdf file
    raw_pdf = pymupdf.open(pdf_path)
    raw_txt = pymupdf4llm.to_text(raw_pdf)

    # sanitize content
    txt = sanitize_text(cast(str, raw_txt))
    if not txt: return

    # chunk text into sentences
    chunks = sentence_chunks(txt)
    if not chunks: return

    # generate normalized vector embeddings
    embeddings = vector_embeddings(chunks, model)

    # construct knowledge base with embeddings
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        knowledge_base.append({
            'id': f'{filename}_{i}',
            'text': chunk,
            'vector': vector
        })

    # export knowledge base as json
    with open(file=json_path, mode='w', encoding='utf-8') as f:
        json.dump(knowledge_base, f)

    # knowledge base constructed
    output_filename = os.path.basename(json_path)
    print(
        f'\n{Color.SUCCESS} Created {Color.CYAN}{output_filename}{Color.RESET} '
        f'from {Color.CYAN}{filename}{Color.RESET}'
    )

def load_model(model_name: str) -> SentenceTransformer|None:
    """Load AI model."""
    print(f'{Color.INFO} Loading AI model {Color.CYAN}{model_name}{Color.RESET}...')

    try:
        model = SentenceTransformer('flooba')
    except Exception as _: # pylint: disable=broad-exception-caught
        print(f'{Color.ERROR} Failed to load model {Color.CYAN}{model_name}{Color.RESET}...')
        model = None

    return model


def main():
    """Does stuff."""
    print(f'{Color.GRAY}.:.:.: {Color.YELLOW}PDF PreProcessor {Color.GRAY}:.:.:.{Color.RESET}')
    pdf_file = select_pdf()
    json_file = select_json() if pdf_file else None
    model = load_model(MODEL_NAME) if json_file else None
    if pdf_file and json_file and model: build_kb(pdf_file, json_file, model)
    input(f'\nPress {Color.ENTER} to exit...')

if __name__ == '__main__': main()
