import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import formulas
import main

raceNumber = 8
year = 2023
cant_drivers = 10

# define drivers
drivers = []

results_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{raceNumber}/results')
results = results_soup.find_all('result')

for i in range(cant_drivers):
    driverid = results[i].find_all('driver')[0]['driverid']
    drivers.append(driverid)
#-----

circuit = formulas.circuit_name(year,raceNumber)

df_positions = pd.DataFrame(columns=['Lap'])

# Define Starting Position
startingG_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{raceNumber}/results')
results = startingG_soup.find_all('result')

for driver in drivers:
    for result in results:
        if driver == result.find_all('driver')[0]['driverid']:
            startingPos = int(result.find_all('grid')[0].text)

            df_positions.loc[0, driver] = startingPos
            df_positions.loc[0, 'Lap'] = 0

# Define positions per lap
laps_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{raceNumber}/laps?limit=2000')
laps_data = laps_soup.find_all('lap')

nLaps = len(laps_data)

for i in range(nLaps):
    timings = laps_data[i].find_all('timing')
    for driver in drivers:
        for timing in timings:
            if timing['driverid'] == driver:
                lap = int(timing['lap'])
                position = timing['position']  # convert to float and then to int
                if position != 'NaN':
                    position = float(position)

                df_positions.loc[int(lap), driver] = position
                df_positions.loc[int(lap), 'Lap'] = lap

# print(df_positions)

fig = plt.figure(figsize=(15, 8))
existing_colors = []
for driver in drivers:
    driverPos = str(df_positions[driver][nLaps])[:-2]

    driver_name = formulas.getLastName(driver)
    color = formulas.getDriverColor(driver,year)
    lineStyle = 'dotted' if color in existing_colors else 'solid'
    existing_colors.append(color)

    plt.plot(df_positions[driver].round().astype('Int64'), label=f'{driver_name} - {driverPos}', color=color,
             linestyle=lineStyle)

plt.xlabel('Lap')
plt.ylabel('Position')

plt.title(f'{circuit} {year} | Top {cant_drivers} Drivers Lap Positions')
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
path = f'/Users/danielalas/Desktop/Personal/F1/Stats/{circuit}/lap_position.png'
plt.savefig(path)

plt.show()

