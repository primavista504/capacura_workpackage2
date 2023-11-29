from transformers import pipeline
import tiktoken

def quality_assessment(pdf_text,json_dict):

    none_list = ['Unknown','unknown', '', [], 'nan', 'Not specified']
    max_tokens = 4097-300

    if not json_dict:
        return 0
    
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    encoded = encoding.encode(f"___________________\n{pdf_text}")
    num_tokens = len(encoded)

    cola_classifier = pipeline(model="yiiino/deberta-v3-large-cola")
    
    points = 20+len(json_dict.items())*10
    print("total_points:",20+len(json_dict.items())*10)
    start_points = points
    
    if num_tokens > max_tokens:
        overlapping_tokens = num_tokens-max_tokens
        reduce_factor = overlapping_tokens/4000
        if reduce_factor > 1:
            reduce_factor = 1
        points -= 20*reduce_factor

    
    for k,v in json_dict.items():

        
        if isinstance(v, str) and v in none_list:
            points -= 10

        if isinstance(v,list):
            try:
                if v[0] in none_list:
                    points -= 10
            except:
                points -= 10
    cola_score = cola_classifier(pdf_text[:max_tokens])
    cola_score_normalized = round(cola_score[0]['score']*100,2)
    points = (((points/(start_points/100))/4*3)+(cola_score_normalized/4))
    return round(points,1)

#quality_assessment(num_tokens,pitchdeck,data_dict)