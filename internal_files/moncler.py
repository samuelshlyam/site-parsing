import requests
import pandas as pd

def fetch_moncler_products(categories):
    base_url = "https://www.moncler.com/on/demandware.store/Sites-MonclerUS-Site/en_US/SearchApi-Search"
    all_products = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
          'Cookie': 'dwanonymous_6ff516fc64e5194a34356fc83db5a3b8=adXIc3AvTbdBAvj7f7aiUC9O9K; __cq_dnt=1; dw_dnt=1; rskxRunCookie=0; rCookie=d05b2bnb49tympf7esh1vclwds9ruf; _fwb=11ZQo4uU6J7XtC5y7qTDbr.1716138026922; OptanonAlertBoxClosed=2024-05-19T17:00:30.127Z; _ga=GA1.1.1391914837.1716138027; tradedoubler=tradedoubler; _scid=e53f9a57-89ca-482f-8e06-de3945bf431f; _cs_c=0; __lt__cid=d946d864-0a26-4772-82be-c8813a053266; FPAU=1.2.966099923.1716138031; _pin_unauth=dWlkPVlUTTROREkwWXpndE4yVXpaUzAwTlRnM0xXRmxOREl0TkRGbU16RmhNR1EyWWpReQ; _fbp=fb.1.1716138030870.1658910019; _tt_enable_cookie=1; _ttp=ixbJ1TRoYtHehshUE_1g1WSNuNH; _sctr=1%7C1716091200000; _ym_uid=171613803723509370; _ym_d=1716138037; FPGCLAW=GCL.1716138764.Cj0KCQjwxqayBhDFARIsAANWRnS93hoOLAoxWrYpvNaZaPU_DfhiJBE75DQIybobJCeQRlb29PwSVSUaArLjEALw_wcB; FPGCLDC=GCL.1716138764.Cj0KCQjwxqayBhDFARIsAANWRnS93hoOLAoxWrYpvNaZaPU_DfhiJBE75DQIybobJCeQRlb29PwSVSUaArLjEALw_wcB; dwanonymous_249c920510bcbe3a8cb25bf01660cb9b=abyoL4Ac7L7HW14ajNFQpjacIV; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22dHz5fDf6fWbwbYiXcUjt%22%7D; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22%22%7D; __rtbh.aid=%7B%22eventType%22%3A%22aid%22%2C%22id%22%3A%22abyoL4Ac7L7HW14ajNFQpjacIV%22%7D; cto_bundle=-GwetV9CMWElMkJQOWhRUWZ2RlVIMUVnMmV5WWpsTjVBJTJCVmRxVEtxdCUyQkM0N0VUdm9jeTc2aXlzYWlXZVJUNEo4T1F2bjF0cVlNanpQNFVLcUVjaW05V0MlMkJGTFVJamd4dHU0WjB6ajRhNk5Ic0F0dU4xTE43QW0lMkJLdUJON0ljbldXRzk3JTJCR0JHb1JkeFhra0k4SWNxYnZXbHhDcFlMYW5waDVrb0hvQTZrZ3o2TWp6VndNRkgyRDBkQjlZdDRQWDRKVlA1czFBaENVdnlxNDV1Y1ZYJTJCbUslMkJVREt6ZyUzRCUzRA; lastRskxRun=1716140263729; OptanonConsent=isGpcEnabled=0&datestamp=Sun+May+19+2024+13%3A37%3A43+GMT-0400+(Eastern+Daylight+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=9c03543f-8b3c-44c9-9649-a9aa5ec3df3c&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1&hosts=H1%3A1%2CH7%3A1%2CH17%3A1%2CH8%3A1%2CH9%3A1%2CH15%3A1%2CH43%3A1%2CH18%3A1%2CH42%3A1%2CH48%3A1%2CH19%3A1%2CH46%3A1%2CH2%3A1%2CH20%3A1%2CH21%3A1%2CH40%3A1%2CH22%3A1%2CH23%3A1%2CH44%3A1%2CH24%3A1%2CH5%3A1%2CH25%3A1%2CH6%3A1%2CH26%3A1%2CH27%3A1%2CH41%3A1%2CH16%3A1%2CH28%3A1%2CH29%3A1%2CH30%3A1%2CH31%3A1%2CH49%3A1%2CH32%3A1%2CH45%3A1%2CH33%3A1%2CH34%3A1%2CH39%3A1%2CH35%3A1%2CH13%3A1%2CH36%3A1%2CH38%3A1%2CH37%3A1%2CH47%3A1%2CH50%3A1%2CH4%3A1%2CH11%3A1&genVendors=V1%3A0%2C&geolocation=US%3BNY&AwaitingReconsent=false; _scid_r=e53f9a57-89ca-482f-8e06-de3945bf431f; dw_locale=en_US; _cs_id=a197a264-e141-af80-bcce-f830663f7823.1716138030.3.1716161269.1716161269.1712046992.1750302030395.1; _ga_Z1W9QE10F0=GS1.1.1716161272.2.0.1716161272.0.0.1899802131; sid=taVpj_pCew97mQFZ1nMQskH91apxWi56OcI; dwsid=rHSwbphcsIbx6HSn2DfjR1gsDEsTROXzs7Mg2_y_CshkKfADkxU5u3PqXEHo6LUtVJFmjblIxJYDnS8KPnkm7w=='
    }

    for category in categories:
        offset = 0
        while True:
            params = {
                'cgid': category,
                'start': offset,
                'sz': 12  # Assuming page size is constant as 12
            }
            response = requests.get(base_url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Failed to fetch data: {response.status_code} - {response.text}")
                break

            data = response.json()
            products = data['data']['products']
            if not products:
                break

            for product in products:
                product_info = {
                    'id': product.get('id', ''),
                    'productName': product.get('productName', ''),
                    'shortDescription': product.get('shortDescription', ''),
                    'productUrl': "https://www.moncler.com" + product.get('productUrl', ''),
                    'price': product.get('price', {}).get('sales', {}).get('formatted', ''),
                    'price_min': product.get('price', {}).get('min', {}).get('sales', {}).get('formatted', ''),
                    'price_max': product.get('price', {}).get('max', {}).get('sales', {}).get('formatted', ''),
                    'imageUrls': [img for img in product.get('imgs', {}).get('urls', [])],
                    'productCharacteristics': product.get('productCharacteristics', ''),
                    'variationAttributes': parse_variation_attributes(product.get('variationAttributes', []))
                }
                all_products.append(product_info)

            # Update offset to next page
            offset += len(products)
            total_count = data['data']['count']
            if offset >= total_count:
                break

    return pd.DataFrame(all_products)

def parse_variation_attributes(variation_attributes):
    # Parse and format variation attributes such as color and size
    attributes = {}
    for attr in variation_attributes:
        if 'values' in attr:
            values = ', '.join([f"{v['displayValue']} (ID: {v['id']})" for v in attr['values']])
        else:
            values = attr.get('displayValue', '')
        attributes[attr['displayName']] = values
    return attributes

# Example categories
#categories = ['men-ready-to-wear', 'women-ready-to-wear']
categories = ['']
# Fetch products
products_df = fetch_moncler_products(categories)
print(products_df.head())

# Save to CSV
products_df.to_csv('moncler_products_detailed.csv', index=False)
print("Saved Moncler products to 'moncler_products_detailed.csv'.")
 