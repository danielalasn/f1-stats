import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

year = 2023
raceNumber = 4

circuits_url = f"http://ergast.com/api/f1/{year}/{raceNumber}/circuits"
circuits_html = requests.get(circuits_url).text
circuit_soup = BeautifulSoup(circuits_html)
circuit = circuit_soup.find_all('locality')[0].text
if circuit == 'Sakhir':
    circuit = 'Bahrain'

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

constructor_color2023 = {'Red Bull': ['white', '#15185F'],
                         'Aston Martin': ['white', '#00594F'],
                         'Mercedes': ['white', '#00A19C'],
                         'Ferrari': ['white', '#FF0200'],
                         'McLaren': ['white', '#FE8001'],
                         'Alpine F1 Team': ['white', '#0C1D2C'],
                         'Haas F1 Team': ['white', '#E1050B'],
                         'Alfa Romeo': ['white', '#A50E2D'],
                         'AlphaTauri': ['white', '#032947'],
                         'Williams': ['white', '#001B54'], }

colors = ['white', 'red']

for i, constructor in enumerate(constructors):
    ax = axes[i // (len(constructors) // 2), i % (len(constructors) // 2)]

    constructor_df = points_df[points_df['constructor'] == constructor]

    constructor_points = sum(constructor_df['points'])
    labels = [f"{row['driver']} ({row['points']})" for _, row in constructor_df.iterrows()]

    if year == 2023:
        ax.pie(constructor_df['points'], labels=labels, autopct='%1.1f%%', colors=constructor_color2023[constructor],
               wedgeprops={'edgecolor': 'black'})
    else:
        ax.pie(constructor_df['points'], labels=labels, autopct='%1.1f%%', colors=colors,
               wedgeprops={'edgecolor': 'black'})

    ax.set_title(f'{constructor} ({constructor_points})')

plt.suptitle(f"Constructor Points Distribution - {circuit}")
plt.tight_layout()
plt.show()