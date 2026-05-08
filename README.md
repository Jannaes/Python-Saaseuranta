Täsmäsääohjelma


Tämä projekti on Pythonilla toteutettu täsmäsääohjelma, joka:

- tallentaa käyttäjän seuraamat paikkakunnat SQLite-tietokantaan
- hakee paikkakuntien lämpötilatiedot Ilmatieteenlaitoksen verkkosivuilta
- tulostaa lämpötilat konsoliin
- kirjoittaa hakutuloksista lokitiedoston (.txt)

Projektin tarkoituksena oli harjoitella:

- Pythonin perusteita
- SQLite-tietokannan käyttöä
- HTTP-pyyntöjä requests-kirjastolla
- virheenkäsittelyä (try/except)
- tiedostokäsittelyä
- silmukoita ja ehtolauseita

Käytetyt teknologiat
- Python 3
- SQLite3
- Requests-kirjasto

******************************************************
Ohjelman toiminta
1. Paikkakuntien hallinta

Ohjelma kysyy käynnistyksen yhteydessä:

Haluatko muuttaa seurattavia paikkakuntia? (K/E)

Jos käyttäjä vastaa K:

- vanhat paikkakunnat poistetaan tietokannasta
- käyttäjä voi syöttää uusia paikkakuntia
- syöttäminen lopetetaan kirjoittamalla X

Paikkakunnat tallennetaan SQLite-tietokantaan.

Jos käyttäjä vastaa E:

- aiemmin syötetyt paikkakunnat jäävät voimaan

2. Lämpötilojen haku

Ohjelma kysyy:

Haluatko hakea lämpötilatiedon Ilmatieteenlaitoksen sivuilta? (K/E)

Jos käyttäjä vastaa K:

- ohjelma lukee kaikki paikkakunnat tietokannasta
- hakee jokaisen paikkakunnan sääsivun
- etsii lämpötilatiedon HTML-sisällöstä
- tulostaa lämpötilan konsoliin
- ohjelma kirjoittaa tiedostopohjaista lokia.

Lokitiedosto sisältää:

- hakuajan
- onnistuneiden hakujen määrän
- paikkakunnat ja lämpötilat
- mahdolliset hakuvirheet

******************************************************

Tietokanta

Projektissa käytetään SQLite-tietokantaa:
sää.db


Suorita ohjelma:
python Palautustehtävä.py


Projektin aikana harjoiteltiin:

- SQLite-tietokannan luontia ja käyttöä
- SQL-kyselyitä (INSERT, SELECT, DELETE)
- HTTP-pyyntöjä Pythonissa
- HTML-sisällön käsittelyä
- lokitiedostojen kirjoittamista
- Pythonin listoja ja tupleja
- virheiden käsittelyä (try/except)
- ohjelman rakenteen suunnittelua
  

Mahdollisia jatkokehityksiä:

- lämpötilojen tallennus tietokantaan
- graafinen käyttöliittymä
- sää-API:n käyttö HTML-parsinnan sijaan
- parempi lämpötilan tunnistus HTML:stä


Tekijä

Projekti on toteutettu harjoitustyönä Python-ohjelmoinnin kurssilla. 

Tämä projekti on tarkoitettu oppimiseen ja portfoliokäyttöön.
