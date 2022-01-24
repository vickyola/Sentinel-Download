from sentinelsat import SentinelAPI
from sentinelsat import read_geojson
from sentinelsat import geojson_to_wkt
import os

from zipfile import ZipFile

# enter username and pw here or set as variables in cli (see workflow)
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
    query = query[['title','beginposition','processinglevel','tileid', 'cloudcoverpercentage']] #what information will be in the Excelsheet
    query['tileid'].fillna((query['title'].str[39:44]), inplace=True) #get missing tileid from title
    query=query.sort_values(by='processinglevel', ascending=False)#sort! Level-2A will come first and will rather be downloaded
    query =query.drop_duplicates(subset=['beginposition', 'tileid'], keep='first')# dublicates will be removed 
    #query.to_excel('querydata.xlsx', sheet_name= str(year))  #creates Excelsheet
    return(query)

#download products and appends product name to list
def download_product(api, product, product_name_list, year):
    for index in product.index:
        product_name =  str(product['title'][index]) + '.zip' 
        if not os.path.exists(product_name ):#
            api.download_all(product.index, directory_path = '/work/wittekii/sentinel/' + year ) #set download directory to /work to avoid quota warnings
        product_name_list.append(product_name)
    
#extract images from product in new directory    
def extract_images(productname, year):
    for i in productname:
        directory_path = '/work/wittekii/sentinel/' + year +'/' + str(i)
        if os.path.exists(directory_path):
            archive = ZipFile(directory_path, 'r')#open ZipFile
            for file in archive.namelist():
                if 'IMG_DATA' in file:
                    archive.extract(file, '/work/wittekii/images/'+ year + '_Images')
    

def main():
    api = api_connect(API_USER, API_PASSWORD) 
    year  =  2021 #set year
    
    footprint = geojson_to_wkt(read_geojson(FOOTPRINT_PATH)) 
    product = querydata(api , footprint,(str(year)+'0101',str(year)+'1231'), year = str(year)) #querydata in excelshet
    product_name_list = list() 
    product_name = download_product(api, product,product_name_list, str(year)) 
    return(extract_images(product_name_list , str(year)))  
if __name__ == "__main__":
	main()
    

