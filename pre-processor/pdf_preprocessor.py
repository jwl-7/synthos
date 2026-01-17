'''PDF Pre-Processor

This module pre-processes PDF books -> JSON embeddings for RAG db.
'''

import json
import os
import re
import tkinter
from tkinter import filedialog
from enum import Enum

import pymupdf.layout
import pymupdf
import pymupdf4llm
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


MODEL_NAME = 'all-mpnet-base-v2'
OUTPUT_FILENAME = 'pdf_kb.json'

class Color(Enum):
    '''Color enums for f-strings.'''
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    INFO = f'{GRAY}[{BLUE}INFO{GRAY}]{RESET}'
    ERROR = f'{GRAY}[{RED}ERROR{GRAY}]{RESET}'
    SUCCESS = f'{GRAY}[{GREEN}SUCCESS{GRAY}]{RESET}'
    ENTER = f'{GRAY}[{YELLOW}ENTER{GRAY}]{RESET}'

    def __str__(self) -> str:
        return self.value


def sanitize_text(text: str) -> str:
    '''Sanitizes raw text extracted from PDF.'''

    # filter out OCR markers and figure captions
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

    return text.strip()


def build_kb(file_path: str, output_file: str, model: SentenceTransformer):
    '''Converts PDF into a JSON-serialized vector database.'''
    embeddings = []
    knowledge_base = []
    filename = os.path.basename(file_path)
    print(f'Reading {Color.CYAN}{filename}{Color.RESET}...')

    # extract text from pdf file
    raw_pdf = pymupdf.open(file_path)
    raw_txt = pymupdf4llm.to_text(raw_pdf)

    # sanitize extracted text
    txt = sanitize_text(raw_txt)

    # split text into sentences by punctuation
    raw_chunks = re.split(r'(?<=[.!?]) +', txt)
    chunks = [char.strip() for char in raw_chunks if len(char.strip()) > 30]
    print(f'{Color.INFO} Filtered out {Color.CYAN}{len(raw_chunks) - len(chunks)} {Color.RESET}noise chunks.')

    # failsafe | no data
    if not chunks:
        print(f'{Color.ERROR} No valid content found.')
        return

    # generate normalized vector embeddings
    print(f'Found {Color.CYAN}{len(chunks)} {Color.RESET}chunks. Starting embedding...')
    for chunk in tqdm(chunks, desc='Embedding', unit='chunk', bar_format='{l_bar}{bar:20}{r_bar}'):
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
    with open(file=output_file, mode='w', encoding='utf-8') as f:
        json.dump(knowledge_base, f)
    print(f'{Color.SUCCESS} Created {Color.CYAN}{output_file} {Color.RESET}from {Color.CYAN}{filename}{Color.RESET}')

if __name__ == '__main__':
    print(Color.ENTER)
    desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')

    # prompt user for file
    root = tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    print('Select PDF file...')
    selected_file = filedialog.askopenfilename(
        title='Select PDF',
        initialdir=desktop_dir,
        filetypes=[('PDF files', '*.pdf'), ('All files', '*.*')]
    )
    root.destroy()

    # build embeddings
    if selected_file:
        print(f'Loading AI model {Color.CYAN}{MODEL_NAME}{Color.RESET}...')
        shared_model = SentenceTransformer(MODEL_NAME)
        build_kb(selected_file, OUTPUT_FILENAME, shared_model)
        input(f'Press {Color.ENTER} to exit...')
    else:
        print(f'{Color.ERROR} File selection cancelled. Exiting...')
