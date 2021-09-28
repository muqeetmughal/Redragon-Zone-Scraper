from woocommerce import API
from settings import Consumer_key, Consumer_secret



class Woo:

    def __init__(self):
        self.wcapi = API(
            url="https://redragon.sale",
            consumer_key=Consumer_key,
            consumer_secret=Consumer_secret,
            wp_api=True,
            version="wc/v3",
            timeout=60
        )


    def add_product(self, data):
        print(self.wcapi.post("products", data).json())