from sentinelsat import SentinelAPI
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

FOOTPRINT_PATH = 'mulde.json'


def api_connect(user, pasw, scihuburl = 'https://scihub.copernicus.eu/dhus'):  #/apihub/   /dhus
	api = SentinelAPI(user, pasw, scihuburl)
	return(api)

def api_query(api, footprint, date, platformname = 'Sentinel-2', cloudcoverpercentage = (0,20)): #100
    query = api.query(area = footprint,#area?
					  date = date,
					  platformname = platformname,
					  cloudcoverpercentage = cloudcoverpercentage)
    query =api.to_dataframe(query)
  #  query = query[['title','beginposition','processinglevel','tileid','size', 'cloudcoverpercentage','uuid']]
    return(query)


	
#  sort values and takes latest???
def sort_product(df):
    df_sorted = df.sort_values(['cloudcoverpercentage'], ascending=[True])#was bedeuted das? ingestiondate = Aufnahmedatum
   # df_sorted = df_sorted.head(1)  #head(1)  erste Reihe?
    return(df_sorted)





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
    
    query.to_excel('querydata.xlsx', sheet_name= str(year))
    #return(query)
    return(query)


def name_product(api, product):
    data_list= list()
    #for i in range(0,len(product.index)):
    for i in range(0,len(product)):
        product_name = str(product['title'][i])# + '.zip'
        data_list.append(product_name)
   
       # api.is_online(product_name)   
    return(data_list)
    
         
    
    
def datainfo(api,product):
    dicto = dict()
  #  key = ['title','beginposition','producttype','processinglevel','tileid','size']
    
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
def download_product(api, product):
    product_name = str(product['title'][0]) + '.zip'
    if not os.path.exists(product_name):#.os
        api.download_all(product.index) #what mean .index?
    return(product_name)
    
 #   '''
#number of products
def product_num(api, footprint, date, platformname = 'Sentinel-2', cloudcoverpercentage = (0,20)):
    coun = api.count(area = footprint,#area?
					  date = date,
					  platformname = platformname,
					  cloudcoverpercentage = cloudcoverpercentage)
    print(coun)
   
    
    
def main():
    api = api_connect(API_USER, API_PASSWORD)  #/apihub/   /dhus
    year  =  2020
    
    
    footprint = geojson_to_wkt(read_geojson(FOOTPRINT_PATH)) 
   
  # products = api_query(api , footprint,(str(year)+'0101',str(year)+'1231') )
   # product= sort_product(products)
       
    
    #number of productin in timespan
    product_num(api , footprint,  (str(year)+'0101',str(year)+'1231') )
     
     # -> df of products 
    
   # print(   name_product(api, product))
    #attributes for filtering
   
    
    
    query= querydata(api , footprint,(str(year)+'0101',str(year)+'1231'), year = str(year)) #querydata in excelshet
    
    
    #overview:
    # odata =datainfo(api,product)  #odata of product as excelsheet dicto
    
    #print(list(odata.keys()))
   
     
   # print(list(product.keys()))   #for filtering? put in list?
''' 
   product_name = download_product(api, product) #just table in zipfile not downlload to see how many pictures
    zipfile = ZipFile(product_name, 'r')    
    zipfile.extractall(r'data_sentinel')
    zipfile.close()
'''
if __name__ == "__main__":
	main()
    
