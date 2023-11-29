import information_extract
from tqdm import tqdm
import os
from matplotlib import pyplot as plt
from matplotlib_venn import venn3
import json

def draw_venn(TAM,SAM,SOM,filename):

    set1={1,2,3,}
    set2={2,3}
    set3={2}

    # plot Venn graph
    venn_diagram = venn3(subsets=[set1, set2, set3], set_labels=('TAM', 'SAM', 'SOM'))

    # Adjust VENN title position
    if '€' not in TAM:
        venn_diagram.get_label_by_id('100').set_text(f'{TAM} €')
    else:
        venn_diagram.get_label_by_id('100').set_text(f'{TAM}')

    venn_diagram.get_label_by_id('100').set_x(-0.6)
    venn_diagram.get_label_by_id('100').set_y(0)
    venn_diagram.get_label_by_id('A').set_x(-0.5)
    venn_diagram.get_label_by_id('A').set_y(0.05)
    if '€' not in SAM:
        venn_diagram.get_label_by_id('110').set_text(f'{SAM} €')
    else:
        venn_diagram.get_label_by_id('110').set_text(f'{SAM}')
    venn_diagram.get_label_by_id('110').set_x(-0.25)
    venn_diagram.get_label_by_id('110').set_y(0)
    venn_diagram.get_label_by_id('B').set_x(-0.32)
    venn_diagram.get_label_by_id('B').set_y(0.05)
    if '€' not in SAM:
        venn_diagram.get_label_by_id('111').set_text(f'{SOM} €')
    else:
        venn_diagram.get_label_by_id('111').set_text(f'{SOM}')
    venn_diagram.get_label_by_id('111').set_x(0.15)
    venn_diagram.get_label_by_id('111').set_y(0)
    venn_diagram.get_label_by_id('C').set_x(0.15)
    venn_diagram.get_label_by_id('C').set_y(0.1)


    plt.savefig(f'.\\venn_plot\\{filename}.png')
    plt.close()  

def load_json(filepath):
    with open(filepath,'r',encoding='utf-8') as f:
        data=json.load(f)
    return data

def main():

    # pdf_dir = str(input("please provide the pdf folder path: "))
    json_dir='extracted_information'
         
    # pdf_file= [i for i in os.listdir(pdf_dir) if i.endswith('.pdf')]

    # print("Extracting Information....")
    # for i in tqdm(pdf_file):
    #     pdf_path=os.path.join(pdf_dir,i)
    #     information_extract.information_extractor(pdf_path)
    # print("Extration Finished")
    # print("Plotting Information....")
    json_file= [i for i in os.listdir(json_dir) if i.endswith('.json')]

    for i in tqdm(json_file):
        print(i)
        filename=i.split('.')[0]
        json_path=os.path.join(json_dir,i)
        data=load_json(json_path)

        TAM=data['TAM']
        SAM=data['SAM']
        SOM=data['SOM']

        if TAM=='Unknown' or SOM=='Unknown'or SAM=='Unknown' or TAM=='Unbekannt' or SAM=='Unbekannt' or SOM=='Unbekannt':
            print("No information retrieved")
            continue

        draw_venn(TAM=TAM,SAM=SAM,SOM=SOM,filename=filename)


if __name__ =="__main__":
    main()