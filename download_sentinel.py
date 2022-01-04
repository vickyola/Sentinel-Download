from sentinelsat import SentinelAPI, make_path_filter 
from sentinelsat import read_geojson
from sentinelsat import geojson_to_wkt
from datetime import date
import pandas as pd
import csv
import os
from os import path
from os import getenv
from zipfile import ZipFile

#run sentenv or enter username and pw here
API_USER = os.getenv('API_USER')
API_PASSWORD =  os.environ.get('API_PASSWORD')
#change path for files
#FOOTPRINT_PATH = 'C:\\Users\\wittekii\\Documents\GitHub\Sentinel-Download\dependencies\mulde.json'
FOOTPRINT_PATH = 'dependencies/mulde.json'
#FOOTPRINT_PATH = 'Sentinel-Download/dependencies/mulde.json'
#os.chdir("C:\\Users\\wittekii\\Documents\\GitHub")
#dire = "C:\\Users\\wittekii\\Documents\\GitHub"

def api_connect(user, pasw, scihuburl = 'https://scihub.copernicus.eu/dhus'):  
	api = SentinelAPI(user, pasw, scihuburl)
	return(api)

def querydata(api, footprint, date, year, platformname = 'Sentinel-2', cloudcoverpercentage = (0,20)): #100
    query = api.query(area = footprint,#area?
					  date = date,
					  platformname = platformname,
					  cloudcoverpercentage = cloudcoverpercentage)
    query = api.to_dataframe(query)
    query = query[['title','beginposition','processinglevel','tileid', 'cloudcoverpercentage']]#,'uuid']]
    query['tileid'].fillna((query['title'].str[39:44]), inplace=True) #get tileid 
    query=query.sort_values(by='processinglevel', ascending=False)
    query =query.drop_duplicates(subset=['beginposition', 'tileid'], keep='first')
    #query.to_excel('querydata.xlsx', sheet_name= str(year))
    return(query)

def first_product_inlist(df):
	df_sorted = df.head(2)
	return(df_sorted)

def download_product(api, product, year):
    path_filter = make_path_filter("*/IMG_DATA/*", exclude=False)  #only images
    api.download_all(product.index, directory_path = 'downloads/' + str(year), nodefilter=path_filter) #what mean .index?        
    

def main():
    api = api_connect(API_USER, API_PASSWORD) 
    year  =  2019
    footprint = geojson_to_wkt(read_geojson(FOOTPRINT_PATH)) 
    query= querydata(api , footprint,(str(year)+'0101',str(year)+'1231'), year = str(year)) #querydata in excelshet
    product= first_product_inlist(query)#weglassen wenn alle
    return(download_product(api, product, year) )#not a zip archive because oonly parts of the product
    
if __name__ == "__main__":
	main()
    
