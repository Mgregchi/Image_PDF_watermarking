import PyPDF2 
import os
from PIL import Image
import time

path = (r"path to folder with watermark image and pdf to add watermark on")
os.chdir(path)
watermarkimg = ('watermark_image.png') # Image to use as watermark, should have white background
                                        # for cool sight and to blend well

pdfFile = open('name_of_PDF_file.pdf', 'rb') # PDF file name
pdfReader = PyPDF2.PdfFileReader(pdfFile)
pdfPage = pdfReader.getPage(0) # page num can be changed to suit need
                                   # getpage(0) 'zero' is the firstpage
# Prepare Image to PDF conversion
n, N, pdf_X, pdf_y = pdfReader.getPage(0).mediaBox

watermark = Image.open(watermarkimg)
# ths created image width can be adjusted, but the height should not be adjusted
newimg = Image.new('RGB', (pdf_X,60), (255,255,255)) # white background
x,y = newimg.size
watermark = watermark.resize((int(x/2), y)) # The watermark width should be determind by user
                    # X should be dertimined by user. but y remains the same
                    # zero (0) refers to left side of the page, half of PDF refers to center
                    # 'X' max subtracted with watermark 'X' plus 5, refers to right corner
wmarkWidth,wmarkHeight = watermark.size
# watermark location on page - Users choice
left    = (0,0)
center  = (int(x/2-wmarkWidth/2),0)
right   = (x-wmarkWidth-5,0)
newimg.paste(watermark, center) # Watermark image pasted with user's choice
newimg.save('created.pdf', resoultion=100.0) # name can be changed

time.sleep(2) # since the program is single thread,
#just to give it time to breath

# Open the newly created PDF file and proceed with merging
# This is in case the PDF file is corrupted
try:
    pdfWatermarkReader = PyPDF2.PdfFileReader(open('continuation.pdf','rb'))
except OSError as err:
    raise Exception(err) # can be removed to suit your need
pdfPage.mergePage(pdfWatermarkReader.getPage(0))
pdfWriter = PyPDF2.PdfFileWriter()
pdfWriter.addPage(pdfPage)

# Scan through pages in PDF file and merge page
for pageNum in range(1, pdfReader.numPages):
    pageObj = pdfReader.getPage(pageNum)
    pageObj.mergePage(pdfWatermarkReader.getPage(0))
    pdfWriter.addPage(pageObj)

watermarkedPDF = open('watermarked.pdf', 'wb') # Create new PDF file 
pdfWriter.write(watermarkedPDF)
pdfFile.close()
watermarkedPDF.close()