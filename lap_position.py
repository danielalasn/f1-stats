import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import main

raceNumber = 5
year = 2023
cant_drivers = 10

#define drivers
drivers = []
results_url = f'http://ergast.com/api/f1/{year}/{raceNumber}/results'
results_html = requests.get(results_url).text
results_soup = BeautifulSoup(results_html)
results = results_soup.find_all('result')
for i in range(cant_drivers):
    driverid = results[i].find_all('driver')[0]['driverid']
    drivers.append(driverid)
#-----

circuit_url = f'http://ergast.com/api/f1/{year}/{raceNumber}/circuits'
circuit_html = requests.get(circuit_url).text
circuit_soup = BeautifulSoup(circuit_html)
locality = circuit_soup.find_all('locality')[0].text
if locality == 'Sakhir':
    locality = 'Bahrain'

df_positions = pd.DataFrame(columns=['Lap'])

# Define Starting Position
startingG_url = f'http://ergast.com/api/f1/{year}/{raceNumber}/results'
startingG_html = requests.get(startingG_url).text
startingG_soup = BeautifulSoup(startingG_html)

results = startingG_soup.find_all('result')

for driver in drivers:
    for result in results:
        if driver == result.find_all('driver')[0]['driverid']:
            startingPos = int(result.find_all('grid')[0].text)

            df_positions.loc[0, driver] = startingPos
            df_positions.loc[0, 'Lap'] = 0

# Define positions per lap
url_laps = f'http://ergast.com/api/f1/{year}/{raceNumber}/laps?limit=2000'
laps_html = requests.get(url_laps).text
laps_soup = BeautifulSoup(laps_html)
laps_data = laps_soup.find_all('lap')

nLaps = len(laps_data)

for i in range(nLaps):
    timings = laps_data[i].find_all('timing')
    for driver in drivers:
        for timing in timings:
            if timing['driverid'] == driver:
                lap = int(timing['lap'])
                position = int(float(timing['position']))  # convert to float and then to int

                df_positions.loc[int(lap), driver] = position
                df_positions.loc[int(lap), 'Lap'] = lap

#thee is an error in http://ergast.com/api/f1/2023/5/results, max grid start is 0
df_positions['max_verstappen'][0] = 9.0

fig = plt.figure(figsize=(15, 8))
existing_colors = []
for driver in drivers:
    driverPos = str(df_positions[driver][nLaps])[:-2]
    if year == 2023:
        driver_name = main.driversId2023[driver]
        color = main.driverColor2023[driver_name]
        if color in existing_colors:
            linestyle = 'dotted'
        else:
            existing_colors.append(color)
            linestyle = 'solid'

        plt.plot(df_positions[driver].round().astype('Int64'), label=f'{driver_name} - {driverPos}', color=color,
                 linestyle=linestyle)

    else:
        plt.plot(df_positions[driver].round().astype('Int64'), label=f'{driver} - {driverPos}')



plt.xlabel('Lap')
plt.ylabel('Position')

plt.title(f'{locality} | Top {cant_drivers} Drivers Lap Positions')
plt.legend(ncol=5, fontsize="11", loc="upper center")

# Define the bins
plt.xlim(0, nLaps)
x_locator = MultipleLocator(5)
plt.gca().xaxis.set_major_locator(x_locator)

plt.ylim(0,20)
plt.locator_params(axis='y', nbins=21)

plt.grid()
plt.gca().yaxis.tick_right()

# Save the fig to a specific path
path = '/Users/danielalas/Desktop/Personal/F1/Stats/Miami/lap_position.png'
# plt.savefig(path)

plt.show()

