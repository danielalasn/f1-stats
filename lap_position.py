import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

raceNumber = 4
year = 2023

drivers = ['perez', 'max_verstappen', 'leclerc', 'alonso', 'sainz',
           'hamilton','stroll','russell','norris','tsunoda']

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
print(results[0])

for driver in drivers:
    for result in results:
        if driver == result.find_all('driver')[0]['driverid']:
            startingPos = int(result.find_all('grid')[0].text)

            df_positions.loc[0, driver] = startingPos
            df_positions.loc[0, 'Lap'] = 0

# Define positions per lap
url_laps = f'http://ergast.com/api/f1/{year}/{raceNumber}/laps?limit=1000'
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

fig = plt.figure(figsize=(15, 8))

for driver in drivers:
    driverPos = str(df_positions[driver][nLaps])[:-2]
    plt.plot(df_positions[driver].round().astype('Int64'), label=f'{driver.title()} - {driverPos}')

plt.xlabel('Lap')
plt.ylabel('Position')
if year == 2023:
    plt.title(f'{locality} | Top 10 Drivers Lap Positions')
else:
    plt.title(f'Race #{raceNumber} | Top 10 Drivers Lap Positions')
plt.legend(ncol=5, fontsize="11", loc="upper right")

# Define the bins
plt.xlim(0, nLaps)
plt.locator_params(axis='x', nbins=nLaps)
plt.ylim(0,16)
plt.locator_params(axis='y', nbins=21)

plt.grid()
plt.gca().yaxis.tick_right()

plt.show()
