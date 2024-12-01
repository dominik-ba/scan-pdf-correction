import os
import sys
from PyPDF2 import PdfReader, PdfWriter

def recursive_process(writer, pages, level=0):
    indent = "  " * level
    print(f"{indent}Processing level {level}, number of pages: {len(pages)}")

    if len(pages) < 2:
        print(f"{indent}Stop recursion with last move.")
        writer.add_page(pages[-1])
        return
    if len(pages) < 3:
        print(f"{indent}Stop recursion.")
        return
    elif len(pages) < 4:
        print(f"{indent}Stop recursion with last move.")
        writer.add_page(pages[-1])
        return
    else:
        print(f"{indent}Moving last page to first position and deleting first and second last pages.")
        # Move the last page to the first position
        writer.add_page(pages[-1])
        writer.add_page(pages[1])

        # Recursively process the subset of pages
        recursive_process(writer, pages[2:-2], level + 1)

def process_pdf(file_path, processed_dir):
    print(f"Processing file: {file_path}")
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        num_pages = len(reader.pages)
        print(f"Number of pages in the PDF: {num_pages}")

        if num_pages < 2:
            print(f"Not enough pages to process in {file_path}")
            return

        writer = PdfWriter()
        pages = reader.pages

        # Initial processing
        recursive_process(writer, pages)

        # Save the modified PDF
        temp_file_path = file_path + ".tmp"
        with open(temp_file_path, "wb") as f_out:
            writer.write(f_out)

        # Replace the original file with the modified file
        os.replace(temp_file_path, file_path)
        print(f"Processed {file_path}")

        # Move the processed file to the processed directory
        if processed_dir:
            os.makedirs(processed_dir, exist_ok=True)
            new_file_path = os.path.join(processed_dir, os.path.basename(file_path))
            os.replace(file_path, new_file_path)
            print(f"Moved {file_path} to {new_file_path}")

def process_directory(directory, processed_dir):
    print(f"Processing directory: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                process_pdf(file_path, processed_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python correct.py <path_to_pdf_or_directory> [--move]")
        sys.exit(1)

    path = sys.argv[1]
    move_files = "--move" in sys.argv

    if os.path.isfile(path) and path.lower().endswith(".pdf"):
        processed_dir = os.path.join(os.path.dirname(os.path.dirname(path)), "processed") if move_files else None
        process_pdf(path, processed_dir)
    elif os.path.isdir(path):
        processed_dir = os.path.join(os.path.dirname(path), "processed") if move_files else None
        process_directory(path, processed_dir)
    else:
        print("Invalid path. Please provide a valid PDF file or directory.")
        sys.exit(1)
