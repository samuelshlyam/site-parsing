import requests
import pandas as pd
class MonclerParser(WebsiteParser):
    def fetch_moncler_products(categories,cookie):
        base_url = "https://www.moncler.com/on/demandware.store/Sites-MonclerUS-Site/en_US/SearchApi-Search"
        all_products = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
              'Cookie': f'{cookie}'
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

    def process_categories(self, categories,cookie):
        # Fetch products
        products_df = fetch_moncler_products(categories,cookie)
        print(products_df.head())

        # Save to CSV
        products_df.to_csv('moncler_products_detailed.csv', index=False)
        print("Saved Moncler products to 'moncler_products_detailed.csv'.")
