import sqlite3
import requests
from datetime import datetime

print("Tervetuloa sääseurantaan!")
conn = sqlite3.connect("sää.db")
print("Haluatko muuttaa seurattavia paikkakuntia? (K/E)")
vastaus = input()

kursori = conn.cursor() # luodaan kursori, joka on ikään kuin tietokantayhteyden kautta kulkeva "työkalu", jolla voidaan suorittaa SQL-kyselyitä

if vastaus.lower() == "k": 
    kursori.execute("DROP TABLE IF EXISTS paikkakunnat") # poistetaan vanha taulu, jotta voidaan luoda uusi
    # tietokannan luonti
    sql = """CREATE TABLE IF NOT EXISTS paikkakunnat(
    nimi text)"""
    kursori.execute(sql) # luodaan uusi taulu, johon tallennetaan seurattavien paikkakuntien nimet
    tyhjennys = """DELETE FROM paikkakunnat"""
    kursori.execute(tyhjennys) # tyhjennetään vanhat seurattavat paikkakunnat, jotta voidaan tallentaa uudet
    conn.commit() # tallennetaan muutokset tietokantaan

    paikkakunta = True 
    print("Syötä seurattavan paikkakunnan nimi ja paina Enter. Kirjoita X lopettaaksesi paikkakuntien syötön.")
    while paikkakunta: # toistetaan, kunnes käyttäjä kirjoittaa X
        paikkakunta = input()

        if paikkakunta.lower() == "x":
            break
        
        insert_sql = "INSERT INTO paikkakunnat VALUES (?)"
        kursori.execute(insert_sql, (paikkakunta,)) # tallennetaan tietokantaan uusi rivi, jossa on syötetty paikkakunta
        conn.commit() # tallennetaan muutokset tietokantaan

    
else: # jos käyttäjä ei halua muuttaa seurattavia paikkakuntia, jatketaan suoraan lämpötilatiedon hakemiseen
    print("Seurattavat paikkakunnat pysyvät ennallaan.")


print("Haluatko hakea lämpötilatiedon Ilmatieteenlaitoksen sivuilta? (K/E)")
vastaus = input()

if vastaus.lower() == "k":

    onnistuneet = 0 # lasketaan onnistuneet hakukerrat lokitiedostoa varten
    lokirivit = [] # luodaan lista, johon tallennetaan lokitiedostoon kirjoitettavat rivit, jotta voidaan kirjoittaa lokitiedostoon vain yksi rivi, jossa on kaikkien haettujen paikkakuntien nimet ja lämpötilatiedot

    sql = "SELECT * FROM paikkakunnat"
    for rivi in kursori.execute(sql): # käydään läpi kaikki tietokannasta haetut rivit, joissa on seurattavien paikkakuntien nimet
        paikkakunta = rivi[0] # haetaan tietokannasta rivi, jossa on seurattavan paikkakunnan nimi, ja tallennetaan se muuttujaan, jotta voidaan hakea lämpötilatieto kyseiselle paikkakunnalle
        url = f"https://www.ilmatieteenlaitos.fi/saa/{paikkakunta}"

        try:
            # haetaan lämpötila Ilmatieteenlaitoksen sivuilta
            response = requests.get(url, params={"encoding": "utf-8"}) 
            html = str(response.text) # haetaan sivun HTML-koodi merkkijonona, jotta voidaan etsiä siitä lämpötilatieto
            indeksi = html.index('°') # Tämä merkki etsitään html sisällöstä
            alku = indeksi -2 # Tämän verran ° -merkin alusta aletaan lukemaan
            loppu = alku + 3 # Tässä lukema päättyy
            html2 = html[alku:loppu] 
            print(f"Lämpötila paikkakunnalla {paikkakunta} on {html2}")
            onnistuneet += 1 # kasvatetaan onnistuneiden hakukertojen määrää yhdellä, jotta voidaan kirjoittaa lokitiedostoon, kuinka monen paikkakunnan lämpötilatiedot saatiin haettua onnistuneesti
            lokirivit.append(f"{paikkakunta}: {html2}") # lisätään lokirivien listaan uusi rivi, jossa on haetun paikkakunnan nimi ja lämpötilatieto

        except:
            print("Hakuvirhe")
            lokirivit.append(f"{paikkakunta}: Hakuvirhe")
 


    def kirjoita_lokiin(yhteenveto): # funktio, joka kirjoittaa lokitiedostoon uuden rivin, jossa on aika ja syötetty paikkakunta, sekä kaikki haettujen paikkakuntien nimet ja lämpötilatiedot, jotka on tallennettu lokirivien listaan
        aika = datetime.now()
        tiedosto = open(r"C:\Users\janna\Desktop\Opiskelu\Kevät 2026\Python-ohjelmointi\Loki.txt", "a") # "a" tarkoittaa, että lisätään uusi rivi
        rivi = str(aika) + " " + yhteenveto
        tiedosto.write(rivi + 
                       "\r\n" + 
                       "\r\n".join(lokirivit) + 
                       "\r\n" + 
                       "******************************************************" + 
                       "\r\n\r\n")
        tiedosto.close()
        print(rivi) 

# \r\n tarkoittaa rivinvaihtoa, jotta lokitiedostoon kirjoitetaan uusi rivi jokaista uutta lokimerkintää varten, ja "\r\n".join(lokirivit) tarkoittaa, että lokirivien listan kaikki rivit yhdistetään yhdeksi merkkijonoksi, jossa jokainen rivi on erotettu toisistaan rivinvaihdolla.

    kirjoita_lokiin("\r\n" + f"Haettiin {onnistuneet} paikkakunnan lämpötilatiedot onnistuneesti:") 

    print("Ohjelman suoritus päättyy. Näkemiin!")

else:
    print("Kirjoita X poistuaksesi.")
    vastaus = input()
    if vastaus.lower() == "x":
        print("Poistutaan ohjelmasta. Näkemiin!")

print()
print("Tietokannan sisältö:")
sql = "SELECT * FROM paikkakunnat"
for rivi in kursori.execute(sql):
    print(rivi[0])


# suljetaan tietokantayhteys 
conn.close()
print()