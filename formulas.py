import requests
from bs4 import BeautifulSoup

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

def getConstructor(driver,year):
    driverInfo = soup(f'https://ergast.com/api/f1/{year}/drivers/{driver}/constructors/')
    constructor = driverInfo.find_all('name')[0].text
    return constructor