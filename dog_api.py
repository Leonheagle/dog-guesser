import requests
import random

def get_all_breeds():
    response=requests.get("https://dog.ceo/api/breeds/list/all")
    breeds=response.json()["message"]
    all_breeds=[]
    for breed,sub_breeds in breeds.items():
        if sub_breeds:
            for sub_breed in sub_breeds:
                all_breeds.append(f"{breed}-{sub_breed}")
        else:
            all_breeds.append(breed)
    return all_breeds
    
def get_random_dog():
    all_breeds=get_all_breeds()
    return random.choice(all_breeds)

def get_dog_by_breed(breed):
    parts = breed.split("-")
    if len(parts)==1:
        url=f"https://dog.ceo/api/breed/{parts[0]}/images/random"
    else:
        url=f"https://dog.ceo/api/breed/{parts[0]}/{parts[1]}/images/random"
    reponse=requests.get(url)
    return reponse.json()["message"]

def get_choices(correct_breed):
    all_breeds=get_all_breeds()
    wrong_breeds=random.sample([breed for breed in all_breeds if breed!=correct_breed],3)
    choices=wrong_breeds+[correct_breed]
    random.shuffle(choices)
    return choices

def quizz():
    correct_breed=get_random_dog()
    image_url=get_dog_by_breed(correct_breed)
    choices=get_choices(correct_breed)
    return correct_breed,image_url,choices

