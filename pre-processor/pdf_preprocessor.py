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

import pymupdf.layout
import pymupdf
import pymupdf4llm
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from colors import Color


MODEL_NAME = 'all-mpnet-base-v2'
LITE_MODE = False


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

def select_json(pdf_path: str) -> str|None:
    """Prompt user to select JSON export destination."""
    input(f'Press {Color.ENTER} to select {Color.JSON} export...')
    pdf_filename = os.path.basename(pdf_path)
    pdf_name = os.path.splitext(pdf_filename)[0]
    pdf_dirname = os.path.dirname(pdf_path)

    root = tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_selection = filedialog.asksaveasfilename(
        title='Save Knowledge Base As',
        filetypes=[('JSON files', '*.json')],
        defaultextension='.json',
        initialfile=f'{pdf_name}.json',
        initialdir=pdf_dirname
    )
    root.destroy()

    if not file_selection:
        print(f'{Color.ERROR} No {Color.JSON} selected.')

    return file_selection

def sanitize_text(text: str) -> str:
    """Sanitizes raw text extracted from PDF."""

    # de-hyphenate words split across lines
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)

    # remove common PDF ligatures
    ligatures = {'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
    for lig, rep in ligatures.items():
        text = text.replace(lig, rep)

    # clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def sentence_chunks(text: str) -> list[str]:
    """Split text up into sentence chunks by punctuation."""
    raw_chunks = re.split(r'(?<=[.!?]) +', text)
    chunks = []

    for chunk in raw_chunks:
        chunk = chunk.strip()

        # too short
        if len(chunk) < 40:
            continue

        # not enough real words
        words = re.findall(r'\b[a-zA-Z]{2,}\b', chunk)
        if len(words) < 5:
            continue

        chunks.append(chunk)

    return chunks

def vector_embeddings(chunks: list[str], model: SentenceTransformer) -> list[list[float]]:
    """Generates normalized vector embeddings from sentence chunks."""
    print(f'{Color.INFO} Found {Color.CYAN}{len(chunks)}{Color.RESET} chunks. Starting embedding...')
    progress_bar_format = '{desc}: |{bar:40}| {n_fmt}/{total_fmt}'
    return [
        model.encode(sentences=chunk, normalize_embeddings=True).tolist()
        for chunk in tqdm(chunks, desc='Encoding chunks', unit='chunk', bar_format=progress_bar_format)
    ]

def build_kb(pdf_path: str, json_path: str, model: SentenceTransformer):
    """Converts PDF -> JSON-serialized vector database."""
    chunks = []
    knowledge_base = []
    filename = os.path.basename(pdf_path)
    print(f'{Color.INFO} Reading {Color.CYAN}{filename}{Color.RESET}...')

    # extract text from pdf file
    raw_pdf = pymupdf.open(pdf_path)
    raw_txt = cast(list[dict], pymupdf4llm.to_text(
        doc=raw_pdf,
        page_chunks=True,
        header=False,
        footer=False,
        ignore_code=True,
        ignore_graphics=True,
        ignore_images=True
    ))

    progress_bar_format = '{desc}: |{bar:40}| {n_fmt}/{total_fmt}'
    for page in tqdm(raw_txt, desc='Processing pages', unit='page', bar_format=progress_bar_format):
        page_txt = sanitize_text(page['text'])

        # empty page
        if not page_txt or not re.search(r'[a-zA-Z0-9]', page_txt):
            continue

        page_chunks = sentence_chunks(page_txt)
        chunks.extend(page_chunks)

    if not chunks:
        print(f'{Color.ERROR} No valid content found.')
        return

    # generate normalized vector embeddings
    embeddings = vector_embeddings(chunks, model)

    # construct knowledge base with embeddings
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        if LITE_MODE: vector = [round(float(v), 5) for v in vector]
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
        f'\n{Color.SUCCESS} Processed {Color.CYAN}{filename}{Color.RESET} '
        f'-> {Color.CYAN}{output_filename}{Color.RESET}'
    )

def load_model(model_name: str) -> SentenceTransformer|None:
    """Load AI model."""
    print(f'{Color.INFO} Loading AI model {Color.CYAN}{model_name}{Color.RESET}...')

    try:
        model = SentenceTransformer(MODEL_NAME)
    except Exception as _: # pylint: disable=broad-exception-caught
        print(f'{Color.ERROR} Failed to load model {Color.CYAN}{model_name}{Color.RESET}...')
        model = None

    return model


def main():
    """Does stuff."""
    print(f'{Color.GRAY}.:.:.: {Color.YELLOW}PDF PreProcessor {Color.GRAY}:.:.:.{Color.RESET}')
    pdf_file = select_pdf()
    json_file = select_json(pdf_file) if pdf_file else None
    model = load_model(MODEL_NAME) if json_file else None
    if pdf_file and json_file and model: build_kb(pdf_file, json_file, model)
    input(f'\nPress {Color.ENTER} to exit...')

if __name__ == '__main__': main()
