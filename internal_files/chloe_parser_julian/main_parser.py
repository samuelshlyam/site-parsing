import requests
from bs4 import BeautifulSoup
import csv
import datetime
import os

class WebsiteParser:
    def __init__(self):
        self.session = requests.Session()

    def read_from_file(self, file_path):
        with open(file_path, 'r',encoding='utf-8') as file:
            return file.read()

    def parse_website(self, source, parser_func):
        html_content = self.read_from_file(source)
        soup = BeautifulSoup(html_content, 'html.parser')
        parsed_data = parser_func(soup)

        return self.convert_to_tsv(parsed_data)

    def convert_to_tsv(self, data):
        output = []
        for row in data:
            output.append([str(item) for item in row])

        return output

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
        file_path = f'{self.directory}/{self.brand}_output_{current_date}.csv'
        
        # Write data to CSV
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(csv_data)
        print(f"Data saved to '{file_path}'")
    
    
    
class WebSiteScrape:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def search_files_directory(directory_path):
        html_files = []
        for filename in os.listdir(directory_path):
            if filename.endswith(".html"):
                html_files.append(filename)
        return html_files


            
        