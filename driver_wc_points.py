import os

import pandas as pd
import matplotlib.pyplot as plt

import formulas
import main

# --------------Changes:
raceNumber = 10
year = 2023
cant_drivers = 10
# ---------------

driverStandings_df = pd.DataFrame(columns=['Driver', 'Start'])

points_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{raceNumber}/driverStandings')
driverStandings = points_soup.find_all('driverstanding')

for driverStanding in driverStandings:
    driver = driverStanding.find_all('driver')[0]['driverid']
    driverStandings_df = driverStandings_df.append({'Driver': driver, 'Start': 0}, ignore_index=True)

for i in range(raceNumber):
    circuit = formulas.circuit_name(year,i+1)

    points_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{i + 1}/driverStandings')
    driverStandings = points_soup.find_all('driverstanding')

    for driverStanding in driverStandings:
        points = driverStanding['points']
        driver = driverStanding.find_all('driver')[0]['driverid']
        driverStandings_df.loc[driverStandings_df['Driver'] == driver, circuit] = points

driverStandings_df = driverStandings_df[:cant_drivers]

higherPoints = float(driverStandings_df[circuit][0])

fig = plt.figure(figsize=(11, 8))

existing_colors = []

for index, row in driverStandings_df.iterrows():
    current_points = row[circuit]
    driver_name = formulas.getLastName(row['Driver'])

    color = formulas.getDriverColor(row['Driver'], year)
    lineStyle = 'dotted' if color in existing_colors else 'solid'
    existing_colors.append(color)

    plt.plot(driverStandings_df.columns[1:], row[1:], label=f'{driver_name} - {current_points}', color=color,
             linestyle=lineStyle)

# print(existing_colors)

plt.title(f'Driver Championship after {circuit} {year} (Top {cant_drivers})')

plt.xlim(0, raceNumber)
plt.ylim(0, higherPoints + 4)

plt.locator_params(axis='y', nbins=20)
plt.legend(ncol=1, fontsize=13)
plt.gca().yaxis.tick_right()
plt.grid()

# Save the fig to a specific path
path = f'/Users/danielalas/Desktop/Personal/F1/Stats/{year}/{circuit}/driver_wc_points.png'
plt.savefig(path)

plt.show()