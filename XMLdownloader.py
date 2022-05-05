import requests
import xml.etree.ElementTree as ET

URL_data = 'http://stripmag.ru/datafeed/p5s_full_stock.xml'
response_data = requests.get(URL_data)
# print(response.text)
with open('data.xml', 'w') as f:
    f.write(response_data.text)
    f.close()

URL_feed = 'http://alitair.1gb.ru/Intim_Ali_allfids_2.xml'
response_feed = requests.get(URL_feed)
with open('feed.xml', 'w', encoding="utf-8") as f:
    f.write(response_feed.text)
    f.close()


def update_feed(data, feed):
    price_update_list = []
    remainder_update_list = []
    data_tree = ET.parse(data)

    feed_tree = ET.parse(feed)

    products = data_tree.findall('product')
    offers = feed_tree.findall('.//offer')
    products_price = {}
    for product in products:
        assort = product.find('.//assort')
        products_price[assort.get('aID')] = \
            [product.find('price').get('RetailPrice'),
             assort.get('sklad')]

    for offer in offers:
        new_price = products_price.get(offer.get('id'))
        if not new_price:
            continue
        if offer.find('price').text != products_price[offer.get('id')][0]:
            price_update_list.append({offer.get('id'): [offer.find('price').text, products_price[offer.get('id')][0]]})
            offer.find('price').text = products_price[offer.get('id')][0]
        if offer.find('quantity').text != products_price[offer.get('id')][1]:
            remainder_update_list.append(
                {offer.get('id'): [offer.find('quantity').text, products_price[offer.get('id')][1]]})
            offer.find('quantity').text = products_price[offer.get('id')][1]

    print(price_update_list)
    print(remainder_update_list)


update_feed('data.xml', 'feed.xml')
