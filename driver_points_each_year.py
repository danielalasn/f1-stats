import formulas
import pandas as pd
import matplotlib.pyplot as plt

startYear = 2020
endYear = 2023
raceNumber = 17
driver = "norris"

cantYears = endYear - startYear +1
df_data = []
colors = []

for i in range(cantYears):
    year = startYear+i
    driversStandings = formulas.soup(f"http://ergast.com/api/f1/{year}/{raceNumber}/driverStandings").find_all("driverstanding")

    for driverStanding in driversStandings:
        driverId = driverStanding.find_all('driver')[0]['driverid']
        if driverId == driver:
            points = float(driverStanding["points"])
            constructor = formulas.getConstructor(driver,year)
            df_data.append({"year": year, "points": points, "constructor": constructor})
            colors.append(formulas.getConstructorColor(constructor,year))


df = pd.DataFrame(df_data)
df['points'] = df['points'].astype(int)

# Bar Graph
bars = plt.bar(df["year"], df["points"],color=colors)
for bar in bars:
    height = bar.get_height()
    width = bar.get_width()
    x = bar.get_x()
    plt.text(x + width / 2, height, height, ha='center', va='bottom')

plt.xlabel("Year")
plt.ylabel("Points")
driverName = formulas.getLastName(driver)
plt.suptitle(f"{driverName} points after first {raceNumber} rounds")
plt.title(f"{startYear} - {endYear}")
plt.xticks(df["year"])

plt.show()
