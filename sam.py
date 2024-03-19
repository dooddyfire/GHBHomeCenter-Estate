from bs4 import BeautifulSoup 
import requests 
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
#Fix
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import re 
import pandas as pd 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
start = 1 
end = 1

area_lis = []
map_link = []
lat_lis = []
long_lis = []
url_lis = []

img_lis = []
type_lis = []
price_lis = []
address_lis = []
prov_lis = []
district_lis = []
subdistrict_lis = []
source_lis = []
web_lis = []
image_lis = []
address_lis = []

for i in range(start,end+1):
    url = "https://www.ghbhomecenter.com/property-for-sale?&pId=395&pg={}".format(i)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source,'html.parser')


    lis = [x['rel'] for x in soup.find_all('div',{'class':'link-property-detail'})]
    
    area_lisx = [f.find('div',{'class':'text-area'}).text.strip() for f in soup.find_all('div',{'class':'link-property-detail'})]
    for a in area_lisx: 

        area_lis.append(a)
        print(a)






    for i in lis: 

        driver.get(i)
        soupx = BeautifulSoup(driver.page_source,'html.parser')

        sect = soupx.find('section',{'class':'page-product-detail'})

        img = soupx.find('div',{'class':'img-fill'}).find('img')['src']
        image_lis.append(img)
        print(img)


        name = sect.find('h1').text 
        print(name)

        url_lis.append(i)
        print(i)

        price = sect.find('h3',{'class':'text-price'}).text.replace("ราคาทรัพย์","").strip()
        print(price)
        price_lis.append(price)

        lisx = [ g for g in sect.find_all('li',{'class':'list-group-item'})]
        print(lisx)

        typex = lisx[0].text.strip()
        print(typex)
        type_lis.append(typex)

        province = lisx[5].text.replace("จังหวัด","").strip()
        print(province)
        prov_lis.append(province)

        district = lisx[-2].text.strip()
        print(district)
        district_lis.append(district)

        subdis = lisx[4].text.strip()
        print(subdis)
        subdistrict_lis.append(subdis)

        address = subdis +" " +district+" "+province
        address_lis.append(address)
        print(address)

        google_maps_regex = re.compile(r'https?://(?:www\.)?google\.com/maps\?.*')

        # Extracting Google Maps links from HTML content
        google_maps_links = google_maps_regex.findall(driver.page_source)

        # Output the extracted links
        if len(google_maps_links) == 0: 
            lat = " "
            long = " "
        else: 
            # Regular expression to extract latitude and longitude values
            google_maps_link = google_maps_links[0]
            lat_long_regex = re.compile(r'daddr=(-?\d+\.\d+),(-?\d+\.\d+)')

            # Extract latitude and longitude values from the Google Maps link
            match = lat_long_regex.search(google_maps_link)

            if match:
                latitude = float(match.group(1))
                longitude = float(match.group(2))
                print("Latitude:", latitude)
                print("Longitude:", longitude)

            else:
                lat = " "
                long = " "
                print("No latitude and longitude found in the link.")

        lat_lis.append(latitude)
        long_lis.append(longitude)     

print(len(image_lis))
print(len(url_lis))
df = pd.DataFrame()

df['link'] = url_lis 
df['type'] = type_lis 
df['area'] = area_lis 
df['price'] = price_lis 
df['lat'] = lat_lis 
df['long'] = long_lis 
df['address'] = address_lis 
df['province'] = prov_lis 
df['district'] = district_lis 
df['subdistrict'] = subdistrict_lis 
df['image'] = image_lis

df.to_excel("TestBam2.xlsx")