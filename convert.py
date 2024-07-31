from PIL import Image
import pillow_heif
from pypdf import PdfMerger
from pathlib import Path
import shutil
from download_files import get_images, get_download_path
import os

def convert_folder(folder, title):
    # Make garbage for intermediate pdfs
    garbage_path = Path('./garbage')
    garbage_path.mkdir(parents=True, exist_ok=True)

    # Convert files to pdf, and queue them to be combined
    def convert(path):
        find_path = path
        print(f"Converting {find_path}...")
        try:
            heif_file = pillow_heif.read_heif(find_path)
            image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw")
            place_path = garbage_path / (path.stem + ".pdf")
            image.save(place_path, format="PDF")
            return place_path
        except Exception as e:
            print(f"Failed to convert {find_path}: {e}")
            return None

    pdfs = [convert(file_path) for file_path in folder.iterdir() if file_path.is_file()]
    pdfs = [pdf for pdf in pdfs if pdf is not None]

    # Merge intermediate pdfs
    try:
        with PdfMerger() as merger:
            for pdf in pdfs:
                merger.append(str(pdf))
            to_downloads = os.path.join(get_download_path(), title + ".pdf")
            merger.write(to_downloads)
    except Exception as e:
        print(f"Failed to merge PDFs: {e}")

    # Delete all intermediate pdfs
    try:
        if garbage_path.exists() and garbage_path.is_dir():
            shutil.rmtree(garbage_path)
            print("Deleted garbage directory and its contents")
        else:
            print("ERROR: garbage does not exist")
    except Exception as e:
        print(f"Failed to delete garbage directory: {e}")

def heic_main():
    heic_path = Path('./heics')
    heic_path.mkdir(parents=True, exist_ok=True)
    get_images()
    convert_folder(Path("./heics"), "result_test")
    try:
        if heic_path.exists() and heic_path.is_dir():
            shutil.rmtree(heic_path)
            print("Deleted heic directory and its contents")
        else:
            print("ERROR: heic does not exist")
    except Exception as e:
        print(f"Failed to heic directory: {e}")