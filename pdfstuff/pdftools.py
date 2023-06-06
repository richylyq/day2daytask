"""
This PDFTools Script has various PDF functions that one may require.
Example Usage: python pdftools.py <function_name> <folder_directory>

Raises:
    SystemExit: when folder doesn't exist
"""

from pypdf import PdfMerger
import argparse
from pathlib import Path
import os


def combinepdf(folderpath):
    """
    Combines PDF into a single PDF Output file

    Args:
        folderpath (path): Folder path for the PDFs you wish to combine
    """
    pdfs = [a for a in os.listdir(folderpath) if a.endswith(".pdf")]

    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(f"{folderpath}/{pdf}")

    merger.write(f"{folderpath}/output.pdf")
    merger.close()
    print("PDF Combined.. Please check.")


# Compile all the functions for PDF Tools
func_dict = {"combinepdf": combinepdf}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("functions")
    parser.add_argument("folderpath")
    args = parser.parse_args()

    chosen_function = args.functions
    target_dir = Path(args.folderpath)

    if not target_dir.exists():
        print("The target directory doesn't exist")
        raise SystemExit(1)

    func_dict[args.functions](target_dir)
