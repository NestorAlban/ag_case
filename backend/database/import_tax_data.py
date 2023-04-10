import fitz, sys
import os
import numpy as np
import cv2
from PIL import Image as im_pil

GENERAL_ROOT = './backend/database/files_root/'

class FileData:
    page1_doc = None
    page3_doc = None
    clean_doc1 = fitz.open()
    clean_doc2 = fitz.open()

    def page1_iter(spages, clean_doc):
        for spage in spages:
            r = spage.rect  # input page rectangle
            d = fitz.Rect(spage.cropbox_position,  # CropBox displacement if not
                spage.cropbox_position)  # starting at (0, 0)
            #--------------------------------------------------------------------------
            # example: cut input page into 2 x 2 parts
            #--------------------------------------------------------------------------
            r1 = r - (0, 0, 0, (r.height)*7/8) # top left rect
            r2 = r1 + ((r1.width)*3/20, (r1.height)*3/4, 0, 0) - (0, 0, (r1.width)*3/40, (r1.height)*1/8)  # top right rect
            r3 = r + ((r.width)*8/10, (r.height)*3/8, 0, 0) - (0, 0, 0, (r.height)*1/4) # bottom left rect
            r4 = r3 + ((r3.width)*1/8, (r3.height)*1/4, 0, 0) - (0, 0, (r3.width)*1/8, (r3.height)*5/8)
            rect_list = [r2, r4]  # put them in a list
            for rx in rect_list:  # run thru rect list
                rx += d  # add the CropBox displacement
                page = clean_doc.new_page(-1,  # new output page with rx dimensions
                                width = rx.width,
                                height = rx.height)
                page.show_pdf_page(
                        page.rect,  # fill all new page with the image
                        spages,  # input document
                        spage.number,  # input page number
                        clip = rx,  # which part to use of input page
                    )
        return clean_doc
    def page3_iter(spages, clean_doc):
        for spage in spages:
            r = spage.rect  # input page rectangle
            d = fitz.Rect(spage.cropbox_position,  
                spage.cropbox_position)  
            r1 = r + ((r.width)*1/4, (r.height)*3/4, 0, 0) - (0, 0, 0, (r.height)*2/20) 
            r2 = r1 + ((r1.width)*8/10, (r1.height)*14/16, 0, 0) - (0, 0, (r1.width)*3/40, 0)  
            rect_list = [r2]  
            for rx in rect_list:  
                rx += d  
                page = clean_doc.new_page(-1,  
                                width = rx.width,
                                height = rx.height)
                page.show_pdf_page(
                        page.rect,  
                        spages,  
                        spage.number,  
                        clip = rx,  
                    )
        return clean_doc
    def save_doc(doc, src):
        doc.save(GENERAL_ROOT+"poster1-" + src,
                garbage=3,  # eliminate duplicate objects
                deflate=True,  # compress stuff where possible
        )

    def create_image(pdf_page, image_name):
        zoom = 4
        mat = fitz.Matrix(zoom, zoom)
        page1 = pdf_page
        pix = page1.get_pixmap(matrix=mat)
        pix.save(image_name)

    def filing_image_crop(page):
        page1 = page
        page1_img_name = GENERAL_ROOT+'poster1-page1-1.png'
        FileData.create_image(page1, page1_img_name)
        
        page1_ii = cv2.imread(page1_img_name)
        gray = cv2.cvtColor(page1_ii, cv2.COLOR_BGR2GRAY)
        rows,cols,_ = page1_ii.shape

        k = []
        for c in range(cols):
            sum_val = 0
            for r in range(rows):
                sum_val =sum_val+ (gray[r,c])/255
            k.append(sum_val)
        new_values_list = k.copy()
        np_array = np.array(new_values_list)
        min_val = min(k)
        min_val_ind = k.index(min_val)
        item_index = np.where(np_array == min_val)[0]
        
        list_gray_imgs = []
        for i in range(len(item_index)):
            ind = item_index[i]
            if i <= 8:
                squares = item_index[i+1]
            else:
                squares = cols
            gray_img_sec = gray[0:rows,ind:squares]
            list_gray_imgs.append(gray_img_sec)
        rectangles_pixels_sum = []
        for i in range(len(list_gray_imgs)):
            if i%2 == 0:
                grb_img = list_gray_imgs[i]
                rows2,cols2 = grb_img.shape
                pixels_sum = 0
                for r2 in range(rows2):
                    for c2 in range(cols2):
                        pixels_sum = pixels_sum +(grb_img[r2, c2])/255
                rectangles_pixels_sum.append(pixels_sum)
        min_rect_val = min(rectangles_pixels_sum)
        min_rect_val_ind = rectangles_pixels_sum.index(min_rect_val)
        text_img = list_gray_imgs[min_rect_val_ind+1]
        new_imag_name = 'poster1-page1-newtext.png'
        text_img_name = GENERAL_ROOT+new_imag_name
        img_data = im_pil.fromarray(text_img)
        img_data.save(text_img_name)

        page1_1_img = im_pil.open(text_img_name)
        im_1 = page1_1_img.convert('RGB')
        new_pdf_name = 'poster1-page1-newtext.pdf'
        text_pdf_name = GENERAL_ROOT+new_pdf_name
        im_1.save(text_pdf_name)
        return [(min_rect_val_ind+1), new_imag_name, new_pdf_name]

    def filing_status_mapping(ind):
        fi_status = None
        if ind == 1:
            fi_status = 'Single'
        elif ind == 3:
            fi_status = 'Married filing jointly'
        elif ind == 5:
            fi_status = 'Married filing separately (MFS)'
        elif ind == 7:
            fi_status = 'Head of household (HOH)'
        elif ind == 9:
            fi_status = 'Qualifying widow(er) (QW)'
        return fi_status


    def start_file_reader(file_path, filename):
        files_names = []
        doc1 = fitz.open(file_path+filename)
        doc2 = fitz.open(file_path+filename)
        files_names.append(filename)
        doc1.select([0])
        doc1.save(file_path+'page1.pdf')
        doc2.select([2])
        doc2.save(file_path+'page3.pdf')
        page1_doc = fitz.open(file_path+'page1.pdf')
        page3_doc = fitz.open(file_path+'page3.pdf')
        clean_doc1 = fitz.open()
        clean_doc2 = fitz.open()
        files_names.append('page1.pdf')
        files_names.append('page3.pdf')
        clean_doc1_1 = FileData.page1_iter(page1_doc, clean_doc1)
        clean_doc2_1 = FileData.page3_iter(page3_doc, clean_doc2)
        FileData.save_doc(clean_doc1_1, 'page1.pdf')
        FileData.save_doc(clean_doc2_1, 'page3.pdf')

        response_doc1 = fitz.open(file_path+'poster1-page1.pdf')
        response_doc2 = fitz.open(file_path+'poster1-page3.pdf')
        files_names.append('poster1-page3.pdf')
        files_names.append('poster1-page1.pdf')
        files_names.append('poster1-page1-1.png')
        page1 = response_doc1.load_page(0)
        page2 = response_doc1.load_page(1)
        image_data = FileData.filing_image_crop(page1)
        text1_ind = image_data[0]
        files_names.append(image_data[1])
        files_names.append(image_data[2])
        def get_user_taxes_data_by_pdf(response_doc1, response_doc2):
            text1 = FileData.filing_status_mapping(text1_ind)
            text2 = int(response_doc2[0].get_text().rstrip().replace(',','').replace('.',''))

            text3 = int(response_doc1[1].get_text().rstrip().replace(',','').replace('.',''))
            print(text1,text2,text3)
            return {'text1':text1, 'text2':text2, 'text3':text3}
        
        values = get_user_taxes_data_by_pdf(response_doc1,response_doc2)
        doc1.close()
        doc2.close()
        page1_doc.close()
        page3_doc.close()
        response_doc1.close()
        response_doc2.close()
        for i in range(len(files_names)):

            file_path = GENERAL_ROOT+ files_names[i]
            if os.path.isfile(file_path):
                try:
                    # Eliminar el archivo
                    os.remove(file_path)
                    print(f"El archivo {file_path} ha sido eliminado exitosamente.")
                except Exception as e:
                    print(f"No se pudo eliminar el archivo {file_path}. Error: {str(e)}")
            else:
                print(f"El archivo {file_path} no existe.")
        return values