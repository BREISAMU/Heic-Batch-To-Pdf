# Heic-Batch-To-Pdf
Python application leveraging Google Drive API to convert a Drive folder of .HEIC images to one combined PDF. Useful for submitting series of IPhone images of paper homework to Gradescope / Canvas

## Important
As of now, folder id must be manually entered, working on searching by name / selection in GUI

## Run Locally
```bash
  git clone https://github.com/BREISAMU/Heic-Batch-To-Pdf.git

  cd Heic-Batch-To-Pdf

  pip install -r requirements.txt

  ** SPECIFY FOLDER OF INTEREST IN params.py **

  py process.py
