import requests
import re


def prenesi_html(url):
    html = requests.get(url)
    # with open("html", "w", encoding="utf-8") as dat:
        # print(html.text, file=dat)
    return html.text


# prenesi_html("https://openlibrary.org/")

def izlusci(html):
    vzorec = r'<div class="book carousel__item">.*?<div class="book-cta">'
    return re.findall(vzorec, html, flags=re.DOTALL)


def izlusci_iz_bloka(blok):
    vzorec = re.compile(
        r"""<a href="(?P<url>.*?)" data-ol-link-track=""", re.DOTALL
    )
    najdba = vzorec.search(blok)
    slovar = {}
    slovar["url"] = najdba["url"]
    return slovar




# print(izlusci_iz_bloka((izlusci(prenesi_html("https://openlibrary.org/")))[0]))




