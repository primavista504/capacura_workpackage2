import json
import os
from deep_translator import GoogleTranslator

def postprocess(pd_path):
    # add also, if duplicate pitchdeck, find all none entries and fill them with both pitchdecks 
    # if they overlap, choose one somehow
    none_list = ['Unknown','unknown', '', [], 'nan', 'Not specified','Unbekannt','unbekannt', 'nan', 'nicht angegeben']


    for pd_file in os.listdir(pd_path):
        with open(pd_path+pd_file, 'r', encoding='utf-8') as fi:
            pdeck = json.load(fi)
            city = pdeck.get('company_city')
            country = pdeck.get('company_country')


            if city not in none_list:
                city = GoogleTranslator(source='auto', target='de').translate(city)
                pdeck['company_city'] = city

            if country not in none_list:
                country = GoogleTranslator(source='auto', target='de').translate(country)
                pdeck['company_country'] = country
            

            # for shareholder in pdeck.get('shareholders'):
            #     if (shareholder in pdeck.get('employees',[]) or shareholder in pdeck.get('founders',[])) and shareholder not in none_list:
            #         print('remove:', shareholder)
            #         pdeck['shareholders'].remove(shareholder)
            #     if len(shareholder.split()) < 2:
            #         pdeck['shareholders'].remove(shareholder)

            # for employee in pdeck.get('employees'):
            #     if len(employee.split()) < 2:
            #         pdeck['employees'].remove(employee)

            # for founder in pdeck.get('founders'):
            #     if len(founder.split()) < 2:
            #         pdeck['founders'].remove(founder)
            # if pdeck.get('SDG') not in none_list:
            #     pdeck['SDG'] = [sdg.lower() for sdg in pdeck.get('SDG')]

            

            with open(pd_path+pd_file, 'w', encoding='utf-8') as f:
                json.dump(pdeck, f, ensure_ascii=False, indent=4)
            
# duplicates maybe the one with most values keep? Or add where its empty especially list can be added to
# try: use shortdescription make edge between each company with weighting of similarity of shortdescription
# tam som sam maybe add with weight of value on edge and them as node.

# powerpoint
if __name__ == "__main__":
    postprocess(r"C:\Users\jack\Desktop\mywork\package2\extracted_information/")


