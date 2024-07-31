import requests

def prenesi_html(url):
    html = requests.get(url)
    with open("html", "w", encoding="utf-8") as dat:
        print(html.text, file=dat)


prenesi_html("https://openlibrary.org/")