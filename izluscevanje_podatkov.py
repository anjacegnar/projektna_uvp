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
        r'<a href="(?P<url>.*?)" data-ol-link-track=', re.DOTALL
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


def izlusci_2(html):
    """Funkcija, ki iz html izlušči blok.""" # blok vsebuje podatke o knjigi, ki jih hočemo potem izluščiti
    for link in linki:
        link = "https://openlibrary.org/" + link
        prenesi_html(link)
        
        vzorec = r'<div class="work-title-and-author mobile">.*?Have read</span></li>'
        return re.findall(vzorec, html, flags=re.DOTALL)

# prenesi_html("https://openlibrary.org/works/OL38382569W")


def izlusci_iz_bloka_2(blok):
    """Funkcija, ki iz bloka izlušči podatke."""
    vzorec = re.compile(
        r'<a href="[^"]*">(?P<naslov>[^<]*)</a>'
        r'<span class="first-published-date"[^>]*>.*?\((?P<leto_izdaje>\d{4})\)</span>'
        r'<h2 class="edition-byline">.*?by <a href="[^"]*" itemprop="author">(?P<avtor>[^<]*)</a>'
        r'<span itemprop="ratingValue">(?P<ocena>[^<]*)</span>'
        r'<li class="readers-stats__review-count">.*?<span itemprop="reviewCount">(?P<stevilo_ocen>\d+)</span>'
        r'<li class="reading-log-stat"><span class="readers-stats__stat">(?P<zeljeno_branje>\d+)</span> <span class="readers-stats__label">Want to read</span>'
        r'<li class="reading-log-stat"><span class="readers-stats__stat">(?P<trenutno_branje>\d+)</span> <span class="readers-stats__label">Currently reading</span>'
        r'<li class="reading-log-stat"><span class="readers-stats__stat">(?P<prebrano>\d+)</span> <span class="readers-stats__label">Have read</span>',
        re.DOTALL
    )
    najdba = vzorec.search(blok)
    slovar = {}

    if najdba:
        slovar["naslov"] = najdba.group("naslov")
        slovar["leto_izdaje"] = najdba.group("leto_izdaje")
        slovar["avtor"] = najdba.group("avtor")
        slovar["ocena"] = najdba.group("ocena")
        slovar["stevilo_ocen"] = najdba.group("stevilo_ocen")
        slovar["zeljeno_branje"] = najdba.group("zeljeno_branje")
        slovar["trenutno_branje"] = najdba.group("trenutno_branje")
        slovar["prebrano"] = najdba.group("prebrano")
    else:
        slovar["naslov"] = None
        slovar["leto_izdaje"] = None
        slovar["avtor"] = None
        slovar["ocena"] = None
        slovar["stevilo_ocen"] = None
        slovar["zeljeno_branje"] = None
        slovar["trenutno_branje"] = None
        slovar["prebrano"] = None
    
    return slovar

