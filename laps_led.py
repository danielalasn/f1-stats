import formulas
import pandas as pd
import matplotlib.pyplot as plt

import main

year = 2023
raceNumber = 5

# Option 1: Specific Race
# Option 2: All races until 'raceNumber'
option = 2

# Output 1: Drivers
# Output 2: Constructors
output = 2

circuit = formulas.circuit_name(year, raceNumber)


# Gets the driver leader for each lap in one race
def specific_race(year, raceNumber):
    leading_drivers = []
    laps_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{raceNumber}/laps?limit=2000')
    laps = laps_soup.find_all('lap')
    for lap in laps:
        leading_driver = lap.find_all('timing')[0]['driverid']
        leading_drivers.append(leading_driver)
    return leading_drivers


# Gets the driver leader for all the races until the raceNumber
def all_season(year, last_race):
    leading_drivers = []
    for i in range(last_race):
        laps_soup = formulas.soup(f'http://ergast.com/api/f1/{year}/{i + 1}/laps?limit=2000')
        laps = laps_soup.find_all('lap')
        for lap in laps:
            leading_driver = lap.find_all('timing')[0]['driverid']
            leading_drivers.append(leading_driver)
    return leading_drivers

# Checks that the output is set correctly
if output == 1 or output == 2:
    # Checks the option (one race or multiple races) define the function to use and the title
    if option == 1:
        leading_drivers = specific_race(year, raceNumber)
        title = f"Number of Laps Led in {circuit} GP - {year}"
    elif option == 2:
        leading_drivers = all_season(year, raceNumber)
        title = f"Number of Laps Led after round {raceNumber} ({circuit} - {year})"
    else:
        print(
            f'{option} is not a valid option, change to: \nOption 1: Specific Race \nOption 2: All races before \'raceNumber\'')
        leading_drivers = []

    # If the option is 1 or 2, the df is created
    if leading_drivers:
        df = pd.DataFrame({'driver': leading_drivers})
        df['laps_led'] = df.groupby('driver')['driver'].transform('count')
        df = df.drop_duplicates().reset_index(drop=True)
        df = df.sort_values('laps_led', ascending=False)

        colors = []

        # Checks the desire output (1: driver, 2: constructor)
        if output == 1:
            # Driver
            if year == 2023:
                drivers_names = []
                for driver in df['driver']:
                    driver_name = main.driversId2023[driver]
                    constructor = formulas.getConstructor(driver, year)
                    colors.append(main.constructorColor2023[constructor])
                    drivers_names.append(driver_name)
                bars = plt.bar(drivers_names, df['laps_led'], color=colors)
            else:
                colors = ['gray', 'black']
                bars = plt.bar(df['driver'], df['laps_led'], color=colors)
            print(df)

        elif output == 2:
            # Driver
            for i in range(len(df['driver'])):
                driver = df['driver'][i]
                df['driver'][i] = formulas.getConstructor(driver, year)
            df = df.rename(columns={'driver': 'constructor'})
            df = df.groupby('constructor')['laps_led'].sum().reset_index()
            df = df.sort_values('laps_led', ascending=False)
            print(df)

            if year == 2023:
                for constructor in df['constructor']:
                    colors.append(main.constructorColor2023[constructor])
            else:
                colors = ['gray', 'black']
            bars = plt.bar(df['constructor'], df['laps_led'], color=colors)

        for bar in bars:
            height = bar.get_height()
            width = bar.get_width()
            x = bar.get_x()

            plt.text(x + width / 2, height, height,
                     ha='center', va='bottom')

        if output == 1: plt.xlabel('Driver')
        else: plt.xlabel('Constructor')

        plt.ylabel('Laps Led')
        plt.title(title)

        # Save the fig to a specific path
        path = f'/Users/danielalas/Desktop/Personal/F1/Stats/Miami/laps_led/{year}.png'
        plt.savefig(path)

        plt.show()

else:
    print(f'{output} is not an output option. Change to:\nOutput 1: Drivers\nOutput 2: Constructors')