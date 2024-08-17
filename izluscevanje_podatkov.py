import requests
import re
import time
import concurrent.futures


def prenesi_html(url):
    """Funkcija, ki prenese html spletne strani, katere url podamo notri."""
    for _ in range(5):
        try:
            html = requests.get(url)
            html.raise_for_status()

            with open("html", "w", encoding="utf-8") as dat:
                dat.write(html.text)

            return html.text
        
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, Exception):
            time.sleep(2)

    return None


def prenesi_stran(stevilka_strani):
    """Funkcija, ki prenese html za določeno stran seznama."""
    url = f"https://openlibrary.org/trending/forever?page={stevilka_strani}"
    return prenesi_html(url)


def izlusci(html):
    """Funkcija, ki iz podanega html izlušči blok.""" # bloki bodo knjige
    vzorec = r'<div class="sri__main">.*?class="bookauthor">'
    bloki = re.findall(vzorec, html, flags=re.DOTALL)
    return bloki


def izlusci_iz_bloka(blok):
    """Funkcija, ki iz bloka izlušči url."""
    vzorec = re.compile(
        r'<a href="(?P<url>.*?)"><img', re.DOTALL
    )
    najdba = vzorec.search(blok)
    slovar = {}
    if najdba:
        slovar["url"] = najdba.group("url")
    else:
        slovar["url"] = None

    return slovar


def pridobi_knjige(stevilka_strani):
    """Funkcija, ki v seznam shrani url-je knjig."""
    linki = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        naloge = []

        for i in range(1, stevilka_strani + 1):
            naloga = executor.submit(prenesi_stran, i)
            naloge.append(naloga)

        for future in concurrent.futures.as_completed(naloge):
            html = future.result()
            if html:
                bloki = izlusci(html)

                for blok in bloki:
                    podatki = izlusci_iz_bloka(blok)
                    url_knjige = podatki["url"]
                    if url_knjige:
                        linki.append(url_knjige)
                    
    return linki


def izlusci_2(linki):
    """Funkcija, ki iz html izlušči blok.""" # blok vsebuje podatke o knjigi, ki jih hočemo potem izluščiti
    bloki = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        naloge = []

        for link in linki:
            nas_link = "https://openlibrary.org" + link
            naloga = executor.submit(prenesi_html, nas_link)
            naloge.append(naloga)

        for future in concurrent.futures.as_completed(naloge):
            html = future.result()
            if html:
                blok = re.findall(r'<div class="work-title-and-author mobile">.*?Have read</span></li>', html, flags=re.DOTALL)
                bloki.extend(blok)
        
    return bloki


def izlusci_iz_bloka_2(blok):
    """Funkcija, ki iz bloka izlušči podatke o knjigi."""
    vzorec = re.compile(
        r'<a href="/works/.*?">(?P<naslov>.*?)</a>.*?'
        r'<span class="first-published-date" title="First published in (?P<leto_izdaje>.*?)">.*?'
        r'<a href="/authors/.*?/.*?" itemprop="author">(?P<avtor>[^<]*)</a>.*?'
        r'<span itemprop="ratingValue">(?P<ocena>.*?)</span>.*?'
        r'<li class="readers-stats__review-count">.*?<span itemprop="reviewCount">(?P<stevilo_ocen>\d+)</span>',
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
    else:
        slovar["naslov"] = None
        slovar["leto_izdaje"] = None
        slovar["avtor"] = None
        slovar["ocena"] = None
        slovar["stevilo_ocen"] = None
    
    return slovar