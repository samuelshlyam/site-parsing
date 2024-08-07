import logging
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
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import datetime
load_dotenv()
app = FastAPI()
@app.post("/run_parser")
async def brand_batch_endpoint(job_id:str, brand_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_parser,job_id, brand_id)
class WebsiteParser:
    def __init__(self):
        self.session = requests.Session()
        self.code = str(uuid.uuid4())
        self.job_id=''
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
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(self.log_file_name),
                logging.StreamHandler()
            ])

        self.logger = logging.getLogger(__name__)
        self.logger.info("This is a log message from the Agent script")

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
        print("I got in here")
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
            print(url)
            response = session.get(url,headers=headers,allow_redirects=True)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
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



def run_parser(job_id,brand_id):
    print(brand_id)
    if int(brand_id)==478:
        categories = ['view-all-shoes-women','view-all-rtw-women','view-all-handbags-women','view-all-slg-women','view-all-jewelry-women','view-all-accessories-women','view-all-rtw-men','view-all-shoes-men','view-all-slg-men','view-all-accessories-men','view-all-bags-men','highlights-women-collection','highlights-men-collection',]
        country_code=['en-it','en-us']
        SaintLaurentParser=SaintLaurentProductParser()
        SaintLaurentParser.job_id=job_id
        SaintLaurentParser.process_categories(categories,country_code)
    if int(brand_id)==229:
        GucciParser = GucciProductParser()
        combined_gucci_categories = ['men-bags', 'men-bags-luggage','men-readytowear','men-shoes','men-accessories-wallets','men-accessories-hats-and-gloves','men-accessories-belts','men-eyewear','jewelry-watches-watches-men','men-accessories','women-shoes','women-handbags','women-accessories-lifestyle-bags-and-luggage','women-readytowear','women-accessories-wallets','women-accessories','jewelry-watches-watches-women', 'women-accessories-belts','women-accessories-silks-and-scarves','women-accessories-hats-and-gloves']
        locales=['it/it','us/en']
        GucciParser.process_categories(combined_gucci_categories,locales)
    if int(brand_id)==26:
        women_categories = ['w-ready-to-wear','W-All-Shoes' ,'W-All-Bags','W-All-Accessories','w-jewellery' ]  # Assuming you have a list of categories
        men_categories = ['M-All-Ready-to-Wear','M-Shoes','M-All-Accessories', 'm-jewellery','M-Bags']
        women_base_url = "https://www.alexandermcqueen.com/api/v1/category/women?locale={locale}&categoryIds={clothing_category}&page={page}&hitsPerPage=30"
        men_base_url = "https://www.alexandermcqueen.com/api/v1/category/men?locale={locale}&categoryIds={clothing_category}&page={page}&hitsPerPage=30"
        category_dicts=[{'category_list':women_categories, 'base_url':women_base_url},{'category_list':men_categories,'base_url':men_base_url}]
        locales=['en-it','en-us',]
        AlexandarMcqueenParser=AlexanderMcqueenParser()
        AlexandarMcqueenParser.job_id = job_id
        AlexandarMcqueenParser.process_categories(category_dicts,locales)
    if int(brand_id)==363:
        categories = ['men','women','children']
        country_codes=['Sites-MonclerEU-Site/en_IT','Sites-MonclerUS-Site/en_US']
        MonclerParser=MonclerProductParser()
        MonclerParser.job_id = job_id
        MonclerParser.process_categories(categories,country_codes)
    if int(brand_id)==314:
        categories=['L1_MEN','L1_WOM','L2_MEN_ACCESSORIES','L2_WOM_LG','L2_WOM_ACCESSORIES','L2_SHOES_WOM','L2_WOM_SLG','L2_SHOES_MAN','L2_DIGITALFW24_MAN','L2_DIGITALFW24_WOM','L2_SS23_WOM','L2_SS23_MAN']
        LoroPianaParser=LoroPianaProductParser()
        LoroPianaParser.job_id = job_id
        country_codes=[{'country_code':'it', 'locale':'it'},{'country_code':'en', 'locale':'us'}]
        LoroPianaParser.process_categories(categories, country_codes)
    if int(brand_id)==310:
        categories = ['cgid%3Dwomen','cgid%3Dmen','cgid%3Dm_fw_collection','cgid%3Dw_fw_precollection']
        country_dicts=[{'country_code':'IT','locale':'en','limit':200,'site_id':'LOE_EUR'},{'country_code':'USA','locale':'en-US','limit':200,'site_id':'LOE_USA'}]
        LoeweParser=LoeweProductParser()
        LoeweParser.process_categories(categories,country_dicts)
    print("Donejbadklj ")
class GucciProductParser(WebsiteParser):
    ##COMPLETE
    def __init__(self):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = "https://www.gucci.com/{locale}/c/productgrid?categoryCode={category}&show=Page&page={page}"
        self.data = pd.DataFrame()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(options=options)
        self.brand = 'gucci'
        super().__init__()
        super().process_website()
    def format_url(self,url):
        """ Helper function to format URLs correctly """
        return f"https:{url}" if url else ''

    def safe_strip(self,value):
        """ Helper function to strip strings safely """
        return value.strip() if isinstance(value, str) else value
    def fetch_data(self,category, base_url,locale):

        all_products = []  # Use a list to store product dictionaries
        try:
            current_url=base_url.format(category=category, page=0,locale=locale)
            self.driver.get(current_url)
            page_source = self.driver.page_source
            self.logger.info(page_source[:10000])
            soup=BeautifulSoup(page_source,'html.parser')
            json_temp=soup.find('pre').text if soup.find('pre') else ''
            json_data=json.loads(json_temp) if json_temp else {}
            total_pages = json_data.get('numberOfPages', 1)
            self.logger.info(f"Category: {category}, Total Pages: {total_pages}")

            for page in range(total_pages):
                current_url = base_url.format(category=category, page=page, locale=locale)
                self.driver.get(current_url)
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                json_temp = soup.find('pre').text if soup.find('pre') else ''
                json_data = json.loads(json_temp) if json_temp else {}
                items = json_data.get('products', {}).get('items', [])
                if not items:
                    self.logger.info(f"No items found on Page: {page + 1}/{total_pages} URL: {current_url}")
                    continue

                for product in items:
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
                    all_products.append(product_info)
                self.logger.info(f"Processed {len(items)} products on Page: {page + 1}/{total_pages} for Category: {category} URL: {current_url}")
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
        self.output_filename=f"{self.brand}_output_{current_date}_{self.code}.csv"
        self.data.to_csv(self.output_filename,sep=',', index=False, quoting=csv.QUOTE_ALL)
        self.upload_url=self.upload_file_to_space(self.output_filename,self.output_filename)
        self.logger.info(f"Complete data saved to {self.output_filename}")
        self.count = len(self.data) - 1
        self.driver.close()
        self.send_output()
class LoroPianaProductParser(WebsiteParser):
    ##COMPLETE
    def __init__(self):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = "https://{locale}.loropiana.com/{country_code}/c/{category}/results?page={page}"
        self.data = pd.DataFrame()
        self.brand = 'loro_piana'

    def format_url(self,url):
        """ Helper function to format URLs correctly """
        return f"https:{url}" if url else ''

    def safe_strip(self,value):
        """ Helper function to strip strings safely """
        return value.strip() if isinstance(value, str) else value
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
            response = session.get(current_url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            total_pages = json_data.get('pagination', {}).get("numberOfPages",0)
            self.logger.info(f"Category: {category}, Total Pages: {total_pages}")

            for page in range(total_pages):
                current_url = base_url.format(category=category, country_code=country_code, locale=locale, page=page)
                response = session.get(current_url, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                items = json_data.get('results', {})
                if not items:
                    self.logger.info(f"No items found on Page: {page+1}/{total_pages}")
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
                    all_products.append(product_info)
                self.logger.info(f"Processed {len(items)} products on Page: {page+1}/{total_pages} for Category: {category} URL: {current_url}")

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
    def __init__(self):
        self.brand = 'alexander_mcqueen'  # Replace spaces with underscores
        self.base_url = ''
        self.data=pd.DataFrame
    def format_url(self,url):
        """ Helper function to format URLs correctly """
        return url if url.startswith('http') else 'https:' + url
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
            response = session.get(current_url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            total_pages = json_data['stats']['nbPages']
            total_pages = total_pages + 1
            self.logger.info(f"Category: {category}, Total Pages: {total_pages}")
            for page in range(total_pages):
                self.logger.info(page)
                current_url=base_url.format(clothing_category=category,locale=locale, page=page)
                response = session.get(current_url, headers=headers)
                response.raise_for_status()
                json_data = response.json()
                products = json_data['products']
                if not products:
                    self.logger.info(f"No items found on Page: {page + 1}/{total_pages} URL: {current_url}")
                    continue
                self.logger.info(f"Last product ID on this page: \n{products[-1].get('id', '')}")
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
                self.logger.info(f"Processed {len(products)} products on Page: {page + 1}/{total_pages} for Category: {category} URL: {current_url}")
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
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(options=options)
        self.base_url="https://www.moncler.com/on/demandware.store/{country_code}/SearchApi-Search?cgid={category}&sz=2000&start=0"
        self.country=''
        self.brand = 'moncler'
    def fetch_moncler_products(self,categories,country_code):
        all_products=[]
        for category in categories:
            offset = 0
            while True:
                formatted_url = self.base_url.format(category=category,country_code=country_code)
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
                self.logger.info(f'Found {len(products)} products on offset {offset}')
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
    def process_categories(self, categories, country_codes):
        # Fetch products
        for country_code in country_codes:
            all_data = pd.DataFrame()
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
    def __init__(self):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = ("https://www.ysl.com/api/v1/category/{category}?locale={locale}&page={page}&categoryIds={category}&hitsPerPage=15")
        self.data = pd.DataFrame()
        self.brand='saint_laurent'
        super().__init__()

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
            self.logger.info(total_pages)
            for page in range(total_pages):
                response = session.get(base_url.format(category=category, page=page,locale=locale), headers=headers)
                response.raise_for_status()
                json_data = response.json()
                items = json_data.get('products', [])
                hits = json_data.get('hitsAlgolia', [])
                if not (items and hits):
                    self.logger.info(f"No items found on page: {page}")
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
                self.logger.info(f"Processed {len(items)} products on page: {page} for Category: {category}")
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

# class DolceGabbanaProductParser():
#     def __init__(self):
#         self.brand = 'dolce_gabbana'  # Replace spaces with underscores
#
#     def fetch_products(self,category, bearer_token,info_dict):
#         base_url = "https://www.dolcegabbana.com/mobify/proxy/api/search/shopper-search/v1/organizations/f_ecom_bkdb_prd/product-search?locale={locale}&siteId={site_id}&refine=c_availableForCustomerGroupA%3DEveryone&limit={limit}&offset={offset}&refine={category}"
#         url = base_url.replace("CATEGORYGOESHERE", category)
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
#             'Authorization': f'Bearer {bearer_token}'
#         }
#         all_products = []
#         offset = 0
#
#         while True:
#             locale=info_dict['locale']
#             site_id=info_dict['site_id']
#             limit = info_dict['limit']
#             formatted_url = url.format(offset=offset,locale=locale,site_id=site_id,limit=limit,category=category)
#             response = requests.get(formatted_url, headers=headers)
#             if response.status_code != 200:
#                 self.logger.info(f"Failed to fetch data: {response.status_code} - {response.text}")
#                 break
#             data = response.json()
#             products = data.get('hits', [])
#             if not products:
#                 print("No more products to fetch.")
#                 break
#
#             for product in products:
#                 # Properly handle and format the images
#                 images = product.get('image', {})  # Ensure to get the image dictionary correctly
#                 images_formatted = f"{images.get('link', '')} ({images.get('alt', '')})" if images else "No image"
#
#                 product_info = {
#                     'category': category,
#                     'productId': product.get('productId', ''),
#                     'productName': product.get('productName', ''),
#                     'price': product.get('price', 0),
#                     'pricePerUnit': product.get('pricePerUnit', 0),
#                     'currency': product.get('currency', ''),
#                     'hitType': product.get('hitType', ''),
#                     'productType_variationGroup': product['productType'].get('variationGroup', False),
#                     'orderable': product.get('orderable', False),
#                     'representedProduct_id': product['representedProduct'].get('id', ''),
#                     'representedProduct_ids': ' | '.join([rp['id'] for rp in product.get('representedProducts', [])]),
#                     'images': images_formatted,  # Use formatted image details here
#                     'c_url': "https://www.dolcegabbana.com" + product.get('c_url', '')
#                 }
#                 all_products.append(product_info)
#
#             print(f"Fetched {len(products)} products from offset {offset} and URL {formatted_url}")
#             offset += limit
#             if offset >= data['total']:
#                 break
#
#         return pd.DataFrame(all_products)
#     def process_categories(self, categories,bearer_token,info_dicts):
#         all_data = pd.DataFrame()
#         for info_dict in info_dicts:
#             self.data=pd.DataFrame()
#             locale=info_dict['locale']
#             for category in categories:
#                 print(f"Fetching products for category: {category}")
#                 category_data = self.fetch_products(category, bearer_token,info_dict)
#                 all_data = pd.concat([all_data, category_data], ignore_index=True)
#                 print(f"Completed fetching for category: {category}")
#             current_date = datetime.datetime.now().strftime("%m_%d_%Y")
#             filename = f'parser-output/dolce_output_{locale}_{current_date}.csv'
#             all_data.to_csv(filename, index=False)
#             print("Complete data saved to 'dolcegabbana_products.csv'")
#         # Save the complete DataFrame to a CSV file


class LoeweProductParser(WebsiteParser):
    ##COMPLETEZ
    def __init__(self):
        # Initialize with common base URL and empty DataFrame to accumulate results
        self.base_url = "https://www.loewe.com/mobify/proxy/api/search/shopper-search/v1/organizations/f_ecom_bbpc_prd/product-search?siteId={site_id}&refine={category}&locale={locale}&offset={offset}&limit={limit}&c_countryCode={country_code}"
        self.data = pd.DataFrame()
        self.brand='Loewe'
        options = Options()
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
                    self.logger.info("Bearer token found:", token)
                    return token


    def format_url(self, url):
        """ Helper function to format URLs correctly """
        return f"https:{url}" if url else ''

    def safe_strip(self, value):
        """ Helper function to strip strings safely """
        return value.strip() if isinstance(value, str) else value

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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3',
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
            response = session.get(current_url, headers=headers)
            response.raise_for_status()
            json_data = response.json()
            items=json_data.get('hits',[])
            totalProducts=int(items[0].get('c_totalProducts','').replace(',','').replace('.',''))

            while offset<=totalProducts:
                current_url = base_url.format(category=category, offset=offset, limit=limit, country_code=country_code,
                                              locale=locale, site_id=site_id)
                response = session.get(current_url, headers=headers)
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
                print(f"Processed {len(items)} products on offset: {offset} for Category: {category} url: {current_url}")
                offset+=limit
            return pd.DataFrame(all_products)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
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


# class TodsProductParser():
#     def __init__(self):
#         # Initialize with common base URL and empty DataFrame to accumulate results
#         self.base_url = ("https://www.tods.com/rest/v2/tods-us/products/search?query=:rank-asc:category:{category}&fields=NAV&currentPage=0&pageSize=1000&key=undefined&lang=en&access_token=TgPITCn5tGqje8P1IHOIdSbrvKA")
#         self.data = pd.DataFrame()
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
    uvicorn.run("run_parser_api:app", port=8008, log_level="info")