import requests

from bs4 import BeautifulSoup
from sqlalchemy import sql
from database import init_db, db_session
from models import *
import sqlalchemy
from woo_commerce import Woo
from sqlalchemy.orm.exc import NoResultFound
class Redragonzone:

    # def if_string_none(string):
    #     if len(string) == 0:
    #         return False
    #     yyyy

    def __init__(self):

        init_db()

        self.woocommerce_api = Woo()
        # self.scrape_and_check_prices()
        
        data = self.single_product_scrape()
        self.woocommerce_api.add_product(data)

    def single_product_scrape(self, url="https://redragonzone.pk/collections/gaming-keyboard-price-in-pakistan/products/redragon-karura-2-k502-rgb-gaming-keyboard"):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        data = {}

        sale_price = 0
        price = 0

        title = str(soup.select_one("h1.page-heading").text).strip()
        description = soup.select_one(".description-text")

        price_div= soup.select_one(".detail-price")

        if price_div.find("span",{"class":"price"}):
            price = price_div.text.replace("\n","").replace("Rs. ","").replace(",","")
            # sale_price = price

        elif price_div.find("span",{"class":"price-sale"}):
            # price = int(price_div.find("del",{"class":"price-compare"}).text.replace("\n","").replace("Rs. ","").replace(",",""))
            price = sale_price = price_div.find("span",{"class":"price-sale"}).text.replace("\n","").replace("Rs. ","").replace(",","")

        data.update({
            "name" : title,
            "type": "simple",
            "slug": "buy-"+str(title).lower().replace(" ","-")+" price-in-pakistan",
            "regular_price": price,
            "description" : str(description)
        })

        images_list = [str(image['src']).split("?")[0] for image in list(soup.select("img.image-zoom"))]
        images = []

        for i, image in enumerate(images_list):
            
            images.append({
                'src' : "https:"+image,
                'name' : f'Buy {title} price in Pakistan ({i+1})',
                'alt' : title
            })
        data.update({"images":images})

        return data


        

        # print()
    def scrape_and_check_prices(self):
        
        

        url = "https://redragonzone.pk/collections/all-products?page={}&sort_by=created-descending"

        page_no = 1
        for page_no in range(1,4):
            
            response = requests.get(url.format(page_no))
        
            soup = BeautifulSoup(response.text, 'html.parser')

            products_on_page = soup.select(".product-grid-item.mode-view-item")
            for product in products_on_page:
                sale_price = 0
                price = 0

                product_name = product.select_one("h5.product-name.balance-false").text
                product_url = "https://redragonzone.pk"+str(product.select_one("h5.product-name.balance-false").select_one('a')['href'])
                price_element = product.select_one(".product-price.notranslate")
                # price = price_element.select_one("span.price")

                if price_element.find("span",{"class":"price"}):
                    price = int(price_element.text.replace("\n","").replace("Rs. ","").replace(",",""))

                elif price_element.find("span",{"class":"price-sale"}):
                    # price = int(price_element.find("span",{"class":"price-compare"}).text.replace("\n","").replace("Rs. ","").replace(",",""))
                    price = sale_price = int(price_element.find("span",{"class":"price-sale"}).text.replace("\n","").replace("Rs. ","").replace(",",""))
                    

                #     print(price)
                # else:
                try:

                    record = db_session.query(RedragonZoneRecords).filter_by(orignal_url=product_url).one()

                    if record:
                        
                        if int(record.price) != int(price):
                            
                            record.price = price
                            db_session.commit()
                            print(f"{record.name} Price Updated")
                        
                        # if int(record.sale_price) != int(sale_price):
                        #     record.sale_price = sale_price
                        #     db_session.commit()
                        #     print(f"{record.name} Sale Price Updated")

                        print(f"{product_name} => Already Exist and Prices are also Revised")

                    else:
                        print("Adding New Record")
                        new_record=RedragonZoneRecords(orignal_url=product_url,name=product_name,price=price,sale_price=sale_price)
                        db_session.add(new_record)
                        db_session.commit()
                        print(product_url, price, sale_price)

                except NoResultFound as e:
                    print(e)
                    print("Adding New Record, Because no Record was")
                    new_record=RedragonZoneRecords(orignal_url=product_url,name=product_name,price=price,sale_price=sale_price)
                    db_session.add(new_record)
                    db_session.commit()
                    print(product_url, price, sale_price)
                

                    




                
               

                # print(price, sale_price)


Redragonzone()