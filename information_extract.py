import pitchdecks
from pdf2image import convert_from_path
import os
import json
from postprocess_pitchdeck import postprocess
assess_quality = False

def information_extractor(pdf_path):

    # Check if the necessary folders exist
    folder_names = ["extracted_information","pdf_pages"]
    for folder_name in folder_names:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f'Folder "{folder_name}" created successfully.')

    # get pdf file

    # pdf_path ='./dataset/'
    # pdf_path = str(input("please provide the pdf file path: "))
    print(pdf_path)
    if pdf_path[-4:] != '.pdf':
        pdf_path += '.pdf'
    company_name = pdf_path.split('/')[-1].split('.pdf')[0]
    if '\\' in pdf_path:
        company_name = pdf_path.split('\\')[-1].split('.pdf')[0]
    print(company_name)

    # create images from pdf pages
    images = convert_from_path(pdf_path)
    n_images = len(images)
    print("read images...")
    pitchdecks.pdf2im(images, n_images)

    # extract and save text from pdf images
    print("extract text...")
    rel_pdf_path = 'pdf_pages/'
    pitchdeck = pitchdecks.read_pdf_img(rel_pdf_path)
    
    # delete pdf images
    delete_folder_path = "pdf_pages"
    for file_name in os.listdir(delete_folder_path):
        file_path = os.path.join(delete_folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    os.rmdir(delete_folder_path)

    output_dict,lang = pitchdecks.extract_information(pitchdeck,company_name)


    try:
        data_dict = json.loads(output_dict)
        #print(data_dict)
        
    except Exception as e:  
        json_e = e
        print("Error:",e)
        print("No data found")
        print('Trying to complete dictionary...')
        try:
            output_dict = pitchdecks.complete_dictionary(output_dict)
            data_dict = json.loads(output_dict)
            print('...successfuly!')
        except:
            print('Skip dictionary due to incompleteness.')
            

    if assess_quality:
        from quality_assessment import quality_assessment
        qual_score = quality_assessment(pitchdeck,data_dict)
        print("pitchdeck quality score:", qual_score)
        data_dict["quality_score"] = str(qual_score)
    data_dict['lang'] = lang
    with open(os.path.join("extracted_information",str(company_name)+'_pitch_data.json'), 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)

    postprocess(pd_path = r"C:\Users\jack\Desktop\mywork\package2\extracted_information/")
