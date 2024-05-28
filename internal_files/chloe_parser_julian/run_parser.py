import os
from brand_parser import BottegaVenetaParser,GucciParser, Chloe
#Folder name for output
output_directory_path = "parser-output"
directory_path = 'brands_html/bottega_veneta'
##Bottega Veneta Parser METHOD 1##
bottega_parser = BottegaVenetaParser(output_directory_path)
##SINGLE FILE RUN##
input_file_path = 'brands_html/bottega_veneta/women_bags.html'
category = os.path.splitext(input_file_path)[0]  # Use the filename as the category  
##Uncomment to run##
#bottega_parser_output = bottega_parser.parse_website(input_file_path, category)
#bottega_parser.write_to_csv(bottega_parser_output)

##MULTIPLE FILE RUN, PASS DIRECTORY PATH
##Comment to run single file##
bottega_parser.parse_directory(directory_path)


#GUCCI PRODUCT FETCH METHOD 2##

gucci_parser = GucciParser()

gucci_categories_womens = ['women-shoes','women-handbags','women-accessories-lifestyle-bags-and-luggage','women-readytowear','women-accessories-wallets','women-accessories','jewelry-watches-watches-women', 'women-accessories-belts','women-accessories-silks-and-scarves','women-accessories-hats-and-gloves']
gucci_categories_mens = ['men-bags', 'men-bags-luggage','men-readytowear','men-shoes','men-accessories-wallets','men-accessories-hats-and-gloves','men-accessories-belts','men-eyewear','jewelry-watches-watches-men','men-accessories'] 
combined_gucci_categories = ['men-bags', 'men-bags-luggage','men-readytowear','men-shoes','men-accessories-wallets','men-accessories-hats-and-gloves','men-accessories-belts','men-eyewear','jewelry-watches-watches-men','men-accessories','women-shoes','women-handbags','women-accessories-lifestyle-bags-and-luggage','women-readytowear','women-accessories-wallets','women-accessories','jewelry-watches-watches-women', 'women-accessories-belts','women-accessories-silks-and-scarves','women-accessories-hats-and-gloves'] 
##UNCOMMENT TO RUN, COMMENT OTHER PARSERS, to avoid multi run##
#gucci_parser.process_categories(combined_gucci_categories)


#CHLOE PRODUCT SCRAPE 3##
directory_path = 'brands_html/chloe'
Chloe.scrape_chloe(directory_path)
