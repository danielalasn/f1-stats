import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

import main

cant_constructors = 5

raceNumber = 5
year = 2005

constructorStandings_df = pd.DataFrame(columns = ['Constructor', 'Start'])

url_laps = f'http://ergast.com/api/f1/{year}/{raceNumber}/constructorStandings'
points_html= requests.get(url_laps).text
points_soup = BeautifulSoup(points_html)
constructorStandings = points_soup.find_all('constructorstanding')

for constructorStanding in constructorStandings:
    constructor = constructorStanding.find_all('name')[0].text
    constructorStandings_df = constructorStandings_df.append({'Constructor':constructor,'Start':0},ignore_index=True)

for i in range(raceNumber):
    circuit_url = f'http://ergast.com/api/f1/{year}/{i+1}/circuits'
    circuit_html= requests.get(circuit_url).text
    circuit_soup = BeautifulSoup(circuit_html)
    locality = circuit_soup.find_all('locality')[0].text
    if locality == 'Sakhir':
        locality = 'Bahrain'

    url_laps = f'http://ergast.com/api/f1/{year}/{i+1}/constructorStandings'
    points_html= requests.get(url_laps).text
    points_soup = BeautifulSoup(points_html)
    constructorStandings = points_soup.find_all('constructorstanding')

    for constructorStanding in constructorStandings:
        points = constructorStanding['points']
        constructor = constructorStanding.find_all('name')[0].text
        constructorStandings_df.loc[constructorStandings_df['Constructor'] == constructor, locality] = points

constructorStandings_df = constructorStandings_df[:cant_constructors]

higherPoints = int(constructorStandings_df[locality][0])

fig = plt.figure(figsize=(11,8))

for index, row in constructorStandings_df.iterrows():
    constructor_name = row['Constructor']
    current_point = row[locality]
    if year == 2023:
        color = main.constructorColor2023[constructor_name]
        plt.plot(constructorStandings_df.columns[1:], row[1:], label=f'{constructor_name} - {current_point}',color=color)
    else:
        plt.plot(constructorStandings_df.columns[1:], row[1:], label=f'{constructor_name} - {current_point}')


plt.title(f'Constructors Championship after {locality} {year} (Top {cant_constructors})')
plt.xlim(0, raceNumber)

plt.ylim(0, higherPoints + 5)

plt.locator_params(axis='y', nbins=30)
plt.legend(ncol=1,fontsize=12)
plt.gca().yaxis.tick_right()
plt.grid()

# Save the fig to a specific path
path = '/Users/danielalas/Desktop/Personal/F1/Stats/Miami/constructor_wc_points.png'
# plt.savefig(path)

plt.show()