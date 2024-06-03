import os
import re
from urllib.parse import urljoin, urlunparse, urlparse

import requests
from bs4 import BeautifulSoup
import csv
import json
import html
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import datetime
from main_parser import WebsiteParser

class BottegaVenetaParser(WebsiteParser):
    #COMPLETE
    
    ## This class parses the HTML files from the Bottega Veneta website. 
    ## website: https://www.bottegaveneta.com
    def __init__(self, directory):
        self.brand = 'bottega_veneta'  # Replace spaces with underscores
        self.directory = directory


    def parse_product_blocks(self, soup, category):
        product_blocks = soup.find_all('article', class_='c-product')
        parsed_data = []

        column_names = [
            'filename','data_pid', 'id', 'name', 'collection', 'productSMC', 'material', 'customization',
            'packshotType', 'brand', 'color', 'colorId', 'size', 'price', 'discountPrice',
            'coupon', 'subCategory', 'category', 'topCategory', 'productCategory', 'macroCategory',
            'microCategory', 'superMicroCategory', 'list', 'stock', 'productGlobalSMC', 'images', 'product_url'
        ]

        parsed_data.append(column_names)

        for block in product_blocks:
            product_data = []

            # Extract data-pid
            data_pid = block['data-pid']

            # Extract data-gtmproduct and parse JSON
            data_gtmproduct = block['data-gtmproduct']
            data_gtmproduct = html.unescape(data_gtmproduct)
            product_info = json.loads(data_gtmproduct)

            # Extract product images
            images = []
            image_container = block.find('div', class_='c-product__imagecontainer')
            if image_container:
                image_elements = image_container.find_all('img', class_='c-product__image')
                for img in image_elements:
                    images.append(img['src'])

            # Extract product URL
            product_url = block.find('a', class_='c-product__link')['href']

            # Append the extracted information to the product_data list
            product_data.append(data_pid)
            product_data.append(product_info['id'])
            product_data.append(product_info['name'])
            product_data.append(product_info['collection'])
            product_data.append(product_info['productSMC'])
            product_data.append(product_info['material'])
            product_data.append(product_info['customization'])
            product_data.append(product_info['packshotType'])
            product_data.append(product_info['brand'])
            product_data.append(product_info['color'])
            product_data.append(product_info['colorId'])
            product_data.append(product_info['size'])
            product_data.append(product_info['price'])
            product_data.append(product_info['discountPrice'])
            product_data.append(product_info['coupon'])
            product_data.append(product_info['subCategory'])
            product_data.append(category)
            product_data.append(product_info['topCategory'])
            product_data.append(product_info['productCategory'])
            product_data.append(product_info['macroCategory'])
            product_data.append(product_info['microCategory'])
            product_data.append(product_info['superMicroCategory'])
            product_data.append(product_info['list'])
            product_data.append(product_info['stock'])
            product_data.append(product_info['productGlobalSMC'])
            product_data.append(', '.join(images))
            product_data.append(product_url)

            parsed_data.append(product_data)

        return parsed_data


class GucciParser():
    ##COMPLETE
    def __init__(self):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = "https://www.gucci.com/us/en/c/productgrid?categoryCode={category}&show=Page&page={page}"
        self.data = pd.DataFrame()
    def format_url(self,url):
        """ Helper function to format URLs correctly """
        return f"https:{url}" if url else ''

    def safe_strip(self,value):
        """ Helper function to strip strings safely """
        return value.strip() if isinstance(value, str) else value
    def fetch_data(self,category, base_url):
        session = requests.Session()
        # Setup retry strategy
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated to use allowed_methods instead of method_whitelist
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3'}
        all_products = []  # Use a list to store product dictionaries
        try:
            response = session.get(base_url.format(category=category, page=0), headers=headers)
            response.raise_for_status()
            json_data = response.json()
            total_pages = json_data.get('numberOfPages', 1)
            print(f"Category: {category}, Total Pages: {total_pages}")

            for page in range(total_pages):
                response = session.get(base_url.format(category=category, page=page), headers=headers)
                response.raise_for_status()
                json_data = response.json()
                items = json_data.get('products', {}).get('items', [])
                if not items:
                    print(f"No items found on Page: {page + 1}/{total_pages}")
                    continue

                for product in items:
                    product_info = {
                        'category': category,
                        'productCode': self.safe_strip(product.get('productCode', '')),
                        'title': self.safe_strip(product.get('title', '')).replace('\n', ' ').replace('\r', ''),
                        'price': self.safe_strip(product.get('price', '')),
                        'rawPrice': self.safe_strip(product.get('rawPrice', '')),
                        'productLink': "https://www.gucci.com/us/en" + self.safe_strip(product.get('productLink', '')),
                        'primaryImage': self.format_url(product.get('primaryImage', {}).get('src', '')),
                        'alternateGalleryImages': " | ".join([self.format_url(img.get('src', '')) for img in product.get('alternateGalleryImages', [])]),
                        'alternateImage': self.format_url(product.get('alternateImage', {}).get('src', '')),
                        'isFavorite': str(product.get('isFavorite', False)).lower(),
                        'isOnlineExclusive': str(product.get('isOnlineExclusive', False)).lower(),
                        'isRegionalOnlineExclusive': str(product.get('isRegionalOnlineExclusive', False)).lower(),
                        'regionalOnlineExclusiveMsg': self.safe_strip(product.get('regionalOnlineExclusiveMsg', '')),
                        'isExclusiveSale': str(product.get('isExclusiveSale', False)).lower(),
                        'label': self.safe_strip(product.get('label', '')),
                        'fullPrice': self.safe_strip(product.get('fullPrice', '')),
                        'position': int(product.get('position', 0)),
                        'productName': self.safe_strip(product.get('productName', '')),
                        'showSavedItemIcon': str(product.get('showSavedItemIcon', False)).lower(),
                        'type': self.safe_strip(product.get('type', '')),
                        'saleType': self.safe_strip(product.get('saleType', '')),
                        'categoryPath': self.safe_strip(product.get('categoryPath', '')),
                        'variant': self.safe_strip(product.get('variant', '')),
                        'videoBackgroundImage': self.format_url(product.get('videoBackgroundImage', '')),
                        'zoomImagePrimary': self.format_url(product.get('zoomImagePrimary', '')),
                        'zoomImageAlternate': self.format_url(product.get('zoomImageAlternate', '')),
                        'filterType': self.safe_strip(product.get('filterType', '')),
                        'nonTransactionalWebSite': self.safe_strip(product.get('nonTransactionalWebSite', '')),
                        'isDiyProduct': str(product.get('isDiyProduct', False)).lower(),
                        'inStockEntry': str(product.get('inStockEntry', False)).lower(),
                        'inStoreStockEntry': str(product.get('inStoreStockEntry', False)).lower(),
                        'inStoreStockRegionalEntry': str(product.get('inStoreStockRegionalEntry', False)).lower(),
                        'visibleWithoutStock': str(product.get('visibleWithoutStock', False)).lower(),
                        'showAvailableInStoreOnlyLabel': str(product.get('showAvailableInStoreOnlyLabel', False)).lower(),
                        'showOutOfStockLabel': str(product.get('showOutOfStockLabel', False)).lower(),
                    }
                    all_products.append(product_info)
                print(f"Processed {len(items)} products on Page: {page + 1}/{total_pages} for Category: {category}")

            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()


    def process_categories(self, categories):
        for category in categories:
            category_data = self.fetch_data(category, self.base_url)
            self.data = pd.concat([self.data, category_data], ignore_index=True)

        # Save the complete DataFrame to a CSV file
        #data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        filename = f'parser-output/gucci_output_{current_date}.csv'
        self.data.to_csv(filename,sep=',', index=False, quoting=csv.QUOTE_ALL)
        print("Complete data saved to 'output_gucci_5_27_24.csv'")
class FendiParser(WebsiteParser):
    ## This class parses the HTML files from the Fendi website. 
    ## website: https://www.fendi.com
    def __init__(self, directory):
        self.brand = 'fendi'  
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
          'product_id','category', 'product_name', 'description', 'price', 'main_image_url',
            'additional_image_url', 'product_details_url'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='product')
        for block in product_blocks:
            try:
                product_id=block.get('data-pid')
                product_name = block.find('a', class_='link').text.strip() if block.find('a', class_='link') else ''
                description = block.find('p', class_='c-tiles__tile-body-type').text.strip() if block.find('p',
                                                                                                           'c-tiles__tile-body-type') else ''
                price = block.find('span', class_='value').text.strip() if block.find('span', class_='value') else ''
                images = block.find_all('img', class_='c-lazyload__image')

                main_image_url = images[0].get('src') or images[0].get('data-src') if images else None
                additional_image_url = images[1].get('src') or images[1].get('data-src') if len(images) > 1 else None
                product_details_url = block.find('a')['href'] if block.find('a') else ''

                product_data_list = [
                    product_id, category, product_name, description, price,
                    main_image_url, additional_image_url, product_details_url
                ]
                parsed_data.append(product_data_list)
            except Exception as e:
                print(f"Error parsing block: {e}")

        return parsed_data


class GivenchyProductParser(WebsiteParser):
    ## This class parses the HTML files from the Bottega Veneta website.
    ## website: https://www.givenchy.com/us/en-US
    def __init__(self, directory):
        self.brand = 'givenchy'  # Replace spaces with underscores
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'user_category','product_id', 'product_url', 'product_name', 'price', 'image_urls','availability','currency','label'
        ]
        parsed_data.append(column_names)

        product_tiles = soup.find_all('div', class_='product-tile')

        for tile in product_tiles:
            product_id = tile.get('data-itemid', '')
            product_url = tile.find('a', class_='thumb-link')['href'] if tile.find('a', class_='thumb-link') else ''
            product_name = tile.find('h2', class_='product-name').text.strip() if tile.find('h2', class_='product-name') else ''
            price_element = tile.find('span', class_='price-sales')
            price = price_element.text.strip() if price_element else ''

            # Extract all image URLs
            image_elements = tile.find_all('img', class_='thumb-img')
            image_urls = [img.get('data-srcset').split()[0] for img in image_elements if img.get('data-srcset')]

            availability=tile.get('data-availability','')
            currency_meta = tile.find('meta', itemprop='priceCurrency')
            currency=''
            if currency_meta:
                currency = currency_meta.get('content','')
            label_element = soup.find('span', class_='tile-label')
            label = label_element.text.strip() if label_element else ''

            product_data = [
                category,
                product_id,
                product_url,
                product_name,
                price,
                ', '.join(image_urls),
                availability,
                currency,
                label
            ]
            parsed_data.append(product_data)

        return parsed_data
    

class CanadaGooseProductParser(WebsiteParser):
    ## This class parses the HTML files from the Bottega Veneta website.
    ## website: https://www.canadagoose.com/us/en
    def __init__(self, directory):
        self.brand = 'canada_goose'  # Replace spaces with underscores
        self.directory = directory
    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'product_id', 'product_url', 'product_name', 'price', 'image_urls', 'color_options'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='grid-tile')

        for block in product_blocks:
            #The product id is not being grabbed properly here and
            #needs to be fixed
            product_id = block.get('data-pid', 'No ID')
            product_link = block.find('a', class_='thumb-link')
            product_url = product_link['href'] if product_link else 'No URL'
            product_name = block.find('div', class_='product-name').text.strip() if block.find('div', class_='product-name') else 'No Name'
            
            price_element = block.find('span', class_='price-sales')
            price = price_element.find('span', class_='value').text.strip() if price_element else 'No Price'
            
            images = block.find_all('img', class_='lazy')
            image_urls = [img.get('data-src', img.get('src', 'No images')) for img in images if 'data-src' in img.attrs] or ['No images']

            # Extract color options
            color_options = []
            color_links = block.find_all('a', class_='swatch')
            for link in color_links:
                color = link.get('title', 'No Color')
                color_image = link.find('img').get('data-src') if link.find('img') else 'No Color Image'
                color_options.append({'color': color, 'image': color_image})

            product_data = [
                product_id,
                f"https://www.canadagoose.com{product_url}",
                product_name,
                price,
                ', '.join(image_urls),
                json.dumps(color_options)  # Store color options as JSON string for simplicity
            ]
            parsed_data.append(product_data)

        return parsed_data
    


class VejaProductParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'veja'  # Replace spaces with underscores
        self.directory = directory
    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'category', 'product_name', 'price', 'main_image_url', 'additional_image_url',
            'product_details_url'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='product-item-info')

        for block in product_blocks:
            product_name = block.find('strong', class_='product name product-item-name').find('a').text.strip()
            price = block.find('span', class_='price').text.strip()
            product_details_url = block.find('a', class_='product-item-link')['href']
            
            images = block.find_all('img', alt=product_name)
            main_image_url = images[0]['src'] if images else 'No image available'
            additional_image_url = images[1]['src'] if len(images) > 1 else 'No additional image available'

            product_data_list = [
                category,
                product_name,
                price,
                main_image_url,
                additional_image_url,
                product_details_url
            ]

            parsed_data.append(product_data_list)

        return parsed_data

    
class StellaProductParser(WebsiteParser):

    ## This class parses the HTML files from the Bottega Veneta website.
    ## website: https://www.stellamccartney.com
    def __init__(self, directory):
        self.brand = 'stella_mccartney'  # Replace spaces with underscores
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'product_id', 'category', 'product_name', 'price', 'main_image_url', 'additional_image_url',
            'product_details_url', 'product_color', 'product_tags'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='product')

        for block in product_blocks:
            product_id = block.get('data-pid', '')
            product_name = block.get('data-name', '')
            price_element = block.find('span', class_='value')
            price = price_element.text.strip() if price_element else ''
            link_element = block.find('a', class_='lazy__link')
            product_details_url = link_element['href'] if link_element else ''
            #product-tile__plp-images-stack
            # Handling images
            images_data = block.find('div', class_='product-tile__plp-images-stack')
            product_images_list = images_data.get('data-product-images',[]).strip()
            product_images_list = json.loads(product_images_list)



            try:
                main_image_url = product_images_list[0].get('url','') if product_images_list else ''
                additional_image_url = " , ".join([s.get('url') for s in product_images_list ])

            except json.JSONDecodeError:
                main_image_url = ''
                additional_image_url = ''

            # Handling color options from buttons
            color_buttons = block.find_all('button', class_='more')
            colors = [btn.get('aria-label').split(' ')[-1] for btn in color_buttons if btn.get('aria-label')]

            # Handling tags
            tags_div = block.find('div', class_='product-tile__body__tags')
            tags = [tag.text for tag in tags_div.find_all('div')] if tags_div else ['']
            tags=[tag.replace('\n','').strip() for tag in tags]
            product_data_list = [
                product_id, category, product_name, price, main_image_url, additional_image_url,
                f"https://www.stellamccartney.com{product_details_url}", ', '.join(colors), ', '.join(tags)
            ]

            parsed_data.append(product_data_list)

        return parsed_data


    
class TomFordProductParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'tom_ford'  # Replace spaces with underscores
        self.directory = directory
    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'product_id', 'product_name', 'product_url', 'price', 'images', 'quick_view_url','variation_count'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='product')

        for block in product_blocks:
            product_id = block.get('data-pid', '')
            product_name = block.find('a', class_='link').text.strip() if block.find('a', class_='link') else ''
            product_url = block.find('a', class_='tile-image-container')['href'] if block.find('a', class_='tile-image-container') else ''
            
            price_element = block.find('span', class_='value')
            price = price_element.text.strip() if price_element else ''
            
            image_elements = block.find_all('img', class_='loaded')
            images = [img['srcset'] for img in image_elements]
            
            quick_view_link = block.find('a', class_='quickview')
            quick_view_url = quick_view_link['href'] if quick_view_link else ''
            
            variation_element = block.find('div', class_='variation-count')
            variation_count = variation_element.text.strip() if variation_element else ''
            product_data = [
                product_id,
                product_name,
                product_url,
                price,
                ', '.join(images),
                quick_view_url,
                variation_count
            ]
            parsed_data.append(product_data)

        return parsed_data
    

    
class OffWhiteProductParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'off_white'  # Replace spaces with underscores
        self.directory = directory
    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'product_id', 'product_url', 'product_name', 'base_price', 'discount_rate', 'sale_price', 'image_urls', 'alt_text'
        ]
        parsed_data.append(column_names)

        product_items = soup.find_all('li')

        for item in product_items:
            div = item.find('div')
            product_id = div.get('data-insights-object-id', '') if div else ''
            product_url = item.find('a', class_='css-dpg8v2')['href'] if item.find('a', class_='css-dpg8v2') else ''
            product_name = item.find('p', class_='css-1dw89jd').text.strip() if item.find('p', class_='css-1dw89jd') else ''
            base_price=''
            discount_rate=''
            sale_price=''
            # Price details
            normal_price_span = item.find('span', class_='css-bks3r1') or item.find('span', class_='css-1go0pru')
            if normal_price_span:
                base_price = normal_price_span.text.strip()
            
            # Extract discount rate if present
            discount_rate_span = item.find('span', class_='css-f5f5h3')
            if discount_rate_span:
                discount_rate = discount_rate_span.text.strip()
            
            # Extract sale price if present
            sale_price_span = item.find('span', class_='css-uqjroe')
            if sale_price_span:
                sale_price = sale_price_span.text.strip()
        
            
            
            # Image URLs and alt text
            images = item.find_all('img')
            image_urls = [img['src'] for img in images if 'src' in img.attrs]
            alt_texts = [img['alt'] for img in images if 'alt' in img.attrs]

            product_data = [
                product_id,
                product_url,
                product_name,
                base_price,
                discount_rate,
                sale_price,
                ', '.join(image_urls),
                ', '.join(alt_texts)
            ]
            parsed_data.append(product_data)

        return parsed_data
    

    
class BallyParser():
    ##COMPLETE
    def __init__(self):
        #https://www.bally.com/_next/data/kHhMfjaaFfoBfxbp7icbW/en/category/men-sale.json
        #https://www.bally.com/_next/data/kHhMfjaaFfoBfxbp7icbW/en/category/women-sale.json
        #https://www.bally.com/_next/data/kHhMfjaaFfoBfxbp7icbW/en/category/men.json
        #https://www.bally.com/_next/data/kHhMfjaaFfoBfxbp7icbW/en/category/women.json
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = "https://www.bally.com/_next/data/kHhMfjaaFfoBfxbp7icbW/en/category/{category}p={page}"
        self.data = pd.DataFrame()
    def format_url(self,url):
        """ Helper function to format URLs correctly """
        return f"https:{url}" if url else ''

    def safe_strip(self,value):
        """ Helper function to strip strings safely """
        return value.strip() if isinstance(value, str) else value


    def fetch_data(self,category, base_url):
        session = requests.Session()
        # Setup retry strategy
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated to use allowed_methods instead of method_whitelist
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3'}
        all_products = []  # Use a list to store product dictionaries
        try:
            response = session.get(base_url.format(category=category, page=1), headers=headers)
            response.raise_for_status()
            json_data = response.json()
            json_data = json_data.get('pageProps',"")
            total_pages = json_data.get('maxPage',None)
            if not total_pages:
                raise ValueError
            print(f"Category: {category}, Total Pages: {total_pages}")

            #for page in range(1,total_pages):
            response = session.get(base_url.format(category=category, page=total_pages), headers=headers)
            response.raise_for_status()
            json_data = response.json()
            json_data = json_data.get('pageProps', "")
            items = json_data.get('category', {}).get('products', [])
            site_category = json_data.get('handle', '')
            if items:

                for product in items:
                    product_info = {
                        'user_defined_categories': category,
                        'category' : site_category ,
                        'title': self.safe_strip(product.get('title', '')).replace('\n', ' ').replace('\r', ''),
                        'price': self.safe_strip(product.get('price', '').get('amount','')),
                        'currency': self.safe_strip(product.get('price', '').get('currencyCode','')),
                        'originalPrice':  self.safe_strip(product.get('originalPrice', '').get('amount','')),
                        'productLink': "https://www.bally.com/en/products/" + self.safe_strip(product.get('handle', '')),
                        'primaryImage': product.get('media', [])[0].get('url', ''),
                        'alternateGalleryImages': " , ".join(
                            [img.get('url', '') for img in product.get('media', [])]),
                        'categoryDescription' : product.get('ClassDescription', {}).get('value',''),
                        'subclass': product.get('SubclassDescription', {}).get('value', '')

                    }
                    all_products.append(product_info)
               # print(f"Processed {len(items)} products on Page: {page + 1}/{total_pages} for Category: {category}")

            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()

    def process_categories(self, categories):
        for category in categories:
            category_data = self.fetch_data(category, self.base_url)
            self.data = pd.concat([self.data, category_data], ignore_index=True)

        # Save the complete DataFrame to a CSV file
        #data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        filename = f'parser-output/bally_output_{current_date}.csv'
        self.data.to_csv(filename,sep=',', index=False, quoting=csv.QUOTE_ALL)
        print("Complete data saved")


class IsabelMarantParser(WebsiteParser):
    ## This class parses the HTML files from the Bottega Veneta website.
    ## website: https://www.givenchy.com/us/en-US
    def __init__(self, directory):
        self.brand = 'isabel_marant'  # Replace spaces with underscores
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'user_category', 'product_url', 'product_name', 'price', 'discounted_price', 'image_urls', 'sizes',
            'availability', 'label'
        ]
        parsed_data.append(column_names)

        product_items = soup.find_all('product-item', class_='product-item')

        for item in product_items:
            product_url = item.find('a', class_='product-item__aspect-ratio')['href'] if item.find('a',class_='product-item__aspect-ratio') else ''
            product_name = item.find('a', class_='product-item-meta__title').text.strip() if item.find('a',class_='product-item-meta__title') else ''

            price_element = item.find('span', class_='price--compare')
            discounted_price_element = item.find('span', class_='price--highlight')

            price = ''
            discounted_price = ''

            if price_element and discounted_price_element:
                price = price_element.text.strip()
                discounted_price = discounted_price_element.text.strip()
            else:
                # For non-discounted items
                regular_price_element = item.find('span', class_='price')
                if regular_price_element:
                    price = regular_price_element.text.strip()

            price = re.sub(r'[^\d.,]', '', price)
            discounted_price = re.sub(r'[^\d.,]', '', discounted_price)
            # Extract all image URLs
            image_elements = item.find_all('img')
            image_urls = [img.get('src') for img in image_elements if img.get('src')]

            # Extract sizes and availability
            sizes_list = item.find('ul', class_='plp-sizes-list')
            sizes = []
            availability = []
            if sizes_list:
                for li in sizes_list.find_all('li'):
                    sizes.append(li.text.strip())
                    availability.append('available' if 'not-available' not in li.get('class', []) else 'not available')

            # Extract labels
            label_elements = item.find_all('span', class_='label label--custom')
            labels = [label.text.strip() for label in label_elements if label.text.strip()]

            product_data = [
                category,
                product_url,
                product_name,
                price,
                discounted_price,
                ', '.join(image_urls),
                ', '.join(sizes),
                ', '.join(availability),
                ', '.join(labels)
            ]
            parsed_data.append(product_data)

        return parsed_data


class Chloe_Parser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'chloe'  # Replace spaces with underscores
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'Cod10', 'Title', 'Price', 'position', 'category', 'macro_category', 'micro_category', 'macro_category_id', 'micro_category_id', 'color', 'color_id', 'product_price', 'discountedPrice', 'price_tf', 'discountedPrice_tf', 'quantity', 'coupon', 'is_in_stock', 'list', 'url', 'img_src', 'filename'
        ]
        parsed_data.append(column_names)
        articlesChloe = soup.find_all('article', {'class': 'item'})

        for articleChloe in articlesChloe:

            product_data = []
            imgSource = articleChloe.find('img')
            if imgSource:
                imgSource = imgSource['src']

            data_pid = articleChloe['data-ytos-track-product-data']

            a_url = articleChloe.find('a')
            if a_url:
                a_url = a_url['href']

            product_info = json.loads(data_pid)

            product_data.append(product_info['product_cod10'])
            product_data.append(product_info['product_title'])
            product_data.append(product_info['product_price'])
            product_data.append(product_info['product_position'])
            product_data.append(product_info['product_category'])
            product_data.append(product_info['product_macro_category'])
            product_data.append(product_info['product_micro_category'])

            product_data.append(product_info['product_macro_category_id'])
            product_data.append(product_info['product_micro_category_id'])
            product_data.append(product_info['product_color'])
            product_data.append(product_info['product_color_id'])
            product_data.append(product_info['product_price'])
            product_data.append(product_info['product_discountedPrice'])

            product_data.append(product_info['product_price_tf'])
            product_data.append(product_info['product_discountedPrice_tf'])
            product_data.append(product_info['product_quantity'])
            product_data.append(product_info['product_coupon'])
            product_data.append(product_info['product_is_in_stock'])
            product_data.append(product_info['list'])

            product_data.append(a_url)

            product_data.append(imgSource)
            product_data.append(category)
            parsed_data.append(product_data)
        return parsed_data
class MCM_Parser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'mcm'  # Replace spaces with underscores
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'user_category', 'product_id', 'product_url', 'product_name', 'price', 'discounted_price', 'image_urls',
            'availability'
        ]
        parsed_data.append(column_names)

        product_tiles = soup.find_all('a', class_='product-tile')

        for tile in product_tiles:
            product_id = tile.get('data-itemid', '')
            product_url = tile.get('href', '')
            product_name = tile.find('h2').text.strip() if tile.find('h2') else ''

            # Price and Discounted Price
            price_element = tile.find('span', class_='price-value')
            price = price_element.text.strip() if price_element else ''
            discounted_price_element = tile.find('span', class_='product-sales-price')
            discounted_price = discounted_price_element.find('span', class_='price-value').text.strip() if discounted_price_element else ''

            # Extract all image URLs
            image_elements = tile.find_all('source', media=True)
            image_urls = [img['srcset'].split()[0] for img in image_elements if 'srcset' in img.attrs]

            availability = tile.get('data-itemid', '')

            product_data = [
                category,
                product_id,
                product_url,
                product_name,
                price,
                discounted_price,
                ', '.join(image_urls),
                availability
            ]
            parsed_data.append(product_data)
        return parsed_data

class CultGaiaProductParser(WebsiteParser):
    ## This class parses the HTML files from the Cult Gaia website.
    ## website: https://www.cultgaia.com
    def __init__(self, directory):
        self.brand = 'cultgaia'  # Replace spaces with underscores
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'user_category', 'product_url', 'product_name', 'price', 'discounted_price', 'image_urls', 'tag'
        ]
        parsed_data.append(column_names)

        product_tiles = soup.find_all('div', class_='products__listing-details')

        for tile in product_tiles:
            product_url = tile.find('a')['href'] if tile.find('a') else ''
            product_name_element = tile.find('p', class_='s upper')
            product_name = product_name_element.contents[0].strip() if product_name_element else ''
            price = tile.find('p', class_='s upper').text.strip().split('$')[-1] if tile.find('p',
                                                                                              class_='s upper') else ''
            discounted_price = ''

            # Check for discounted price
            compare_price = tile.find('s', {'data-compare-price': ''})
            if compare_price and compare_price.previous_sibling:
                discounted_price = compare_price.previous_sibling.strip()

            # Extract all image URLs
            image_urls = []
            gallery = tile.find_previous_sibling('div', class_='products__listing-image')
            if gallery:
                image_elements = gallery.find_all('img')
                for img in image_elements:
                    srcset = img.get('srcset', '').split(',')
                    for src in srcset:
                        url = src.strip().split(' ')[0]
                        if url:
                            image_urls.append(url)

            # Extract tag
            tag = tile.find('p', class_='tag').text.strip() if tile.find('p', class_='tag') else ''

            product_data = [
                category,
                product_url,
                product_name,
                price,
                discounted_price,
                ', '.join(image_urls),
                tag
            ]
            parsed_data.append(product_data)

        return parsed_data

from bs4 import BeautifulSoup

class GoldenGooseProductParser(WebsiteParser):
    ## This class parses the HTML files from the Golden Goose website.
    ## website: https://www.goldengoose.com
    def __init__(self, directory):
        self.brand = 'goldengoose'  # Replace spaces with underscores
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'user_category', 'product_id', 'product_url', 'product_name', 'price', 'discounted_price', 'image_urls'
        ]
        parsed_data.append(column_names)

        product_tiles = soup.find_all('li', class_='product-tile-container')

        for tile in product_tiles:
            product_div = tile.find('div', class_='product master')
            product_id = product_div['data-pid'] if product_div else ''
            product_url = tile.find('a', class_='js-product-tile_link')['href'] if tile.find('a', class_='js-product-tile_link') else ''
            product_name = tile.find('div', class_='pdp-link').find('a').text.strip() if tile.find('div', class_='pdp-link') and tile.find('div', class_='pdp-link').find('a') else ''
            price_element = tile.find('div', class_='price')
            price = price_element.find('span', class_='value').text.strip() if price_element and price_element.find('span', class_='value') else ''
            discounted_price = ''

            # Extract all image URLs
            image_urls = []
            picture_elements = tile.find_all('picture', class_='akamai-picture')
            for picture in picture_elements:
                source_elements = picture.find_all('source')
                for source in source_elements:
                    srcset = source.get('data-srcset', '').split(',')
                    for src in srcset:
                        url = src.strip().split(' ')[0]
                        if url:
                            image_urls.append(url)
                img_elements = picture.find_all('img')
                for img in img_elements:
                    url = img.get('data-src', '') or img.get('src', '')
                    if url:
                        image_urls.append(url)

            product_data = [
                category,
                product_id,
                product_url,
                product_name,
                price,
                discounted_price,
                ', '.join(image_urls)
            ]
            parsed_data.append(product_data)

        return parsed_data
class BalenciagaParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'balenciaga'  # Replace spaces with underscores
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        product_blocks = soup.find_all('article', class_='c-product')
        parsed_data = []

        column_names = [
            'data_pid', 'id', 'name', 'collection', 'productSMC', 'material', 'customization',
            'packshotType', 'brand', 'color', 'colorId', 'size', 'price', 'discountPrice',
            'coupon', 'subCategory', 'category', 'topCategory', 'productCategory', 'macroCategory',
            'microCategory', 'superMicroCategory', 'list', 'stock', 'productGlobalSMC', 'images', 'product_url'
        ]

        parsed_data.append(column_names)

        for block in product_blocks:
            product_data = []

            # Extract data-pid
            data_pid = block['data-pid']

            # Extract data-gtmproduct and parse JSON
            data_gtmproduct = block['data-gtmproduct']
            data_gtmproduct = html.unescape(data_gtmproduct)
            product_info = json.loads(data_gtmproduct)

            # Extract product images
            images = []
            image_container = block.find('div', class_='c-product__imageslider')
            if image_container:
                image_elements = image_container.find_all('img', class_='c-product__image')
                for img in image_elements:
                    images.append(img['src'])

            # Extract product URL
            product_url = block.find('a', class_='c-product__focus')['href']

            # Append the extracted information to the product_data list
            product_data.append(data_pid)
            product_data.append(product_info['id'])
            product_data.append(product_info['name'])
            product_data.append(product_info['collection'])
            product_data.append(product_info['productSMC'])
            product_data.append(product_info['material'])
            product_data.append(product_info['customization'])
            product_data.append(product_info['packshotType'])
            product_data.append(product_info['brand'])
            product_data.append(product_info['color'])
            product_data.append(product_info['colorId'])
            product_data.append(product_info['size'])
            product_data.append(product_info['price'])
            product_data.append(product_info['discountPrice'])
            product_data.append(product_info['coupon'])
            product_data.append(product_info['subCategory'])
            product_data.append(category)
            product_data.append(product_info['topCategory'])
            product_data.append(product_info['productCategory'])
            product_data.append(product_info['macroCategory'])
            product_data.append(product_info['microCategory'])
            product_data.append(product_info['superMicroCategory'])
            product_data.append(product_info['list'])
            product_data.append(product_info['stock'])
            product_data.append(product_info['productGlobalSMC'])
            product_data.append(', '.join(images))
            product_data.append(product_url)

            parsed_data.append(product_data)

        return parsed_data

class SaintLaurentParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'saint_laurent'  # Replace spaces with underscores
        self.directory = directory
    def parse_product_blocks(self, soup, category):
        product_blocks = soup.find_all('article', class_='c-product')
        parsed_data = []
        column_names = [
            'data_pid', 'id', 'name', 'collection', 'productSMC', 'material', 'customization',
            'packshotType', 'brand', 'color', 'colorId', 'size', 'price', 'discountPrice',
            'coupon', 'subCategory', 'category', 'topCategory', 'productCategory', 'macroCategory',
            'microCategory', 'superMicroCategory', 'list', 'stock', 'productGlobalSMC', 'images', 'product_url'
        ]
        parsed_data.append(column_names)
        for block in product_blocks:
            product_data = []
            # Extract data-pid
            data_pid = block['data-pid']
            # Extract data-gtmproduct and parse JSON
            data_gtmproduct = block['data-gtmproduct']
            data_gtmproduct = html.unescape(data_gtmproduct)
            product_info = json.loads(data_gtmproduct)
            images = []
            # Extract main product image
            main_image_container = block.find('div', class_='c-product__imagecontainerinner')
            if main_image_container:
                main_image = main_image_container.find('img', class_='c-product__image')
                if main_image:
                    if 'data-srcset' in main_image.attrs:
                        srcset = main_image['data-srcset']
                        image_urls = [url.strip().split(' ')[0] for url in srcset.split(',') if
                                      'saint-laurent.dam.kering.com' in url]
                        images.extend(image_urls)
                    elif 'data-src' in main_image.attrs:
                        image_url = main_image['data-src']
                        if 'saint-laurent.dam.kering.com' in image_url:
                            images.append(image_url)
                    elif 'src' in main_image.attrs:
                        image_url = main_image['src']
                        if 'saint-laurent.dam.kering.com' in image_url:
                            images.append(image_url)
            # Extract carousel images
            carousel_container = block.find('div', class_='c-productcarousel')
            if carousel_container:
                carousel_images = carousel_container.find_all('img', class_='c-product__image')
                for img in carousel_images:
                    if 'data-srcset' in img.attrs:
                        srcset = img['data-srcset']
                        image_urls = [url.strip().split(' ')[0] for url in srcset.split(',') if
                                      'saint-laurent.dam.kering.com' in url]
                        images.extend(image_urls)
                    elif 'data-src' in img.attrs:
                        image_url = img['data-src']
                        if 'saint-laurent.dam.kering.com' in image_url:
                            images.append(image_url)
                    elif 'src' in img.attrs:
                        image_url = img['src']
                        if 'saint-laurent.dam.kering.com' in image_url:
                            images.append(image_url)
            # Remove exact duplicate image URLs
            images = list(set(images))
            # Extract product URL
            product_url = block.find('a', class_='c-product__link')['href']
            # Append the extracted information to the product_data list
            product_data.append(data_pid)
            product_data.append(product_info['id'])
            product_data.append(product_info['name'])
            product_data.append(product_info['collection'])
            product_data.append(product_info['productSMC'])
            product_data.append(product_info['material'])
            product_data.append(product_info['customization'])
            product_data.append(product_info['packshotType'])
            product_data.append(product_info['brand'])
            product_data.append(product_info['color'])
            product_data.append(product_info['colorId'])
            product_data.append(product_info['size'])
            product_data.append(product_info['price'])
            product_data.append(product_info['discountPrice'])
            product_data.append(product_info['coupon'])
            product_data.append(product_info['subCategory'])
            product_data.append(category)
            product_data.append(product_info['topCategory'])
            product_data.append(product_info['productCategory'])
            product_data.append(product_info['macroCategory'])
            product_data.append(product_info['microCategory'])
            product_data.append(product_info['superMicroCategory'])
            product_data.append(product_info['list'])
            product_data.append(product_info['stock'])
            product_data.append(product_info['productGlobalSMC'])
            product_data.append(', '.join(images))
            product_data.append(product_url)
            parsed_data.append(product_data)
        return parsed_data

class AlexanderMcqueenParser(WebsiteParser):
    def __init__(self, base_url):
        self.brand = 'alexander_mcqueen'  # Replace spaces with underscores
        self.base_url = base_url
    def format_url(self,url):
        """ Helper function to format URLs correctly """
        return url if url.startswith('http') else 'https:' + url
    def fetch_data(self,category, base_url):
        session = requests.Session()
        retries = requests.adapters.Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
        all_products = []
        try:
            response = session.get(base_url.format(clothing_category=category, page=0), headers=headers)
            response.raise_for_status()
            json_data = response.json()
            total_pages = json_data['stats']['nbPages']
            total_pages = total_pages + 1
            print(f"Category: {category}, Total Pages: {total_pages}")
            for page in range(total_pages):
                print(page)
                response = session.get(base_url.format(clothing_category=category, page=page), headers=headers)
                response.raise_for_status()
                json_data = response.json()
                products = json_data['products']
                if not products:
                    print(f"No items found on Page: {page + 1}/{total_pages}")
                    continue
                for product in products:
                    images = product.get('images', [])
                    product_info = {
                        'category': category,
                        'id': product.get('id', ''),
                        'isSku': product.get('isSku', ''),
                        'isSmc': product.get('isSmc', ''),
                        'name': product.get('name', ''),
                        'microColor': product.get('microColor', ''),
                        'microColorHexa': product.get('microColorHexa', ''),
                        'color': product.get('color', ''),
                        'size': product.get('size', ''),
                        'styleMaterialColor': product.get('styleMaterialColor', ''),
                        'brightcoveId': product.get('brightcoveId', ''),
                        'images': " | ".join([self.format_url(img['src']) for img in images]),
                        'bornSeasonDesc': product.get('bornSeasonDesc', ''),
                        'macroCategory': product['categories'].get('macroCategory', ''),
                        'superMicroCategory_en_US': product['categories']['superMicroCategory'].get('en_US', ''),
                        'url': "https://www.alexandermcqueen.com" + product.get('url', ''),
                        'smcUrl': "https://www.alexandermcqueen.com" + product.get('smcUrl', ''),
                        'alternativeAsset': self.format_url(product.get('alternativeAsset', {}).get('src', '')),
                        'price_hasSalePrice': product.get('price', {}).get('hasSalePrice', ''),
                        'price_currencyCode': product.get('price', {}).get('currencyCode', ''),
                        'price_percentageOff': product.get('price', {}).get('percentageOff', ''),
                        'price_listPrice': product.get('price', {}).get('listPrice', ''),
                        'price_salePrice': product.get('price', {}).get('salePrice', ''),
                        'price_finalPrice': product.get('price', {}).get('finalPrice', '')
                    }
                    all_products.append(product_info)
                print(f"Processed {len(products)} products on Page: {page + 1}/{total_pages} for Category: {category}")
            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()

    def process_categories(self, categories):
        data = pd.DataFrame()
        for category in categories:
            category_data = self.fetch_data(category, self.base_url)
            data = pd.concat([data, category_data], ignore_index=True)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        filename = f'parser-output/alexander_mcqueen_output_{current_date}.csv'
        data.to_csv(filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        print("Complete data saved to 'alexandermcqueen_products.csv'")




class Dolce_Gabbana_Parser(WebsiteParser):
    def __init__(self):
        self.brand = 'dolce_gabbana'  # Replace spaces with underscores

    def fetch_products(self,category, bearer_token):
        base_url = "https://www.dolcegabbana.com/mobify/proxy/api/search/shopper-search/v1/organizations/f_ecom_bkdb_prd/product-search?siteId=dolcegabbana_us&q=&refine=CATEGORYGOESHERE&refine=htype%3Dvariation_group&refine=c_availableForCustomerGroupA%3DEveryone&sort=&currency=USD&locale=en&offset={offset}&limit=24"
        url = base_url.replace("CATEGORYGOESHERE", category)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Authorization': f'Bearer {bearer_token}'
        }
        all_products = []
        offset = 0

        while True:
            formatted_url = url.format(offset=offset)
            response = requests.get(formatted_url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch data: {response.status_code} - {response.text}")
                break
            data = response.json()
            products = data.get('hits', [])
            if not products:
                print("No more products to fetch.")
                break

            for product in products:
                # Properly handle and format the images
                images = product.get('image', {})  # Ensure to get the image dictionary correctly
                images_formatted = f"{images.get('link', '')} ({images.get('alt', '')})" if images else "No image"

                product_info = {
                    'category': category,
                    'productId': product.get('productId', ''),
                    'productName': product.get('productName', ''),
                    'price': product.get('price', 0),
                    'pricePerUnit': product.get('pricePerUnit', 0),
                    'currency': product.get('currency', ''),
                    'hitType': product.get('hitType', ''),
                    'productType_variationGroup': product['productType'].get('variationGroup', False),
                    'orderable': product.get('orderable', False),
                    'representedProduct_id': product['representedProduct'].get('id', ''),
                    'representedProduct_ids': ' | '.join([rp['id'] for rp in product.get('representedProducts', [])]),
                    'images': images_formatted,  # Use formatted image details here
                    'c_url': "https://www.dolcegabbana.com" + product.get('c_url', '')
                }
                all_products.append(product_info)

            print(f"Fetched {len(products)} products from offset {offset}.")
            offset += 24
            if offset >= data['total']:
                break

        return pd.DataFrame(all_products)
    def process_categories(self, categories,bearer_token):
        all_data = pd.DataFrame()
        for category in categories:
            print(f"Fetching products for category: {category}")
            category_data = self.fetch_products(category, bearer_token)
            all_data = pd.concat([all_data, category_data], ignore_index=True)
            print(f"Completed fetching for category: {category}")

        # Save the complete DataFrame to a CSV file
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        filename = f'parser-output/dolce_output_{current_date}.csv'
        all_data.to_csv(filename, index=False)
        print("Complete data saved to 'dolcegabbana_products.csv'")


class StoneIslandParser(WebsiteParser):

    def __init__(self, directory):
        self.brand = 'stone_island'  # Replace with brand name
        self.directory = directory

    # THIS WILL BE EDITED FOR EACH BRAND. THIS SHOULD BE THE ONLY CODE BEING UPDATED. MUST BE NAMED parse_product_blocks
    def parse_product_blocks(self, soup, category):
        parsed_data = []
        container_prods = soup.find('ul', {'class': 'products'})

        ##SELECT ALL BLOCKS FIRST

        articulos = container_prods.find_all('li', {'class': 'item'})
        column_names = [
            'category', 'product_title', 'product_price', 'product_discountedPrice', 'product_position',
            'product_cod10', 'product_brand', 'product_category', 'product_macro_category', 'product_micro_category',
            'product_macro_category_id', 'product_color', 'product_color_id', 'product_micro_category_id',
            'product_price_tf', 'product_discountedPrice_tf', 'product_quantity', 'product_coupon',
            'product_is_in_stock', 'a_href', 'img']
        parsed_data.append(column_names)

        for articulo in articulos:
            item_desc = articulo.find('div', {'class': 'item'})

            data_gtmproduct = item_desc['data-ytos-track-product-data']
            data_gtmproduct = html.unescape(data_gtmproduct)
            product_info = json.loads(data_gtmproduct)

            product_position = product_info['product_position']
            product_cod10 = product_info['product_cod10']

            product_brand = product_info['product_brand']
            product_category = product_info['product_category']
            product_macro_category = product_info['product_macro_category']
            product_micro_category = product_info['product_micro_category']
            product_macro_category_id = product_info['product_macro_category_id']
            product_color = product_info['product_color']
            product_color_id = product_info['product_color_id']
            product_title = product_info['product_title']

            product_price = product_info['product_price']
            product_discountedPrice = product_info['product_discountedPrice']
            product_micro_category_id = product_info['product_micro_category_id']
            product_price_tf = product_info['product_price_tf']
            product_discountedPrice_tf = product_info['product_discountedPrice_tf']

            product_quantity = product_info['product_quantity']
            product_coupon = product_info['product_coupon']
            product_is_in_stock = product_info['product_is_in_stock']

            a_href = articulo.find('a', {'class': 'itemLink'})

            a_href = a_href['href']

            img = articulo.find('img')
            img = img.get('src')

            product_data = [
                category,
                product_title,
                product_price,
                product_discountedPrice,
                product_position,
                product_cod10,
                product_brand,
                product_category,
                product_macro_category,
                product_micro_category,
                product_macro_category_id,
                product_color,
                product_color_id,
                product_micro_category_id,
                product_price_tf,
                product_discountedPrice_tf,
                product_quantity,
                product_coupon,
                product_is_in_stock,
                a_href,
                img,
            ]
            parsed_data.append(product_data)

        return parsed_data


class EtroProductParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'etro'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'user_category', 'product_id', 'product_url', 'product_name', 'price', 'discounted_price', 'image_urls'
        ]
        parsed_data.append(column_names)

        product_tiles = soup.find_all('article', class_='producttile')

        for tile in product_tiles:
            product_id = tile['data-productid'] if 'data-productid' in tile.attrs else ''
            product_url = tile.find('a', class_='producttile-gallery-inner')['href'] if tile.find('a',
                                                                                                  class_='producttile-gallery-inner') else ''
            product_name = tile.find('h2', class_='producttile-name').text.strip() if tile.find('h2',
                                                                                                class_='producttile-name') else ''

            # Price elements
            price = ''
            discounted_price = ''
            price_element = tile.find('span', class_='price--full')
            discounted_price_element = tile.find('span', class_='price--current')

            if price_element and discounted_price_element:
                price = price_element.text.strip()
                discounted_price = discounted_price_element.text.strip()
            elif discounted_price_element:
                price = discounted_price_element.text.strip()

            # Extract all image URLs
            image_urls = []
            picture_elements = tile.find_all('picture')
            for picture in picture_elements:
                source_elements = picture.find_all('source')
                for source in source_elements:
                    srcset = source.get('data-srcset', '').split(',')
                    for src in srcset:
                        url = src.strip().split(' ')[0]
                        if url:
                            image_urls.append(url)
                img_elements = picture.find_all('img')
                for img in img_elements:
                    url = img.get('data-src', '') or img.get('src', '')
                    if url:
                        image_urls.append(url)

            product_data = [
                category,
                product_id,
                product_url,
                product_name,
                price,
                discounted_price,
                ', '.join(image_urls)
            ]
            parsed_data.append(product_data)

        return parsed_data

class BalmainProductParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'balmain'
        self.directory = directory
    def parse_product_blocks(self, soup, category):

        parsed_data = []
        column_names = [
            'product_id', 'category', 'item_name', 'quantity', 'inventory_ats', 'price', 'full_price', 'discount_name',
            'pre_order', 'item_ean', 'item_master', 'item_category', 'item_category2', 'item_category3',
            'image_url', 'product_url'
        ]
        parsed_data.append(column_names)

        product_items = soup.find_all('div', class_='product-body')
        print(len(product_items))

        for item in product_items:
            full_price = None
            product_info = item.find('div', class_='product')
            if product_info:
                data_analytics = product_info['data-analytics']
                analytics_data = json.loads(html.unescape(data_analytics))
                product_data = analytics_data['product']
                product_tile = product_info.find('div', class_='product-tile')
                # print(product_tile)
                product_box = product_tile.find('div', class_='tile-box')
                price_info = product_box.find('div', class_='price')
                full_price_block = price_info.find('span', class_='strike-through list')
                if full_price_block:
                    full_price = full_price_block.find('span', class_='value')
                    full_price = full_price['content']

                images = [img['src'] for img in item.find_all('img') if img.get('src')]
                product_url = item.find('a', class_='tile-body')['href']
                if len(images) == 1:
                    image_url = images[0]
                elif len(images) >= 2:
                    image_url = images[1]
                else:
                    image_url = None

                product_data_list = [
                    product_data.get('item_id', ''),
                    category,
                    product_data.get('item_name', ''),
                    product_data.get('quantity', ''),
                    product_data.get('inventory_ats', ''),
                    product_data.get('price', ''),
                    full_price,
                    product_data.get('discount_name', ''),
                    product_data.get('pre_order', ''),
                    product_data.get('item_ean', ''),
                    product_data.get('item_master', ''),
                    product_data.get('item_category', ''),
                    product_data.get('item_category2', ''),
                    product_data.get('item_category3', ''),
                    image_url,
                    'us.balmain.com' + str(product_url)
                ]

                parsed_data.append(product_data_list)

        return parsed_data

class MonclerParser(WebsiteParser):
    def __init__(self):
        self.brand = 'moncler'  # Replace spaces with underscores
    def fetch_moncler_products(self,categories, cookie):
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
                        'variationAttributes': self.parse_variation_attributes(product.get('variationAttributes', []))
                    }
                    all_products.append(product_info)

                # Update offset to next page
                offset += len(products)
                total_count = data['data']['count']
                if offset >= total_count:
                    break

        return pd.DataFrame(all_products)

    def parse_variation_attributes(self, variation_attributes):
        # Parse and format variation attributes such as color and size
        attributes = {}
        for attr in variation_attributes:
            if 'values' in attr:
                values = ', '.join([f"{v['displayValue']} (ID: {v['id']})" for v in attr['values']])
            else:
                values = attr.get('displayValue', '')
            attributes[attr['displayName']] = values
        return attributes

    def process_categories(self, categories, cookie):
        # Fetch products
        all_data = self.fetch_moncler_products(categories, cookie)
        print(all_data.head())

        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        filename = f'parser-output/moncler_output_{current_date}.csv'
        all_data.to_csv(filename, index=False)
        print("Complete data saved to 'moncler_products.csv'")

class VersaceProductParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'versace'
        self.directory = directory
    def parse_product_blocks(self, soup, category):
        product_blocks = soup.select('.product-tile-show')
        parsed_data = []

        column_names = [
            'product_id', 'availability', 'category', 'image_url', 'list_price', 'name',
            'price', 'quantity', 'sale', 'sale_percentage', 'sale_price', 'sku',
            'stock', 'product_url', 'personalized', 'preorder', 'shoppable', 'promotional_code_name',
            'promotional_code_value', 'tax_included'
        ]
        parsed_data.append(column_names)

        for block in product_blocks:
            json_data_element = block.find('span', class_='analytics-product-data')
            if json_data_element:
                json_data = json_data_element.get('data-tracking-products', '')
                try:
                    product_info = json.loads(html.unescape(json_data))
                except json.JSONDecodeError:
                    continue  # Skip this block if JSON data is invalid or empty
            else:
                continue  # Skip if no json data element found

            product_data = [
                block['data-product-id'],
                product_info.get('product_availability'),
                product_info.get('product_category'),
                product_info.get('product_image'),
                product_info.get('product_list_price'),
                product_info.get('product_name'),
                product_info.get('product_price'),
                product_info.get('product_quantity'),
                product_info.get('product_sale'),
                product_info.get('product_sale_percentage'),
                product_info.get('product_sale_price'),
                product_info.get('product_sku'),
                product_info.get('product_stock'),
                block.find('a', class_='back-to-product-anchor-js')['href'],
                product_info.get('product_personalized'),
                product_info.get('product_preorder'),
                product_info.get('product_shoppable'),
                product_info.get('promotional_code_name'),
                product_info.get('promotional_code_value'),
                product_info.get('product_tax_included')
            ]

            parsed_data.append(product_data)

        return parsed_data
class FerragamoProductParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'ferragamo'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'product_id', 'product_url', 'product_name', 'price','old_price', 'image_urls', 'label'
        ]
        parsed_data.append(column_names)

        product_items = soup.find_all('li', class_='r23-grid--list-plp__item')

        for item in product_items:
            product_id = item.find('button', class_='r23-grid--list-plp__item__product-wishlist')['data-partnumber']
            product_link = item.find('a')
            product_url = product_link['href']
            product_name = item.find('div', class_='r23-grid--list-plp__item__info__product-name').text.strip()
            product_price = item.find('span', class_='r23-grid--list-plp__item__info__product-price-new').text.strip()
            old_product_price = item.find('s',class_='r23-grid--list-plp__item__info__product-price-old').text.strip()
            label = item.find('span', class_='r23-grid--list-plp__item__st').text if item.find('span', class_='r23-grid--list-plp__item__st') else ''

            images = item.find_all('img', class_='r23-grid--list-plp__item__img')
            image_urls = [img.get('data-src', 'src') for img in images]

            product_data = [
                product_id,
                f"https://www.ferragamo.com{product_url}",
                product_name,
                product_price,
                old_product_price,
                ', '.join(image_urls),
                label
            ]
            parsed_data.append(product_data)

        return parsed_data


class BurberryParser(WebsiteParser):

    def __init__(self, directory):
        self.brand = "burberry"
        self.directory = directory

    def parse_product_blocks(self, soup, category):

        product_blocks = soup.select('a.product-card-v2-anchor, a.redesigned-product-card__link')
        print(len(product_blocks))
        parsed_data = []

        column_names = [
            'category', 'name', 'product_id', 'product_url', 'image_url', 'full_price', 'discount_price', 'tag(s)']

        parsed_data.append(column_names)

        base_url = soup.find('meta', {'property': 'org:url'})
        if base_url:
            base_url = base_url['content']
        else:
            base_url = "https://us.burberry.com/"

        for product in product_blocks:
            name = product.select_one('.product-card-v2-title, .product-card-content__title').get_text(strip=True) if product.select_one('.product-card-v2-title, .product-card-content__title') else ''

            product_link = urljoin(base_url, product['href'])

            product_id = re.search('\-p(\d+)/?$', product_link, flags=re.I)
            product_id = product_id.group(1) if product_id else "unavailable"

            price = product.select_one('.product-card-price__current-price, .product-card-v2-price__current').get_text(
                strip=True) if product.select_one('.product-card-price__current-price, .product-card-v2-price__current') else ''

            discount_price = ""  # empty for now and can be added later if found

            image_url = product.select_one(
                '.redesigned-product-card__picture img, .product-card-v2-carousel-container__media__picture img')['src']

            tags = product.select_one('.product-card-labels__flag, .product-card-v2-carousel-labels__label')
            tags = tags.get_text(strip=True) if tags else ""

            product_data = [
                category,
                name,
                product_id,
                product_link,
                image_url,
                price,
                discount_price,
                tags
            ]

            parsed_data.append(product_data)

        return parsed_data


class KenzoParser(WebsiteParser):

    def __init__(self, directory):
        self.brand = "kenzo"
        self.directory = directory

    def parse_product_blocks(self, soup, category):

        product_blocks = soup.select("div[is='m-product-tile']")
        print(len(product_blocks))
        parsed_data = []

        column_names = [
            'category', 'name', 'product_id', 'product_url', 'image_url', 'other_images', 'full_price',
            'discount_price', 'stock', 'color', 'tag(s)']

        parsed_data.append(column_names)

        base_url = soup.find('meta', {'property': 'org:url'})
        if base_url:
            base_url = base_url['content']
            base_url = urlunparse(urlparse(base_url)[:3] + ('', '', ''))
        else:
            base_url = "https://www.kenzo.com/"

        for product in product_blocks:

            name = product.select_one('a[class*="title t-body-bold t-plain"]').get_text(strip=True)

            product_link = product.select_one('a[class*="title t-body-bold t-plain"]')
            product_link = urljoin(base_url, product_link['href'])

            product_id = product['data-pid'] if product.get('data-pid') else "unavailable"

            price = product.select_one('.prices .price-sales, .prices .price').get_text(strip=True).lower()
            price = re.sub('price\s+reduced\s+from', '', price, flags=re.I | re.S).replace('to', '').strip()

            discount_price = product.select_one('.prices .reduced-price')
            discount_price = discount_price.get_text(strip=True) if discount_price else ""

            all_images = []
            for img in product.select("[is='m-tile-images'] img"):
                image_url = self.get_biggest_image_srcset(img)
                if image_url and image_url not in all_images:
                    all_images.append(image_url)

            image_url = all_images[0] if all_images else ""

            other_images = ' , '.join(all_images[1:]) if len(all_images) > 1 else ""

            stock_status = product.select_one('.stock-state')
            stock_status = stock_status.get('aria-label') or stock_status.get_text(strip=True) if stock_status else ""

            colors_ul = product.select_one('ul[is="m-tile-color"]')
            if colors_ul:
                colors = [li.find('button')['aria-label'] for li in colors_ul.select('li') if li.find('button')]
                colors = [re.sub('color\s+product', '', color, flags=re.I).strip() for color in colors]
                colors = [color for color in colors if color]
                if colors and colors_ul.select_one('.more-color'):
                    colors.append(colors_ul.select_one('.more-color').get_text(strip=True) + " more")
                colors = ', '.join(colors)
            else:
                colors = ""

            tags = product.select_one('[is="m-product-tag"]')
            tags = tags.get_text(strip=True) if tags else ""

            product_data = [
                category,
                name,
                product_id,
                product_link,
                image_url,
                other_images,
                price,
                discount_price,
                stock_status,
                colors,
                tags
            ]

            parsed_data.append(product_data)

        return parsed_data

    def get_biggest_image_srcset(self, img_tag):
        if not img_tag or 'srcset' not in img_tag.attrs:
            if img_tag and img_tag.get('src'):
                return img_tag['src']
            return None

        srcset = img_tag['srcset']
        srcset_entries = srcset.split(',')

        images = []
        for entry in srcset_entries:
            parts = entry.strip().split(' ')
            url = parts[0]
            if len(parts) > 1:
                descriptor = parts[1]
                if descriptor.endswith('w'):
                    width = int(descriptor[:-1])
                    images.append((width, url))
                elif descriptor.endswith('x'):
                    density = float(descriptor[:-1])
                    width = density * 1920
                    images.append((width, url))
                else:
                    continue
            else:
                images.append((1920, url))

        if not images:
            return None

        biggest_image_url = max(images, key=lambda x: x[0])[1]
        return biggest_image_url
class JimmyChooParser(WebsiteParser):

    def __init__(self, directory):
        self.brand = 'jimmy_choo'  # Replace spaces with underscores
        self.directory = directory

    def parse_product_blocks(self,soup,category):
        product_blocks = soup.select('.product-tile')
        print(len(product_blocks))
        parsed_data = []
        column_names = [
            'category', 'name', 'product_id', 'product_url', 'image_url','full_price','discount_price']
        parsed_data.append(column_names)
        for product in product_blocks:
            name = product.select_one(
               '.product-name a').text.strip() if product.select_one('.product-name a') else None
            product_id = product.get('data-itemid')
            product_url = product.select_one(
               '.product-name a').get('href') if product.select_one('.product-name a') else None
            image_url_tag = product.select_one('.js-producttile_image')
            image_url = image_url_tag.get(
               'data-main-src') if image_url_tag else None
            price = product.select_one('.product-standard-price').text.strip(
            ) if product.select_one('.product-standard-price') else None
            discount_price_tag = product.select_one('.product-discount-price')
            discount_price = discount_price_tag.text.strip() if discount_price_tag else None
            product_data = [
               category,
               name,
                product_id,
              product_url,
              image_url,
             price,
          discount_price,
            ]
            parsed_data.append(product_data)
        return parsed_data


class BrunelloCucinelliParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'brunello_cucinelli'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'user_category', 'product_url', 'product_id', 'product_name', 'price', 'discounted_price', 'image_urls',
            'sizes',
            'availability', 'label'
        ]
        parsed_data.append(column_names)

        product_items = soup.find_all('div', class_='product')

        for item in product_items:
            product_url_element_list = list(item.find_all('a', class_='js-pdp-variant-link'))
            try:
                product_url_element = product_url_element_list[0] if product_url_element_list[0] else ''
                product_name_element = product_url_element_list[1] if product_url_element_list[1] else ''
            except:
                product_url_element = ''
                product_name_element = ''
            product_url = product_url_element['href'] if product_url_element else ''
            product_id = product_url_element['data-pid'] if product_url_element else ''
            product_name = product_name_element.get_text() if product_name_element else ''
            product_name = self.clean_text(product_name)


            price_element = item.find('span', class_='price')
            discounted_price_element = item.find('span', class_='sales cc-sales')

            price = ''
            discounted_price = ''

            if price_element and discounted_price_element:
                price = price_element.find('span', class_='value').text.strip() if price_element.find('span',
                                                                                                      class_='value') else ''
                discounted_price = discounted_price_element.find('span',
                                                                 class_='value').text.strip() if discounted_price_element.find(
                    'span', class_='value') else ''
            else:
                regular_price_element = item.find('span', class_='cc-price-text')
                if regular_price_element:
                    price = regular_price_element.text.strip()

            # Clean up the price and discounted price
            price = re.sub(r'[^\d.,]', '', price)
            discounted_price = re.sub(r'[^\d.,]', '', discounted_price)

            # Extract all image URLs
            image_elements = item.find_all('img')
            image_urls = [img.get('src') for img in image_elements if img.get('src')]

            # Extract sizes and availability
            sizes_list = item.find_all('li', class_='cc-size-container')
            sizes = []
            availability = []
            if sizes_list:
                for li in sizes_list:
                    size_text = li.find('label').text.strip() if li.find('label') else ''
                    sizes.append(size_text)
                    availability.append(
                        'available' if 'cc-size-no-available' not in li.get('class', []) else 'not available')

            # Extract labels (if any)
            label_elements = item.find_all('span', class_='cc-product-tag')
            labels = [label.text.strip() for label in label_elements if label.text.strip()]

            product_data = [
                category,
                product_url,
                product_id,
                product_name,
                price,
                discounted_price,
                ', '.join(image_urls),
                ', '.join(sizes),
                ', '.join(availability),
                ', '.join(labels)
            ]
            parsed_data.append(product_data)

        return parsed_data

    def clean_text(self,text):
        # Remove excessive whitespace and unwanted price or other numeric values
        text = re.sub(r'\$\d+,*\d*\.*\d*', '', text)  # Remove price
        text = re.sub(r'[\r\n]+', ' ', text)  # Replace newlines and multiple returns with a single space
        text = re.sub(r'\s{2,}', ' ', text)  # Replace multiple spaces with a single space
        return text.strip()


class DSquaredParser(WebsiteParser):

    def __init__(self, directory):
        self.brand = 'dsquared2'  # Replace with brand name
        self.directory = directory

    # THIS WILL BE EDITED FOR EACH BRAND. THIS SHOULD BE THE ONLY CODE BEING UPDATED. MUST BE NAMED parse_product_blocks
    def parse_product_blocks(self, soup, category):
        parsed_data = []
        container_prods = soup.find('div', {'id': 'productgrid'})
        articulos = container_prods.find_all('section')

        ##SELECT ALL BLOCKS FIRST

        column_names = [
            'data_id', 'name_prod', 'product_originalprice_tf', 'product_discount_tf', 'product_currentprice_tf',
            'product_instock', 'product_breadcrumb_label', 'url', 'imgs']
        parsed_data.append(column_names)

        for articulo in articulos:
            data_id = articulo.get('data-id', '')
            name_prod = articulo.get('aria-label', '')

            info_data = articulo.get('data-tc-analytics', '')
            info_data = html.unescape(info_data)
            info_data = json.loads(info_data) if info_data else None
            if info_data:
                product_originalprice_tf = info_data.get('product_originalprice_tf', '')

                product_discount_tf = info_data.get('product_discount_tf', '')
                product_currentprice_tf = info_data.get('product_currentprice_tf', '')

                product_instock = info_data.get('product_instock', '')
                product_breadcrumb_label = info_data.get('product_breadcrumb_label', '')
                url = info_data.get('product_url_page', '')

                imgs = articulo.find_all('img')
                imgs_list = []
                for img in imgs:
                    img_src = img.get('src', '')
                    imgs_list.append(img_src)

                imgs = ", ".join(imgs_list)
                product_data = [
                    data_id,
                    name_prod,
                    product_originalprice_tf,
                    product_discount_tf,
                    product_currentprice_tf,
                    product_instock,
                    product_breadcrumb_label,
                    url,
                    imgs,
                ]
                parsed_data.append(product_data)

        return parsed_data


class CelineParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'celine'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        container_prods = soup.find_all('div', class_='m-product-listing')

        column_names = [
            'product_id', 'product_name', 'product_price', 'product_color', 'category', 'image_urls'
        ]
        parsed_data.append(column_names)

        for item in container_prods:
            product_id = item.get('data-id', '')

            imgs = item.find_all('img')
            imgs_list = []
            for img in imgs:
                img_src = img.get('data-lazy-src', '') or img.get('src', '')
                imgs_list.append(img_src)

            image_urls = ", ".join(imgs_list)

            meta_div = item.find('div', class_='m-product-listing__meta')
            if meta_div:
                meta_title_div = meta_div.find('div', class_='m-product-listing__meta-title')
                product_name = meta_title_div.get_text(strip=True) if meta_title_div else ''

                color_span = meta_div.find('span', class_='a11y')
                product_color = color_span.get_text(strip=True) if color_span else ''

                price_strong = meta_div.find('strong', class_='f-body--em')
                product_price = price_strong.get_text(strip=True) if price_strong else ''
            else:
                product_name = ''
                product_color = ''
                product_price = ''

            product_data = [
                product_id,
                product_name,
                product_price,
                product_color,
                category,
                image_urls
            ]
            parsed_data.append(product_data)

        return parsed_data


class LoroPianaParser():
    ##COMPLETE
    def __init__(self):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = "https://us.loropiana.com/en/c/{category}/results?page={page}"
        self.data = pd.DataFrame()
    def format_url(self,url):
        """ Helper function to format URLs correctly """
        return f"https:{url}" if url else ''

    def safe_strip(self,value):
        """ Helper function to strip strings safely """
        return value.strip() if isinstance(value, str) else value
    def fetch_data(self,category, base_url):
        session = requests.Session()
        # Setup retry strategy
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated to use allowed_methods instead of method_whitelist
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3'}
        all_products = []  # Use a list to store product dictionaries
        try:
            response = session.get(base_url.format(category=category, page=0), headers=headers)
            response.raise_for_status()
            json_data = response.json()
            total_pages = json_data.get('pagination',{}).get('numberOfPages', 1)
            print(f"Total Pages: {total_pages}")

            for page in range(total_pages):
                response = session.get(base_url.format(category=category, page=page), headers=headers)
                response.raise_for_status()
                json_data = response.json()
                items = json_data.get('results', [])
                if not items:
                    print(f"No items found on Page: {page + 1}/{total_pages}")
                    continue

                for product in items:
                    product_info = {
                        'category': category,
                        'product_id': product.get('code',''),
                        'price': product.get('price',{}).get('value',''),
                        'currency': product.get('price', {}).get('currencyIso', ''),
                        'imageUrls': [img.get('url','') for img in product.get('images', [])],
                        'name': product.get('name',''),
                        'material': product.get('eshopMaterialCode',''),
                        'colors':[color for color in product.get('allColorVariants', [])] if product.get('allColorVariants', []) else '',
                        'url': self.format_url(product.get('url','')),
                        }
                    all_products.append(product_info)
                print(f"Processed {len(items)} products on Page: {page + 1}/{total_pages} for Category: {category}")

            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()


    def process_categories(self, categories):
        for category in categories:
            category_data = self.fetch_data(category, self.base_url)
            self.data = pd.concat([self.data, category_data], ignore_index=True)

        # Save the complete DataFrame to a CSV file
        #data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        filename = f'parser-output/loro_piana_output_{current_date}.csv'
        self.data.to_csv(filename,sep=',', index=False, quoting=csv.QUOTE_ALL)
        print(f"Complete data saved to 'loro_piana_output_{current_date}.csv'")


class MarniParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'marni'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'original_price', 'discounted_price',
            'category', 'image_urls', 'product_url'
        ]
        parsed_data.append(column_names)

        items = soup.find_all('div', class_='col-12 col-md-3 single-element show-second-image')

        for item in items:
            product_id = item.find('div', class_='product').get('data-pid', '')
            product_name = item.find('div', class_='single-element-content-detail-description').find('a').text.strip()
            product_url = item.find('div', class_='single-element-content-detail-description').find('a').get('href', '')
            category = item.get('data-category', '')

            # Extract prices
            price_div = item.find('div', class_='price')
            original_price = price_div.find('span', class_='strike-through list')
            discounted_price = price_div.find('span', class_='sales')

            if original_price:
                original_price = original_price.find('span', class_='value').text.strip()
                discounted_price = discounted_price.find('span',
                                                         class_='value').text.strip() if discounted_price else ''
            else:
                original_price = discounted_price.find('span',
                                                         class_='value').text.strip() if discounted_price else ''
                discounted_price = ''
            original_price = original_price.strip('\n\n- Original Price') if original_price else ''
            discounted_price = discounted_price.strip('\n\n- Discounted Price') if discounted_price else ''
            # Extract image URLs
            image_divs = item.find_all('img', class_='tile-image')
            image_urls = [img.get('data-srcset', '') for img in image_divs]

            product_data = [
                product_id,
                product_name,
                original_price,
                discounted_price,
                category,
                ', '.join(image_urls),
                product_url
            ]
            parsed_data.append(product_data)

        return parsed_data

class PradaParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'prada'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'price',
            'category', 'image_urls', 'product_url', 'colors'
        ]
        parsed_data.append(column_names)

        items = soup.find_all('li', class_='w-full h-auto lg:h-full')

        for item in items:
            product_card = item.find('article', class_='product-card')
            if not product_card:
                continue

            product_id = product_card.get('data-element', '')
            product_name = product_card.find('h3', class_='product-card__name').text.strip() if product_card.find('h3', class_='product-card__name') else ''
            product_url = product_card.find('a', class_='product-card__link').get('href', '') if product_card.find('a', class_='product-card__link') else ''
            category = category

            price = product_card.find('p', class_='product-card__price--new').text.strip() if product_card.find('p', class_='product-card__price--new') else ''

            # Extract image URLs
            image_divs = product_card.find_all('img', class_='product-card__picture')
            image_urls = []
            for img in image_divs:
                srcset = img.get('data-srcset', '')
                if srcset:
                    first_url = srcset.split()[0]
                    if first_url:
                        image_urls.append(first_url)

            # Extract colors
            colors = []
            color_dots = product_card.find_all('span', class_='w-3 h-3 rounded-full absolute border border-solid border-general-divider')
            for dot in color_dots:
                style = dot.get('style', '')
                color = style.split('background: ')[1][:-1] if 'background: ' in style else ''
                colors.append(color)

            product_data = [
                product_id,
                product_name,
                price,
                category,
                ', '.join(image_urls),
                product_url,
                ', '.join(colors)
            ]
            parsed_data.append(product_data)

        return parsed_data


class TodsParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'tods'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'price',
            'category', 'image_urls', 'product_url', 'colors'
        ]
        parsed_data.append(column_names)

        items = soup.find_all('div', class_='card display scrolling')

        for item in items:
            product_id = item.get('data-sku', '')
            product_link = item.find('a', class_='card-link')
            product_url = product_link.get('href', '') if product_link else ''
            product_name = product_link.get('aria-label', '').split(',')[1].strip() if product_link else ''
            price = product_link.get('aria-label', '').split(',')[-1].strip() if product_link else ''
            color = product_link.get('aria-label', '').split(',')[2].strip() if product_link else ''
            category = category

            # Extract image URLs
            img_box = item.find('div', class_='img-box')
            image_urls = []
            if img_box:
                picture = img_box.find('picture')
                if picture:
                    sources = picture.find_all('source')
                    for source in sources:
                        srcset = source.get('srcset', '')
                        if srcset:
                            first_url = srcset.split(',')[0].split()[0]
                            if first_url:
                                image_urls.append(first_url)

                    img_tag = picture.find('img')
                    if img_tag:
                        img_src = img_tag.get('data-src', '')
                        if img_src:
                            image_urls.append(img_src)

            product_data = [
                product_id,
                product_name,
                price,
                category,
                ', '.join(image_urls),
                product_url,
                color
            ]
            parsed_data.append(product_data)

        return parsed_data

class ValentinoParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'valentino'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'price', 'category',
            'image_urls', 'product_url', 'colors', 'status'
        ]
        parsed_data.append(column_names)

        items = soup.find_all('li', class_='productCard-wrapper')

        for item in items:
            product_id = item.get('data-product-sku', '')
            product_name = item.get('data-product-name', '')
            price = item.get('data-price', '0.0')
            category = category
            status = item.get('data-status', '')
            color_description = item.get('data-color-description', '')

            # Extract product URL
            product_link = item.find('a', class_='productCard__image')
            product_url = product_link.get('href', '') if product_link else ''

            # Extract image URLs from both picture classes
            image_urls = []
            image_containers = item.find_all('picture')
            for container in image_containers:
                img = container.find('img')
                if img:
                    srcset = img.get('data-srcset', '').split(', ')
                    if srcset:
                        # Get the highest resolution image
                        image_urls.append(srcset[-1].split(' ')[0])

            product_data = [
                product_id,
                product_name,
                price,
                category,
                ', '.join(image_urls),
                product_url,
                color_description,
                status
            ]
            parsed_data.append(product_data)

        return parsed_data


class JacquemusParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'jacquemus'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'price', 'category',
            'image_urls', 'product_url', 'colors', 'status'
        ]
        parsed_data.append(column_names)

        items = soup.find_all('div', class_='product__tile')

        for item in items:
            # Extract product ID and other details from data-gtmdata attribute
            gtm_data = item.find('input', class_='gtmdata')
            if gtm_data:
                data = gtm_data.get('data-gtmdata', '')
                data = json.loads(data.replace('&quot;', '"')) if data else {}
                product_id = data.get('id', '')
                product_name = data.get('name', '')
                price = data.get('price', '0.0')
                color_description = data.get('color', '')
                status = 'in stock' if data.get('in_stock', 0) == 1 else 'out of stock'
            else:
                product_id = ''
                product_name = ''
                price = '0.0'
                color_description = ''
                status = ''

            # Extract category
            category = category

            # Extract product URL
            product_title = item.find('a', class_='product__title__content')
            product_url = product_title.get('href', '') if product_title else ''

            # Extract image URLs
            image_urls = []
            images = item.find_all('img', class_='product__visuals__content')
            print(images)
            for img in images:
                main_image = img.get('src', '')
                image_urls.append(main_image)
                srcset = img.get('srcset', '').split(', ')
                for src in srcset:
                    image_urls.append(src.split(' ')[0])

            # Extract colors
            colors = []
            color_elements = item.find_all('div', class_='product__swatches__attributes__value')
            for color_element in color_elements:
                color_span = color_element.find('span')
                if color_span:
                    colors.append(color_span.text.strip())

            product_data = [
                product_id,
                product_name,
                price,
                category,
                ', '.join(image_urls),
                product_url,
                ', '.join(colors),
                status
            ]
            parsed_data.append(product_data)

        return parsed_data
