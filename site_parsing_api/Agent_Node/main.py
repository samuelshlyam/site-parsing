import sys

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import logging.handlers
import os
import time
import uuid
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import boto3
import requests
import uvicorn
from bs4 import BeautifulSoup
# from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import datetime
# load_dotenv()
app = FastAPI()
# SETTINGS_URL="https://raw.githubusercontent.com/samuelshlyam/API_Parser_Settings/main/settings.json"
@app.post("/run_parser")
async def brand_batch_endpoint(job_id:str, brand_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_parser,job_id, brand_id)
def fetch_settings():
    try:
        response = requests.get(os.getenv('SETTINGS_URL'))
        response.raise_for_status()  # Raises an HTTPError for bad responses
        print(f"This is the settings file\n{response.json()}")
        return response.json()
    except requests.RequestException as e:
        return None





def run_parser(job_id,brand_id):
    print(f"This is the currently running brand_id:{brand_id}, job_id{job_id}")
    settings=fetch_settings()
    print(f"This is the currently relevant setting{settings.get(brand_id)}")
    if int(brand_id)==478:
        brand_settings=settings.get(brand_id)
        categories=brand_settings.get("Categories")
        locales=brand_settings.get("Locales")
        base_url=brand_settings.get("Base_URL")
        print(f"These are the parameters being used for this parser:\nBase URL:{base_url}\nCategories:{categories}\nLocales:{locales}")
        SaintLaurentParser=SaintLaurentProductParser(job_id,base_url)
        SaintLaurentParser.process_categories(categories,locales)
    if int(brand_id)==229:
        brand_settings = settings.get(brand_id)
        categories = brand_settings.get("Categories")
        locales = brand_settings.get("Locales")
        base_url = brand_settings.get("Base_URL")
        print(f"These are the parameters being used for this parser:\nBase URL:{base_url}\nCategories:{categories}\nLocales:{locales}")
        GucciParser = GucciProductParser(job_id,base_url)
        GucciParser.process_categories(categories,locales)
    if int(brand_id)==26:
        brand_settings = settings.get(brand_id)
        categories = brand_settings.get("Categories")
        locales = brand_settings.get("Locales")
        base_url = brand_settings.get("Base_URL")
        print(f"These are the parameters being used for this parser:\nBase URL:{base_url}\nCategories:{categories}\nLocales:{locales}")
        AlexandarMcqueenParser=AlexanderMcqueenParser(job_id,base_url)
        AlexandarMcqueenParser.process_categories(categories,locales)
    if int(brand_id)==363:
        brand_settings = settings.get(brand_id)
        categories = brand_settings.get("Categories")
        locales = brand_settings.get("Locales")
        base_url = brand_settings.get("Base_URL")
        print(f"These are the parameters being used for this parser:\nBase URL:{base_url}\nCategories:{categories}\nLocales:{locales}")
        MonclerParser=MonclerProductParser(job_id,base_url)
        MonclerParser.process_categories(categories,locales)
    if int(brand_id)==314:
        brand_settings = settings.get(brand_id)
        categories = brand_settings.get("Categories")
        locales = brand_settings.get("Locales")
        base_url = brand_settings.get("Base_URL")
        print(f"These are the parameters being used for this parser:\nBase URL:{base_url}\nCategories:{categories}\nLocales:{locales}")
        LoroPianaParser=LoroPianaProductParser(job_id,base_url)
        LoroPianaParser.process_categories(categories, locales)
    if int(brand_id)==310:
        brand_settings = settings.get(brand_id)
        categories = brand_settings.get("Categories")
        locales = brand_settings.get("Locales")
        base_url = brand_settings.get("Base_URL")
        print(f"These are the parameters being used for this parser:\nBase URL:{base_url}\nCategories:{categories}\nLocales:{locales}")
        LoeweParser=LoeweProductParser(job_id,base_url)
        LoeweParser.process_categories(categories,locales)
    if int(brand_id)==157:
        brand_settings = settings.get(brand_id)
        categories = brand_settings.get("Categories")
        locales = brand_settings.get("Locales")
        base_url = brand_settings.get("Base_URL")
        print(f"These are the parameters being used for this parser:\nBase URL:{base_url}\nCategories:{categories}\nLocales:{locales}")
        DolceParser=DolceGabbanaProductParser(job_id,base_url)
        DolceParser.process_categories(categories,locales)
    if int(brand_id)==500:
        brand_settings = settings.get(brand_id)
        categories = brand_settings.get("Categories")
        locales = brand_settings.get("Locales")
        base_url = brand_settings.get("Base_URL")
        print(f"These are the parameters being used for this parser:\nBase URL:{base_url}\nCategories:{categories}\nLocales:{locales}")
        StoneIslandParser = StoneIslandProductParser(job_id,base_url)
        StoneIslandParser.process_categories(categories, locales)
    if int(brand_id)==125:
        brand_settings = settings.get(brand_id)
        categories = brand_settings.get("Categories")
        locales = brand_settings.get("Locales")
        base_url = brand_settings.get("Base_URL")
        print(f"These are the parameters being used for this parser:\nBase URL:{base_url}\nCategories:{categories}\nLocales:{locales}")
        ChloeParser = ChloeProductParser(job_id,base_url)
        ChloeParser.process_categories(categories, locales)
    if int(brand_id)==110:
        brand_settings = settings.get(brand_id)
        categories = brand_settings.get("Categories")
        locales = brand_settings.get("Locales")
        base_url = brand_settings.get("Base_URL")
        print(f"These are the parameters being used for this parser:\nBase URL:{base_url}\nCategories:{categories}\nLocales:{locales}")
        CanadaGooseParser = CanadaGooseProductParser(job_id,base_url)
        CanadaGooseParser.process_categories(categories, locales)
    print("Done")
#Categories in case necessary for Dolce
# categories = ['cgid%3Dwomen-bags', 'cgid%3Dwomen-apparel', 'cgid%3Djewellry-for-her', 'cgid%3Dwomen-shoes',
        #              'cgid%3Dwomen-accessories', 'cgid%3Dwomen-accessories-sunglasses', 'cgid%3Dmen-apparel',
        #              'cgid%3Dmen-tailoring', 'cgid%3Dmen-bags', 'cgid%3Dmen-shoes', 'cgid%3Dmen-accessories',
        #              'cgid%3Dmen-accessories-sunglasses', 'cgid%3Djewellry-for-him']
class WebsiteParser:
    def format_url(self, url):
        """ Helper function to format URLs correctly """
        if url:
            return url if url.startswith('http') else 'https:' + url
        else:
            return ""

    def safe_strip(self, value):
        """ Helper function to strip strings safely """
        return value.strip() if isinstance(value, str) else value
    def __init__(self):
        self.session = requests.Session()
        self.code = str(uuid.uuid4())
        self.setup_logging()
        self.count=0
        self.upload_url=''
        self.output_filename=''


    def convert_to_tsv(self, data):
        output = []
        for row in data:
            output.append([str(item) for item in row])

        return output

    def setup_logging(self):
        current_date = datetime.datetime.now().strftime("%d_%m_%Y")
        self.log_file_name = f'{self.brand}_{self.code}_{current_date}.log'

        # Initially get a unique logger using a UUID, brand ID, and job ID
        logger_name = f"Brand Name: {self.brand}, Job ID: {self.job_id}, UUID: {self.code}"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)  # Set logger to DEBUG to capture all messages
        self.logger.propagate = False  # Prevent propagation to root logger

        # Set formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create handler for logs that go to the file on the debug level
        self.log_file_handler = logging.handlers.RotatingFileHandler(self.log_file_name)
        self.log_file_handler.setFormatter(formatter)
        self.log_file_handler.setLevel(logging.DEBUG)

        # Create handler for logs that go to the console on the info level
        self.log_console_handler = logging.StreamHandler(sys.stdout)
        self.log_console_handler.setFormatter(formatter)
        self.log_console_handler.setLevel(logging.INFO)

        self.logger.addHandler(self.log_file_handler)
        self.logger.addHandler(self.log_console_handler)

        # Initial test that the logger is instantiated and working properly
        self.logger.debug("This is a debug message (should appear in file only)")
        self.logger.info("This is an info message (should appear in both file and console)")
        self.logger.warning("This is a warning message (should appear in both file and console)")
        self.logger.error("This is an error message (should appear in both file and console)")
        self.logger.critical("This is a critical message (should appear in both file and console)")

    def write_to_tsv(self, file_path, tsv_data):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(tsv_data)
    # def write_to_csv(self, file_path, csv_data):
    #     with open(file_path, 'w', newline='', encoding='utf-8') as file:
    #         writer = csv.writer(file, delimiter=',')
    #         writer.writerows(csv_data)
    def write_to_csv(self, csv_data):
        current_date = datetime.datetime.now().strftime("%d_%m_%Y")

        file_path = f'output_{self.brand}_{self.code}_{current_date}.csv'

        # Write data to CSV
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(csv_data)
        self.logger.info(f"Data saved to '{file_path}'")
        return file_path

    def send_output(self):
        self.logger.info(f"Starting send output")
        self.log_url = self.upload_file_to_space(self.log_file_name, self.log_file_name)
        logging.shutdown()
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
        }

        params = {
            'job_id': str(self.job_id),
            'resultUrl': str(self.upload_url),
            'logUrl': str(self.log_url),
            'count': int(self.count)
        }
        os.remove(self.output_filename)
        os.remove(self.log_file_name)
        self.logger.info(f"Finishing send output:\nParams:{params}")
        requests.post(f"{os.getenv('MANAGER_ENDPOINT')}/job_complete", params=params, headers=headers)
    @staticmethod
    def open_link(url):
        try:
            session = requests.Session()
            # Setup retry strategy
            retries = Retry(
                total=5,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated to use allowed_methods instead of method_whitelist
            )
            session.mount("https://", HTTPAdapter(max_retries=retries))
            headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.3"}
            self.logger.info(f"This is the url that is being opened {url}")
            response = session.get(url,headers=headers,allow_redirects=True)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.info(f"An error occurred when trying to open url: {url}\n{e}")
            return None

    def upload_file_to_space(self, file_src, save_as, is_public=True):
        spaces_client = self.get_s3_client()
        space_name = 'iconluxurygroup-s3'  # Your space name

        spaces_client.upload_file(file_src, space_name, save_as, ExtraArgs={'ACL': 'public-read'})
        self.logger.info(f"File uploaded successfully to {space_name}/{save_as}")
        # Generate and return the public URL if the file is public
        if is_public:
            # upload_url = f"{str(os.getenv('SPACES_ENDPOINT'))}/{space_name}/{save_as}"
            upload_url = f"https://iconluxurygroup-s3.s3.us-east-2.amazonaws.com/{save_as}"
            self.logger.info(f"Public URL: {upload_url}")
            return upload_url

    def get_s3_client(self):
        session = boto3.session.Session()
        client = boto3.client(service_name='s3',
                              region_name=os.getenv('REGION'),
                              aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                              aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        # client = boto3.client(service_name='s3',
        #                       region_name=REGION,
        #                       aws_access_key_id=AWS_ACCESS_KEY_ID,
        #                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        return client




class GucciProductParser(WebsiteParser):
    ##COMPLETE
    def __init__(self,job_id,base_url):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.data = pd.DataFrame()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--headless=new")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.brand="gucci"
        self.job_id=job_id
        self.base_url=base_url
        super().__init__()
    def fetch_data(self,category, base_url,locale):
        all_products = []  # Use a list to store product dictionaries
        try:
            current_url=base_url.format(category=category, page=0,locale=locale)
            self.driver.get(current_url)
            page_source=self.driver.execute_script("return document.documentElement.outerHTML;")
            self.logger.info(page_source[:10000])
            soup=BeautifulSoup(page_source,'html.parser')
            json_temp=soup.find('pre').text if soup.find('pre') else ''
            json_data=json.loads(json_temp) if json_temp else {}
            total_pages = json_data.get('numberOfPages', 1)
            self.logger.info(f"Category: {category}, Total Pages: {total_pages}")

            for page in range(total_pages):
                current_url = base_url.format(category=category, page=page, locale=locale)
                self.driver.get(current_url)
                page_source=self.driver.execute_script("return document.documentElement.outerHTML;")
                soup=BeautifulSoup(page_source,'html.parser')
                json_temp=soup.find('pre').text if soup.find('pre') else ''
                json_data=json.loads(json_temp) if json_temp else {}
                items = json_data.get('products', {}).get('items', [])
                if not items:
                    self.logger.info(f"No items found on Page: {page + 1}/{total_pages} URL: {current_url}")
                    continue

                for product in items:
                    self.logger.info(f"This is the product json that is currently being parsed\n{product}")
                    product_info = {
                        'category': category,
                        'productCode': self.safe_strip(product.get('productCode', '')),
                        'title': self.safe_strip(product.get('title', '')).replace('\n', ' ').replace('\r', ''),
                        'price': self.safe_strip(product.get('price', '')),
                        'rawPrice': self.safe_strip(product.get('rawPrice', '')),
                        'productLink': self.safe_strip(product.get('productLink', '')),
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
                    self.logger.info(f"This is the info that it got for this product\n{product_info}")
                    all_products.append(product_info)
                self.logger.info(f"Processed {len(items)} products on Page: {page + 1}/{total_pages} for Category: {category} URL: {current_url}")
            self.logger.info(f"This is the list of product info that it got for this category\n{all_products}")
            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            self.logger.info(f"An error occurred: {e}")
            return pd.DataFrame()


    def process_categories(self, categories,locales):
        for locale in locales:
            self.data=pd.DataFrame()
            for category in categories:
                category_data = self.fetch_data(category, self.base_url,locale)
                self.data = pd.concat([self.data, category_data], ignore_index=True)
            # Save the complete DataFrame to a CSV file
            #data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        self.output_filename = f"{self.brand}_output_{current_date}_{self.code}.csv"
        self.data.to_csv(self.output_filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        self.upload_url=self.upload_file_to_space(self.output_filename, self.output_filename)
        self.logger.info(f"Complete data saved to {self.output_filename}")
        self.count = len(self.data) - 1
        self.send_output()
class LoroPianaProductParser(WebsiteParser):
    ##COMPLETE
    def __init__(self,job_id,base_url):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = base_url
        self.job_id=job_id
        self.data = pd.DataFrame()
        self.brand = 'loro_piana'
        super().__init__()
    def fetch_data(self,category, base_url,country_code, locale):
        session = requests.Session()
        # Setup retry strategy
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]  # Updated to use allowed_methods instead of method_whitelist
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
        all_products = []  # Use a list to store product dictionaries
        try:
            current_url=base_url.format(category=category, country_code=country_code, locale=locale, page=0)
            self.logger.info(f"This is the current_url {current_url}")
            response = session.get(current_url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            total_pages = json_data.get('pagination', {}).get("numberOfPages",0)
            self.logger.info(f"Category: {category}, Total Pages: {total_pages}")

            for page in range(total_pages):
                current_url = base_url.format(category=category, country_code=country_code, locale=locale, page=page)
                response = session.get(current_url, headers=headers)
                self.logger.info(f"This is the current_url {current_url}")
                response.raise_for_status()
                json_data = response.json()
                items = json_data.get('results', {})
                if not items:
                    self.logger.info(f"No items found on Page: {page+1}/{total_pages}")
                    continue

                for data in items:
                    self.logger.info(f"This the json for the currently parsed product\n{data}")
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
                        'primaryImage': data.get('images', [])[0].get('url', '') if data.get('images') else '',
                        'alternateGalleryImages': " | ".join(
                            [img.get('url', '') for img in data.get('images', [])[1:]]),
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
                    self.logger.info(f"This the data found for the current product\n{product_info}")
                    all_products.append(product_info)
                self.logger.info(f"Processed {len(items)} products on Page: {page+1}/{total_pages} for Category: {category} URL: {current_url}")
            self.logger.info(f"This is all of the product data for:\nCategory:{category}\n{all_products}")
            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            self.logger.info(f"An error occurred: {e}")
            return pd.DataFrame()


    def process_categories(self, categories, country_dicts):
        for country_dict in country_dicts:
            locale=country_dict['locale']
            country_code=country_dict['country_code']
            for category in categories:
                category_data = self.fetch_data(category, self.base_url, country_code, locale)
                self.data = pd.concat([self.data, category_data], ignore_index=True)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        self.output_filename = f"{self.brand}_output_{current_date}_{self.code}.csv"
        self.data.to_csv(self.output_filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        self.upload_url=self.upload_file_to_space(self.output_filename, self.output_filename)
        self.logger.info(f"Complete data saved to {self.output_filename}")
        self.count = len(self.data) - 1
        self.send_output()
        # Save the complete DataFrame to a CSV file
        #data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
class AlexanderMcqueenParser(WebsiteParser):
    def __init__(self,job_id,base_url):
        self.brand = 'alexander_mcqueen'  # Replace spaces with underscores
        self.base_url = base_url
        self.data=pd.DataFrame
        self.job_id=job_id
        super().__init__()
    def fetch_data(self,category, base_url,locale):
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
            current_url=base_url.format(clothing_category=category,locale=locale, page=0)
            self.logger.info(f"This is the current_url {current_url}")
            response = session.get(current_url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            total_pages = json_data['stats']['nbPages']
            total_pages = total_pages + 1
            self.logger.info(f"Category: {category}, Total Pages: {total_pages}")
            for page in range(total_pages):
                self.logger.info(page)
                current_url=base_url.format(clothing_category=category,locale=locale, page=page)
                self.logger.info(f"This is the current_url {current_url}")
                response = session.get(current_url, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                products = json_data['products']
                if not products:
                    self.logger.info(f"No items found on Page: {page + 1}/{total_pages} URL: {current_url}")
                    continue
                for product in products:
                    self.logger.info(f"This the json for the currently parsed product\n{product}")
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
                    self.logger.info(f"This the data found for the current product\n{product_info}")
                    all_products.append(product_info)
                self.logger.info(f"Processed {len(products)} products on Page: {page + 1}/{total_pages} for Category: {category} URL: {current_url}")
            self.logger.info(f"This is all of the product data for:\nCategory:{category}\n{all_products}")
            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            self.logger.info(f"An error occurred: {e}")
            return pd.DataFrame()

    def process_categories(self, category_dicts,locales):
        for locale in locales:
            self.data = pd.DataFrame()
            for category_dict in category_dicts:
                categories = category_dict["category_list"]
                self.base_url = category_dict["base_url"]
                for category in categories:
                    category_data = self.fetch_data(category, self.base_url,locale)
                    self.data = pd.concat([self.data, category_data], ignore_index=True)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        self.output_filename = f"{self.brand}_output_{current_date}_{self.code}.csv"
        self.data.to_csv(self.output_filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        self.upload_url=self.upload_file_to_space(self.output_filename, self.output_filename)
        self.logger.info(f"Complete data saved to {self.output_filename}")
        self.count = len(self.data) - 1
        self.send_output()

class MonclerProductParser(WebsiteParser):
    def __init__(self,job_id,base_url):
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        options.add_argument("--start-maximized")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument("--headless=new")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        # Set up the Chrome driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.base_url=base_url
        self.country=''
        self.brand = 'moncler'
        self.job_id=job_id
        super().__init__()
    def fetch_moncler_products(self,categories,country_code):
        all_products=[]
        for category in categories:
            offset = 0
            while True:
                formatted_url = self.base_url.format(category=category,country_code=country_code)
                self.logger.info(f"This is the current url: {formatted_url}")
                self.driver.get(formatted_url)
                self.country=country_code.split('/')[-1]
                response = self.driver.find_element(By.TAG_NAME, "body").text
                self.logger.info(type(response))
                self.logger.info(response[:1000])
                data = json.loads(response)
                products = data['data']['products']
                if not products:
                    break

                for product in products:
                    self.logger.info(f"This is the current product: {product}")
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
                    self.logger.info(f"This is the product info: {product_info}\nthat was gotten for this product data {product}")
                    all_products.append(product_info)

                # Update offset to next page
                offset += len(products)
                self.logger.info(f'Found {len(products)} products on offset {offset}')
                total_count = data['data']['count']
                if offset >= total_count:
                    break
            self.logger.info(f"This is all of the product data for:\nCategory:{category}\n{all_products}")
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
    def process_categories(self, categories, country_codes):
        # Fetch products
        all_data = pd.DataFrame()
        for country_code in country_codes:
            some_data = self.fetch_moncler_products(categories, country_code)
            all_data = pd.concat([all_data, some_data], ignore_index=True)
            self.logger.info(all_data.head())
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        self.output_filename = f"{self.brand}_output_{current_date}_{self.code}.csv"
        all_data.to_csv(self.output_filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        self.upload_url=self.upload_file_to_space(self.output_filename, self.output_filename)
        self.logger.info(f"Complete data saved to {self.output_filename}")
        self.count=len(all_data)-1
        self.send_output()
class SaintLaurentProductParser(WebsiteParser):
    def __init__(self,job_id,base_url):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = base_url
        self.data = pd.DataFrame()
        self.brand='saint_laurent'
        self.job_id=job_id
        super().__init__()

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
            current_url=self.base_url.format(category=category, page=0,locale=locale)
            self.logger.info(f"This is the current url:{current_url}")
            response = session.get(current_url, headers=headers)
            response.raise_for_status()
            json_data = response.json()

            total_pages=json_data.get('stats',{}).get('nbPages',0)
            self.logger.info(f"This is the total # of pages: {total_pages}")
            for page in range(total_pages):
                current_url=self.base_url.format(category=category, page=page,locale=locale)
                self.logger.info(f"This is the current url: {current_url}")
                response = session.get(current_url, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                items = json_data.get('products', [])
                hits = json_data.get('hitsAlgolia', [])
                if not (items and hits):
                    self.logger.info(f"No items found on page: {page}")
                    continue

                for product,hit in zip(items,hits):
                    price_dict=product.get('price', 0)
                    self.logger.info(f"These are the json that will be parsed\nProduct:\n{product}\nHit:\n{hit}")
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
                    self.logger.info(f"This is the product data: \n{product_info}\nFor product:\n{product}\nHit:\n{hit}")
                    all_products.append(product_info)
                self.logger.info(f"Processed {len(items)} products on page: {page} for Category: {category}")
            self.logger.info(f"This is all of the product data for:\nCategory:{category}\n{all_products}")
            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            self.logger.info(f"An error occurred: {e}")
            return pd.DataFrame()

    def process_categories(self, categories, locales):
        for locale in locales:
            for category in categories:
                category_data = self.fetch_data(category, self.base_url, locale)
                self.data = pd.concat([self.data, category_data], ignore_index=True)
        # Save the complete DataFrame to a CSV file
        # data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        self.output_filename = f"{self.brand}_output_{current_date}_{self.code}.csv"
        self.data.to_csv(self.output_filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        self.upload_url=self.upload_file_to_space(self.output_filename, self.output_filename)
        self.logger.info(f"Complete data saved to {self.output_filename}")
        self.count = len(self.data) - 1
        self.send_output()

class DolceGabbanaProductParser(WebsiteParser):
    def __init__(self,job_id,base_url):
        self.brand = 'dolce_gabbana'  # Replace spaces with underscores
        self.base_url=base_url
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        options.add_argument("--start-maximized")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument("--headless=new")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        # Set up the Chrome driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.job_id=job_id
        super().__init__()
    def get_bearer_token(self):
        self.driver.get("https://www.dolcegabbana.com/en-us/fashion/women/bags/handbags/")
        for i in range(2):
            load_more_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            'button.Button__btn--_SznX.CategoryPaginationLoadMore__category-pagination__load-more--SOwaX.Button__btn--secondary--Tpjc0'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            self.driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(1)

        # Get performance logs
        logs = self.driver.get_log("performance")
        # Search for Bearer token in logs
        for entry in logs:
            if "Bearer" in str(entry.get("message", {})):
                token = json.loads(entry.get("message", {})).get("message", {}).get("params", {}).get('request',{}).get("headers",{}).get("Authorization")
                if token and token.startswith("Bearer "):
                    token = token.split(" ")[-1]
                    self.logger.info(f"Bearer token found: {token}")
                    return token

    def fetch_products(self,category,info_dict):
        base_url = self.base_url
        bearer_token=self.get_bearer_token()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Authorization': f'Bearer {bearer_token}'
        }
        all_products = []
        offset = 0

        while True:
            locale=info_dict['locale']
            site_id=info_dict['site_id']
            limit = info_dict['limit']
            formatted_url = base_url.format(offset=offset,locale=locale,site_id=site_id,limit=limit,category=category)
            self.logger.info(f"This is the current url: {formatted_url}")
            response = requests.get(formatted_url, headers=headers)
            if response.status_code != 200:
                self.logger.info(f"Failed to fetch data: {response.status_code} - {response.text}")
                break
            data = response.json()
            products = data.get('hits', [])
            if not products:
                self.logger.info("No more products to fetch.")
                break

            for product in products:
                self.logger.info(f"These are the json that will be parsed\nProduct:\n{product}")
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
                self.logger.info(f"This is the product data:\n")
                all_products.append(product_info)

            self.logger.info(f"Fetched {len(products)} products from offset {offset} and URL {formatted_url}")
            offset += limit
            if offset >= data['total']:
                break
        self.logger.info(f"This is all of the product data for:\nCategory:{category}\n{all_products}")
        return pd.DataFrame(all_products)
    def process_categories(self, categories,info_dicts):
        all_data = pd.DataFrame()
        for info_dict in info_dicts:
            self.data=pd.DataFrame()
            if categories:
                for category in categories:
                    self.logger.info(f"Fetching products for category: {category}")
                    category_data = self.fetch_products(category,info_dict)
                    all_data = pd.concat([all_data, category_data], ignore_index=True)
                    self.logger.info(f"Completed fetching for category: {category}")
            else:
                self.logger.info(f"Fetching products for all of Dolce")
                category_data = self.fetch_products("", info_dict)
                all_data = pd.concat([all_data, category_data], ignore_index=True)
                self.logger.info(f"Completed fetching for all of Dolce")
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        self.output_filename = f"{self.brand}_output_{current_date}_{self.code}.csv"
        self.data.to_csv(self.output_filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        self.upload_url = self.upload_file_to_space(self.output_filename, self.output_filename)
        self.logger.info(f"Complete data saved to {self.output_filename}")
        self.count = len(self.data) - 1
        self.send_output()
        # Save the complete DataFrame to a CSV file


class LoeweProductParser(WebsiteParser):
    ##COMPLETEZ
    def __init__(self,job_id,base_url):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = base_url
        self.job_id=job_id
        self.data = pd.DataFrame()
        self.brand='Loewe'
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        options.add_argument("--start-maximized")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--headless=new")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        # Set up the Chrome driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        super().__init__()

    def get_bearer_token(self):
        # Navigate to the page
        self.driver.get("https://www.loewe.com/usa/en/women/shoes")
        for i in range(2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.execute_script("window.scrollBy(0, -arguments[0]);", 100)
            time.sleep(1)

        # Get performance logs
        logs = self.driver.get_log("performance")
        # Search for Bearer token in logs
        for entry in logs:
            if "Bearer" in str(entry.get("message", {})):
                token = json.loads(entry.get("message", {})).get("message", {}).get("params", {}).get('request',{}).get("headers",{}).get("Authorization")
                if token and token.startswith("Bearer "):
                    token = token.split(" ")[-1]
                    self.logger.info(f"Bearer token found: {token}")
                    return token


    def fetch_data(self, category, base_url,country_dict):
        bearer_token = self.get_bearer_token()
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Authorization': f'Bearer {bearer_token}'
                }
        all_products = []  # Use a list to store product dictionaries
        limit=country_dict['limit']
        country_code=country_dict['country_code']
        locale=country_dict['locale']
        site_id=country_dict['site_id']
        try:
            offset=0
            current_url=base_url.format(category=category, offset=offset, limit=2, country_code=country_code,
                                        locale=locale, site_id=site_id)
            self.logger.info(f"This is the current URL: {current_url}")
            response = session.get(current_url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            items=json_data.get('hits',[])
            totalProducts=int(items[0].get('c_totalProducts','').replace(',','').replace('.',''))

            while offset<=totalProducts:
                current_url = base_url.format(category=category, offset=offset, limit=limit, country_code=country_code,
                                              locale=locale, site_id=site_id)
                self.logger.info(f"This is the current URL: {current_url}")
                response = session.get(current_url, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                items = json_data.get('hits', [])
                if not items:
                    self.logger.info(f"No items found on offset: {offset}")
                    continue

                for product in items:
                    self.logger.info(f"This is the current product json:\n{product}")
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
                    self.logger.info(f"This is the current product info:\n{product_info}")
                    all_products.append(product_info)
                self.logger.info(f"Processed {len(items)} products on offset: {offset} for Category: {category} url: {current_url}")
                offset+=limit
                self.logger.info(f"Offset: {offset}")
            self.logger.info(f"This is all of the product data for:\nCategory:{category}\n{all_products}")
            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            self.logger.info(f"An error occurred: {e}")
            return pd.DataFrame()

    def process_categories(self, categories,country_dicts):
        for country_dict in country_dicts:
            self.data = pd.DataFrame()
            for category in categories:
                category_data = self.fetch_data(category, self.base_url,country_dict)
                self.data = pd.concat([self.data, category_data], ignore_index=True)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        self.output_filename = f"{self.brand}_output_{current_date}_{self.code}.csv"
        self.data.to_csv(self.output_filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        self.upload_url = self.upload_file_to_space(self.output_filename, self.output_filename)
        self.logger.info(f"Complete data saved to {self.output_filename}")
        self.count = len(self.data) - 1
        self.send_output()
class StoneIslandProductParser(WebsiteParser):
    def __init__(self,job_id,base_url):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = base_url
        self.data = pd.DataFrame()
        self.brand='stone_island'
        self.job_id=job_id
        super().__init__()

    def fetch_data(self,category,locale_dict):
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        all_products = []  # Use a list to store product dictionaries
        locale=locale_dict.get('locale','')
        size = locale_dict.get('size','')
        start = locale_dict.get('start','')
        try:
            current_url = self.base_url.format(category=category, size=size, start=start, locale=locale)
            self.logger.info(f"This is the current url: {current_url}")
            response = session.get(current_url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            if isinstance(json_data, str):
                json_data = json.loads(json_data)
            products=json_data.get('data',{}).get('products',[])

            for product in products:
                self.logger.info(f"Current product json: {product}")
                product_info = {
                    'category': category,
                    'type': self.safe_strip(product.get('type', '')),
                    'masterId': self.safe_strip(product.get('masterId', '')),
                    'uuid': self.safe_strip(product.get('uuid', '')),
                    'id': self.safe_strip(product.get('id', '')),
                    'productName': self.safe_strip(product.get('productName', '')),
                    'shortDescription': self.safe_strip(product.get('shortDescription', '')),
                    'productUrl': self.safe_strip(product.get('productUrl', '')),
                    'route': self.safe_strip(product.get('route', '')),
                    'originalModelName': self.safe_strip(product.get('originalModelName', '')),
                    'isComingSoon': str(product.get('isComingSoon', False)).lower(),
                    'price_sales_value': self.safe_strip(product.get('price', {}).get('sales', {}).get('value', '')),
                    'price_sales_currency': self.safe_strip(
                        product.get('price', {}).get('sales', {}).get('currency', '')),
                    'price_sales_formatted': self.safe_strip(
                        product.get('price', {}).get('sales', {}).get('formatted', '')),
                    'image_urls': ','.join(product.get('imgs', {}).get('urls', [])),
                    'image_alt': self.safe_strip(product.get('imgs', {}).get('alt', '')),
                    'analytics_item_name': self.safe_strip(product.get('analyticsAttributes', {}).get('item_name', '')),
                    'analytics_item_category': self.safe_strip(
                        product.get('analyticsAttributes', {}).get('item_category', '')),
                    'analytics_item_category2': self.safe_strip(
                        product.get('analyticsAttributes', {}).get('item_category2', '')),
                    'analytics_item_category3': self.safe_strip(
                        product.get('analyticsAttributes', {}).get('item_category3', '')),
                    'analytics_item_category4': self.safe_strip(
                        product.get('analyticsAttributes', {}).get('item_category4', '')),
                    'analytics_item_category5': self.safe_strip(
                        product.get('analyticsAttributes', {}).get('item_category5', '')),
                    'analytics_item_variant': self.safe_strip(
                        product.get('analyticsAttributes', {}).get('item_variant', '')),
                    'analytics_item_MFC': self.safe_strip(product.get('analyticsAttributes', {}).get('item_MFC', '')),
                    'availability_lowStock': str(product.get('availability', {}).get('lowStock', False)).lower(),
                    'available': str(product.get('available', False)).lower(),
                    'earlyaccess_private': str(product.get('earlyaccess', {}).get('private', False)).lower(),
                    'imageBackground': self.safe_strip(product.get('imageBackground', '')),
                    'assetOverride_plp': self.safe_strip(product.get('assetOverride', {}).get('plp', '')),
                    'assetOverride_plpeditorial': self.safe_strip(
                        product.get('assetOverride', {}).get('plpeditorial', '')),
                    'assetOverride_icongallery': self.safe_strip(
                        product.get('assetOverride', {}).get('icongallery', '')),
                    'seoName': self.safe_strip(product.get('seoName', '')),
                }

                # Handle variationAttributes
                for attr in product.get('variationAttributes', []):
                    attr_id = attr.get('attributeId', '')
                    product_info[f'variationAttribute_{attr_id}_displayName'] = self.safe_strip(
                        attr.get('displayName', ''))
                    product_info[f'variationAttribute_{attr_id}_displayValue'] = self.safe_strip(
                        attr.get('displayValue', ''))
                    product_info[f'variationAttribute_{attr_id}_swatchable'] = str(
                        attr.get('swatchable', False)).lower()
                    product_info[f'variationAttribute_{attr_id}_values'] = ','.join(
                        [self.safe_strip(value.get('displayValue', '')) for value in attr.get('values', [])])

                # Add locale information
                product_info.update(locale_dict)
                self.logger.info(f"This is the current product info:\n{product_info}")
                all_products.append(product_info)
            self.logger.info(f"This is all of the product data for:\nCategory:{category}\n{all_products}")
            return pd.DataFrame(all_products)
        except Exception as e:
            self.logger.info(f"An error occurred: {e}")
            return pd.DataFrame()

    def process_categories(self, categories, locale_dicts):
        for locale_dict in locale_dicts:
            self.data = pd.DataFrame()
            for category in categories:
                category_data = self.fetch_data(category, locale_dict)
                self.data = pd.concat([self.data, category_data], ignore_index=True)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        self.output_filename = f"{self.brand}_output_{current_date}_{self.code}.csv"
        self.data.to_csv(self.output_filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        self.upload_url = self.upload_file_to_space(self.output_filename, self.output_filename)
        self.logger.info(f"Complete data saved to {self.output_filename}")
        self.count = len(self.data) - 1
        self.send_output()
class ChloeProductParser(WebsiteParser):
    def __init__(self,job_id,base_url):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = base_url
        self.data = pd.DataFrame()
        self.job_id=job_id
        self.brand='chloe'
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        options.add_argument("--start-maximized")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument("--headless=new")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        # Set up the Chrome driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        super().__init__()
    def fetch_data(self,category,locale_dict):
        locale=locale_dict.get("locale","")
        size=locale_dict.get("size","")

        self.logger.info(f"This is the size: {size}, locale: {locale}")
        try:
            locale_TF = True if "US" in locale else False
            current_url = self.base_url.format(category=category, size=size,locale=locale)
            self.logger.info(f"This is the current url: {current_url}")
            self.driver.get(current_url)
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "body")))  # Wait for the page to load
            product_html=self.driver.execute_script("return document.documentElement.outerHTML;")
            soup=BeautifulSoup(product_html, 'html.parser')
            product_info = self.get_product_info(soup,category,locale_TF)
            return pd.DataFrame(product_info)
        except Exception as e:
            self.logger.info(f"An error occurred: {e}")
            return pd.DataFrame()
    def extract_product_id(self,product_url,locale_TF):
        self.logger.info(f"Currently getting the product ID for {product_url}")
        self.driver.get(product_url)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body")))  # Wait for the page to load
        except:
            self.logger.info(f"Couldn't find a body tag for product url: {product_url}")
        html=self.driver.page_source
        if locale_TF:
            pid_text='Item code: '
        else:
            pid_text='Codice articolo: '
        self.logger.info(f"This is the pid text that is being looked for: {pid_text}")
        soup_pid=BeautifulSoup(html, 'html.parser') if html else ''
        if soup_pid:
            main_item = soup_pid.find('div', class_='itemdescription')
            if main_item:
                # Extract the Style ID
                style_id_text=main_item.text
                self.logger.info(f"Product ID text on page: {style_id_text}")
                style_id = style_id_text.split(pid_text)[-1].strip()
                self.logger.info(f"Product ID: {style_id}")
                return style_id
            else:
                self.logger.info(f'Product ID not found for url: {product_url}')
                return ""
    def get_product_info(self,soup,category,locale_TF):
        self.logger.info(f"Starting to get the product data from category:{category}")
        parsed_data = []
        articlesChloe = soup.find_all('article', {'class': 'item'})

        for articleChloe in articlesChloe:

            product_data = {}
            imgSource = articleChloe.find('img')
            if imgSource:
                imgSource = imgSource['src']

            data_pinfo = articleChloe['data-ytos-track-product-data']

            a_url = articleChloe.find('a')
            if a_url:
                a_url = a_url['href']
            product_id = self.extract_product_id(a_url,locale_TF)

            product_info = json.loads(data_pinfo)

            product_data['Product_ID']=product_id
            product_data['Cod10']=product_info.get('product_cod10','')
            product_data['Title']=product_info.get('product_title','')
            product_data['Price']=product_info.get('product_price','')
            product_data['position']=product_info.get('product_position','')
            product_data['category']=product_info.get('product_category','')
            product_data['macro_category']=product_info.get('product_macro_category','')
            product_data['micro_category']=product_info.get('product_micro_category','')

            product_data['macro_category_id']=product_info.get('product_macro_category_id','')
            product_data['micro_category_id']=product_info.get('product_micro_category_id','')
            product_data['color']=product_info.get('product_color','')
            product_data['color_id']=product_info.get('product_color_id','')
            product_data['product_price']=product_info.get('product_price','')
            product_data['discountedPrice']=product_info.get('product_discountedPrice','')

            product_data['price_tf']=product_info.get('product_price_tf','')
            product_data['discountedPrice_tf']=product_info.get('product_discountedPrice_tf','')
            product_data['quantity']=product_info.get('product_quantity','')
            product_data['coupon']=product_info.get('product_coupon','')
            product_data['is_in_stock']=product_info.get('product_is_in_stock','')
            product_data['list']=product_info.get('list','')

            product_data['url']=a_url

            product_data['img_src']=imgSource
            product_data['img_src']=category
            self.logger.info(f"This is the currently found product data {product_data}")
            parsed_data.append(product_data)
        return parsed_data
    def process_categories(self, categories, locale_dicts):
        for locale_dict in locale_dicts:
            self.logger.info(f"Currently working on locale: {locale_dict}")
            self.data = pd.DataFrame()
            for category in categories:
                self.logger.info(f"Currently working on category: {category}")
                category_data = self.fetch_data(category, locale_dict)
                self.data = pd.concat([self.data, category_data], ignore_index=True)
        current_date = datetime.datetime.now().strftime("%m_%d_%Y")
        self.output_filename = f"{self.brand}_output_{current_date}_{self.code}.csv"
        self.data.to_csv(self.output_filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
        self.upload_url = self.upload_file_to_space(self.output_filename, self.output_filename)
        self.logger.info(f"Complete data saved to {self.output_filename}")
        self.count = len(self.data) - 1
        self.send_output()


class CanadaGooseProductParser:
    pass
# class TodsProductParser():
#     def __init__(self,job_id):
#         # Initialize with common base URL and empty DataFrame to accumulate results
#         self.base_url = ("https://www.tods.com/rest/v2/tods-us/products/search?query=:rank-asc:category:{category}&fields=NAV&currentPage=0&pageSize=1000&key=undefined&lang=en&access_token=TgPITCn5tGqje8P1IHOIdSbrvKA")
#         self.data = pd.DataFrame()
#         self.job_id=job_id
#
#     def format_url(self, url):
#         """ Helper function to format URLs correctly """
#         return f"https:{url}" if url else ''
#
#     def safe_strip(self, value):
#         """ Helper function to strip strings safely """
#         return value.strip() if isinstance(value, str) else value
#
#     def fetch_data(self, category, base_url, cookie):
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
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3',
#             'Cookie' : cookie
#         }
#         all_products = []  # Use a list to store product dictionaries
#         try:
#             response = session.get(base_url.format(category=category, page=0), headers=headers)
#             response.raise_for_status()
#             json_data = response.json()
#             results=json_data.get("searchPageData",{}).get("results","")
#             for result in results:
#                 product=result.get("product","")
#                 if isinstance(product,dict):
#                     product_info = {
#                         "category":category,
#                         'aggregatedStock': product.get('aggregatedStock', ''),
#                         'baseOptions': product.get('baseOptions', []),
#                         'categories': product.get('categories', []),
#                         'code': product.get('code', ''),
#                         'color': product.get('color', ''),
#                         'colorGA': product.get('colorGA', ''),
#                         'colorVariantNumber': product.get('colorVariantNumber', ''),
#                         'currentHero': product.get('currentHero', False),
#                         'freeTextLabel': product.get('freeTextLabel', ''),
#                         'galleryAltText': product.get('galleryAltText', []),
#                         'hasVirtualTryOn': product.get('hasVirtualTryOn', False),
#                         'isBlocked': product.get('isBlocked', False),
#                         'isDiscount': product.get('isDiscount', False),
#                         'name': product.get('name', ''),
#                         'nameGA': product.get('nameGA', ''),
#                         'price_currencyIso': product.get('price', {}).get('currencyIso', ''),
#                         'price_formattedValue': product.get('price', {}).get('formattedValue', ''),
#                         'price_value': product.get('price', {}).get('value', ''),
#                         'primaryImageAlt': product.get('primaryImageAlt', ''),
#                         'primaryImageUrl': product.get('primaryImageUrl', ''),
#                         'salableStores': product.get('salableStores', False),
#                         'secondaryImageAlt': product.get('secondaryImageAlt', ''),
#                         'secondaryImageUrl': product.get('secondaryImageUrl', ''),
#                         'stockLabel': product.get('stockLabel', ''),
#                         'url': product.get('url', ''),
#                         'volumePricesFlag': product.get('volumePricesFlag', False)
#                     }
#                 else:
#                     print(f"The product is of the wrong type:\n{product}")
#                     break
#
#                 all_products.append(product_info)
#             print(f"Processed {len(results)} for Category: {category}")
#             return pd.DataFrame(all_products)
#         except requests.exceptions.RequestException as e:
#             print(f"An error occurred: {e}")
#             return pd.DataFrame()
#
#     def process_categories(self, categories, cookie):
#         for category in categories:
#             category_data = self.fetch_data(category, self.base_url, cookie)
#             self.data = pd.concat([self.data, category_data], ignore_index=True)
#
#         # Save the complete DataFrame to a CSV file
#         # data.to_csv('gucci_products_complete.tsv', sep='\t', index=False, quoting=csv.QUOTE_ALL)
#         current_date = datetime.datetime.now().strftime("%m_%d_%Y")
#         filename = f'parser-output/tods_output_{current_date}.csv'
#         self.data.to_csv(filename, sep=',', index=False, quoting=csv.QUOTE_ALL)
#         print(f"Complete data saved to 'tods_output_{current_date}.csv'")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0" , log_level="info")