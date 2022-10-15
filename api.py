"""Test demonstration of using the plant classification API"""
import requests
import json
from pprint import pprint

API_KEY = "2b10uuyJqUMMO3Kxz3JmqHPGuu" 	# Set you API_KEY here

def convert_data_to_names(plant_results: list):
    names = []
    for i in range(len(plant_results)):
        names.append({})
        data = plant_results[i]
        names[i]['score'] = data['score']
        names[i]['scientific name'] = data['species']['scientificNameWithoutAuthor']
        names[i]['common names'] = data['species']['commonNames']
    return names


def prediction_using_file(paths):
    api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"

    # put image path here
    datas = []
    for i in range(len(paths)):
        datas.append(open(paths[i], 'rb'))


    # put organ of plant which is being in the picture
    data = {
            'organs': ['leaf'] * len(paths)
    }

    files = [
            ('images', (paths[i], datas[i])) for i in range(len(paths))
    ]

    req = requests.Request('POST', url=api_endpoint, files=files, data=data)
    prepared = req.prepare()

    s = requests.Session()
    response = s.send(prepared)
    if str(response.status_code)[0] == '2':
        json_result = json.loads(response.text)
        plant_results = sorted(json_result["results"], key=lambda x: x["score"], reverse=True)
        return convert_data_to_names(plant_results)


def prediction_using_url(urls: list[str]) -> list[dict]:
    encoded_urls = [url.replace(':', '%3A').replace('/', '%2F') for url in urls]
    request_string = f'https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}'
    for url in encoded_urls:
        request_string += f'&images={url}'
    request_string += f'&organs=leaf' * len(urls)
    response = requests.get(request_string)
    print(response.status_code)
    if str(response.status_code)[0] == '2':
        json_result = json.loads(response.text)
        plant_results = sorted(json_result["results"], key=lambda x: x["score"], reverse=True)
        return convert_data_to_names(plant_results)



