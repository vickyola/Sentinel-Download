from sentinelsat import SentinelAPI, make_path_filter 
from sentinelsat import read_geojson
from sentinelsat import geojson_to_wkt
from datetime import date
import pandas as pd
import csv
from zipfile import ZipFile
import os

#run sentenv or enter username and pw here
API_USER = os.getenv('API_USER')
API_PASSWORD =  os.environ.get('API_PASSWORD')
#change path for files
#os.chdir("C:\\Users\\wittekii\\Documents\\GitHub")
#FOOTPRINT_PATH = 'dependencies/mulde.json'
#FOOTPRINT_PATH = 'Sentinel-Download/dependencies/mulde.json'
FOOTPRINT_PATH = 'C:\\Users\\wittekii\\Documents\GitHub\Sentinel-Download\dependencies\mulde.json'

os.chdir("C:\\Users\\wittekii\\Documents\\GitHub")

def api_connect(user, pasw, scihuburl = 'https://scihub.copernicus.eu/dhus'):  #/apihub/   /dhus
	api = SentinelAPI(user, pasw, scihuburl)
	return(api)


#put some querydata in Excelsheet (for a year) 
def querydata(api, footprint, date,year, platformname = 'Sentinel-2', cloudcoverpercentage = (0,20)): #100
    query = api.query(area = footprint,#area?
					  date = date,
					  platformname = platformname,
					  cloudcoverpercentage = cloudcoverpercentage)

    query = api.to_dataframe(query)
    query = query.sort_values(['cloudcoverpercentage'], ascending=[True])
    query =query[['title','beginposition','processinglevel','tileid', 'cloudcoverpercentage']]#,'uuid']]
    query['tileid'].fillna((query['title'].str[39:44]), inplace=True) #get tileid from title
    query=query.sort_values(by='processinglevel', ascending=False)
    query =query.drop_duplicates(subset=['beginposition', 'tileid'], keep='first')
    query.to_excel('querydata.xlsx', sheet_name= str(year))
    return(query)



def datainfo(api,product):
    dicto = dict()
    for i in range(0,len(product)):
        odata = api.get_product_odata(product['uuid'][i],full= True)
        #'''
        for key in odata:
            if key not in dicto:
                dicto[key] = odata[key]
            elif type(dicto[key]) == list:#check whether it already exist 
                dicto[key].append(odata[key])
            else:
                dicto[key] = [dicto[key],odata[key]] #create new entry
    df = pd.DataFrame(data=dicto)#, index=[0])
    df = (df.T)
    df.to_excel('dicto.xlsx')#,  sheet_name =datename )
  #  '''
    return(odata)

#'''   
# Checks if compressed product exists. 
# If not, downloads it. 
# Returns name of file.

def first_product_inlist(df):
	df_sorted = df.head(1)
	return(df_sorted)

def download_product(api, product):
    product_name = str(product['title'][0]) + '.zip'    
    #here path filter- check whether it work for Sentinel2!!
    path_filter = make_path_filter("*TCI*", exclude=False)
    #api.download_all(<products>, nodefilter=path_filter)
    if not os.path.exists(product_name):#.os
        api.download_all(product.index, nodefilter=path_filter) #what mean .index?        
    return(product_name)
    
 #   '''

def main():
    api = api_connect(API_USER, API_PASSWORD) 
    year  =  2020
    footprint = geojson_to_wkt(read_geojson(FOOTPRINT_PATH)) 
    query= querydata(api , footprint,(str(year)+'0101',str(year)+'1231'), year = str(year)) #querydata in excelshet
    product= first_product_inlist(query)
    product_name = download_product(api, product) #
    zipfile = ZipFile(product_name, 'r')    
    zipfile.extractall(r'data_sentinel')
    zipfile.close()
if __name__ == "__main__":
	main()
    
