from bs4 import BeautifulSoup
import requests
for i in range(2,20):
    url = "https://www.flipkart.com/televisions/pr?sid=ckf%2Cczl&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&otracker=categorytree&p%5B%5D=facets.serviceability%5B%5D%3Dtrue&p%5B%5D=facets.brand%255B%255D%3DSamsung&otracker=nmenu_sub_TVs+%26+Appliances_0_Samsung&otracker=nmenu_sub_TVs+%26+Appliances_0_Samsung&page="+str(i)
    r = requests.get(url)
    print(r)

    soup = BeautifulSoup(r.text,"lxml")
    np = soup.find("a",class_ ="_1LKTO3").get("href")
    cnp = "https://www.flipkart.com"+np
    print(cnp)
