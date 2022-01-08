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
	df_sorted = df.head(1)
	return(df_sorted)

def download_product(api, product, year):
    product_name =  str(product['title'][0]) + '.zip'  #'downloads/' + str(year) +'/'+
    #print(product_name )
    if not os.path.exists(product_name ):#.os
        api.download_all(product.index, directory_path = 'downloads/' + year ) #what mean .index?
   
    return(product_name)

def extract_images(productname, year):
    directory_path = 'downloads/' + year +'/' + productname 
    archive = ZipFile(directory_path, 'r')
    
   # print(archive.namelist())
    for file in archive.namelist():
        if 'IMG_DATA' in file:
           # print(file)
            archive.extract(file, year + '_Images')

def main():
    api = api_connect(API_USER, API_PASSWORD) 
    year  =  2016
    
    footprint = geojson_to_wkt(read_geojson(FOOTPRINT_PATH)) 
    query= querydata(api , footprint,(str(year)+'0101',str(year)+'1231'), year = str(year)) #querydata in excelshet
    #product= first_product_inlist(query)#weglassen wenn alle
    product_name = download_product(api, query, str(year)) #just table in zipfile not downlload to see how many pictures
    return(extract_images(product_name , str(year)))
    #zipfile = ZipFile(product_name, 'r')    
   # zipfile.extractall(r'data_sentinel')
    #zipfile.close()    
if __name__ == "__main__":
	main()
    


#todo check whether zip is working
#download whole product 
#unpack?
#extract images with glob
