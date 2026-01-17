"""PDF Pre-Processor

This module pre-processes PDF books -> JSON embeddings for RAG db.
"""

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
    if not re.search(r'[a-zA-Z0-9]', text):
        return ''

    # clean whitespace
    return text.strip()

def build_kb(file_path: str, output_path: str, model: SentenceTransformer):
    """Converts PDF into a JSON-serialized vector database."""

    # setup
    embeddings = []
    knowledge_base = []
    filename = os.path.basename(file_path)
    print(f'{Color.INFO} Reading {Color.CYAN}{filename}{Color.RESET}...')

    # extract text from pdf file
    raw_pdf = pymupdf.open(file_path)
    raw_txt = pymupdf4llm.to_text(raw_pdf)

    # sanitize extracted text
    txt = sanitize_text(cast(str, raw_txt))

    # split text into sentences by punctuation
    raw_chunks = re.split(r'(?<=[.!?]) +', txt)
    chunks = [char.strip() for char in raw_chunks if len(char.strip()) > 30]
    print(f'{Color.INFO} Filtered out {Color.CYAN}{len(raw_chunks) - len(chunks)}{Color.RESET} noise chunks.')

    # no data
    if not chunks:
        print(f'{Color.ERROR} No valid content found.')
        return

    # generate normalized vector embeddings
    print(f'{Color.INFO} Found {Color.CYAN}{len(chunks)}{Color.RESET} chunks. Starting embedding...')
    for chunk in tqdm(chunks, desc='Encoding', unit='chunk', bar_format='{l_bar}{bar:20}{r_bar}'):
        vector = model.encode(sentences=chunk, normalize_embeddings=True).tolist()
        embeddings.append(vector)

    # construct knowledge base with embeddings
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        knowledge_base.append({
            'id': f'{filename}_{i}',
            'text': chunk,
            'vector': vector
        })

    # export knowledge base as json
    with open(file=output_path, mode='w', encoding='utf-8') as f:
        json.dump(knowledge_base, f)

    # knowledge base constructed
    output_filename = os.path.basename(output_path)
    print(
        f'\n{Color.SUCCESS} Created {Color.CYAN}{output_filename}{Color.RESET} '
        f'from {Color.CYAN}{filename}{Color.RESET}'
    )


if __name__ == '__main__':
    # user file selection | PDF INPUT
    input(f'Press {Color.ENTER} to select a PDF for processing...')
    root = tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    selected_file = filedialog.askopenfilename(
        title='Select PDF',
        filetypes=[('PDF files', '*.pdf')],
        initialdir=os.getcwd()
    )

    if not selected_file:
        # no file selected
        print(f'{Color.ERROR} Selection cancelled.')
        root.destroy()
    else:
        # user file selection | PDF OUTPUT
        print(f'{Color.INFO} Selected: {Color.CYAN}{os.path.basename(selected_file)}{Color.RESET}')
        output_save_path = filedialog.asksaveasfilename(
            title='Save Knowledge Base As',
            defaultextension='.json',
            filetypes=[('JSON files', '*.json')],
            initialfile='pdf_kb.json'
        )
        root.destroy()

        if not output_save_path:
            # no file selection
            print(f'{Color.ERROR} Save location required. Exiting.')
        else:
            # load AI model and build embeddings
            print(f'{Color.INFO} Loading AI model {Color.CYAN}{MODEL_NAME}{Color.RESET}...')
            shared_model = SentenceTransformer(MODEL_NAME)
            build_kb(selected_file, output_save_path, shared_model)

            # embeddings created
            print(f'{Color.SUCCESS} Processing Complete!')
            input(f'\nPress {Color.ENTER} to exit...')
