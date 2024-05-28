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

    def parse_website(self, source, category):
        return super().parse_website(source, lambda soup: self.parse_product_blocks(soup, category))

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
    def parse_directory(self, directory_path):
        all_data = []
        header_added = False
        total_files = len([f for f in os.listdir(directory_path) if f.endswith('.txt') or f.endswith('.html')])
        processed_files = 0

        print(f"Found {total_files} HTML files in the directory.")
        print("Processing files...")

        for filename in os.listdir(directory_path):
            if filename.endswith('.txt') or filename.endswith('.html'):
                file_path = os.path.join(directory_path, filename)
                category = os.path.splitext(filename)[0]  # Use the filename as the category

                tsv_output = self.parse_website(file_path, category)

                if not header_added:
                    all_data.append(tsv_output[0])  # Add the header row only once
                    header_added = True

                # Add the filename as a new column to the parsed data
                for row in tsv_output[1:]:
                    row.append(filename)
                    all_data.append(row)

                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

        # # Add the 'filename' column name to the header row
        # all_data[0].append('filename')

        print("Writing data to CSV file...")
        #self.write_to_tsv(output_file, all_data)
        self.write_to_csv(all_data)

        print(f"Parsing completed. CSV file saved as: {self.directory}")

        return all_data

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
        
    def parse_website(self, source, category):
        return super().parse_website(source, lambda soup: self.parse_product_blocks(soup, category))

    def parse_product_blocks(self, soup, category):
        parsed_data = []
        column_names = [
          'product_id','category', 'product_name', 'description', 'price', 'main_image_url',
            'additional_image_url', 'product_details_url','filename'
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
    def parse_directory(self, directory_path):
        all_data = []
        header_added = False
        total_files = len([f for f in os.listdir(directory_path) if f.endswith('.txt') or f.endswith('.html')])
        processed_files = 0

        print(f"Found {total_files} HTML files in the directory.")
        print("Processing files...")

        for filename in os.listdir(directory_path):
            if filename.endswith('.txt')  or filename.endswith('.html'):
                file_path = os.path.join(directory_path, filename)
                category = os.path.splitext(filename)[0]  # Use the filename as the category

                tsv_output = self.parse_website(file_path, category)

                if not header_added:
                    all_data.append(tsv_output[0])  # Add the header row only once
                    header_added = True

                # Add the filename as a new column to the parsed data
                for row in tsv_output[1:]:
                    row.append(filename)
                    all_data.append(row)

                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

        print("Writing data to CSV file...")
        # self.write_to_tsv(output_file, all_data)
        self.write_to_csv(all_data)

        print(f"Parsing completed. CSV file saved as: {self.directory}")

        return all_data

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
    
    def parse_website(self, source, category):
        return super().parse_website(source, lambda soup: self.parse_product_blocks(soup, category))

    def parse_directory(self, directory_path):
        all_data = []
        header_added = False
        total_files = len([f for f in os.listdir(directory_path) if f.endswith('.txt') or f.endswith('.html')])
        processed_files = 0

        print(f"Found {total_files} HTML files in the directory.")
        print("Processing files...")

        for filename in os.listdir(directory_path):
            if filename.endswith('.txt') or filename.endswith('.html'):
                file_path = os.path.join(directory_path, filename)
                category = os.path.splitext(filename)[0]  # Use the filename as the category

                tsv_output = self.parse_website(file_path, category)

                if not header_added:
                    tsv_output[0].append('filename')  # Add the new column name for filename
                    all_data.append(tsv_output[0])  # Add the header row only once
                    header_added = True

                # Add the filename as a new column to the parsed data
                for row in tsv_output[1:]:
                    row.append(filename)
                    all_data.append(row)

                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

        print("Writing data to CSV file...")
        self.write_to_csv(all_data)


        return all_data
class CanadaGooseProductParser(WebsiteParser):
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
            image_urls = [img['data-src'] for img in images if 'data-src' in img.attrs] or ['No images']

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
    
    def parse_website(self, source, category):
        return super().parse_website(source, lambda soup: self.parse_product_blocks(soup, category))

    def parse_directory(self, directory_path, output_file):
        all_data = []
        header_added = False
        total_files = len([f for f in os.listdir(directory_path) if f.endswith('.txt')])
        processed_files = 0

        print(f"Found {total_files} HTML files in the directory.")
        print("Processing files...")

        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                category = os.path.splitext(filename)[0]  # Use the filename as the category

                tsv_output = self.parse_website(file_path, category)

                if not header_added:
                    tsv_output[0].append('filename')  # Add the new column name for filename
                    all_data.append(tsv_output[0])  # Add the header row only once
                    header_added = True

                # Add the filename as a new column to the parsed data
                for row in tsv_output[1:]:
                    row.append(filename)
                    all_data.append(row)

                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

        print("Writing data to CSV file...")
        self.write_to_csv(output_file, all_data)

        print(f"Parsing completed. CSV file saved as: {output_file}")

        return all_data

class VejaProductParser(WebsiteParser):
    def parse_website(self, source, category):
        return super().parse_website(source, lambda soup: self.parse_product_blocks(soup, category))
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

    def parse_directory(self, directory_path, output_file):
        all_data = []
        header_added = False
        total_files = len([f for f in os.listdir(directory_path) if f.endswith('.txt')])
        processed_files = 0

        print(f"Found {total_files} HTML files in the directory.")
        print("Processing files...")

        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                category = os.path.splitext(filename)[0]  # Use the filename as the category

                tsv_output = self.parse_website(file_path, category)

                if not header_added:
                    tsv_output[0].append('filename')  # Add the new column name for filename
                    all_data.append(tsv_output[0])  # Add the header row only once
                    header_added = True

                # Add the filename as a new column to the parsed data
                for row in tsv_output[1:]:
                    row.append(filename)
                    all_data.append(row)

                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

        print("Writing data to CSV file...")
        self.write_to_csv(output_file, all_data)

        print(f"Parsing completed. CSV file saved as: {output_file}")

        return all_data
    
class StellaProductParser(WebsiteParser):

    ## This class parses the HTML files from the Bottega Veneta website.
    ## website: https://www.stellamccartney.com
    def __init__(self, directory):
        self.brand = 'stella_mccartney'  # Replace spaces with underscores
        self.directory = directory

    def parse_website(self, source, category):
        return super().parse_website(source, lambda soup: self.parse_product_blocks(soup, category))

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

    def parse_directory(self, directory_path):
        all_data = []
        header_added = False
        total_files = len([f for f in os.listdir(directory_path) if f.endswith('.txt') or f.endswith('.html')])
        processed_files = 0

        print(f"Found {total_files} HTML files in the directory.")
        print("Processing files...")

        for filename in os.listdir(directory_path):
            if filename.endswith('.txt') or filename.endswith('.html'):
                file_path = os.path.join(directory_path, filename)
                category = os.path.splitext(filename)[0]  # Use the filename as the category

                tsv_output = self.parse_website(file_path, category)

                if not header_added:
                    tsv_output[0].append('filename')  # Add the new column name for filename
                    all_data.append(tsv_output[0])  # Add the header row only once
                    header_added = True

                # Add the filename as a new column to the parsed data
                for row in tsv_output[1:]:
                    row.append(filename)
                    all_data.append(row)

                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

        print("Writing data to CSV file...")
        self.write_to_csv(all_data)

        print(f"Parsing completed. CSV file saved as: {self.directory}")

        return all_data
    
class TomFordProductParser(WebsiteParser):
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
    
    def parse_website(self, source, category):
        return super().parse_website(source, lambda soup: self.parse_product_blocks(soup, category))
    def parse_directory(self, directory_path, output_file):
        all_data = []
        header_added = False
        total_files = len([f for f in os.listdir(directory_path) if f.endswith('.txt')])
        processed_files = 0

        print(f"Found {total_files} HTML files in the directory.")
        print("Processing files...")

        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                category = os.path.splitext(filename)[0]  # Use the filename as the category

                tsv_output = self.parse_website(file_path, category)

                if not header_added:
                    tsv_output[0].append('filename')  # Add the new column name for filename
                    all_data.append(tsv_output[0])  # Add the header row only once
                    header_added = True

                # Add the filename as a new column to the parsed data
                for row in tsv_output[1:]:
                    row.append(filename)
                    all_data.append(row)

                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

        print("Writing data to CSV file...")
        self.write_to_csv(output_file, all_data)

        print(f"Parsing completed. CSV file saved as: {output_file}")

        return all_data
    
class OffWhiteProductParser(WebsiteParser):
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

    def parse_website(self, source, category):
        return super().parse_website(source, lambda soup: self.parse_product_blocks(soup, category))
    
    def parse_directory(self, directory_path, output_file):
        all_data = []
        header_added = False
        total_files = len([f for f in os.listdir(directory_path) if f.endswith('.txt')])
        processed_files = 0

        print(f"Found {total_files} HTML files in the directory.")
        print("Processing files...")

        for filename in os.listdir(directory_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(directory_path, filename)
                category = os.path.splitext(filename)[0]  # Use the filename as the category

                tsv_output = self.parse_website(file_path, category)

                if not header_added:
                    tsv_output[0].append('filename')  # Add the new column name for filename
                    all_data.append(tsv_output[0])  # Add the header row only once
                    header_added = True

                # Add the filename as a new column to the parsed data
                for row in tsv_output[1:]:
                    row.append(filename)
                    all_data.append(row)

                processed_files += 1
                progress = (processed_files / total_files) * 100
                print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

        print("Writing data to TSV file...")
        self.write_to_csv(output_file, all_data)

        print(f"Parsing completed. TSV file saved as: {output_file}")

        return all_data
    
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