import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt

import main

# Specific Race
raceNumber = 5
year = 2023

# Compare only 2 drivers
drivers = ['max_verstappen', 'alonso']

if len(drivers) != 2:
    print("Compare 2 Drivers")
else:
    circuit_url = f'http://ergast.com/api/f1/{year}/{raceNumber}/circuits'
    circuit_html = requests.get(circuit_url).text
    circuit_soup = BeautifulSoup(circuit_html)
    locality = circuit_soup.find_all('circuitname')[0].text

    url_laps = f'http://ergast.com/api/f1/{year}/{raceNumber}/laps?limit=2000'
    laps_html = requests.get(url_laps).text
    laps_soup = BeautifulSoup(laps_html)

    df_times = pd.DataFrame(columns=['lap'])

    laps_data = laps_soup.find_all('lap')
    nLaps = len(laps_data)

    position2 = 0

    for i in range(nLaps):
        timings = laps_data[i].find_all('timing')

        for driver in drivers:
            for timing in timings:
                if timing['driverid'] == driver:
                    print(timing)
                    lap = int(timing['lap'])
                    time = datetime.strptime(timing['time'], "%M:%S.%f").strftime("%M:%S.%f")
                    df_times.loc[int(lap) - 1, driver] = time
                    df_times.loc[int(lap) - 1, 'lap'] = lap

                    position1 = position2
                    position2 = timing['position']

    df_times['difference'] = pd.to_datetime(df_times[drivers[0]], format="%M:%S.%f") - pd.to_datetime(
        df_times[drivers[1]], format="%M:%S.%f")

    df_times['difference'] = df_times['difference'].dt.total_seconds()

    df_times['cumulative'] = df_times['difference'].cumsum()

    cumulative_df = df_times[['lap', 'cumulative']].copy()

    nLaps = max(cumulative_df['lap'])
    plt.figure(figsize=(10, 6))

    driver1 = main.driversId2023[drivers[0]]
    driver2 = main.driversId2023[drivers[1]]

    plt.plot(cumulative_df['lap'], cumulative_df['cumulative'], label=driver2, color=main.driverColor2023[driver2] if year == 2023 else 'blue')
    plt.axhline(0, color=main.driverColor2023[driver1] if year == 2023 else 'red', linestyle='--', label=driver1)

    plt.xlim(1, nLaps)
    plt.xticks(np.arange(0, nLaps + 1, 5))

    plt.xlabel('Lap')
    plt.ylabel('Time Interval (seconds)')
    plt.title(f'Time Interval between {driver1}({position1}) and {driver2}({position2}) - {locality}')
    plt.legend(fontsize=15)
    plt.grid(True)

    # Save the fig to a specific path
    path = '/Users/danielalas/Desktop/Personal/F1/Stats/Miami/lap_time_interval.png'
    # plt.savefig(path)

    plt.show()
