import fastf1 as ff1
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

import formulas

year = 2023
raceNumber = 10

circuit = formulas.circuit_name(year,raceNumber)

finishStats_soup = formulas.soup(f"http://ergast.com/api/f1/{year}/{raceNumber}/results")
results = finishStats_soup.find_all('result')

for result in results:
    rank = result.find_all('fastestlap')[0]['rank']
    if rank == "1":
        driver = result.find_all('driver')[0]['code']

colormap = mpl.cm.plasma

session = ff1.get_session(year, raceNumber, 'R')
weekend = session.event
session.load()
lap = session.laps.pick_driver(driver).pick_fastest()

x = lap.telemetry['X']
y = lap.telemetry['Y']
color = lap.telemetry['Speed']

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

fastestTime = str(lap.LapTime)[10:19]

fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle(f'{circuit} Fastest Lap Speed - {driver} ({fastestTime})', size=24, y=0.97)

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')


ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

norm = plt.Normalize(color.min(), color.max())
lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)

lc.set_array(color)

line = ax.add_collection(lc)


cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")

# Save the fig to a specific path
path = f'/Users/danielalas/Desktop/Personal/F1/Stats/{year}/{circuit}/fastest_lap_map.png'
plt.savefig(path)

plt.show()