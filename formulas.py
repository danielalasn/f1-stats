import requests
from bs4 import BeautifulSoup
import main

def soup(link):
    url = link
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    return soup

def circuit_name(year,raceNumber):
    circuits = soup(f'http://ergast.com/api/f1/{year}/{raceNumber}/circuits')
    country = circuits.find_all('country')[0].text
    if country == "USA":
        country = circuits.find_all('locality')[0].text
    return country

def getConstructor(driverid,year):
    driverInfo = soup(f'https://ergast.com/api/f1/{year}/drivers/{driverid}/constructors/')
    constructor = driverInfo.find_all('name')[0].text
    return constructor

def getLastName(driver):
    driverInfo = soup(f'http://ergast.com/api/f1/drivers/{driver}')
    last_name = driverInfo.familyname.text
    return last_name

def getDriverColor(driverId,year):
    constructor = getConstructor(driverId, year)
    if constructor in main.constructorColors:
        color = main.constructorColors[constructor]
    else:
        color = '#5A646D'
    return color

def getConstructorColor(constructor,year):
    if constructor in main.constructorColors:
        color = main.constructorColors[constructor]
    else:
        color = '#5A646D'
    return color