#!/usr/bin/python3

import requests
import datetime
from bs4 import BeautifulSoup

def get_station_id(station_name):
  url = 'http://webapps.marine.ie/IrishTidesChartingApplication/TidePredictions.aspx'
  rep = requests.get(url)
  soup = BeautifulSoup(rep.text, features='html.parser')
  form = soup.find('form')
  opts = form.find_all('option')
  stations = {}
  for o in opts:
    stations[o.text] = o['value']
  return stations.get(station_name, None)


def get_tide_table(station, dt):

  url = 'http://webapps.marine.ie/IrishTidesChartingApplication/TidePredictions.aspx'
  rep = requests.get(url)

  soup = BeautifulSoup(rep.text, features='html.parser')
  form = soup.find('form')
  inputs = form.find_all('input')

  post_data = {}

  for i in inputs:
    post_data[i['name']] = i['value']

  post_data['lstSites'] = station
  #post_data['SelectedDateTime'] = '01/02/2021'
  post_data['SelectedDateTime'] = '%s/%s/%s' % (dt.day, dt.month, dt.year)

  rep = requests.post(url, data=post_data)

  soup = BeautifulSoup(rep.text, features='html.parser')

  dp = soup.find(id='DataPanel')

  d_tbl = dp.find('table')

  d_rows = d_tbl.find_all('tr')

  data = {}

  for row in d_rows:
    d_td = row.find_all('td')
    if d_td:
      data[d_td[0].text] = d_td[1].text

  return data

def main():

  STATION = 'Dublin Port'
  YEAR = 2021

  station_id = get_station_id('Dublin Port')
  req_date = datetime.date(YEAR, 1, 1)
  sixdays = datetime.timedelta(days=6)

  print('datetime,tidelevel')
  while req_date.year == YEAR:
    tides = get_tide_table(station_id, req_date)
    req_date = req_date + sixdays
    for d in tides:
      print('%s,%s' % (d, tides[d]))

main()
