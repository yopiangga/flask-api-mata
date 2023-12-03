import json
import config.app as config
import method.cosinus_similarity as cosinus_similarity
from sklearn.feature_extraction.text import CountVectorizer

dir_data = config.path + "dataset/data-d4-l1-v4.csv"

with open(dir_data, 'r') as file:
    data = json.load(file)
data = data['data']

def text_to_destination(text):
    ids = []
    titles = []
    descriptions = []

    for i, d in enumerate(data):
        ids.append(d['id'].lower())
        titles.append(d['title'].lower())
        descriptions.append(d['deskripsi'].lower())

    ids.append(text.lower())
    titles.append(text.lower())
    descriptions.append(text.lower())

    vectorizer = CountVectorizer()
    # vectorizer = ""
    id_vectorized_docs = vectorizer.fit_transform(ids).toarray()
    title_vectorized_docs = vectorizer.fit_transform(titles).toarray()
    description_vectorized_docs = vectorizer.fit_transform(descriptions).toarray()

    sim_ids = []
    sim_titles = []
    sim_descriptions = []

    for i, id in enumerate(ids):
        temp = cosinus_similarity.cosine_similarity(id_vectorized_docs[len(ids)-1], id_vectorized_docs[i])
        sim_ids.append(temp)

        temp = cosinus_similarity.cosine_similarity(title_vectorized_docs[len(titles)-1], title_vectorized_docs[i])
        sim_titles.append(temp)

        temp = cosinus_similarity.cosine_similarity(description_vectorized_docs[len(descriptions)-1], description_vectorized_docs[i])
        sim_descriptions.append(temp)
    
    sorted_list_id = sorted(sim_ids, reverse=True)
    second_max_value_id = sorted_list_id[1]
    second_max_index_id = sim_ids.index(second_max_value_id)

    sorted_list_title = sorted(sim_titles, reverse=True)
    second_max_value_title = sorted_list_title[1]
    second_max_index_title = sim_titles.index(second_max_value_title)

    sorted_list_description = sorted(sim_descriptions, reverse=True)
    second_max_value_description = sorted_list_description[1]
    second_max_index_description = sim_descriptions.index(second_max_value_description)

    threshold = 0.3
    true_index = 0

    if(second_max_value_id > threshold):
        true_index = second_max_index_id
    elif(second_max_value_title > threshold):
        true_index = second_max_index_title
    else:
        true_index = second_max_index_description

    return data[true_index]
