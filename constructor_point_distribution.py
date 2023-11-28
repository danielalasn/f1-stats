import pandas as pd
import matplotlib.pyplot as plt

import formulas
import main

year = 2023
raceNumber = 22

circuit = formulas.circuit_name(year,raceNumber)

drivers_soup = formulas.soup(f"http://ergast.com/api/f1/{year}/{raceNumber}/driverStandings")
drivers = drivers_soup.find_all('driverstanding')

points_df = pd.DataFrame(columns=['driver', 'constructor', 'points'])

for driver in drivers:
    driverCode = driver.find_all('driver')[0]['code']
    constructor = driver.find_all('constructor')[0].find_all('name')[0].text
    points = float(driver['points'])

    points_df = points_df.append({'driver': driverCode, 'constructor': constructor, 'points': points},
                                 ignore_index=True)


points_df = points_df.sort_values('constructor')

grouped_df = points_df.groupby('constructor')['points'].sum().reset_index()

points_df = points_df.merge(grouped_df, on='constructor').sort_values(by=['points_y', 'constructor', 'points_x'],
                                                                      ascending=[False, True, False])
points_df = points_df.drop('points_y', axis=1)
points_df = points_df.rename(columns={'points_x': 'points'})

points_df = points_df[points_df['points'] != 0]

print(points_df)
constructors = points_df['constructor'].unique()

fig, axes = plt.subplots(2, (len(constructors) + 1) // 2, figsize=(15, 10))

colors = ['white', 'black']

for i, constructor in enumerate(constructors):
    ax = axes[i // ((len(constructors) + 1) // 2), i % ((len(constructors) + 1) // 2)]

    constructor_df = points_df[points_df['constructor'] == constructor]

    constructor_points = sum(constructor_df['points'])
    labels = [f"{row['driver']} ({row['points']})" for _, row in constructor_df.iterrows()]


    ax.pie(constructor_df['points'], labels=labels, autopct='%1.1f%%',
           colors=[main.constructorColors[constructor],'white', 'gray'],
           wedgeprops={'edgecolor': 'black'},
           textprops={'color': 'black'})


    ax.set_title(f'{constructor} ({constructor_points})')

if len(constructors) % 2 != 0:
    axes[-1, -1].axis('off')

# plt.suptitle(f"Constructor Points Distribution after {circuit} GP {year}", size=25)
plt.suptitle(f"Constructor Points Distribution 2023 Season", size=25)

plt.tight_layout()

# Save the fig to a specific path
path = f'/Users/danielalas/Desktop/Personal/F1/Stats/{year}/{circuit}/constructor_points_distribution.png'
plt.savefig(path)

plt.show()
