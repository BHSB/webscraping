from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#Root URL missing integer specifying which page. Starts at 0
root_url = 'https://www.bananafingers.co.uk/category/climbing-shoes?page='

#Function to parse html page as soup
def page_to_soup(root_url):
    uClient = uReq(root_url)
    page_html = uClient.read()
    uClient.close()

    return soup(page_html, "html.parser")

#Create list of all the pages
pages_of_soup = [page_to_soup(root_url + str(x)) for x in range(8)]

#Create a text filename
filename = "climbing_shoes.csv"
f = open(filename, "w")

headers = "Brand, Model, Descripion, Price, RRP, Discount\n"

f.write(headers)

# Loop through pages
for page in pages_of_soup:
    shoes = page.findAll("div", {"class":"node-product-teaser-list-view__product-info-wrapper"})

    for shoe in shoes:

        brand = shoe.div.div.text.strip()

        model = shoe.h4.text

        desc_container = shoe.findAll("div", {"class":"node-product-teaser-list-view__description"})
        description = desc_container[0].text.strip()
        description = description.replace(',','').replace('*','').replace('\n','').replace('\r','')

        price_container = shoe.find("div", {"class":"node-product-teaser-list-view__price__sell-price"})
        price = price_container.text.strip().replace('£','')

        try:
            rrp_container = shoe.findAll("div", {"class":"node-product-teaser-list-view__price__rrp"})
            rrp = rrp_container[0].text.strip().replace('£','')
        except:
            rrp = price

        per_discount = int(round((1 - (float(price) / float(rrp))) * 100))

        # print("*" * 10)
        # print("Brand:", repr(brand))
        # print("Model:", repr(model))
        # print("Description:", repr(description))
        # print("Price:", repr(price))
        # print("RRP:", repr(rrp))

        f.write(f"{brand}, {model}, {description}, {price}, {rrp}, {per_discount}\n")

f.close()
