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



filename = "TestBam1166.xlsx"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
start = 11 
end = 66

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
name_lis = []
gmap_lis = []

for i in range(start,end+1):
    url = "https://www.ghbhomecenter.com/property-for-sale?&pId=395&pg={}".format(i)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source,'html.parser')


    lis = [x['rel'] for x in soup.find_all('div',{'class':'link-property-detail'})]

    print("Page : ",i)
    area_lisx = [f.find('div',{'class':'text-area'}).text.strip() for f in soup.find_all('div',{'class':'link-property-detail'})]
    for a in area_lisx: 

        area_lis.append(a)
        print(a)






    for u in lis: 

        url_lis.append(u)
        print(u)

        driver.get(u)
        soupx = BeautifulSoup(driver.page_source,'html.parser')

        sect = soupx.find('section',{'class':'page-product-detail'})

        try:
            img = soupx.find('div',{'class':'img-fill'}).find('img')['src']
            image_lis.append(img)
            print(img)
        except: 
            img = " "
            image_lis.append(img)
            print(img)

        try:
            name = sect.find('h1').text 
            name_lis.append(name)
            print(name)
        except: 
            name = " "
            name_lis.append(name)
            print(name)


        try:
            price = sect.find('h3',{'class':'text-price'}).text.replace("ราคาทรัพย์","").strip()
            
        except: 
            price = " "
        print(price)
        price_lis.append(price)

        lisx = [ g for g in sect.find_all('li',{'class':'list-group-item'})]
        print(lisx)

        try:
            typex = lisx[0].text.strip()
            
        except: 
            typex = " "
        
        print(typex)
        type_lis.append(typex)

        try:
            province = lisx[5].text.replace("จังหวัด","").strip()
        
        except:
            province = " "

        prov_lis.append(province)
        print(province)

        try:
            district = lisx[-2].text.strip()
        except: 
            district = " "

        
        district_lis.append(district)
        print(district)

        try:
            subdis = lisx[4].text.strip()
        except:
            subdis = " "
        subdistrict_lis.append(subdis)
        print(subdis)

        try:
            address = subdis +" " +district+" "+province
        except: 
            address = " "

        
        print(address)
        address_lis.append(address)

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

            gmap_lis.append(google_maps_link)

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

        print("---------------------")

print(len(image_lis))
print(len(url_lis))
df = pd.DataFrame()

df['name'] = name_lis 
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
#df['Google Map'] = gmap_lis

df.to_excel(filename)

print("finish")