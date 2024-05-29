import os
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
        self.brand = 'stella_mccartney'  # Replace spaces with underscores
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
            'user_category', 'product_url', 'product_name', 'price', 'original_price', 'image_urls', 'sizes',
            'availability', 'label'
        ]
        parsed_data.append(column_names)

        product_items = soup.find_all('product-item', class_='product-item')

        for item in product_items:
            product_url = item.find('a', class_='product-item__aspect-ratio')['href'] if item.find('a',class_='product-item__aspect-ratio') else ''
            product_name = item.find('a', class_='product-item-meta__title').text.strip() if item.find('a',class_='product-item-meta__title') else ''

            price_element = item.find('span', class_='price--highlight')
            price = price_element.text.strip() if price_element else ''

            original_price_element = item.find('span', class_='price--compare')
            original_price = original_price_element.text.strip() if original_price_element else ''

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
                original_price,
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
            'user_category', 'product_url', 'product_name', 'price', 'original_price', 'image_urls', 'sizes',
            'availability', 'label'
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