import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr, mannwhitneyu

'''
Tämä ohjelma on osa data-analytiikan harjoitustyötä, jonka raportti on nimellä
"Hinnan, genren ja alennuskampanjoiden yhteys pelien suosioon GOG.com-alustalla."

Tässä analyysissä käytetään siivottua datasettiä (cleaned_gog_dataset.csv), joka saadaan aikaan ajamalla ensin data_cleaning.py-tiedosto.

Analyysissa tarkastellaan:
1. Pelien yleisimmät hinnat
2. Pelien yleisimmät genret
3. Pelien määrä julkaisuvuoden mukaan
4. Pelien hinta verrattuna suosioon (eli käyttäjäarvosteluiden lukumäärään)
5. Alennusten vaikutus pelien suosioon (ristiintaulukointi)
6. Suosituimmat peligenret
7. Extra: Pelien suosio julkaisuvuosittain ( ei lopullisessa raportissa)

Tehnyt Noora Nevalainen.

'''
# Sisäänluettava tiedosto.
inputfile = 'cleaned_gog_dataset.csv'

# Lukee datan csv-tiedostosta.
df = pd.read_csv(inputfile)

print("Datasetti luettu onnistuneesti.")

# 1. Pelien yleisimmät hinnat

# Luo hintaluokat 0–50 €, kahden euron välein.
bins = np.arange(0, 52, 2)
df["price_bin"] = pd.cut(df["finalAmount"], bins=bins, right=False)

# Laskee montako peliä on kussakin hintaluokassa.
price_counts = df["price_bin"].value_counts().sort_index()

plt.figure(figsize=(12, 6))
labels = [f"{int(bins[i])}–{int(bins[i+1])} €" for i in range(len(bins)-1)]
plt.bar(labels, price_counts.values, width=0.8)

plt.xlabel("Pelin hinta (€)")
plt.ylabel("Pelien lukumäärä")
plt.title("Pelien hintojen jakauma GOG.comissa (hintaluokat 2 € välein)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Pelien yleisimmät genret

# Laskee eri peligenrejen esiintymismäärät.
genre_counts = df["main_genre"].value_counts()

# Analyysiin otetaan mukaan 6 suosituinta genreä.
top_genres = genre_counts.head(6)

# Niputtaa loput Muut-kategoriaan.
other_genres = genre_counts.iloc[6:].sum()

pie_data = top_genres.copy()
pie_data["Muut"] = other_genres

# Ympyräkaavio
plt.figure(figsize=(10, 8))
plt.pie(
    pie_data.values,
    labels=pie_data.index,
    autopct='%.1f%%',
    startangle=90,
    pctdistance=0.8
)
plt.title("Pelien päägenrejen jakauma Gog.comissa")
plt.tight_layout()
plt.show()

# 3. Pelien määrä julkaisuvuoden mukaan

df["release_year"] = df["release_year"].astype(int)
# Laskee pelien lukumäärän per julkaisuvuosi.
year_counts = df["release_year"].value_counts().sort_index()

plt.figure(figsize=(10, 6))
plt.fill_between(
    year_counts.index,
    year_counts.values,
    step="mid",
    alpha=0.7
)
plt.plot(year_counts.index, year_counts.values)

plt.xlabel("Julkaisuvuosi")
plt.ylabel("Pelien lukumäärä")
plt.title("GOG.com-pelien julkaisuvuosien jakauma")
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Hinta verrattuna suosioon (korrelaatio ja trendiviiva)

# Outlier-arvojen esille kaivelu, kaikki jotka ovat saaneet epäilyttävän paljon käyttäjäarvosteluita.
hits = df[df["reviewCount"] > 2000]
# Tulostaa poikkeavuudet.
print("Poikkeavuudet käyttäjäarvioiden määrissä:")
print(hits[["title", "reviewCount", "finalAmount"]])

x = df["finalAmount"]
y = df["reviewCount"]

# Trendiviivan laskeminen polyfitillä.
m, b = np.polyfit(x, y, 1)

plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.4)
plt.plot(x, m*x + b, color="red", linewidth=2)  # trendiviiva

plt.xlabel("Pelin hinta (€)")
plt.ylabel("Arvioiden määrä")
plt.title("Pelin hinnan ja käyttäjäarvioiden määrän välinen hajonta, trendiviivalla")
plt.tight_layout()
plt.show()

# Pearson -korrelaatio.
corr, p_value = pearsonr(x, y)
print(f"Korrelaatio (Pearson r): {corr:.3f}")
print(f"p-arvo: {p_value:.5f}")
print()

# 5. Alennusten vaikutus pelien suosioon.
# Ristiintaulukointi: isDiscounted × reviewCount

print("Alennusten vaikutus pelien suosioon.")
group_means = df.groupby("isDiscounted")["reviewCount"].mean()
group_counts = df["isDiscounted"].value_counts()

print("Keskiarvot:")
print(group_means)
print("\nHavaintojen lukumäärät:")
print(group_counts)

# Alennus vs. normaalihintainen.
discounted = df[df["isDiscounted"] == True]["reviewCount"]
not_discounted = df[df["isDiscounted"] == False]["reviewCount"]

# Valitsin tähän Mann–Whitney U-testin.
stat, p_value = mannwhitneyu(discounted, not_discounted, alternative="two-sided")

print(f"Mann–Whitney U testin p-arvo: {p_value:.5f}")

# 6. Suosituimmat peligenret
# Mitataan keskimääräiset käyttäjäarviot peligenreittäin.

genre_reviews = df.groupby("main_genre")["reviewCount"].mean().sort_values(ascending=False)

plt.figure(figsize=(10,6))
genre_reviews.plot(kind="bar")

plt.xlabel("Genre")
plt.ylabel("Arvioiden määrän keskiarvo")
plt.title("Suosituimmat genret käyttäjäarvioiden määrän mukaan")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

print("Keskimääräiset käyttäjäarviomäärät genreittäin:")
print(genre_reviews)

# 7. extra: Pelien suosio julkaisuvuosittain
# Tätä en ottanut raporttiin mukaan, mutta kiinnosti löytyykö mitään yhteyttä suosioon.

df["release_year"] = df["release_year"].astype(int)

x = df["release_year"]
y = df["reviewCount"]

plt.figure(figsize=(10,6))
plt.scatter(x, y, alpha=0.3)
plt.xlabel("Pelin julkaisuvuosi")
plt.ylabel("Arvioiden määrä")
plt.title(" Käyttäjäarvioiden lukumäärät pelien julkaisuvuosittain")
plt.tight_layout()
plt.show()

corr, p_value = pearsonr(x, y)
print(f"Korrelaatio (Pearson r): {corr:.3f}")
print(f"p-arvo: {p_value:.5f}")