"""
This PDFTools Script has various PDF functions that one may require.
Example Usage: python pdftools.py <function_name> <folder_directory>

Raises:
    SystemExit: when folder doesn't exist
"""

import argparse
import os
from pathlib import Path

import PyPDF2
from docx import Document
from pypdf import PdfMerger
import fitz


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


def pdftodocx(pdftoconvert, savelocation):
    """
    Converts PDF into .docx document

    Args:
        pdftoconvert (PDF): Input PDF awaiting to be converted
        savelocation (.docx): Output .docx converted from PDF
    """

    pdf_file = open(pdftoconvert, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    docx_document = Document()

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()

        # Add the extracted text to the Word document
        docx_document.add_paragraph(text)

    docx_document.save(savelocation)
    pdf_file.close()

    print("PDF Converted! Please check your .docx")


def rotatepdf(input_path, output_path, degrees):
    """
    Rotates PDF based on given degree

    Args:
        input_path (PDF): original PDF
        output_path (PDF): rotated PDF
        degrees (int): amount of degree you wish to rotate your pdf to
    """
    with open(input_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page.rotate(degrees)
            pdf_writer.add_page(page)

        with open(output_path, "wb") as output_file:
            pdf_writer.write(output_file)

        print("PDF rotation completed!")


def pagereplace(input_pdf_path, replacement_pdf_path, output_pdf_path, page_number):
    """
    Page replace for PDF documents based on
    specified replacement PDF into original PDF

    Args:
        input_pdf_path (PDF): Original PDF
        replacement_pdf_path (PDF): PDF containing the page to be replaced
        output_pdf_path (PDF): save location for final PDF
        page_number (int): page number to be replaced
    """
    input_pdf = fitz.open(input_pdf_path)
    replacement_pdf = fitz.open(replacement_pdf_path)

    if int(page_number) < 1 or int(page_number) > len(input_pdf):
        print("Invalid page number.")
        input_pdf.close()
        replacement_pdf.close()
        return
    # Copy all pages from the original PDF to a new PDF, except the page to be replaced
    output_pdf = fitz.open()
    for i in range(len(input_pdf)):
        if i == int(page_number) - 1:
            output_pdf.insert_pdf(
                replacement_pdf, from_page=0, to_page=0, start_at=int(page_number) - 1
            )
        else:
            output_pdf.insert_pdf(input_pdf, from_page=i, to_page=i)

    # Save the modified PDF
    output_pdf.save(output_pdf_path)
    output_pdf.close()

    input_pdf.close()
    replacement_pdf.close()


# Compile all the functions for PDF Tools
func_dict = {
    "combinepdf": combinepdf,
    "pdftodocx": pdftodocx,
    "rotatepdf": rotatepdf,
    "pagereplace": pagereplace,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--functions",
        help="select the PDF Tools function you want to use",
        required=True,
        dest="functions",
    )
    parser.add_argument(
        "-fp",
        "--folderpath",
        help="Input the input folder path for PDF combine",
        required=False,
        dest="folderpath",
    )
    parser.add_argument(
        "-ifp",
        "--inputfilepath",
        help="filepath for PDF to be converted",
        required=False,
        dest="inputfilepath",
    )
    parser.add_argument(
        "-sp",
        "--savepath",
        help="Save Folder Path for PDF Tools functions",
        required=False,
        dest="savepath",
    )
    parser.add_argument(
        "-d",
        "--degrees",
        help="Rotational Degree for PDF Rotate function",
        required=False,
        dest="degrees",
    )
    parser.add_argument(
        "-r",
        "--replacepdf",
        help="PDF to declare for replacement",
        required=False,
        dest="replacepdf",
    )
    parser.add_argument(
        "-p",
        "--pages",
        help="page number to declare for replacement",
        required=False,
        dest="pagereplace",
    )

    args = parser.parse_args()
    chosen_function = args.functions

    if func_dict[args.functions] == combinepdf:
        target_dir = Path(args.folderpath)
        if not target_dir.exists():
            print("The target directory doesn't exist")
            raise SystemExit(1)
        func_dict[args.functions](target_dir)
    elif func_dict[args.functions] == pdftodocx:
        inputfilepath = Path(args.inputfilepath)
        filename = os.path.splitext(args.inputfilepath.split("\\")[-1])[0]
        savepath = Path(args.savepath + f"/{filename}.docx")
        if not inputfilepath.exists():
            print("The target directory doesn't exist")
            raise SystemExit(1)
        func_dict[args.functions](inputfilepath, savepath)
    elif func_dict[args.functions] == rotatepdf:
        inputfilepath = Path(args.inputfilepath)
        filename = os.path.splitext(args.inputfilepath.split("\\")[-1])[0]
        savepath = Path(args.savepath + f"/{filename}.pdf")
        degrees = args.degrees
        if not inputfilepath.exists():
            print("The target directory doesn't exist")
            raise SystemExit(1)
        func_dict[args.functions](inputfilepath, savepath, int(degrees))
    elif func_dict[args.functions] == pagereplace:
        inputfilepath = Path(args.inputfilepath)
        filename = os.path.splitext(args.inputfilepath.split("\\")[-1])[0]
        savepath = Path(args.savepath + f"/{filename}_new.pdf")
        replacepdf = Path(args.replacepdf)
        replacepages = args.pagereplace
        func_dict[args.functions](inputfilepath, replacepdf, savepath, replacepages)
