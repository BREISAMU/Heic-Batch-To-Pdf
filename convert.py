from PIL import Image
import pillow_heif
from pypdf import PdfMerger
from pathlib import Path
import shutil

folder_path = Path('/path/to/your/folder')

def convert_folder(folder):
    # Make garbage for intermediate pdfs
    garbage_path = Path('./garbage')
    garbage_path.mkdir(parents=True, exist_ok=True)

    # Convert files to pdf, and queue them to be combined
    def convert(path):
        find_path = "./" + str(folder) + "/" + path
        heif_file = pillow_heif.read_heif(find_path)
        image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw",)
        place_path = "./garbage/" + path[:len(path) - 5] + ".pdf"
        image.save(place_path, format("pdf"))
        return place_path

    pdfs = []
    for file_path in folder.iterdir():
        if file_path.is_file():
            pdfs += [convert(file_path.name)]

    # Merge intermediate pdfs
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write("result.pdf")
    merger.close()
    
    # Delete all intermediate pdfs
    if garbage_path.exists() and garbage_path.is_dir():
        shutil.rmtree("garbage")
        print(f"Deleted garbage directory and its contents")
    else:
        print(f"ERROR: garbage does not exist")
    

convert_folder(Path("./heics"))