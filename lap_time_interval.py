import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

import formulas
import main

# Specific Race
raceNumber = 8
year = 2023

# Compare only 2 drivers
drivers = ['max_verstappen', 'alonso']

if len(drivers) != 2:
    print("Compare 2 Drivers")
else:
    circuit = formulas.circuit_name(year,raceNumber)

    laps_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{raceNumber}/laps?limit=2000')

    df_times = pd.DataFrame(columns=['lap'])
    laps_data = laps_soup.find_all('lap')
    nLaps = len(laps_data)

    position2 = 0

    for i in range(nLaps):
        timings = laps_data[i].find_all('timing')

        for driver in drivers:
            for timing in timings:
                if timing['driverid'] == driver:
                    lap = int(timing['lap'])
                    time = datetime.strptime(timing['time'], "%M:%S.%f").strftime("%M:%S.%f")
                    df_times.loc[int(lap) - 1, driver] = time
                    df_times.loc[int(lap) - 1, 'lap'] = lap

                    position1 = position2
                    position2 = timing['position']

    df_times['difference'] = pd.to_datetime(df_times[drivers[1]], format="%M:%S.%f") - pd.to_datetime(
        df_times[drivers[0]], format="%M:%S.%f")

    df_times['difference'] = df_times['difference'].dt.total_seconds()

    df_times['cumulative'] = df_times['difference'].cumsum()

    cumulative_df = df_times[['lap', 'cumulative']].copy()

    nLaps = max(cumulative_df['lap'])
    plt.figure(figsize=(10, 6))

    driver1 = formulas.getLastName(drivers[0])
    constructor1 = formulas.getConstructor(drivers[0],year)
    driver2 = formulas.getLastName(drivers[1])
    constructor2 = formulas.getConstructor(drivers[1], year)

    plt.plot(cumulative_df['lap'], cumulative_df['cumulative'], label=driver2,
             color=formulas.getConstructorColor(constructor2,year))
    plt.axhline(0, color=formulas.getConstructorColor(constructor1,year), linestyle='--', label=driver1)

    plt.xlim(1, nLaps)
    plt.xticks(np.arange(0, nLaps + 1, 5))

    plt.xlabel('Lap')
    plt.ylabel('Time Interval (seconds)')
    plt.title(f'Time Interval between {driver1}({position1}) and {driver2}({position2}) - {circuit} {year}')
    plt.legend(fontsize=15)
    plt.grid(True)

    # Save the fig to a specific path
    path = f'/Users/danielalas/Desktop/Personal/F1/Stats/{circuit}/lap_time_interval.png'
    plt.savefig(path)

    plt.show()
