import requests
from bs4 import BeautifulSoup
import csv
import datetime
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class WebsiteParser:
    def __init__(self):
        self.session = requests.Session()

    def read_from_file(self, file_path):
        with open(file_path, 'r',encoding='utf-8') as file:
            return file.read()



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

#Legacy, only direct path to directory with html files
    # def parse_directory(self, directory_path):
    #     all_data = []
    #     header_added = False
    #     total_files = len([f for f in os.listdir(directory_path) if f.endswith('.txt') or f.endswith('.html')])
    #     processed_files = 0

    #     print(f"Found {total_files} HTML files in the directory.")
    #     print("Processing files...")

    #     for filename in os.listdir(directory_path):
    #         if filename.endswith('.txt') or filename.endswith('.html'):
    #             file_path = os.path.join(directory_path, filename)
    #             category = os.path.splitext(filename)[0]  # Use the filename as the category

    #             tsv_output = self.parse_website(file_path,category)

    #             if not header_added:
    #                 tsv_output[0].append('filename')  # Add the new column name for filename
    #                 all_data.append(tsv_output[0])  # Add the header row only once
    #                 header_added = True

    #             # Add the filename as a new column to the parsed data
    #             for row in tsv_output[1:]:
    #                 row.append(filename)
    #                 all_data.append(row)

    #             processed_files += 1
    #             progress = (processed_files / total_files) * 100
    #             print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

    #     print("Writing data to CSV file...")
    #     self.write_to_csv(all_data)

    #     return all_data

    def parse_directory(self, directory_path):
        all_data = []
        header_added = False
        total_files = sum([len(files) for r, d, files in os.walk(directory_path) if any(f.endswith(('.txt', '.html')) for f in files)])
        processed_files = 0

        print(f"Found {total_files} HTML/TXT files in the directory and its subdirectories.")
        print("Processing files...")

        for root, dirs, files in os.walk(directory_path):
            for filename in files:
                if filename.endswith('.txt') or filename.endswith('.html'):
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, directory_path)
                    category = os.path.splitext(relative_path)[0]  # Use the relative path as the category

                    tsv_output = self.parse_website(file_path, category)

                    if not header_added:
                        tsv_output[0].extend(['filename', 'relative_path'])  # Add new column names
                        all_data.append(tsv_output[0])  # Add the header row only once
                        header_added = True

                    # Add the filename and relative path as new columns to the parsed data
                    for row in tsv_output[1:]:
                        row.extend([filename, relative_path])
                        all_data.append(row)

                    processed_files += 1
                    progress = (processed_files / total_files) * 100
                    print(f"Progress: {progress:.2f}% ({processed_files}/{total_files} files processed)")

        print("Writing data to CSV file...")
        self.write_to_csv(all_data)

        return all_data

    def parse_website(self, source,category):
        html_content = self.read_from_file(source)
        soup = BeautifulSoup(html_content, 'html.parser')
        parsed_data = self.parse_product_blocks(soup,category)
        return self.convert_to_tsv(parsed_data)
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


