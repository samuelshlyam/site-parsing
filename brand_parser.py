import os
import re
from urllib.parse import urljoin, urlunparse, urlparse
from bs4 import BeautifulSoup, Tag
import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import json
import html
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import datetime
import time
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
            image_container = block.find('div', class_='c-product__imagecontainer')
            if image_container:
                image_elements = image_container.find_all('img', class_='c-product__image')
                for img in image_elements:
                    images.append(img.get('src', ''))
                    images.append(img.get('data-src', ''))
                    images.append(img.get('srcset', ''))
            images = list(set(images))
            images = [image for image in images if image != '' and "/on/demandware.static/" not in image]
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


    def process_categories(self, categories,output_dir):
        for category in categories:
            category_data = self.fetch_data(category, self.base_url)
            self.data = pd.concat([self.data, category_data], ignore_index=True)
        # Save the complete DataFrame to a CSV file
        #data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")

        if not os.path.exists(output_dir):
          os.makedirs(output_dir)
        filename=os.path.join(output_dir,f"gucci_output_{current_date}.csv")
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
    ## This class parses the HTML files from the Canada Goose website.
    ## website: https://www.canadagoose.com/us/en
    def __init__(self, directory):
        self.brand = 'canada_goose'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'product_id', 'product_url', 'product_name', 'price', 'image_urls', 'color_options'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='product')

        for block in product_blocks:
            # Extract product ID from the data-pid attribute
            product_id = block.get('data-pid', 'No ID')

            # Extract product URL
            product_link = block.find('a', class_='thumb-link')
            product_url = product_link['href'] if product_link else 'No URL'

            # Extract product name
            product_name = block.find('div', class_='product-name').text.strip() if block.find('div', class_='product-name') else 'No Name'

            # Extract price
            price_element = block.find('span', class_='price-sales')
            price = price_element.find('span', class_='value').text.strip() if price_element else 'No Price'

            # Extract image URLs
            image_urls = []
            images = block.find_all('div', class_='slideritem')
            for image in images:
                img=image.find("img")
                if 'srcset' in img.attrs:
                    srcset = img['srcset'].split(', ')
                    for src in srcset:
                        image_urls.append(src.split(' ')[0])
                elif 'src' in img.attrs:
                    image_urls.append(img['src'])
                elif 'data-src' in img.attrs:
                    image_urls.append(img['data-src'])

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
            'category', 'product_id', 'product_name', 'price', 'discount_price', 'main_image_url',
            'additional_image_url',
            'product_details_url'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='product-item-info')

        for block in product_blocks:
            product_name = block.find('strong', class_='product name product-item-name').find('a').text.strip()
            full_price_element = block.find('span', class_='old-price')
            if full_price_element:
                discount_price_element = block.find('span', class_='normal-price')
                price = full_price_element.find('span', class_='price').text.strip()
                discount_price = discount_price_element.find('span', class_='price').text.strip()
            else:
                price_element = block.find('span', class_='normal-price')
                price = price_element.find('span', class_='price').text.strip()
                discount_price = ''
            product_details_url = block.find('a', class_='product-item-link')['href']

            images = block.find_all('img', alt=product_name)
            main_image_url = images[0]['src'] if images else 'No image available'
            additional_image_url = images[1]['src'] if len(images) > 1 else 'No additional image available'
            product_id = product_details_url.split("-")[-1].replace(".html", '')
            product_data_list = [
                category,
                product_id,
                product_name,
                price,
                discount_price,
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
            # product-tile__plp-images-stack
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
    def parse_product_blocks(self, soup,category):
        parsed_data = []
        column_names = [
            'product_id', 'product_name', 'product_url', 'price', 'images', 'quick_view_url','variation_count'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='product-tile-wrap')
        for block_temp in product_blocks:
            block=block_temp.find('div',class_='product')
            product_id = block.get('data-pid', '')
            product_name = block.find('a', class_='link').text.strip() if block.find('a', class_='link') else ''
            product_url = block.find('a', class_='tile-image-container')['href'] if block.find('a', class_='tile-image-container') else ''
            product_url= f"https://www.tomfordfashion.com/{product_url}" if product_url else ''

            price_element = block.find('span', class_='value')
            price = price_element.text.strip() if price_element else ''

            image_elements = block.find_all('img', class_='loaded')
            images = [img['srcset'] for img in image_elements]

            quick_view_link = block.find('a', class_='quickview')
            quick_view_url = quick_view_link['href'] if quick_view_link else ''

            variation_element = block.find('div', class_='variation-count')
            variation_count = variation_element.text.strip() if variation_element else ''

            if "-" not in product_id:
                if block:
                    product_id = self.extract_product_id(str(block_temp))
                else:
                    product_id=''

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

    def extract_product_id(self,html_content):
        # Regular expression to find the specific script tag
        pattern = r'<script>window\._gdl=window\._gdl\|\|\[];window\._gdl\.push\((.*?)\);</script>'

        # Find all matches
        matches = re.findall(pattern, html_content)

        if matches:
            # Get the first match
            data_string = matches[0]

            # Convert the string to a Python dictionary
            data = json.loads(data_string)

            # Extract the product ID
            product_id = data['d']['id']

            return product_id

        return None
class OffWhiteProductParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'off_white'  # Replace spaces with underscores
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'category', 'product_name', 'product_id', 'product_url', 'image_url', 'full_price', 'discount_price',
            'availability'
        ]
        parsed_data.append(column_names)
        main_block=soup.find("div",class_="css-1fb01a3 emnvohd7")
        product_blocks = main_block.find_all('li')

        for product in product_blocks:
            # Extract product name
            name_element = product.find('p', class_='css-1dw89jd e1i2jpfv10')
            product_name = name_element.get_text(strip=True) if name_element else ''

            # Extract product URL
            url_element = product.find('a', class_='css-1ym16s2 e1i2jpfv14')
            product_url = url_element.get('href') if url_element else ''

            # Extract product ID
            temp_id=product_url.split("-")[-1]
            product_id=temp_id
            # Extract image URL
            image_element = product.find('img', class_='css-wn0zwz er5xw931')
            image_url = image_element.get('src') if image_element else ''

            # Extract prices
            full_price = ''
            discount_price = ''
            availability = 'In stock'

            price_container = product.find('div', class_='e1i2jpfv9 css-1hril2i e1933l763')
            if price_container:
                full_price_element = price_container.find('span', class_='css-1go0pru e1933l761')
                discount_price_element = price_container.find('span', class_='css-uqjroe e1933l762')
                sale_price_element = price_container.find('span', class_='css-bks3r1 e1933l761')

                if full_price_element:
                    full_price = full_price_element.get_text(strip=True)
                if sale_price_element:
                    full_price = sale_price_element.get_text(strip=True)

                discount_price = discount_price_element.get_text(strip=True) if discount_price_element else ''

            # Check for sold-out status
            sold_out_element = product.find('div', class_='css-x9w7eo e1i2jpfv17')
            if sold_out_element and 'sold out' in sold_out_element.text.lower():
                availability = 'Sold out'

            product_data = [
                category,
                product_name,
                product_id,
                f"https://www.off---white.com{product_url}" if product_url else '',
                image_url,
                full_price,
                discount_price,
                availability
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
        self.base_url = "https://www.bally.com/_next/data/gxuqF1sbaiaHSoITbcXSx/en/category/{category}p={page}"
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
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(options=options)

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
            'Product_ID','Cod10', 'Title', 'Price', 'position', 'category', 'macro_category', 'micro_category', 'macro_category_id', 'micro_category_id', 'color', 'color_id', 'product_price', 'discountedPrice', 'price_tf', 'discountedPrice_tf', 'quantity', 'coupon', 'is_in_stock', 'list', 'url', 'img_src', 'filename'
        ]
        parsed_data.append(column_names)
        articlesChloe = soup.find_all('article', {'class': 'item'})

        for articleChloe in articlesChloe:

            product_data = []
            imgSource = articleChloe.find('img')
            if imgSource:
                imgSource = imgSource['src']

            data_pinfo = articleChloe['data-ytos-track-product-data']

            a_url = articleChloe.find('a')
            if a_url:
                a_url = a_url['href']

            product_id=''
            product_id=self.extract_product_id(a_url)


            product_info = json.loads(data_pinfo)

            product_data.append(product_id)
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
    def extract_product_id(self,product_url):
        self.driver.get(product_url)
        time.sleep(1)
        html=self.driver.page_source
        pid_text='Item code:'
        soup_pid=BeautifulSoup(html, 'html.parser') if html else ''
        if soup_pid:
            main_item = soup_pid.find('div', class_='itemdescription')
            if main_item:
                # Extract the Style ID
                style_id_text=main_item.text
                print(style_id_text)
                style_id = style_id_text.split(pid_text)[1].strip()
                print(f"Product ID: {style_id}")
                return style_id
            else:
                print(f'Product ID not found for url: {product_url}')
        else:
            print(f'Your URL is broken: {product_url}')
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
                    images.append(img.get('src',''))
                    images.append(img.get('data-src',''))
                    images.append(img.get('srcset',''))
            images=list(set(images))
            images=[image for image in images if image != '' and "/on/demandware.static/" not in image]
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

#class SaintLaurentParser(WebsiteParser):
    # def __init__(self, directory):
    #     self.brand = 'saint_laurent'  # Replace spaces with underscores
    #     self.directory = directory
    # def parse_product_blocks(self, soup, category):
    #     product_blocks = soup.find_all('article', class_='c-product')
    #     parsed_data = []
    #     column_names = [
    #         'data_pid', 'id', 'name', 'collection', 'productSMC', 'material', 'customization',
    #         'packshotType', 'brand', 'color', 'colorId', 'size', 'price', 'discountPrice',
    #         'coupon', 'subCategory', 'category', 'topCategory', 'productCategory', 'macroCategory',
    #         'microCategory', 'superMicroCategory', 'list', 'stock', 'productGlobalSMC', 'images', 'product_url'
    #     ]
    #     parsed_data.append(column_names)
    #     for block in product_blocks:
    #         product_data = []
    #         # Extract data-pid
    #         data_pid = block['data-pid']
    #         # Extract data-gtmproduct and parse JSON
    #         data_gtmproduct = block['data-gtmproduct']
    #         data_gtmproduct = html.unescape(data_gtmproduct)
    #         product_info = json.loads(data_gtmproduct)
    #         images = []
    #         # Extract main product image
    #         main_image_container = block.find('div', class_='c-product__imagecontainerinner')
    #         if main_image_container:
    #             main_image = main_image_container.find('img', class_='c-product__image')
    #             if main_image:
    #                 if 'data-srcset' in main_image.attrs:
    #                     srcset = main_image['data-srcset']
    #                     image_urls = [url.strip().split(' ')[0] for url in srcset.split(',') if
    #                                   'saint-laurent.dam.kering.com' in url]
    #                     images.extend(image_urls)
    #                 elif 'data-src' in main_image.attrs:
    #                     image_url = main_image['data-src']
    #                     if 'saint-laurent.dam.kering.com' in image_url:
    #                         images.append(image_url)
    #                 elif 'src' in main_image.attrs:
    #                     image_url = main_image['src']
    #                     if 'saint-laurent.dam.kering.com' in image_url:
    #                         images.append(image_url)
    #         # Extract carousel images
    #         carousel_container = block.find('div', class_='c-productcarousel')
    #         if carousel_container:
    #             carousel_images = carousel_container.find_all('img', class_='c-product__image')
    #             for img in carousel_images:
    #                 if 'data-srcset' in img.attrs:
    #                     srcset = img['data-srcset']
    #                     image_urls = [url.strip().split(' ')[0] for url in srcset.split(',') if
    #                                   'saint-laurent.dam.kering.com' in url]
    #                     images.extend(image_urls)
    #                 elif 'data-src' in img.attrs:
    #                     image_url = img['data-src']
    #                     if 'saint-laurent.dam.kering.com' in image_url:
    #                         images.append(image_url)
    #                 elif 'src' in img.attrs:
    #                     image_url = img['src']
    #                     if 'saint-laurent.dam.kering.com' in image_url:
    #                         images.append(image_url)
    #         # Remove exact duplicate image URLs
    #         images = list(set(images))
    #         # Extract product URL
    #         product_url = block.find('a', class_='c-product__link')['href']
    #         # Append the extracted information to the product_data list
    #         product_data.append(data_pid)
    #         product_data.append(product_info['id'])
    #         product_data.append(product_info['name'])
    #         product_data.append(product_info['collection'])
    #         product_data.append(product_info['productSMC'])
    #         product_data.append(product_info['material'])
    #         product_data.append(product_info['customization'])
    #         product_data.append(product_info['packshotType'])
    #         product_data.append(product_info['brand'])
    #         product_data.append(product_info['color'])
    #         product_data.append(product_info['colorId'])
    #         product_data.append(product_info['size'])
    #         product_data.append(product_info['price'])
    #         product_data.append(product_info['discountPrice'])
    #         product_data.append(product_info['coupon'])
    #         product_data.append(product_info['subCategory'])
    #         product_data.append(category)
    #         product_data.append(product_info['topCategory'])
    #         product_data.append(product_info['productCategory'])
    #         product_data.append(product_info['macroCategory'])
    #         product_data.append(product_info['microCategory'])
    #         product_data.append(product_info['superMicroCategory'])
    #         product_data.append(product_info['list'])
    #         product_data.append(product_info['stock'])
    #         product_data.append(product_info['productGlobalSMC'])
    #         product_data.append(', '.join(images))
    #         product_data.append(product_url)
    #         parsed_data.append(product_data)
    #     return parsed_data

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
                        'superMicroCategory_en_US': product['categories'].get('superMicroCategory',{}).get('en_US', ''),
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

    def process_categories(self, categories,output_dir):
        data = pd.DataFrame()
        for category in categories:
            category_data = self.fetch_data(category, self.base_url)
            data = pd.concat([data, category_data], ignore_index=True)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        if not os.path.exists(output_dir):
          os.makedirs(output_dir)
        filename=os.path.join(output_dir,f"alexander_mcqueen_output_{current_date}.csv")
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

        articulos = container_prods.find_all('li', {'class': 'item'}) if container_prods else []

        #COLUMN NAMES
        column_names = [
            'category', 'product_title', 'product_price', 'product_discountedPrice', 'product_position',
            'product_cod10', 'product_brand', 'product_category', 'product_macro_category', 'product_micro_category',
            'product_macro_category_id', 'product_color', 'product_color_id', 'product_micro_category_id',
            'product_price_tf', 'product_discountedPrice_tf', 'product_quantity', 'product_coupon',
            'product_is_in_stock', 'a_href', 'img']
        parsed_data.append(column_names)

        for articulo in articulos:
            item_desc = articulo.find('div', {'class': 'item'})

            data_gtmproduct = item_desc.get('data-ytos-track-product-data','') if item_desc else ''
            data_gtmproduct = html.unescape(data_gtmproduct)
            product_info = json.loads(data_gtmproduct) if data_gtmproduct else ''
            if product_info:
              product_position = product_info.get('product_position','')
              product_cod10 = product_info.get('product_cod10','')

              product_brand = product_info.get('product_brand','')
              product_category = product_info.get('product_category','')
              product_macro_category = product_info.get('product_macro_category','')
              product_micro_category = product_info.get('product_micro_category','')
              product_macro_category_id = product_info.get('product_macro_category_id','')
              product_color = product_info.get('product_color','')
              product_color_id = product_info.get('product_color_id','')
              product_title = product_info.get('product_title','')

              product_price = product_info.get('product_price','')
              product_discountedPrice = product_info.get('product_discountedPrice','')
              product_micro_category_id = product_info.get('product_micro_category_id','')
              product_price_tf = product_info.get('product_price_tf','')
              product_discountedPrice_tf = product_info.get('product_discountedPrice_tf','')
              product_quantity = product_info.get('product_quantity','')
              product_coupon = product_info.get('product_coupon','')
              product_is_in_stock = product_info.get('product_is_in_stock','')
            else:
              product_position = ''
              product_cod10 = ''
              product_brand = ''
              product_category = ''
              product_macro_category = ''
              product_micro_category = ''
              product_macro_category_id = ''
              product_color = ''
              product_color_id = ''
              product_title = ''
              product_price = ''
              product_discountedPrice = ''
              product_micro_category_id = ''
              product_price_tf = ''
              product_discountedPrice_tf = ''
              product_quantity = ''
              product_coupon = ''
              product_is_in_stock = ''

            a_href = articulo.find('a', {'class': 'itemLink'})

            a_href = a_href.get('href','')

            img = articulo.find('img')
            img = img.get('src','')

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
                images = list(set(images))
                images = [image for image in images if image != '' and "logo-sm" not in image]

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
                    ", ".join(images),
                    'us.balmain.com' + str(product_url)
                ]

                parsed_data.append(product_data_list)

        return parsed_data

class MonclerParser(WebsiteParser):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(options=options)
        self.base_url="https://www.moncler.com/on/demandware.store/{country_code}/SearchApi-Search?cgid={category}&sz=2000&start=0"
        self.country=''
    def fetch_moncler_products(self,categories,country_code):
        all_products=[]
        for category in categories:
            offset = 0
            while True:
                formatted_url = self.base_url.format(category=category,country_code=country_code)
                self.driver.get(formatted_url)
                self.country=country_code.split('/')[-1]
                response = self.driver.find_element(By.TAG_NAME, "body").text
                print(type(response))
                print(response[:10000])
                data = json.loads(response)
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
                print(f'Found {len(products)} products on offset {offset}')
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
        filename = f'parser-output/moncler_output_{self.country}_{current_date}.csv'
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
        self.brand = 'jimmy_choo'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'category', 'product_name', 'full_price', 'discount_price', 'colors', 'article_id',
            'product_url', 'color_code', 'image_urls', 'product_type', 'currency', 'description'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('li', class_='js-grid-tile')

        for product in product_blocks:
            details_element = product.find('div', class_='js-googledatalayer-data-productTile')
            details_dict = details_element.get('data-value') if details_element else ''
            if details_dict:
                details_dict = json.loads(details_dict)
                product_id = details_dict.get('id', '')
                category = details_dict.get('subcategory', '')
                product_name = details_dict.get('name', '')
                full_price = details_dict.get('base_price', '')
                discount_price = details_dict.get('price', '')
                colors = details_dict.get('color', '')
                article_id = details_dict.get('attributes', {}).get('Article_ID', '')
                product_url = details_dict.get('url', '')
                master_id = details_dict.get('masterID', '').replace('_S', '')
                color_code = product_id.replace('_S', '').replace(master_id, '')
                image_urls = details_dict.get('image_urls', [])
                product_type = details_dict.get('type', '')
                currency = details_dict.get('currency', '')
                description = details_dict.get('description', '')
            else:
                # Extract product ID
                product_id = product.get('data-itemid', '')

                # Extract product name
                name_element = product.find('h2', class_='product-name')
                product_name = name_element.get_text(strip=True) if name_element else ''

                # Extract product URL
                url_element = name_element.find('a') if name_element else None
                product_url = url_element.get('href') if url_element else ''

                # Extract image URLs
                image_urls = []
                images = product.find_all('img', class_='product-image-slider-item')
                for img in images:
                    image_urls.append(img.get('data-src', img.get('src', '')))

                # Extract prices
                full_price = ''
                discount_price = ''

                # Look for price in the price range element
                price_element = product.find('div', class_='price-range')
                if price_element:
                    full_price_tag = price_element.find('span', class_='js-st-price')
                    full_price = full_price_tag.get_text(strip=True) if full_price_tag else ''

                    discount_price_tag = price_element.find('span', class_='js-sl-price')
                    discount_price = discount_price_tag.get_text(strip=True) if discount_price_tag else ''
                # Look for prices in the standard-price element if not found in price-range
                if not full_price:
                    standard_price_element = product.find('div', class_='standart-price')
                    if standard_price_element:
                        full_price_tag = standard_price_element.find('span', class_='js-st-price')
                        full_price = full_price_tag.get_text(strip=True) if full_price_tag else ''
                if not discount_price:
                    top = product.find('div', class_='price-range')
                    if top:
                        discount_price_tag = top.find('span', class_='product-sale-price-wrap')
                        if discount_price_tag:
                            discount_price_tag = discount_price_tag.find('span', class_="js-sl-price")
                            discount_price = discount_price_tag.get_text(strip=True)

                # Extract Colors

                color_elements = product.find_all('img', class_='js-defer-image')
                colors = []
                for color in color_elements:
                    colors.append(color.get('alt'))
                colors = ', '.join(colors)

                article_id = ''
                product_type = ''
                currency = ''
                description = ''
                color_code = ''
                product_type = ''

            product_data = [
                product_id,
                category,
                product_name,
                full_price,
                discount_price,
                colors,
                article_id,
                product_url,
                color_code,
                "|".join(image_urls),
                product_type,
                currency,
                description
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
            'product_id','color_id', 'product_name', 'product_price','currency', 'product_color', 'category', 'image_urls','product_url'
        ]
        parsed_data.append(column_names)

        for item in container_prods:
            product_id = item.get('data-id', '')
            color_id=product_id.split('.')[1] if product_id and '_' not in product_id  else ''
            imgs = item.find_all('img')
            imgs_list = []
            for img in imgs:
                img_src = img.get('data-lazy-src', '') or img.get('src', '')
                if img_src:
                    img_src=img_src.split("?")[0]
                imgs_list.append(img_src)

            image_urls = ", ".join(imgs_list)

            meta_div = item.find('div', class_='m-product-listing__meta')
            link = item.find('a', href=True)
            product_url = link['href']
            category_internal=link.get('category','')
            if meta_div:
                meta_title_div = meta_div.find('div', class_='m-product-listing__meta-title')
                product_name = meta_title_div.get_text(strip=True) if meta_title_div else ''

                color_span = meta_div.find('span', class_='a11y')
                product_color = color_span.get_text(strip=True) if color_span else ''
                product_color=product_color.split("; ")[1] if product_color else ''

                price_strong = meta_div.find('strong', class_='f-body--em')
                product_price = price_strong.get_text(strip=True) if price_strong else ''
                if product_price:
                    price=product_price.split(' ')[0]
                    currency=product_price.split(' ')[1]
                else:
                    price = ''
                    currency = ''
            else:
                product_name = ''
                product_color = ''
                price = ''
                currency=''

            product_data = [
                product_id,
                color_id,
                product_name,
                price,
                currency,
                product_color,
                category_internal,
                image_urls,
                product_url
            ]
            parsed_data.append(product_data)

        return parsed_data


# class LoroPianaParser():
#     ##COMPLETE
#     def __init__(self):
#         # Initialize with common base URL and empty DataFrame to accumulate results
#         self.base_url = "https://us.loropiana.com/en/c/{category}/results?page={page}"
#         self.data = pd.DataFrame()
#     def format_url(self,url):
#         """ Helper function to format URLs correctly """
#         return f"https:{url}" if url else ''
#
#     def safe_strip(self,value):
#         """ Helper function to strip strings safely """
#         return value.strip() if isinstance(value, str) else value
#     def fetch_data(self,category, base_url):
#         session = requests.Session()
#         # Setup retry strategy
#         retries = Retry(
#             total=5,
#             backoff_factor=1,
#             status_forcelist=[429, 500, 502, 503, 504],
#             allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated to use allowed_methods instead of method_whitelist
#         )
#         session.mount("https://", HTTPAdapter(max_retries=retries))
#
#         headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3'}
#         all_products = []  # Use a list to store product dictionaries
#         try:
#             response = session.get(base_url.format(category=category, page=0), headers=headers)
#             response.raise_for_status()
#             json_data = response.json()
#             total_pages = json_data.get('pagination',{}).get('numberOfPages', 1)
#             print(f"Total Pages: {total_pages}")
#
#             for page in range(total_pages):
#                 response = session.get(base_url.format(category=category, page=page), headers=headers)
#                 response.raise_for_status()
#                 json_data = response.json()
#                 items = json_data.get('results', [])
#                 if not items:
#                     print(f"No items found on Page: {page + 1}/{total_pages}")
#                     continue
#
#                 for product in items:
#                     product_info = {
#                         'category': category,
#                         'product_id': product.get('code',''),
#                         'price': product.get('price',{}).get('value',''),
#                         'currency': product.get('price', {}).get('currencyIso', ''),
#                         'imageUrls': [img.get('url','') for img in product.get('images', [])],
#                         'name': product.get('name',''),
#                         'material': product.get('eshopMaterialCode',''),
#                         'colors':[color for color in product.get('allColorVariants', [])] if product.get('allColorVariants', []) else '',
#                         'url': self.format_url(product.get('url','')),
#                         }
#                     all_products.append(product_info)
#                 print(f"Processed {len(items)} products on Page: {page + 1}/{total_pages} for Category: {category}")
#
#             return pd.DataFrame(all_products)
#         except requests.exceptions.RequestException as e:
#             print(f"An error occurred: {e}")
#             return pd.DataFrame()
#
#
#     def process_categories(self, categories):
#         for category in categories:
#             category_data = self.fetch_data(category, self.base_url)
#             self.data = pd.concat([self.data, category_data], ignore_index=True)
#
#         # Save the complete DataFrame to a CSV file
#         #data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
#         current_date = datetime.datetime.now().strftime("%m_%d_%Y")
#         filename = f'parser-output/loro_piana_output_{current_date}.csv'
#         self.data.to_csv(filename,sep=',', index=False, quoting=csv.QUOTE_ALL)
#         print(f"Complete data saved to 'loro_piana_output_{current_date}.csv'")


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
            original_price = original_price.replace(r'\n\n- Original Price', '') if original_price else ''
            discounted_price = discounted_price.replace(r'\n\n- Discounted Price', '') if discounted_price else ''
            # Extract image URLs
            image_divs = item.find_all('img', class_='ls-is-cached lazyloaded')
            image_urls = []
            for img in image_divs:
                srcset = img.get('srcset', '')
                if srcset:
                    # Extract all URLs from srcset
                    urls = re.findall(r'(https?://\S+)(?=\s\d+w)', srcset)
                    # Add the largest image (last URL) to the list
                    if urls:
                        image_urls.append(urls[-1])

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
            'category', 'image_urls', 'product_url'
        ]
        parsed_data.append(column_names)

        items = soup.find_all('li', class_='w-full h-auto lg:h-full')

        for item in items:
            product_card = item.find('article', class_='product-card')
            if not product_card:
                continue

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
            product_id=product_url.split("/")[-1]
            product_data = [
                product_id,
                product_name,
                price,
                category,
                '| '.join(image_urls),
                product_url
            ]
            parsed_data.append(product_data)

        return parsed_data


# class TodsParser(WebsiteParser):
#     def __init__(self, directory):
#         self.brand = 'tods'
#         self.directory = directory
#
#     def parse_product_blocks(self, soup, category):
#         parsed_data = []
#
#         column_names = [
#             'product_id', 'product_name', 'price',
#             'category', 'image_urls', 'product_url', 'colors'
#         ]
#         parsed_data.append(column_names)
#
#         items = soup.find_all('div', class_='card display scrolling')
#
#         for item in items:
#             product_id = item.get('data-sku', '')
#             product_link = item.find('a', class_='card-link')
#             product_url = product_link.get('href', '') if product_link else ''
#             product_name = product_link.get('aria-label', '').split(',')[1].strip() if product_link else ''
#             price = product_link.get('aria-label', '').split(',')[-1].strip() if product_link else ''
#             color = product_link.get('aria-label', '').split(',')[2].strip() if product_link else ''
#             category = category
#
#             # Extract image URLs
#             img_box = item.find('div', class_='img-box')
#             image_urls = []
#             if img_box:
#                 picture = img_box.find('picture')
#                 if picture:
#                     sources = picture.find_all('source')
#                     for source in sources:
#                         srcset = source.get('srcset', '')
#                         if srcset:
#                             first_url = srcset.split(',')[0].split()[0]
#                             if first_url:
#                                 image_urls.append(first_url)
#
#                     img_tag = picture.find('img')
#                     if img_tag:
#                         img_src = img_tag.get('data-src', '')
#                         if img_src:
#                             image_urls.append(img_src)
#
#             product_data = [
#                 product_id,
#                 product_name,
#                 price,
#                 category,
#                 ', '.join(image_urls),
#                 product_url,
#                 color
#             ]
#             parsed_data.append(product_data)
#
#         return parsed_data

class ValentinoParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'valentino'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'price', 'discount_price' 'category',
            'image_urls', 'product_url', 'colors', 'status'
        ]
        parsed_data.append(column_names)

        items = soup.find_all('li', class_='productCard-wrapper')

        for item in items:
            product_id = item.get('data-product-sku', '')
            product_name = item.get('data-product-name', '')
            price = item.get('data-full-price', '')
            discount_price = item.get('data-price', '')
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
                discount_price,
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
            'product_id', 'color_id', 'product_name', 'price', 'discount_price', 'category',
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
                category_internal=data.get('category','')
                color_description = data.get('color', '')
                status = 'in stock' if data.get('in_stock', 0) == 1 else 'out of stock'
            else:
                product_id = ''
                product_name = ''
                price = '0.0'
                color_description = ''
                status = ''
                category_internal=''

            if not category_internal:
                category_internal=category

            # Extract discount price
            price_element=item.find('div', class_='product__price')
            discount_price_element=price_element.find('span', class_='product__price__value -saled')
            discount_price=discount_price_element.text.strip() if discount_price_element else ''

            # Extract category
            category = category

            # Extract product URL
            product_title = item.find('a', class_='product__title__content')
            product_url = product_title.get('href', '') if product_title else ''

            # Extract image URLs
            image_urls = []
            images = item.find_all('img', class_='product__visuals__content')
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
            color_id=product_id.split('-')[-1]
            product_data = [
                product_id,
                color_id,
                product_name,
                price,
                discount_price,
                category_internal,
                ', '.join(image_urls),
                product_url,
                ', '.join(colors),
                status
            ]
            parsed_data.append(product_data)

        return parsed_data



class LouboutinParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'christian_louboutin'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'price', 'category',
            'image_urls', 'product_url','color', 'material', 'season'
        ]
        parsed_data.append(column_names)

        rows=soup.find_all('div', class_='row-product')
        for row in rows:
            items = row.find_all('div', class_='product-item-info')
            for item in items:
              url_piece=item.find('a',class_="product-item-link")
              product_url=url_piece.get('href') if url_piece else ''
              price=item.find('span', class_='price')
              price=price.text.strip() if price else ''
              name=item.find('p', class_='m-0')
              name=name.text.strip() if name else ''

              # Extract image URLs
              image = item.find('img', class_='photo')
              image=image.get('src','') if image else ''

              product_id,color,material,season=self.extract_product_page_info(product_url)


              product_data = [
                  product_id,
                  name,
                  price,
                  category,
                  image,
                  product_url,
                  color,
                  material,
                  season
              ]
              parsed_data.append(product_data)

        return parsed_data
    def extract_product_page_info(self, product_url):
        print(f"Processing URL: {product_url}")
        html=self.open_link(product_url)
        pid_text = 'Reference :'
        color_text='Color :'
        material_text='Material :'
        season_text='Collection :'
        soup_pid=BeautifulSoup(html, 'html.parser') if html else ''
        if soup_pid:
            details_item=soup_pid.find('div',class_='additional-attributes-wrapper')
            p_items = details_item.find_all('p') if details_item else None
            if not p_items:
                return '', '', '', ''
            style_id_item=''
            color_item=''
            material_item=''
            season_item=''
            for item in p_items:
              if pid_text in item.text:
                style_id_item=item.text.strip()
              if color_text in item.text:
                color_item=item.text.strip()
              if material_text in item.text:
                material_item=item.text.strip()
              if season_text in item.text:
                season_item=item.text.strip()
            # Extract the Style I
            print(f"This is the item that contains style ID: {style_id_item}")
            style_id_list=style_id_item.split(pid_text) if style_id_item else []
            style_id = style_id_item.split(pid_text)[1].strip() if len(style_id_list)>1 else ''
            print(f"Product ID: {style_id}")

            # Extract the color
            print(f"This is the item that contains color: {color_item}")
            color_list=color_item.split(color_text) if color_item else []
            color = color_item.split(color_text)[1].strip() if len(color_list)>1 else ''
            print(f"Color: {color}")

            # Extract the material
            print(f"This is the item that contains material: {material_item}")
            material_list=material_item.split(material_text) if material_item else []
            material = material_item.split(material_text)[1].strip() if len(material_list)>1 else ''
            print(f"Material: {material}")

            # Extract the season
            print(f"This is the item that contains season: {season_item}")
            season_list=season_item.split(season_text) if season_item else []
            season = season_item.split(season_text)[1].strip() if len(season_list)>1 else ''
            print(f"Season: {season}")
            return style_id, color, material, season

        else:
            print(f'Your URL is broken: {product_url}')
            return '', '', '', ''


class PalmAngelsParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'palm_angels_old'  # Assuming 'farfetch' as the brand based on the HTML
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'price', 'category',
            'image_urls', 'product_url', 'sale_price', 'original_price', 'discount'
        ]
        parsed_data.append(column_names)

        items = soup.find_all('div', class_='css-u7k64p')  # Targeting the product card class

        for item in items:
            # Extract product URL from product title link
            product_title = item.find('a', class_='css-1kcohcr')
            product_url = product_title.get('href', '') if product_title else ''
            product_url=f"https://www.palmangels.com{product_url}"

            product_id=product_url.split("-")[-1]



            # Extract product name from product title text
            product_name_element = item.find('h2', class_='css-869f5i')
            product_name = product_name_element.text.strip() if product_name_element else ''

            # Extract image URLs from image sources
            image_urls = []
            images = item.find_all('img', class_='css-x5s4ri')
            for img in images:
                image_urls.append(img.get('src', ''))

            # Extract price details
            price_container = item.find('div', class_='css-1vwkltk')  # Find the price container
            if price_container:
                # Check for sale price first (assuming it's displayed prominently)
                sale_price_element = price_container.find('span', class_='css-nh3e0y')
                if sale_price_element:  # If sale price exists, use that and original price
                    sale_price = sale_price_element.text.strip() if sale_price_element else ''
                    original_price_element = price_container.find('span', class_='css-2droiu')
                    original_price = original_price_element.text.strip() if original_price_element else ''
                    discount_element = price_container.find('span', class_='css-hledai')
                    discount = discount_element.text.strip() if discount_element else ''
                else:  # If no sale price, use the regular price
                    original_price_element = price_container.find('span', class_='css-ltnzhu')
                    original_price = original_price_element.text.strip() if original_price_element else ''
                    sale_price = ''
                    discount = ''
            else:
                sale_price = ''
                original_price = ''
                discount = ''

            # Colors are not explicitly available in this HTML structure


            product_data = [
                product_id,  # Assuming product ID is not available
                product_name,
                original_price,  # Use sale price if available
                category,
                ', '.join(image_urls),
                product_url,
                sale_price,
                original_price,
                discount
            ]
            parsed_data.append(product_data)

        return parsed_data

class MooseKnucklesParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'moose_knuckles'  # Assuming 'Moose Knuckles' as the brand
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'price', 'category',
            'image_urls', 'product_url', 'colors', 'sale_price', 'original_price'
        ]
        parsed_data.append(column_names)

        items = soup.find_all('div', class_='ProductTile_productitem-block__2sZ1u')  # Target product blocks

        for item in items:
            # Extract product URL from product title link
            product_title = item.find('a', class_='ProductTile_productimg-link__MpSEW')
            product_url = product_title.get('href', '') if product_title else ''

            # Extract product name directly from the title text with proper class selection
            product_name_element = item.find('span', class_='ProductTile_productname-link__3X5yR')
            product_name = product_name_element.text.strip() if product_name_element else ''

            # Rest of the code remains the same for extracting image, colors, and prices

            # Extract image URL from product image
            image_container = item.find('div', class_='ProductTile_productimage-block__3Djn2')
            image_element = image_container.find('img', class_='ProductTile_product-img__2vdMI')
            image_url = image_element.get('src', '') if image_element else ''

            # Extract colors (assuming color information is in the swatches)
            colors = []
            color_list = item.find('ul', class_='color_id OptionColorTiles_optionColorTiles__2WXHX')
            if color_list:
                color_items = color_list.find_all('li')
                for color_item in color_items:
                    color_info = color_item.find('span', class_='relative')
                    color_text = color_info.text.strip() if color_info else ''
                    colors.append(color_text)

            # Extract price directly from the price container
            price_container = item.find('div', class_='product-price configurableproduct')
            price = price_container.text.strip() if price_container else ''

            # Assuming no sale price or discount information available
            try:
                sale_price = price.split("$")[2]
            except:
                sale_price=''
            original_price = price.split("$")[1] if price.split("$")[1] else ''
            price=original_price
            product_id=product_url.split("-")[-1]
            if not product_id.startswith("m"):
                product_id = product_url.split("-")[-2]

            product_data = [
                product_id,  # Assuming product ID is not available
                product_name,
                price,
                category,
                image_url,
                product_url,
                ', '.join(colors),
                sale_price,
                original_price
            ]
            parsed_data.append(product_data)

        return parsed_data

class AcneStudiosParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'acne_studios'  # Assuming 'acne_studios' as the brand based on the HTML
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'price', 'category',
            'image_urls', 'product_url', 'colors', 'sale_price', 'original_price', 'discount'
        ]
        parsed_data.append(column_names)

        # Target the tile class containing product information
        items = soup.find_all('div', class_='tile tile--span-4 tile--has-link product-tile')

        for item in items:
            # Extract product URL from product title link
            product_title_link = item.find('a', class_='tile__link')
            product_url = product_title_link.get('href', '') if product_title_link else ''

            # Extract product name from product title text
            product_name_element = item.find('div', class_='product-tile__name')
            product_name = product_name_element.find('a').text.strip() if product_name_element else ''
            product_id=None
            # Extract image URLs from image sources
            image_urls = []
            images = item.find_all('img', class_='lazyautosizes')
            for image in images:
                image_url = image.get('data-src', '')
                if not product_id:
                    product_id=image.get('alt','')
                    product_id=product_id.split(',')[0]
                    product_id = product_id.split(' ')[0]
                if image_url:
                    image_urls.append(image_url)

            # Extract price details
            price_container = item.find('div', class_='product-tile__price text-mask---small-down')
            if price_container:
                original_price = price_container.text.strip()
                sale_price = ''
                discount = ''
            else:
                original_price = ''
                sale_price = ''
                discount = ''

            # Extract colors from color list (assuming 'text-mask color--gray text--no-case' contains color info)
            colors = []
            color_info = item.find('ul')
            if color_info:
                color_items = color_info.find_all('li')
                for color_item in color_items:
                    colors.append(color_item.text.strip())
            length=len(product_id) if product_id else ''
            if length != 16 or not product_id:
                product_id = self.extract_product_id(product_url)
            product_data = [
                product_id,
                product_name,
                original_price,
                category,
                ','.join(image_urls),
                product_url,
                ','.join(colors),
                sale_price,
                original_price,
                discount
            ]
            parsed_data.append(product_data)

        return parsed_data
    def extract_product_id(self,product_url):
        html=self.open_link(product_url)
        pid_text = 'Style ID:'
        soup_pid=BeautifulSoup(html, 'html.parser') if html else ''
        if soup_pid:
            style_id_item = soup_pid.find('li', string=lambda text: pid_text in text if text else False)

            if style_id_item:
                # Extract the Style ID
                style_id = style_id_item.text.split(pid_text)[1].strip()
                print(f"Product ID: {style_id}")
                return style_id
            else:
                print("Product ID not found.")
        else:
            print(f'Your URL is broken: {product_url}')


class TheRowParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'the_row'  # Assuming 'therow' as the brand based on the HTML
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'product_id', 'product_name', 'price', 'category',
            'image_urls', 'product_url', 'sale_price', 'status'
        ]
        parsed_data.append(column_names)

        # Target the product container class
        items = soup.find_all('div', class_='ProductItem')

        for item in items:
            product_id=None
            # Extract product URL from product title link
            product_title_link = item.find('a', class_='ProductItem__ImageWrapper ProductItem__ImageWrapper--withAlternateImage')
            product_url = product_title_link.get('href', '') if product_title_link else ''
            product_url= 'https://www.therow.com' + product_url
            # Extract product name from product title text
            product_name_element = item.find('h3', class_='ProductItem__Title Heading')
            product_name = product_name_element.text.strip() if product_name_element else ''

            # Extract image URLs from image sources (considering both main and alternate images)
            image_urls = []
            images = item.find_all('img', class_=['ProductItem__Image ProductItem__Image--alternate', 'ProductItem__Image'])
            for img in images:
                image_urls.append(img.get('src', ''))
                if not product_id:
                    pid_temp = img.get('src', '')
                    product_id=pid_temp.split('/')[-1].split('_')[0]
            if len(product_id)<10:
                product_id=self.extract_product_id(product_url)

            image_urls =[x for x in image_urls if x.strip()]
            # Extract price details
            price_container = item.find('div', class_='ProductItem__PriceList Heading')  # Find the price container
            if price_container:
                price_element = price_container.find('span', class_='ProductItem__Price Price Price--highlight Text--subdued')
                price = price_element.text.strip() if price_element else ''
                sale_price_element = price_container.find('span', class_='ProductItem__Price Price Price--compareAt Text--subdued')
                sale_price = sale_price_element.text.strip() if sale_price_element else ''
                if sale_price:
                  original_price=sale_price
                  sale_price=price
                else:
                    original_price = price
            else:
                sale_price = ''
                original_price = ''

            # Check for sold-out indication
            sold_out_label = item.find('span', class_='ProductItem__Label ProductItem__Label--soldOut Heading Text--subdued')
            is_sold_out = 'Yes' if sold_out_label else 'No'

            # Colors are not explicitly available in this product information snippet

            product_data = [
                product_id,
                product_name,
                original_price,
                category,
                ', '.join(image_urls),
                product_url,
                sale_price,
                is_sold_out
            ]
            parsed_data.append(product_data)

        return parsed_data
    def extract_product_id(self, product_url):
        html_content=self.open_link(product_url)
        pid_text='Style:'
        soup_pid=BeautifulSoup(html_content, 'html.parser') if html_content else ''
        if soup_pid:
            style_id_item = soup_pid.find('li', string=lambda text: pid_text in text if text else False)

            if style_id_item:
                # Extract the Style ID
                style_id = style_id_item.text.split(pid_text)[1].strip()
                print(f"Product ID: {style_id}")
                return style_id
            else:
                main_item = soup_pid.find('div',class_='product-more__content')
                style_id_item = main_item.find_all('li')
                if style_id_item:
                    style_id = style_id_item[-1].text.strip()
                    if len(style_id.split(pid_text))>1:
                        style_id=style_id.split(pid_text)[1].strip()
                        return style_id
                    print(f"Product ID: {style_id}")
                    return style_id

                print("Product ID not found.")
        else:
            print(f'Your URL is broken: {product_url}')


class ManoloBlahnikParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'manolo_blahnik'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'category', 'product_name', 'product_id', 'product_url', 'image_urls', 'price', 'discount_price',
            'description'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='item product product-item flex flex-col w-full')

        for product in product_blocks:
            # Extract product name
            name_element = product.find('h2', class_='product-info-text')
            product_name = name_element.get_text(strip=True) if name_element else ''

            # Extract product URL and ID from the 'a' tag
            url_element = product.find('a', class_='product-item-photo')
            product_url = url_element.get('href') if url_element else ''

            # Extract product ID from the onclick attribute
            onclick_text = url_element.get('onclick', '') if url_element else ''
            product_id_match = re.search(r'"id":"([^"]+)"', onclick_text)
            product_id = product_id_match.group(1) if product_id_match else ''

            # Extract image URLs
            image_urls = []
            images = product.find_all('img', class_='object-contain w-full')
            for img in images:
                image_urls.append(img.get('src'))

            # Extract price
            full_price_element = product.find('span', class_='price-regular_price')
            if not full_price_element:
                price_element = product.find('span', class_='price-final_price')
                price = price_element.get_text(strip=True) if price_element else ''
                discount_price = ''
            else:
                discount_price_element = product.find('span', class_='price-final_price')
                discount_price = discount_price_element.get_text(strip=True) if discount_price_element else ''
                price_element = product.find('span', class_='price-regular_price')
                price = price_element.get_text(strip=True) if price_element else ''

            # Extract description
            description_element = product.find('div', class_='product-info-short')
            description = description_element.get_text(strip=True) if description_element else ''

            product_data = [
                category,
                product_name,
                product_id,
                product_url,
                ', '.join(image_urls),
                price,
                discount_price,
                description,
            ]
            parsed_data.append(product_data)

        return parsed_data

class GianvitoRossiParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'gianvito_rossi'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'category', 'product_name', 'product_id', 'product_url', 'image_urls', 'price','discount_price'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('section', class_='b-product_tile')

        for product in product_blocks:
            # Extract product name
            product_name = product.get('data-product-name', '')

            # Extract product ID
            product_id = product.get('data-product-id', '')

            # Extract product URL
            url_element = product.find('a', class_='b-product_tile-image_link')
            product_url = url_element.get('href') if url_element else ''

            # Extract image URLs
            image_urls = []
            picture_elements = product.find_all('picture', class_='b-product_tile-image')
            for picture in picture_elements:
                img_tag = picture.find('img')
                if img_tag:
                    image_urls.append(img_tag.get('src', ''))

            category_element=product.find('a', class_='b-product_tile-link')
            category_dict=category_element.get('data-analytics','')
            category_dict=json.loads(category_dict) if category_dict else category
            category_internal=category_dict.get('category','')
            if not category_internal:
              category_internal=category
            # Extract price
            price_element = product.find('span', class_='b-price-item')
            price = price_element.get_text(strip=True) if price_element else ''

            discount_price_element = product.find('span', class_='b-price-item m-new')
            discount_price = discount_price_element.get_text(strip=True) if discount_price_element else ''
            if discount_price:
              price_element = product.find('span', class_='b-price-item m-old')
              price = price_element.get_text(strip=True) if price_element else ''
            product_data = [
                category_internal,
                product_name,
                product_id,
                product_url,
                ', '.join(image_urls),
                price,
                discount_price
            ]
            parsed_data.append(product_data)

        return parsed_data

class MiuMiuParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'miu_miu'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'category', 'product_name', 'product_id', 'product_url', 'image_urls', 'price'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('li', class_='h-full')

        for product in product_blocks:
            # Extract product name
            name_element = product.find('h3', class_='card__title')
            product_name = name_element.get_text(strip=True) if name_element else ''

            # Extract product URL
            url_element = product.find('a', class_='h-full')
            product_url = url_element.get('href') if url_element else ''

            # Extract product ID from URL
            product_id = product_url.split('/')[-1] if product_url else ''

            # Extract image URLs
            image_urls = []
            images = product.find_all('source')
            for img in images:
                image_urls.append(img.get('data-srcset', ''))

            # Extract price
            price_element = product.find('p', class_='card__price')
            price = price_element.get_text(strip=True) if price_element else ''

            product_data = [
                category,
                product_name,
                product_id,
                f"https://www.miumiu.com{product_url}" if product_url else '',
                ', '.join(image_urls),
                price
            ]
            parsed_data.append(product_data)

        return parsed_data


class BirkenstockParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'birkenstock'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'category', 'product_name', 'product_id', 'product_url', 'image_urls', 'full_price', 'discount_price'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('li', class_='xlt-producttile')

        for product in product_blocks:
            # Extract product name
            name_element = product.find('div', class_='product-modelname')
            product_name = name_element.get_text(strip=True) if name_element else ''
            product_name += ' ' + product.find('div', class_='product-shortname').get_text(strip=True) if product.find(
                'div', class_='product-shortname') else ''

            # Extract product URL
            url_element = product.find('a', class_='product-tile')
            product_url = url_element.get('href') if url_element else ''

            # Extract image URLs and Product ID
            product_id=None
            image_urls = []
            images = product.find_all('img', class_='standard-tileimage')
            for img in images:
                image_urls.append(img.get('src', ''))
                if not product_id:
                    product_id = ", ".join(
                        img.get('src', '').split("/")[-1].split(".jpg")[0].replace("_sole", '').split("_"))

            # Extract prices
            full_price = ''
            discount_price = ''

            price_element = product.find('span', class_='price-standard')
            if price_element:
                full_price = price_element.get_text(strip=True)

            discount_price_element = product.find('span', class_='price-promotion')
            if discount_price_element:
                discount_price = discount_price_element.get_text(strip=True)
                full_price_element = product.find('span', class_='price-strike')
                if full_price_element:
                    full_price = full_price_element.get_text(strip=True)

            product_data = [
                category,
                product_name,
                product_id,
                f"https://www.birkenstock.com{product_url}" if product_url else '',
                ', '.join(image_urls),
                full_price,
                discount_price
            ]
            parsed_data.append(product_data)

        return parsed_data

class AquazzuraParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'aquazzura'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'category', 'product_name', 'product_id', 'product_url', 'image_url', 'full_price', 'discount_price'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='wrapp-single-item')

        for product in product_blocks:
            # Extract product name
            name_element = product.find('h2', class_='card-product__info__intro__link__name')
            product_name = name_element.get_text(strip=True) if name_element else ''

            # Extract product ID
            product_id = product.find('article').get('data-sku', '')

            # Extract product URL
            url_element = product.find('a', class_='card-product__media_link')
            product_url = url_element.get('href') if url_element else ''

            # Extract image URL
            image_element = product.find('img')
            image_url = image_element.get('data-src', '') if image_element else ''

            # Extract prices
            full_price = ''
            discount_price = ''

            price_container = product.find('div', class_='product-price')
            if price_container:
                original_price_element = price_container.find('span', class_='product-price_original')
                if original_price_element:
                    full_price = original_price_element.get_text(strip=True)
                    discount_price_element = price_container.find('div')
                    if discount_price_element:
                        discount_price = discount_price_element.get_text(strip=True).split()[-1]
                else:
                    full_price_element = price_container.find('span')
                    full_price = full_price_element.get_text(strip=True) if full_price_element else ''

            product_data = [
                category,
                product_name,
                product_id,
                f"https://www.aquazzura.com{product_url}" if product_url else '',
                image_url,
                full_price,
                discount_price
            ]
            parsed_data.append(product_data)

        return parsed_data


class LoeweParser(WebsiteParser):
    ##COMPLETEZ
    def __init__(self):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = "https://www.loewe.com/mobify/proxy/api/search/shopper-search/v1/organizations/f_ecom_bbpc_prd/product-search?siteId=LOE_USA&refine=htype%3Dset%7Cvariation_group&refine=price%3D%280.01..1370000000%29&refine={category}&refine=c_LW_custom_level%3Dwomen&currency=USD&locale=en-US&offset={offset}&limit=32&c_isSaUserType=false&c_expanded=true&c_countryCode=US"
        self.data = pd.DataFrame()

    def format_url(self, url):
        """ Helper function to format URLs correctly """
        return f"https:{url}" if url else ''

    def safe_strip(self, value):
        """ Helper function to strip strings safely """
        return value.strip() if isinstance(value, str) else value

    def fetch_data(self, category, base_url, bearer_token):
        session = requests.Session()
        # Setup retry strategy
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated to use allowed_methods instead of method_whitelist
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3',
            'Authorization': f'Bearer {bearer_token}'
                }
        all_products = []  # Use a list to store product dictionaries
        try:
            offset=0
            response = session.get(base_url.format(category=category, offset=0), headers=headers)
            response.raise_for_status()
            json_data = response.json()
            items=json_data.get('hits',[])
            totalProducts=int(items[0].get('c_totalProducts','').replace(',',''))

            while offset<=totalProducts:
                response = session.get(base_url.format(category=category, offset=offset), headers=headers)
                response.raise_for_status()
                json_data = response.json()
                items = json_data.get('hits', [])
                if not items:
                    print(f"No items found on offset: {offset}")
                    continue

                for product in items:
                    product_data = product.get('c_gtm_data', {})
                    all_images = json.loads(product.get('c_allImages', '[]'))
                    color_swatches = json.loads(product.get('c_colorSwatches', '[]'))

                    product_info = {
                        # Extracting information from c_gtm_data
                        'brand': product_data.get('brand', ''),
                        'category': product_data.get('category', ''),
                        'id': product_data.get('id', ''),
                        'name': product_data.get('name', ''),
                        'price_gtm': product_data.get('price', ''),
                        'productColor': product_data.get('productColor', ''),
                        'colorId': product_data.get('colorId', ''),
                        'productEan': product_data.get('productEan', ''),
                        'productGender': product_data.get('productGender', ''),
                        'productMasterId': product_data.get('productMasterId', ''),
                        'productStock': product_data.get('productStock', ''),
                        'isDiscounted': product_data.get('isDiscounted', ''),
                        'position_gtm': product_data.get('position', ''),
                        'currency': product.get('currency', ''),
                        'image': {
                            'alt': product.get('image', {}).get('alt', ''),
                            'disBaseLink': product.get('image', {}).get('disBaseLink', ''),
                            'link': product.get('image', {}).get('link', ''),
                            'title': product.get('image', {}).get('title', '')
                        },
                        'imageUrl':product.get('image', {}).get('link', ''),
                        'orderable': product.get('orderable', False),
                        'price': product.get('price', ''),
                        'pricePerUnit': product.get('pricePerUnit', ''),
                        'productId': product.get('productId', ''),
                        'productName': product.get('productName', ''),
                        'productType': product.get('productType', {}),
                        'representedProduct': product.get('representedProduct', {}),
                        'representedProducts': product.get('representedProducts', []),
                        'c_totalProducts': product.get('c_totalProducts', ''),
                        'c_lineImagePath': product.get('c_lineImagePath', ''),
                        'c_productDetailPageURL': product.get('c_productDetailPageURL', ''),
                        'c_imageURL': product.get('c_imageURL', ''),
                        'c_isPromoPrice': product.get('c_isPromoPrice', False),
                        'c_showStandardPrice': product.get('c_showStandardPrice', False),
                        'c_salesPriceFormatted': product.get('c_salesPriceFormatted', ''),
                        'c_standardPriceFormatted': product.get('c_standardPriceFormatted', ''),
                        'c_hidePrice': product.get('c_hidePrice', False),
                        'c_colorSwatches': color_swatches,
                        'c_colorSelected': product.get('c_colorSelected', ''),
                        'c_allImages': all_images,
                        'c_LW_limiterColorBadges': product.get('c_LW_limiterColorBadges', ''),
                        'c_availabilityStatus': product.get('c_availabilityStatus', ''),
                        'c_productDetailUrlComplete': product.get('c_productDetailUrlComplete', '')
                    }
                    all_products.append(product_info)
                print(f"Processed {len(items)} products on offset: {offset} for Category: {category}")
                offset+=32
            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()

    def process_categories(self, categories,bearer_token):
        for category in categories:
            category_data = self.fetch_data(category, self.base_url,bearer_token)
            self.data = pd.concat([self.data, category_data], ignore_index=True)

        # Save the complete DataFrame to a CSV file
        # data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        filename = f'parser-output/loewe_output_{current_date}.csv'
        self.data.to_csv(filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        print(f"Complete data saved to 'loewe_output_{current_date}.csv'")

class SaintLaurentParser(WebsiteParser):
    def __init__(self):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = ("https://www.ysl.com/api/v1/category/{category}?locale={locale}&page={page}&categoryIds={category}&hitsPerPage=15")
        self.data = pd.DataFrame()

    def format_url(self, url):
        """ Helper function to format URLs correctly """
        return f"https:{url}" if url else ''

    def safe_strip(self, value):
        """ Helper function to strip strings safely """
        return value.strip() if isinstance(value, str) else value

    def fetch_data(self, category, base_url,locale):
        session = requests.Session()
        # Setup retry strategy
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated to use allowed_methods instead of method_whitelist
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3'
        }
        all_products = []  # Use a list to store product dictionaries
        try:
            response = session.get(base_url.format(category=category, page=0,locale=locale), headers=headers)
            response.raise_for_status()
            json_data = response.json()

            total_pages=json_data.get('stats',{}).get('nbPages',0)
            print(total_pages)
            for page in range(total_pages):
                response = session.get(base_url.format(category=category, page=page,locale=locale), headers=headers)
                response.raise_for_status()
                json_data = response.json()
                items = json_data.get('products', [])
                hits = json_data.get('hitsAlgolia', [])
                if not (items and hits):
                    print(f"No items found on page: {page}")
                    continue

                for product,hit in zip(items,hits):
                    price_dict=product.get('price', 0)
                    product_info = {
                        'category':product.get('categories',{}).get('productCategory',''),
                        'product_url':product.get('url',''),
                        'product_color': product.get('color', ''),
                        'product_relatedColors': [{
                            'color': color.get('color', ''),
                            'colorHex': color.get('colorHex', ''),
                            'styleMaterialColor': color.get('styleMaterialColor', ''),
                            'swatchUrl': color.get('swatchUrl', ''),
                            'employeeSaleVisible': color.get('employeeSaleVisible', False)
                        } for color in product.get('relatedColors', [])],
                        'product_styleMaterialColor': product.get('styleMaterialColor', ''),
                        'product_thumbnailUrls': product.get('thumbnailUrls', []),
                        'product_inStock': product.get('inStock', False),
                        'product_stock': product.get('stock', 0),
                        'product_categoryIds': product.get('categoryIds', []),
                        'product_ID': product.get('id', ''),
                        'product_bornSeasonDesc': product.get('bornSeasonDesc', ''),
                        'product_name': product.get('name', ''),
                        'product_microColor': product.get('microColor', ''),
                        'product_image':product.get('image',{}).get('src',''),
                        'product_images':" | ".join([image.get('srcset','') for image in product.get('images',{})]),
                        # Extract data from the second JSON (hit)
                        'hit_id': hit.get('id', ''),
                        'hit_isSku': hit.get('isSku', False),
                        'hit_size': hit.get('size', ''),
                        'hit_categories': hit.get('categories', {}),
                        'hit_imageThumbnail': hit.get('imageThumbnail', {}).get('src', ''),
                        'hit_priceDetails': hit.get('price', {}),
                        'hit_formattedSize': hit.get('formattedSize', ''),
                        'hit_swatches': [{
                            'smcId': swatch.get('smcId', ''),
                            'microColorHexa': swatch.get('microColorHexa', ''),
                            'microColor': swatch.get('microColor', ''),
                            'swatchImage': swatch.get('swatchImage', ''),
                            'url': swatch.get('url', '')
                        } for swatch in product.get('swatches', [])],
                        'price_id':price_dict.get('id',''),
                        'price_has_sale_price': price_dict.get('hasSalePrice', ''),
                        'price_currency': price_dict.get('currencyCode', ''),
                        'price_percentageOff': price_dict.get('percentageOff', ''),
                        'sale_price': price_dict.get('salePrice', ''),
                        'list_price': price_dict.get('listPrice', ''),
                        'final_price':price_dict.get('finalPrice',''),
                        'has_empl_sale':price_dict.get('hasEmployeeSalePromotion',''),
                        'isPriceOnDemand': price_dict.get('isPriceOnDemand', '')
                    }
                    all_products.append(product_info)
                print(f"Processed {len(items)} products on page: {page} for Category: {category}")
            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()

    def process_categories(self, categories, locales):
        for locale in locales:
            for category in categories:
                category_data = self.fetch_data(category, self.base_url, locale)
                self.data = pd.concat([self.data, category_data], ignore_index=True)
            # Save the complete DataFrame to a CSV file
            # data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
            current_date = datetime.datetime.now().strftime("%m_%d_%Y")
            filename = f'parser-output/YSL_output_{locale}_{current_date}.csv'
            self.data.to_csv(filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
            print(f"Complete data saved to 'YSL_output_{locale}_{current_date}.csv'")

class TodsParser(WebsiteParser):
    def __init__(self):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = ("https://www.tods.com/rest/v2/tods-us/products/search?query=:rank-asc:category:{category}&fields=NAV&currentPage=0&pageSize=1000&key=undefined&lang=en&access_token=TgPITCn5tGqje8P1IHOIdSbrvKA&Cookie={cookie}")
        self.data = pd.DataFrame()

    def format_url(self, url):
        """ Helper function to format URLs correctly """
        return f"https:{url}" if url else ''

    def safe_strip(self, value):
        """ Helper function to strip strings safely """
        return value.strip() if isinstance(value, str) else value

    def fetch_data(self, category, base_url, cookie):
        session = requests.Session()
        # Setup retry strategy
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated to use allowed_methods instead of method_whitelist
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3'
        }
        all_products = []  # Use a list to store product dictionaries
        try:
            response = session.get(base_url.format(category=category, page=0, cookie=cookie), headers=headers)
            response.raise_for_status()
            json_data = response.json()
            results=json_data.get("searchPageData",{}).get("results","")
            for result in results:
                product=result.get("product","")
                if isinstance(product,dict):
                    product_info = {
                        "category":category,
                        'aggregatedStock': product.get('aggregatedStock', ''),
                        'baseOptions': product.get('baseOptions', []),
                        'categories': product.get('categories', []),
                        'code': product.get('code', ''),
                        'color': product.get('color', ''),
                        'colorGA': product.get('colorGA', ''),
                        'colorVariantNumber': product.get('colorVariantNumber', ''),
                        'currentHero': product.get('currentHero', False),
                        'freeTextLabel': product.get('freeTextLabel', ''),
                        'galleryAltText': product.get('galleryAltText', []),
                        'hasVirtualTryOn': product.get('hasVirtualTryOn', False),
                        'isBlocked': product.get('isBlocked', False),
                        'isDiscount': product.get('isDiscount', False),
                        'name': product.get('name', ''),
                        'nameGA': product.get('nameGA', ''),
                        'price_currencyIso': product.get('price', {}).get('currencyIso', ''),
                        'price_formattedValue': product.get('price', {}).get('formattedValue', ''),
                        'price_value': product.get('price', {}).get('value', ''),
                        'primaryImageAlt': product.get('primaryImageAlt', ''),
                        'primaryImageUrl': product.get('primaryImageUrl', ''),
                        'salableStores': product.get('salableStores', False),
                        'secondaryImageAlt': product.get('secondaryImageAlt', ''),
                        'secondaryImageUrl': product.get('secondaryImageUrl', ''),
                        'stockLabel': product.get('stockLabel', ''),
                        'url': product.get('url', ''),
                        'volumePricesFlag': product.get('volumePricesFlag', False)
                    }
                else:
                    print(f"The product is of the wrong type:\n{product}")
                    break

                all_products.append(product_info)
            print(f"Processed {len(results)} for Category: {category}")
            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()

    def process_categories(self, categories, cookie):
        for category in categories:
            category_data = self.fetch_data(category, self.base_url, cookie)
            self.data = pd.concat([self.data, category_data], ignore_index=True)

        # Save the complete DataFrame to a CSV file
        # data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        filename = f'parser-output/tods_output_{current_date}.csv'
        self.data.to_csv(filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        print(f"Complete data saved to 'tods_output_{current_date}.csv'")
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
            total_pages = json_data.get('pagination', {}).get("numberOfPages",0)
            print(f"Category: {category}, Total Pages: {total_pages}")

            for page in range(total_pages):
                response = session.get(base_url.format(category=category, page=page), headers=headers)
                response.raise_for_status()
                json_data = response.json()
                items = json_data.get('results', {})
                if not items:
                    print(f"No items found on Page: {page + 1}/{total_pages}")
                    continue

                for data in items:
                    product_info = {
                        'code': self.safe_strip(data.get('code', '')),
                        'solrIsFeatured': str(data.get('solrIsFeatured', False)).lower(),
                        'invertedImages': str(data.get('invertedImages', False)).lower(),
                        'genderFluid': str(data.get('genderFluid', False)).lower(),
                        'isAvailable': str(data.get('isAvailable', False)).lower(),
                        'variantsNr': data.get('variantsNr', ''),
                        'price_currencyIso': self.safe_strip(data.get('price', {}).get('currencyIso', '')),
                        'price_value': data.get('price', {}).get('value', ''),
                        'price_priceType': self.safe_strip(data.get('price', {}).get('priceType', '')),
                        'price_formattedValue': self.safe_strip(data.get('price', {}).get('formattedValue', '')),
                        'price_minQuantity': data.get('price', {}).get('minQuantity', None),
                        'price_maxQuantity': data.get('price', {}).get('maxQuantity', None),
                        'primaryImage': self.format_url(
                            data.get('images', [])[0].get('url', '') if data.get('images') else ''),
                        'alternateGalleryImages': " | ".join(
                            [self.format_url(img.get('url', '')) for img in data.get('images', [])[1:]]),
                        'configurable': str(data.get('configurable', False)).lower(),
                        'name': self.safe_strip(data.get('name', '')),
                        'eshopMaterialCode': self.safe_strip(data.get('eshopMaterialCode', '')),
                        'gtmInfo': self.safe_strip(data.get('gtmInfo', '')),
                        'alternativeUrl': self.safe_strip(data.get('alternativeUrl', '')),
                        'relativeUrl': self.safe_strip(data.get('relativeUrl', '')),
                        'url': self.safe_strip(data.get('url', '')),
                        'colors': self.safe_strip(data.get('colors', '')),
                        'variantSizes': self.safe_strip(data.get('variantSizes', '')),
                        'allColorVariants': data.get('allColorVariants', []),
                        'productsInLook': self.safe_strip(data.get('productsInLook', '')),
                        'configurableMto': str(data.get('configurableMto', False)).lower(),
                        'configurableScarves': str(data.get('configurableScarves', False)).lower(),
                        'doubleGender': self.safe_strip(data.get('doubleGender', '')),
                        'preorderable': str(data.get('preorderable', False)).lower(),
                        'backorderable': self.safe_strip(data.get('backorderable', '')),
                        'flPreviewProduct': str(data.get('flPreviewProduct', False)).lower(),
                        'digitalUrl': self.safe_strip(data.get('digitalUrl', '')),
                        'description': self.safe_strip(data.get('description', '')),
                        'eshopValid': str(data.get('eshopValid', False)).lower(),
                        'forceMrf': str(data.get('forceMrf', False)).lower(),
                        'normalProductEshopValid': str(data.get('normalProductEshopValid', False)).lower(),
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
        print("Complete data saved to 'output_loro_piana_5_27_24.csv'")

class HernoParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'herno'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'category', 'product_name', 'product_id', 'price', 'discount_price',
            'product_url', 'image_urls', 'color_name', 'currency'
        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='b-product_tile')

        for product in product_blocks:
            category = product.get('data-category', '')
            # Extract product name
            name_element = product.find('a', class_='b-product_name')
            product_name = name_element.get_text(strip=True) if name_element else ''

            # Extract product ID and color ID
            product_id = product.get('data-itemid', '')

            # Extract product URL
            product_url = name_element.get('href', '') if name_element else ''

            # Extract image URLs
            image_element = product.find('img', class_='b-product_image')
            image_urls = []
            if image_element:
                main_image = image_element.get('data-src', '')
                alt_image = image_element.get('data-altimage', '')
                main_image_2 = f"https://us.herno.com{main_image}" if main_image else ""
                alt_image_2 = f"https://us.herno.com{alt_image}" if alt_image else ""
                image_urls = list(filter(None, [main_image_2, alt_image_2]))

            # Extract prices
            price_container = product.find('div', class_='b-product_price')
            if price_container:
                price_element = price_container.find('div', class_='b-product_price-standard')
                price = price_element.get_text(strip=True) if price_element else ''

                discount_price_element = price_container.find('span', class_='b-product_price-sales')
                discount_price = discount_price_element.get_text(
                    strip=True) if discount_price_element and not 'h-hidden' in discount_price_element.get('class',
                                                                                                           []) else ''


            else:
                price = ''
                discount_price = ''
                discount_percentage = ''

            # Extract currency
            if '$' in price:
                currency = 'USD'  # Assuming USD based on the $ sign in prices
            else:
                currency = ''
            # Extract color name
            color_name = product.get('data-variant', '')

            # These fields are not directly available in the given HTML

            # Clean up prices
            price = re.sub(r'[^\d.]', '', price)
            discount_price = re.sub(r'[^\d.]', '', discount_price)

            product_data = [
                category,
                product_name,
                product_id,
                price,
                discount_price,
                f"https://us.herno.com{product_url}" if product_url else '',
                '|'.join(image_urls),  # Join multiple image URLs with a separator
                color_name,
                currency
            ]
            parsed_data.append(product_data)

        return parsed_data

class LanvinParser(WebsiteParser):
    def __init__(self, directory):
        self.brand = 'lanvin'
        self.directory = directory

    def parse_product_blocks(self, soup, category):
        parsed_data = []

        column_names = [
            'category', 'product_id', 'price',
            'product_url', 'image_urls', 'name', 'currency'

        ]
        parsed_data.append(column_names)

        product_blocks = soup.find_all('div', class_='product-item')
        for product in product_blocks:
            # Extract product name
            name_element = product.find('p', class_='sr-product-title')
            name = name_element.find('a').get_text(strip=True) if name_element else ''

            # Extract product URL
            product_url = name_element.find('a')['href'] if name_element else ''
            product_url=f"https://us.lanvin.com{product_url}" if product_url else ''
            product_id=self.extract_product_id(product_url)

            # Extract price
            price_element = product.find('p', class_='product-price')
            price = price_element.get_text(strip=True) if price_element else ''

            # Extract currency
            currency = 'USD' if '$' in price else ''

            # Clean up price
            price = re.sub(r'[^\d.]', '', price)

            # Extract image URLs
            image_elements = product.find_all('div', class_='image')
            image_urls = []
            for img in image_elements:
                img_src = img.find('img')
                if img_src and 'data-srcset' in img_src.attrs:
                    srcset = img_src['data-srcset']
                    highest_res_img = srcset.split(',')[-1].split()[0]
                    image_urls.append(highest_res_img)

            product_data = [
                category,
                product_id,
                price,
                product_url,
                '|'.join(image_urls),
                name,
                currency
            ]
            parsed_data.append(product_data)

        return parsed_data
    def extract_product_id(self, product_url):
        html_content=self.open_link(product_url)
        soup_pid=BeautifulSoup(html_content, 'html.parser') if html_content else ''
        if soup_pid:
            style_id_item = soup_pid.find('span',class_='bodyBase')
            style_id = style_id_item.text.strip() if style_id_item else ''
            if style_id:
                print(f"Found Product ID: {style_id}")
                return style_id

            print("Product ID not found.")
            return style_id
        else:
            print(f'Your URL is broken: {product_url}')
            return ''


