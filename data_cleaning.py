import pandas as pd

'''
Tämä ohjelma on osa data-analytiikan harjoitustyötä, jonka raportti on nimellä
"Hinnan, genren ja alennuskampanjoiden yhteys pelien suosioon GOG.com-alustalla."

Datasetin siivoaminen. Ajetaan ennen analyysia.

Alkuperäinen datasetti gog_games_dataset.csv on hyvin laaja ja sisältää analyysin kannalta turhia sarakkeita, kuten kuva- ja videolinkkejä,
joten ne siivotaan tällä ohjelmalla pois. Tuloksena ohjelma tallentaa siivotun datasetin, jota käytetään itse analyysissa.

Tehnyt Noora Nevalainen.
'''

inputfile = 'gog_games_dataset.csv'
outputfile = 'cleaned_gog_dataset.csv'

data = pd.read_csv(inputfile)

# Ottaa vain pelit huomioon, sillä yllättäen pelikauppapaikka sisältää muitakin kuin pelinimikkeitä.
df = data[data["isGame"] == True].copy()

# Valitsee analyysia varten mielenkiintoiset sarakkeet. Kaikkia näitä en lopulta käyttänyt analyysissa.
cols = [
    "title",    # pelin nimi
    "developer",    # pelin kehittäjä
    "publisher",    # pelin julkaisija
    "genres",   # peligenret
    "category", # kategoria
    "overallAvgRating", # keskimääräinen käyttäjien antama arvio/arvosana pelille
    "reviewCount",  # käyttäjäarvioiden määrä
    "finalAmount",  # lopullinen hinta
    "baseAmount",   # perushinta
    "discountPercentage",   # alennusprosentti
    "isDiscounted", # onko peli alennuksessa
    "isFree",   # onko ilmaispeli
    "globalReleaseDate",    # alkuperäinen julkaisupäivä unix-timestampilla
    "isGame"   # onko kyseessä peli
]

# Kopioi valitun sisällön uuteen dataframeen.
df = df[cols].copy()

# Päägenre muodostuu ensimmäisestä genrestä, joka on listattuna "genres"-arvon sisällä.
df["main_genre"] = (
    df["genres"]
    .astype(str)
    .str.split(",")
    .str[0]
    .str.replace(r"[\[\]']", "", regex=True)
    .str.strip()
)

# Muuttaa julkaisuvuoden.
df["release_year"] = pd.to_datetime(
    df["globalReleaseDate"],
    unit="s",
    errors="coerce"
).dt.year

# Poistaa datasetistä pelit, joilla ei ole ollenkaan arvioita.
df = df[df["reviewCount"] > 0]

# Siistii pois mahdolliset ei-numeeriset arvot näistä sarakkeista.
df = df.dropna(subset=["overallAvgRating", "finalAmount", "release_year"])

# Siivottu data tallennetaan uuteen tiedostoon ilman indeksejä.
df.to_csv(outputfile, index=False)


print("Data on siivottu onnistuneesti analyysia varten.")
print(df.info())
print(df.head(10))
print(df["genres"].head())
print(df["main_genre"].head())

# Testinä etsitään tiedot Morrowind-sanan sisältävästä pelistä:
# game = df[df["title"].str.contains("Morrowind", case=False, na=False)]
# print(game.T)