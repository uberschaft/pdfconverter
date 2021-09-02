from pdf2image import convert_from_path
from PIL import Image
from PyPDF4 import PdfFileWriter, PdfFileReader
from time import perf_counter
import os
import PyPDF2
import PyPDF4
import glob
import gc

t1_start = perf_counter()
try:
    os.makedirs(os.getcwd()+"/original-PDFs")
    print("Directory " , os.getcwd()+"/original-PDFs" ,  " Created ")
except FileExistsError:
    print("Directory " , os.getcwd()+"/original-PDFs" ,  " already exists")
os.popen('cp '+"*.pdf"+' '+os.getcwd()+'/original-PDFs')
pdf = []
for i in glob.glob("*.pdf"):
    pdf.append(i)
pdf_list = [None]*len(pdf)
for i in range(len(pdf)):
    base = os.path.basename(pdf[i])
    pdf_list[i] = (os.path.splitext(base)[0])
pdf_list.remove('watermark')




pdfcount = 0

while (pdfcount < len(pdf_list)):

    workdir = os.getcwd()+"/"

    print("**************PDF to Non-Selectable PDF Converter**************\n**************PDF to be processed: "+pdf_list[pdfcount]+"**************")

    input_pdf = pdf_list[pdfcount]
    dirName = workdir+input_pdf
    extensionName = ".pdf"
    pdfName = input_pdf + extensionName

    print("**************Original PDF has been copied**************\n**************watermark is being added**************")

    PyPDF4.PdfFileReader(pdfName)


    def put_watermark(input_pdf, output_pdf, watermark):

        watermark_instance = PdfFileReader(watermark)

        watermark_page = watermark_instance.getPage(0)

        pdf_reader = PdfFileReader(pdfName)

        pdf_writer = PdfFileWriter()

        for page in range(pdf_reader.getNumPages()):

            page = pdf_reader.getPage(page)

            pdf_writer.addPage(page)

        with open(output_pdf, 'wb') as out:

            pdf_writer.write(out)

    if __name__ == "__main__":
        put_watermark(
            input_pdf=pdfName,
            output_pdf=workdir+pdfName,
            watermark='watermark.pdf'
        )

    print("**************watermark has been added**************\n**************Images are being converted**************")

    try:
        os.makedirs(dirName)
        print("Directory " , dirName ,  " Created ")
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")

    images = convert_from_path(pdfName, dpi=600, output_folder=dirName, size = (1920,1080), thread_count = 4)


    print("**************JPGs are being created**************")
    image_count = len(images)

    for i in range(len(images)):

    	# Save pages as images in the pdf
    	images[i].save(workdir+input_pdf+"/"+input_pdf+ str(i) +'.jpg', 'JPEG')
    	print(str(i+1)+"/"+str(image_count)+" converted")

    print("**************JPGs have been created**************\n**************conversion is done**************\n**************Final PDF is being created**************")



    i=1
    image_list = []
    list = []


    for i in range(len(images)):
    	list.append(Image.open(workdir+input_pdf+"/"+input_pdf+ str(i) +".jpg"))

    im1 = Image.open(workdir+str(input_pdf)+"/"+input_pdf+ str(0) +".jpg")
    pdf1_filename = workdir+pdfName

    im1.save(pdf1_filename, "PDF" ,resolution=100.0, save_all=True, append_images=list)
    print("**************PDF has been created**************")

    for i in range(image_count):
        os.remove(dirName +"/"+input_pdf+ str(i) +".jpg")
        print(str(i+1)+"/"+str(image_count)+" deleted")

    files = glob.glob(dirName + '/'+'*ppm')
    for f in files:
        os.remove(f)

    try:
        os.rmdir(dirName)
        print("Images have been deleted!")
    except OSError:
        print("Directory " , dirName ,  " is not empty")

    print("PDF "+pdf_list[pdfcount]+" has been converted")
    gc.collect()
    pdfcount += 1
    if (pdfcount == len(pdf_list)):
        print("**************ALL PDFs have been converted**************")
        t1_stop = perf_counter()
        print("Done in:", t1_stop-t1_start, "seconds")
    else:
        pass
