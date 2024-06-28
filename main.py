from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language':'en-US,en;q=0.9',
}
url=input("Enter Full Url of Zillow.com from Data You want to Scrap :")
time.sleep(5)
response=requests.get(url=url,headers=header).text
soup=BeautifulSoup(response,'html.parser')
prices=soup.find_all(class_='PropertyCardWrapper__StyledPriceGridContainer-srp-8-102-0__sc-16e8gqd-0 eFBhnu')
price=[price.text.split('+')[0].replace("/mo","").replace("$","") for price in prices]
locations=soup.find_all(name='address')
location=[location.text for location in locations]
links=soup.select('.property-card-data a[href]')
link=[]
for lnk in links:
    href=lnk['href']
    if 'https' not in href:
        linkurl=f"https://zillow.com/{href}"
    else:
        linkurl=href
    link.append(linkurl)
gformurl=input("Enter Your Google Form Url Here with Price(first),Location(Second),Link(Third):")
for n in range(len(price)):
    driver=webdriver.Chrome()
    driver.get(gformurl)
    time.sleep(5)
    inputprice=driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    inputprice.send_keys(price[n])
    time.sleep(1)
    inputlocation=driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    inputlocation.send_keys(location[n])
    
    time.sleep(1)
    inputlink=driver.find_element(By.XPATH,value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    inputlink.send_keys(link[n])
    
    time.sleep(1)
    submit=driver.find_element(By.CSS_SELECTOR,value='div.uArJ5e.UQuaGc.Y5sE8d.VkkpIf.QvWxOd').click()
    time.sleep(1)
