import sqlite3
import requests
from datetime import datetime

print("Tervetuloa sääseurantaan!")
conn = sqlite3.connect("sää.db")
print("Haluatko muuttaa seurattavia paikkakuntia? (K/E)")
vastaus = input()

kursori = conn.cursor() # luodaan kursori, joka on ikään kuin tietokantayhteyden kautta kulkeva "työkalu", jolla voidaan suorittaa SQL-kyselyitä

if vastaus.lower() == "k": 
    # kursori.execute("DROP TABLE IF EXISTS paikkakunnat") # poistetaan vanha taulu, jotta voidaan luoda uusi, jossa on päivitetyt seurattavat paikkakunnat
    # tietokannan luonti
    sql = """CREATE TABLE IF NOT EXISTS paikkakunnat(
    nimi text,
    lämpötila integer)"""
    kursori.execute(sql)
    tyhjennys = """DELETE FROM paikkakunnat"""
    kursori.execute(tyhjennys) # tyhjennetään vanhat seurattavat paikkakunnat, jotta voidaan tallentaa uudet
    conn.commit() # tallennetaan muutokset tietokantaan

    paikkakunta = True
    print("Syötä seurattavan paikkakunnan nimi, kirjoita X lopettaaksesi: ")
    while paikkakunta: # toistetaan, kunnes käyttäjä kirjoittaa X
        paikkakunta = input()

        if paikkakunta.lower() == "x":
            break
        
        insert_sql = "INSERT INTO paikkakunnat VALUES (?, ?)"
        kursori.execute(insert_sql, (paikkakunta, 0)) # tallennetaan tietokantaan uusi rivi, jossa on syötetty paikkakunta ja lämpötila 0
        conn.commit() # tallennetaan muutokset tietokantaan

    
else: # jos käyttäjä ei halua muuttaa seurattavia paikkakuntia, jatketaan suoraan lämpötilatiedon hakemiseen
    print("Seurattavat paikkakunnat pysyvät ennallaan. Kirjoita X poistuaksesi.")
    vastaus = input()
    if vastaus.lower() == "x":
        print("Poistutaan.")


print("Haluatko hakea lämpötilatiedon Ilmatieteenlaitoksen sivuilta? (K/E)")
vastaus = input()

if vastaus.lower() == "k":

    onnistuneet = 0 # lasketaan onnistuneet hakukerrat, jotta voidaan kirjoittaa lokitiedostoon, kuinka monta paikkakunnan lämpötilatiedot saatiin haettua onnistuneesti
    lokirivit = [] # luodaan lista, johon tallennetaan lokitiedostoon kirjoitettavat rivit, jotta voidaan kirjoittaa lokitiedostoon vain yksi rivi, jossa on kaikkien haettujen paikkakuntien nimet ja lämpötilatiedot

    sql = "SELECT * FROM paikkakunnat"
    for rivi in kursori.execute(sql): 
        paikkakunta = rivi[0]
        url = f"https://www.ilmatieteenlaitos.fi/saa/{paikkakunta}"

        try:
            # haetaan lämpötila Ilmatieteenlaitoksen sivuilta
            response = requests.get(url, params={"encoding": "utf-8"}) 
            html = str(response.text)
            indeksi = html.index('°') # Tämä merkki etsitään html sisällöstä
            alku = indeksi -2 # Tämän verran ° -merkin alusta aletaan lukemaan
            loppu = alku + 3 # Tässä lukema päättyy
            html2 = html[alku:loppu]
            print(f"Lämpötila paikkakunnalla {paikkakunta} on {html2} astetta")
            onnistuneet += 1 # kasvatetaan onnistuneiden hakukertojen määrää yhdellä, jotta voidaan kirjoittaa lokitiedostoon, kuinka monen paikkakunnan lämpötilatiedot saatiin haettua onnistuneesti
            lokirivit.append(f"{paikkakunta} - {html2} astetta") # lisätään lokirivien listaan uusi rivi, jossa on haetun paikkakunnan nimi ja lämpötilatieto

        except:
            print("Virhe käsittelyssä")
            lokirivit.append(f"{paikkakunta} - Hakuvirhe")


else:
    print("Kirjoita X poistuaksesi.")
    vastaus = input()
    if vastaus.lower() == "x":
        print("Poistutaan.")

    # lämpötila = "0" # alustetaan lämpötila, jotta se on määritettynä, vaikka sitä ei haettaisi



def kirjoita_lokiin(yhteenveto): # funktio, joka kirjoittaa lokitiedostoon uuden rivin, jossa on aika ja syötetty paikkakunta, sekä kaikki haettujen paikkakuntien nimet ja lämpötilatiedot, jotka on tallennettu lokirivien listaan
        aika = datetime.now()
        tiedosto = open(r"C:\Users\janna\Desktop\Opiskelu\Kevät 2026\Python-ohjelmointi\Loki.txt", "a") # "a" tarkoittaa, että lisätään uusi rivi
        rivi = str(aika) + " " + yhteenveto
        tiedosto.write(rivi + "\r\n" + "\r\n".join(lokirivit) + "\r\n\r\n") # kirjoitetaan lokitiedostoon uusi rivi, jossa on aika ja syötetty paikkakunta, sekä kaikki haettujen paikkakuntien nimet ja lämpötilatiedot, jotka on tallennettu lokirivien listaan
        tiedosto.close()
        print(rivi) 

# \r\n tarkoittaa rivinvaihtoa, jotta lokitiedostoon kirjoitetaan uusi rivi jokaista uutta lokimerkintää varten, ja "\r\n".join(lokirivit) tarkoittaa, että lokirivien listan kaikki rivit yhdistetään yhdeksi merkkijonoksi, jossa jokainen rivi on erotettu toisistaan rivinvaihdolla.

kirjoita_lokiin(f"Haettiin {onnistuneet} paikkakunnan lämpötilatiedot onnistuneesti.") 

print()
print("Tietokannan sisältö:")
sql = "SELECT * FROM paikkakunnat"
for rivi in kursori.execute(sql):
    print(rivi)


# suljetaan tietokantayhteys 
conn.close()
print()
print("Tietokantayhteys suljettu")