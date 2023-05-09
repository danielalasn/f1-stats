import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import main

# --------------Changes:
raceNumber = 5
year = 2023
cant_drivers = 10
# ---------------

driverStandings_df = pd.DataFrame(columns=['Driver', 'Start'])

url_laps = f'http://ergast.com/api/f1/{year}/{raceNumber}/driverStandings'
points_html = requests.get(url_laps).text
points_soup = BeautifulSoup(points_html)
driverStandings = points_soup.find_all('driverstanding')

for driverStanding in driverStandings:
    driver = driverStanding.find_all('driver')[0]['driverid']
    driverStandings_df = driverStandings_df.append({'Driver': driver, 'Start': 0}, ignore_index=True)

for i in range(raceNumber):
    circuit_url = f'http://ergast.com/api/f1/{year}/{i + 1}/circuits'
    circuit_html = requests.get(circuit_url).text
    circuit_soup = BeautifulSoup(circuit_html)
    locality = circuit_soup.find_all('locality')[0].text
    if locality == 'Sakhir':
        locality = 'Bahrain'

    url_laps = f'http://ergast.com/api/f1/{year}/{i + 1}/driverStandings'
    points_html = requests.get(url_laps).text
    points_soup = BeautifulSoup(points_html)
    driverStandings = points_soup.find_all('driverstanding')

    for driverStanding in driverStandings:
        points = driverStanding['points']
        driver = driverStanding.find_all('driver')[0]['driverid']
        driverStandings_df.loc[driverStandings_df['Driver'] == driver, locality] = points

driverStandings_df = driverStandings_df[:cant_drivers]
print(driverStandings_df)

higherPoints = int(driverStandings_df[locality][0])

fig = plt.figure(figsize=(11, 8))

existing_colors = []

for index, row in driverStandings_df.iterrows():
    current_points = row[locality]

    if year == 2023:
        driver_name = main.driversId2023[row['Driver']]
        color = main.driverColor2023[driver_name]
        if color in existing_colors:
            linestyle = 'dotted'
        else:
            existing_colors.append(color)
            linestyle = 'solid'

        plt.plot(driverStandings_df.columns[1:], row[1:], label=f'{driver_name} - {current_points}', color=color,
                 linestyle=linestyle)
    else:
        driver_name = row['Driver']
        plt.plot(driverStandings_df.columns[1:], row[1:], label=f'{driver_name} - {current_points}')

print(existing_colors)

plt.title(f'Driver Championship after {locality} {year} (Top {cant_drivers})')

plt.xlim(0, raceNumber)
plt.ylim(0, higherPoints + 4)

plt.locator_params(axis='y', nbins=20)
plt.legend(ncol=1, fontsize=13)
plt.gca().yaxis.tick_right()
plt.grid()

# Save the fig to a specific path
path = '/Users/danielalas/Desktop/Personal/F1/Stats/Miami/driver_wc_points.png'
# plt.savefig(path)

plt.show()