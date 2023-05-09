import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

import main

year = 2023
raceNumber = 5

circuits_url = f"http://ergast.com/api/f1/{year}/{raceNumber}/circuits"
circuits_html = requests.get(circuits_url).text
circuit_soup = BeautifulSoup(circuits_html)
circuit = circuit_soup.find_all('circuitname')[0].text
print(circuit)

drivers_url = f"http://ergast.com/api/f1/{year}/{raceNumber}/driverStandings"
drivers_html = requests.get(drivers_url).text
drivers_soup = BeautifulSoup(drivers_html)

drivers = drivers_soup.find_all('driverstanding')

points_df = pd.DataFrame(columns=['driver', 'constructor', 'points'])

for driver in drivers:
    driverCode = driver.find_all('driver')[0]['code']
    constructor = driver.find_all('constructor')[0].find_all('name')[0].text
    points = int(driver['points'])

    points_df = points_df.append({'driver': driverCode, 'constructor': constructor, 'points': points},
                                 ignore_index=True)
points_df = points_df.sort_values('constructor')

grouped_df = points_df.groupby('constructor')['points'].sum().reset_index()

points_df = points_df.merge(grouped_df, on='constructor').sort_values(by=['points_y', 'constructor', 'points_x'],
                                                                      ascending=[False, True, False])
points_df = points_df.drop('points_y', axis=1)
points_df = points_df.rename(columns={'points_x': 'points'})

constructors = points_df['constructor'].unique()

fig, axes = plt.subplots(2, len(constructors) // 2, figsize=(15, 10))



colors = ['white', 'red']

for i, constructor in enumerate(constructors):
    ax = axes[i // (len(constructors) // 2), i % (len(constructors) // 2)]

    constructor_df = points_df[points_df['constructor'] == constructor]

    constructor_points = sum(constructor_df['points'])
    labels = [f"{row['driver']} ({row['points']})" for _, row in constructor_df.iterrows()]

    if year == 2023:
        ax.pie(constructor_df['points'], labels=labels, autopct='%1.1f%%', colors=[main.constructorColor2023[constructor],'white'],
               wedgeprops={'edgecolor': 'black'},
               textprops={'color': 'black'})
    else:
        ax.pie(constructor_df['points'], labels=labels, autopct='%1.1f%%', colors=colors,
               wedgeprops={'edgecolor': 'black'})

    ax.set_title(f'{constructor} ({constructor_points})')

plt.suptitle(f"Constructor Points Distribution - {circuit}", size=25)
plt.tight_layout()

# Save the fig to a specific path
path = '/Users/danielalas/Desktop/Personal/F1/Stats/Miami/constructor_points_distribution.png'
# plt.savefig(path)

plt.show()
