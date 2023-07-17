import pandas as pd
import matplotlib.pyplot as plt

import formulas
import main

cant_constructors = 5

raceNumber = 10
year = 2023

constructorStandings_df = pd.DataFrame(columns = ['Constructor', 'Start'])

points_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{raceNumber}/constructorStandings')
constructorStandings = points_soup.find_all('constructorstanding')

for constructorStanding in constructorStandings:
    constructor = constructorStanding.find_all('name')[0].text
    constructorStandings_df = constructorStandings_df.append({'Constructor':constructor,'Start':0},ignore_index=True)

for i in range(raceNumber):
    circuit = formulas.circuit_name(year,i+1)

    points_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{i+1}/constructorStandings')
    constructorStandings = points_soup.find_all('constructorstanding')

    for constructorStanding in constructorStandings:
        points = constructorStanding['points']
        constructor = constructorStanding.find_all('name')[0].text
        constructorStandings_df.loc[constructorStandings_df['Constructor'] == constructor, circuit] = points

constructorStandings_df = constructorStandings_df[:cant_constructors]

higherPoints = int(constructorStandings_df[circuit][0])

fig = plt.figure(figsize=(11,8))

for index, row in constructorStandings_df.iterrows():
    constructor_name = row['Constructor']
    current_point = row[circuit]

    color = main.constructorColors[constructor_name]
    plt.plot(constructorStandings_df.columns[1:], row[1:], label=f'{constructor_name} - {current_point}',color=color)


plt.title(f'Constructors Championship after {circuit} {year} (Top {cant_constructors})')
plt.xlim(0, raceNumber)

plt.ylim(0, higherPoints + 5)

plt.locator_params(axis='y', nbins=30)
plt.legend(ncol=1,fontsize=12)
plt.gca().yaxis.tick_right()
plt.grid()

# Save the fig to a specific path
path = f'/Users/danielalas/Desktop/Personal/F1/Stats/{year}/{circuit}/constructor_wc_points.png'
plt.savefig(path)

plt.show()