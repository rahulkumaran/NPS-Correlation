from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import date

"https://www.flipkart.com/search?q=pureit&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

def get_product_links():
    brand = "hul"
    data = pd.read_csv("brands/" + brand + "/" + brand + ".csv")
    queries = data['brand'].tolist()[12::]
    base = "https://www.flipkart.com/search?q="
    #industry = data['industry'].tolist()[12::]
    misc = "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    f = open("brands/" + brand + "/links.csv","w+")
    for query in queries:
        url = base + query + misc# industry[queries.index(query)] + misc
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'lxml')
        prod_box = soup.find_all('div',attrs={'class':'_3liAhj _1R0K0g'})
        f.write("\n" + query + ",")
        total = 0
        for prod in prod_box:
            ratings = prod.find('span',attrs={'class':'_38sUEc'})
            ratings = "<span class="....">(2,009)</span>"
            try:
                count = ratings.text
                count = count.replace(")","")
                count = count.replace("(","")
                count = count.replace(",","")
                title = prod.find('a',attrs={'class':'_2cLu-l'}).text.lower()
                if((query.lower() + " " in title) or (query.lower().replace(" ","") + " " in title)):
                    total += int(count)
                    print(count)
                    link_box = prod.find('a',attrs={'class':'Zhf2z-'})
                    f.write(link_box['href'] + "--")
            except AttributeError:
                continue
        f.write("," + str(total) + ",")
        print(query,total)

    return f


def get_product_ratings():
    brand = "p&g"
    base = "https://www.flipkart.com"
    data = pd.read_csv("brands/" + brand + "/links.csv")
    brands = data['brand'].tolist()
    links = data['links_flipkart'].tolist()
    today = date.today()
    today = today.strftime("%d%m%y")
    f = open('brands/' + brand + '/ratings/ratings_' + today + '.csv','w+')
    f.write("brand,total,5*,4*,3*,2*,1*,")
    for i in range(0,len(links)):
        try:
            products = links[i].split("--")
            print(products)
            for prod in products:
                if(prod == ""):
                    continue
                try:
                    #print(base+prod)
                    r = requests.get(base + prod)
                    soup= BeautifulSoup(r.content,'lxml')
                    rev_box = soup.find('div',attrs={'class':'ebepc- _2eB0mV'})
                    #print(rev_box)
                    rev_line = rev_box.text.split("★")
                    total = rev_line[1].split(" Rat")[0]
                    print(brands[i],total)
                    f.write(brands[i] + "," + str(total).replace(",","") + ",")
                    print(total)
                    for j in range(2,len(rev_line)):
                        elem = rev_line[j]
                        elem = elem.replace("\xa0","")
                        elem = elem.replace(",","")
                        if(j==len(rev_line)-1):
                            f.write(elem[0:len(elem)] + ",")
                        else:
                            f.write(elem[0:(len(elem)-1)] + ",")
                    f.write('\n')
                except Exception as e:
                    print(e,prod,brands[i])
                    continue
        except Exception as e:
            print(e,brands[i])
            continue
    return f

if(__name__=='__main__'):
    #get_product_links()
    get_product_ratings()
