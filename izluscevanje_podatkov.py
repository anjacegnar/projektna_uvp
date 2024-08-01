import requests
import re


def prenesi_html(url):
    """Funkcija, ki prenese html spletne strani, katere url podamo notri."""
    html = requests.get(url)
    with open("html", "w", encoding="utf-8") as dat:
        print(html.text, file=dat)
    return html.text


# prenesi_html("https://openlibrary.org/")

def izlusci(html):
    """Funkcija, ki iz podanega html izlušči blok.""" # bloki bodo knjige
    vzorec = r'<div class="book carousel__item">.*?<div class="book-cta">'
    return re.findall(vzorec, html, flags=re.DOTALL)


def izlusci_iz_bloka(blok):
    """Funkcija, ki iz bloka izlušči url."""
    vzorec = re.compile(
        r"""<a href="(?P<url>.*?)" data-ol-link-track=""", re.DOTALL
    )
    najdba = vzorec.search(blok)
    slovar = {}
    slovar["url"] = najdba["url"]
    return slovar # vrne slovar, z enim elementom: ključ je "url" in vrednost dejanski url



# print(izlusci_iz_bloka((izlusci(prenesi_html("https://openlibrary.org/")))[0]))


def pridobi_knjige(url):
    html = prenesi_html(url)
    bloki = izlusci(html)
    linki = []

    for blok in bloki:
        podatki = izlusci_iz_bloka(blok)
        url_knjige = podatki["url"]
        if url_knjige:
            linki.append(url_knjige)
    return linki


linki = pridobi_knjige("https://openlibrary.org/")



