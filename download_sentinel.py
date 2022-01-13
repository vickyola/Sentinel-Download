from sentinelsat import SentinelAPI, make_path_filter 
from sentinelsat import read_geojson
from sentinelsat import geojson_to_wkt
#import pandas as pd
import os
import glob
#from os import path
#from os import getenv
from zipfile import ZipFile

#run sentenv or enter username and pw here
API_USER = os.getenv('API_USER')
API_PASSWORD =  os.environ.get('API_PASSWORD')
FOOTPRINT_PATH = 'dependencies/mulde.json'


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

def download_product(api, product, product_name_list, year):
    for index in product.index:
        product_name =  str(product['title'][index]) + '.zip' 
        if not os.path.exists(product_name ):#.os 
            api.download_all(product.index, directory_path = '/work/wittekii/sentinel/' + year ) 
        product_name_list.append(product_name)
    
    
def extract_images(productname, year):
    #productname =  str(product['title'][0]) + '.zip'  #'downloads/' + str(year) +'/'+
    for i in productname:
        directory_path = '/work/wittekii/sentinel/' + year +'/' + str(i)
        #directory_path = 'downloads/' + year +'/' + str(i)
        archive = ZipFile(directory_path, 'r')#open ZipFile
        for file in archive.namelist():
            if 'IMG_DATA' in file:
                archive.extract(file, '/work/wittekii/images/'+ year + '_Images')
    

def main():
    api = api_connect(API_USER, API_PASSWORD) 
    year  =  2017
    
    footprint = geojson_to_wkt(read_geojson(FOOTPRINT_PATH)) 
    product = querydata(api , footprint,(str(year)+'0101',str(year)+'1231'), year = str(year)) #querydata in excelshet
    #product = first_product_inlist(query)#dont use if all and change query to product
    product_name_list = list()
    product_name = download_product(api, product,product_name_list, str(year)) #just table in zipfile not downlload to see how many pictures

    return(extract_images(product_name_list , str(year)))  #das geht irgendwie nicht, wird nur eins extrahiert kp warum
if __name__ == "__main__":
	main()
    

