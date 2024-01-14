
import requests

def translate(text_for_translate, lang1: str, lang2: str):
    langpair = lang1 + '|' + lang2
    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/get"

    querystring = {"langpair": langpair,"q": text_for_translate,"mt": "1","onlyprivate": "0","de": "a@b.c"}

    headers = {
        "X-RapidAPI-Key": "44918ba503msh73dace5ec4ca264p13b441jsn2021a19be84e",
	    "X-RapidAPI-Host": "translated-mymemory---translation-memory.p.rapidapi.com"
        }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()['responseData']['translatedText']

def paraphrase(text):
    url = "https://paraphrasing-paraphrase-api-rewriter.p.rapidapi.com/paraphrase-parrot-pt/get_paraphrase_en"

    payload = {
        "input_text": text,
        "num_versions_text": 1
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "44918ba503msh73dace5ec4ca264p13b441jsn2021a19be84e",
        "X-RapidAPI-Host": "paraphrasing-paraphrase-api-rewriter.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return translate(response.json()[0], "en", "ru")
def summarize(text):
    url = "https://summarize-texts.p.rapidapi.com/pipeline"

    payload = {
        "input": text}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "44918ba503msh73dace5ec4ca264p13b441jsn2021a19be84e",
        "X-RapidAPI-Host": "summarize-texts.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return translate(response.json()['output'][0]['text'], 'en', 'ru')