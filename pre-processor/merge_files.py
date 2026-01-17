"""Merge Files

This utility module helps merge
multiple knowledge bases (JSON) -> mega knowledge base (JSON).

Input files must be Output from the PDF Pre-Processor.
"""
import json
import os
import tkinter
from tkinter import filedialog
from colors import Color


def merge_json_files():
    """Merges multiple JSON knowledge bases."""
    root = tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    print(f'{Color.INFO} Select JSON files...')
    file_paths = filedialog.askopenfilenames(
        title='Select JSON Knowledge Bases',
        filetypes=[('JSON files', '*.json')]
    )
    root.destroy()

    if not file_paths:
        print(f'{Color.ERROR} No files selected. Exiting.')
        return

    master_kb = []

    for path in file_paths:
        filename = os.path.basename(path)
        print(f'Merging: {Color.CYAN}{filename}{Color.RESET}...')

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except UnicodeDecodeError:
            with open(path, 'r', encoding='utf-16') as f:
                data = json.load(f)

        master_kb.extend(data)

    output_name = 'combo_kb.json'
    with open(output_name, 'w', encoding='utf-8') as f:
        json.dump(master_kb, f)

    print(f'\n{Color.SUCCESS} Combined {Color.CYAN}{len(file_paths)}{Color.RESET} files into {Color.CYAN}{output_name}{Color.RESET}')
    print(f'{Color.INFO} Total entries: {len(master_kb)}')

if __name__ == '__main__':
    print(Color.ENTER)
    merge_json_files()
    input(f'Press {Color.ENTER} to exit...')
