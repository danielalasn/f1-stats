import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt

opcion = 1
if opcion == 1:
    #Specific Race results
    raceNumber = 1
    year = 2023
elif opcion == 2:
    #Last Race results:
    raceNumber = "last"
    year = "current"
else:
    print("No es una opcion")

#Compare only 2 drivers
drivers = ['russell','alonso']


if len(drivers)!=2:
    print("Compare 2 Drivers")
else:
    circuit_url = f'http://ergast.com/api/f1/{year}/{raceNumber}/circuits'
    circuit_html = requests.get(circuit_url).text
    circuit_soup = BeautifulSoup(circuit_html)
    locality = circuit_soup.find_all('locality')[0].text
    if locality == 'Sakhir':
        locality = 'Bahrain'

    url_laps = f'http://ergast.com/api/f1/{year}/{raceNumber}/laps?limit=1000'
    laps_html= requests.get(url_laps).text
    laps_soup = BeautifulSoup(laps_html)

    df_times = pd.DataFrame(columns = ['lap'])

    laps_data = laps_soup.find_all('lap')
    nLaps = len(laps_data)
    print(nLaps)


    for i in range(nLaps):
        timings = laps_data[i].find_all('timing')
        for driver in drivers:
            for timing in timings:
                if timing['driverid'] == driver:
                    lap = int(timing['lap'])
                    time = datetime.strptime(timing['time'], "%M:%S.%f").strftime("%M:%S.%f")
                    df_times.loc[int(lap)-1, driver] = time
                    df_times.loc[int(lap)-1, 'lap'] = lap


    df_times['difference'] = pd.to_datetime(df_times[drivers[0]], format="%M:%S.%f") - pd.to_datetime(df_times[drivers[1]], format="%M:%S.%f")

    df_times['difference'] = df_times['difference'].dt.total_seconds()

    df_times['cumulative'] = df_times['difference'].cumsum()

    startingRow = pd.DataFrame({'lap': [0], 'cumulative': [0]}, index=[0])
    cumulative_df = df_times[['lap', 'cumulative']].copy()

    cumulative_df = pd.concat([startingRow, cumulative_df]).reset_index(drop=True)

    nLaps = max(cumulative_df['lap'])

    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_df['lap'], cumulative_df['cumulative'], label=drivers[1])
    plt.axhline(0, color='red', linestyle='--', label=drivers[0])

    plt.xlim(0, nLaps)
    plt.xticks(np.arange(0, nLaps+1, 5))

    plt.xlabel('Lap')
    plt.ylabel('Time Interval (seconds)')
    plt.title(f'Time Interval between {drivers[0].capitalize()} and {drivers[1].capitalize()} - {locality}')
    plt.legend(fontsize=15)
    plt.grid(True)
    plt.show()