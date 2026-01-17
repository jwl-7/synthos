"""Merge JSON KB files

This utility module helps merge
multiple knowledge bases (JSON) -> mega knowledge base (JSON).

Input files must be Output from the PDF Pre-Processor.
"""

# pylint: disable=multiple-statements

import json
import os
import tkinter
from tkinter import filedialog
from typing import cast

from colors import Color


def select_json_input() -> tuple[str]|None:
    """Prompt user to select JSON files for merging KB."""
    input(f'Press {Color.ENTER} to select {Color.JSON} files for merging...')

    root = tkinter.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_selection = filedialog.askopenfilenames(
        title='Select JSON Knowledge Bases',
        defaultextension='.json',
        filetypes=[('JSON files', '*.json')]
    )
    root.destroy()

    if not file_selection:
        print(f'{Color.ERROR} No {Color.JSON} selected.')

    return cast(tuple[str], file_selection)

def select_json_output() -> str|None:
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

def merge_json_kb(json_input_paths: tuple[str], json_output_path: str):
    """Merges multiple JSON knowledge bases."""
    combo_kb = []

    for path in json_input_paths:
        fname = os.path.basename(path)
        print(f'Merging {Color.CYAN}{fname}{Color.RESET}...')
        with open(file=path, mode='r', encoding='utf-8') as f:
            data = json.load(f)
        combo_kb.extend(data)

    with open(file=json_output_path, mode='w', encoding='utf-8') as f:
        json.dump(combo_kb, f)

    # knowledge bases merged
    output_filename = os.path.basename(json_output_path)
    print(
        f'\n{Color.SUCCESS} Combined {Color.CYAN}{len(json_input_paths)}{Color.RESET} files '
        f'-> {Color.CYAN}{output_filename}{Color.RESET}'
    )
    print(f'{Color.INFO} Total entries: {len(combo_kb)}')

def main():
    """Does stuff."""
    print(f'{Color.GRAY}.:.:.: {Color.YELLOW}JSON Knowledge Base File Merger {Color.GRAY}:.:.:.{Color.RESET}')
    json_input_files = select_json_input()
    json_output_file = select_json_output() if json_input_files else None
    if json_input_files and json_output_file: merge_json_kb(json_input_files, json_output_file)
    input(f'\nPress {Color.ENTER} to exit...')

if __name__ == '__main__': main()
