import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import datetime as dt

raceNumber = 4
drivers = ['perez', 'leclerc']
year = 2023

circuit_url = f'http://ergast.com/api/f1/{year}/{raceNumber}/circuits'
circuit_html = requests.get(circuit_url).text
circuit_soup = BeautifulSoup(circuit_html)
locality = circuit_soup.find_all('locality')[0].text
if locality == 'Sakhir':
    locality = 'Bahrain'

url_laps = f'http://ergast.com/api/f1/2023/{raceNumber}/laps?limit=1000'
laps_html = requests.get(url_laps).text
laps_soup = BeautifulSoup(laps_html)

df_times = pd.DataFrame(columns=['Lap'])

laps_data = laps_soup.find_all('lap')
nLaps = len(laps_data)

for i in range(nLaps):
    timings = laps_data[i].find_all('timing')
    for driver in drivers:
        for timing in timings:
            if timing['driverid'] == driver:
                lap = int(timing['lap'])
                time = datetime.strptime(timing['time'], "%M:%S.%f").strftime("%M:%S.%f")
                df_times.loc[int(lap) - 1, driver] = time
                df_times.loc[int(lap) - 1, 'Lap'] = lap
print(df_times)

# -------Graph
fig, lapTimeGraph = plt.subplots(figsize=(10, 5))


lapTimeGraph.set_xlim(1, nLaps)
lapTimeGraph.locator_params(axis='x', nbins=nLaps / 2)

lapTimeGraph.locator_params(axis='y', nbins=15)

for driver in drivers:
    df_times[driver] = df_times[driver].apply(lambda x: dt.datetime.strptime(x, '%M:%S.%f').time())
    df_times[driver] = df_times[driver].apply(lambda x: (x.minute * 60 + x.second + x.microsecond / 1000000) / 60)

lapTimeGraph.plot(df_times['Lap'], df_times[drivers[0]], label=drivers[0], color='#1f77b4')
lapTimeGraph.plot(df_times['Lap'], df_times[drivers[1]], label=drivers[1], color='#d62728')

lapTimeGraph.set_xlabel('Lap')
lapTimeGraph.set_ylabel('Time (Minutes:Seconds)')
lapTimeGraph.set_title(f'Best Red Bull vs Best Ferrari {locality} Lap Times')

def format_time(x, pos):
    d = dt.datetime(1, 1, 1) + dt.timedelta(seconds=x * 60)
    return d.strftime("%M:%S")


lapTimeGraph.yaxis.set_major_formatter(plt.FuncFormatter(format_time))

lapTimeGraph.legend(fontsize="15", loc="upper right")

lapTimeGraph.grid()

plt.show()
