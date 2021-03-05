import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo

def getDataFromFlipKart(searchString):
    try:
        data = []
        flipkart_url = "https://www.flipkart.com/search?q=" + searchString # preparing the URL to search the product on flipkart
        uClient = uReq(flipkart_url) # requesting the webpage from the internet
        flipkartPage = uClient.read() # reading the webpage
        uClient.close() # closing the connection to the web server
        flipkart_html = bs(flipkartPage, "html.parser") # parsing the webpage as HTML
        bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"}) # seacrhing for appropriate tag to redirect to the product link
        del bigboxes[0:3] # the first 3 members of the list do not contain relevant information, hence deleting them.
        #box = bigboxes[0] #  taking the first iteration (for demo)
        pages = flipkart_html.find("div",{"class":"_2MImiq"})
        strr=pages.span.text
        end_page=strr.replace("Page 1 of ","")
        end_page=end_page.replace(",","")
        print(end_page)
        for ind in range(int(end_page)):
            if(len(data)<11):
                appendedUrl="&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="
                bigboxes=bigboxes
                if(ind!=0):
                    new_url=flipkart_url+appendedUrl+str(ind)
                    uClient = uReq(new_url) # requesting the webpage from the internet
                    flipkartPage = uClient.read() # reading the webpage
                    uClient.close() # closing the connection to the web server
                    flipkart_html = bs(flipkartPage, "html.parser") # parsing the webpage as HTML
                    bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"}) # seacrhing for appropriate tag to redirect to the product link
                    del bigboxes[0:3]
                for bbox in bigboxes:
                    box = bbox #  taking the first iteration (for demo)
                    try:
                        if(box.div.div.div!=None):
                            productLink = "https://www.flipkart.com" + box.div.div.div.a['href'] # extracting the actual product link
                            prodRes = requests.get(productLink) # getting the product page from server
                            prod_html = bs(prodRes.text, "html.parser") # parsing the product page as HTML
                            name= prod_html.find('span',{'class':'B_NuCI'}).text
                            price= prod_html.find('div',{'class':'_30jeq3 _16Jk6d'}).text
                            original_price= prod_html.find('div',{'class':'_3I9_wc _2p6lqe'})
                            if(original_price!=None):
                                original_price= original_price.text
                            #print(original_price)
                            discount= prod_html.find('div',{'class':'_3Ay6Sb _31Dcoz'})
                            if(discount != None):
                                discount=discount.span.text

                            #print(discount)
                            available_offer= prod_html.find_all('span',{'class':'_3j4Zjq row'})
                            av_offer=''
                            if(available_offer != None):
                                for av in available_offer:
                                    for ii in av.li.span:
                                        #print(ii)
                                        #print(len(av.li.span))
                                        if(ii != None):
                                            av_offer+=' '+str(ii)
                                    av_offer+=' ; '

                            #print(av_offer)
                            specifications= prod_html.find('table',{'class':'_14cfVK'})
                            spec=''
                            if(specifications != None):
                                #print(specifications)
                                for td in specifications.tbody.find_all('tr'):
                                    print(td)
                                    if(td!=None):
                                        for iii in td:
                                            if(iii != None):
                                                spec+=str(iii.text) + ' : '
                                        #for ii in td[1].ul.li:
                                         #   if(ii != None):
                                          #      spec+=str(ii.text) + ' '
                                        spec+=" ; "
                            print(spec)

                            mydict = {"name": name, "price": price, "original_price": original_price, "discount": discount,
                                          "available_offer": av_offer,"specifications": spec}
                            data.append(mydict)
                    except Exception as e:
                        print(e)
        print(data)
        return data
    except Exception as e:
        print(e)