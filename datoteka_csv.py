import csv
from izluscevanje_podatkov import *

def pridobi_podatke(stevilka_strani=50):
    """Funkcija, ki ustvari seznam podatkov, ki jih bomo zapisali v csv."""
    podatki = []
    linki = pridobi_knjige(stevilka_strani)
    bloki_2 = izlusci_2(linki)

    for blokec in bloki_2:
        podatki_iz_bloka = izlusci_iz_bloka_2(blokec)
        vsi_podatki = True
        for vrednost in podatki_iz_bloka.values():
            if vrednost == None:
                vsi_podatki = False
                break

        if vsi_podatki:
            podatki.append(podatki_iz_bloka)
        
    return podatki


def naredi_csv(datoteka):
    """Funkcija, ki naredi csv datoteko in vanjo zapiše pridobljene podatke."""
    podatki = pridobi_podatke()
    kljuci = ["naslov", "leto_izdaje", "avtor", "ocena", "stevilo_ocen"]
    
    with open(datoteka, "w", encoding="utf-8", newline="") as dat:
        pisatelj = csv.DictWriter(dat, fieldnames=kljuci)
        pisatelj.writeheader()
        pisatelj.writerows(podatki)

        
naredi_csv("datoteka.csv")