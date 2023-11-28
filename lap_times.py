import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import datetime as dt

from matplotlib.ticker import MultipleLocator

import formulas
import main

raceNumber = 21

drivers = ['leclerc', 'perez']
year = 2023

circuit = formulas.circuit_name(year,raceNumber)

laps_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{raceNumber}/laps?limit=2000')

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

# -------Graph
fig, lapTimeGraph = plt.subplots(figsize=(10, 5))

lapTimeGraph.set_xlim(1, nLaps)
x_major_locator = MultipleLocator(5)
lapTimeGraph.xaxis.set_major_locator(x_major_locator)

for driver in drivers:
    df_times[driver] = df_times[driver].apply(lambda x: dt.datetime.strptime(x, '%M:%S.%f').time())
    df_times[driver] = df_times[driver].apply(lambda x: (x.minute * 60 + x.second + x.microsecond / 1000000) / 60)

color1 = formulas.getDriverColor(drivers[0],year)
color2 = formulas.getDriverColor(drivers[1],year)

lapTimeGraph.plot(df_times['Lap'], df_times[drivers[0]], label=drivers[0], color=color1, linestyle = 'solid')
lapTimeGraph.plot(df_times['Lap'], df_times[drivers[1]], label=drivers[1], color=color2,
                  linestyle='dotted' if color1 == color2 else 'solid')

lapTimeGraph.set_xlabel('Lap')
lapTimeGraph.set_ylabel('Time (Minutes:Seconds)')
lapTimeGraph.set_title(f'{formulas.getLastName(drivers[0])} vs {formulas.getLastName(drivers[1])}\
 Lap Times - {circuit} {year}')


def format_time(x, pos):
    d = dt.datetime(1, 1, 1) + dt.timedelta(seconds=x * 60)
    return d.strftime("%M:%S")


lapTimeGraph.yaxis.set_major_formatter(plt.FuncFormatter(format_time))

lapTimeGraph.legend(fontsize="15", loc="upper left")
lapTimeGraph.grid()

# Save the fig to a specific path
# path = '/Users/danielalas/Desktop/Personal/F1/Stats/Miami/lap_times.png'
# plt.savefig(path)

plt.show()
