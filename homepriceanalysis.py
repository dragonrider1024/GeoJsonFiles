import numpy as np
from urllib.parse import urlencode, quote_plus
import requests
from bs4 import BeautifulSoup
import csv
import collections

ZWSID = "X1-ZWz187zr42dpmz_93aho"

base_url = "https://www.zillow.com/webservice"
getSearchResults = "GetSearchResults.htm"
getDeepComps = "GetDeepComps.htm"
address = "17 Sunnyside Ave" #should be url encoded
citystatezip = "Burlington, MA" #shoulde be url encoded
rentzestimate = True

found = set([]) #hashset to store all the zpid of retrieved data

def GetSearchResults(zws_id:str,address:str, citystatezip:str, rentzestimate:bool)->str:
	parameters = {"address":address, "citystatezip":citystatezip}
	encoded = urlencode(parameters, quote_via = quote_plus)
	request_url = base_url + "/" + getSearchResults + "?" + "zws-id="+zws_id+"&"+encoded
	zpid = ""
	with requests.get(request_url) as resp:
		data = resp.content.decode('utf-8')
		soup = BeautifulSoup(data, 'xml')
		zpid = soup.find('zpid').text
	return zpid

def GetDeepComps(zws_id:str, zpid:str, count:int, rentzestimate:bool, csv_writer)->dict:
	found.add(zpid)
	queue = collections.deque()
	queue.append(zpid)
	while queue:
		zpid = queue.popleft()
		request_url = base_url + "/" + getDeepComps + "?" + "zws-id="+zws_id+"&"+"zpid="+zpid+"&count="+str(count)
		with requests.get(request_url) as resp:
			data = resp.content.decode('utf-8')
			soup = BeautifulSoup(data, 'xml')
			comparables = soup.find_all('comp')
			for comp in comparables:
				zpid = comp.find('zpid').text
				details = comp.find('homedetails').text
				taxassess = comp.find('taxAssessment').text if comp.find('taxAssessment') else np.nan
				taxassessmentyear = comp.find('taxAssessmentYear').text if comp.find('taxAssessmentYear') else np.nan
				yearbuild = comp.find('yearBuilt').text if comp.find('yearBuilt') else np.nan
				area = comp.find('finishedSqFt').text if comp.find('finishedSqFt') else np.nan
				lastsoldprice = comp.find('lastSoldPrice').text if comp.find('lastSoldPrice') else np.nan
				lastsolddate = comp.find('lastSoldDate').text if comp.find('lastSoldDate') else np.nan
				zestimate = comp.find('zestimate').find('amount').text
				link = comp.find('links').find('comparables').text
				street = comp.find('address').find('street').text
				city = comp.find('address').find('city').text
				state = comp.find('address').find('state').text
				zipcode = comp.find('address').find('zipcode').text
				bathrooms = comp.find('bathrooms').text if comp.find('bathrooms') else np.nan
				bedrooms = comp.find('bedrooms').text if comp.find('bedrooms') else np.nan
				totalrooms = comp.find('totalRooms').text if comp.find('totalRooms') else np.nan
				if zpid not in found:
					print(zpid, link, taxassess, lastsoldprice, zestimate, street, city, state, zipcode, lastsolddate, yearbuild, area, bathrooms, bedrooms, totalrooms)
					entry = [zpid, link, taxassess, lastsoldprice, zestimate, street, city, state, zipcode, lastsolddate, yearbuild, area, bathrooms, bedrooms, totalrooms]
					csv_writer.writerow(entry)
					found.add(zpid)
					if len(found) < 10000:
						queue.append(zpid)
					



		

if __name__ == "__main__":
	zpid = GetSearchResults(ZWSID, address, citystatezip, rentzestimate)
	with open('zillowdata.csv', 'w') as outputfile:
		csv_writer = csv.writer(outputfile, delimiter=',')
		header = ['zpid', 'link', 'taxassess', 'lastsoldprice', 'zestimate', 'street', 'city', 'state', 'zipcode', 'lastsolddate', 'yearbuild', 'area', 'bathrooms', 'bedrooms', 'totalrooms']
		csv_writer.writerow(header)
		GetDeepComps(ZWSID, zpid, 25, rentzestimate, csv_writer)


