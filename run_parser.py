import os
from brand_parser import BottegaVenetaParser, GucciParser, FendiParser, BallyParser, StellaProductParser, \
    GivenchyProductParser, CanadaGooseProductParser, IsabelMarantParser

#Folder name for output
output_directory_path = "parser-output"
#directory_path = 'brands_html/bottega_veneta'
##Bottega Veneta Parser METHOD 1##
bottega_parser = BottegaVenetaParser(output_directory_path)
##SINGLE FILE RUN##
input_file_path = 'brands_html/bottega_veneta/women_bags.html'
category = os.path.splitext(input_file_path)[0]  # Use the filename as the category  
##Uncomment to run##
bottega_parser_output = bottega_parser.parse_website(input_file_path, category)
bottega_parser.write_to_csv(bottega_parser_output)

##MULTIPLE FILE RUN, PASS DIRECTORY PATH
##Comment to run single file##
directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\bottega_veneta'
bottega_parser.parse_directory(directory_path)


#GUCCI PRODUCT FETCH METHOD 2##

gucci_parser = GucciParser()

gucci_categories_womens = ['women-shoes','women-handbags','women-accessories-lifestyle-bags-and-luggage','women-readytowear','women-accessories-wallets','women-accessories','jewelry-watches-watches-women', 'women-accessories-belts','women-accessories-silks-and-scarves','women-accessories-hats-and-gloves']
gucci_categories_mens = ['men-bags', 'men-bags-luggage','men-readytowear','men-shoes','men-accessories-wallets','men-accessories-hats-and-gloves','men-accessories-belts','men-eyewear','jewelry-watches-watches-men','men-accessories'] 
combined_gucci_categories = ['men-bags', 'men-bags-luggage','men-readytowear','men-shoes','men-accessories-wallets','men-accessories-hats-and-gloves','men-accessories-belts','men-eyewear','jewelry-watches-watches-men','men-accessories','women-shoes','women-handbags','women-accessories-lifestyle-bags-and-luggage','women-readytowear','women-accessories-wallets','women-accessories','jewelry-watches-watches-women', 'women-accessories-belts','women-accessories-silks-and-scarves','women-accessories-hats-and-gloves'] 
##UNCOMMENT TO RUN, COMMENT OTHER PARSERS, to avoid multi run##
#gucci_parser.process_categories(combined_gucci_categories)


##START FENDI PARSER##
# directory_path = 'internal_html/fendi'
fendi_parser = FendiParser(output_directory_path)
# fendi_parser.parse_directory(directory_path)


###BALLY START
bally_parser = BallyParser()
category_list = ['men-sale.json?', 'women-sale.json?', 'men.json?', 'women.json?']
# bally_parser.process_categories(category_list)

#BALLY END

#STELLA START
#stella_parser = StellaProductParser(output_directory_path)
##Comment to run single file##
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\stella_mccartney'
#stella_parser.parse_directory(directory_path)
#stella end

#givenchy START
#givenchy_parser = GivenchyProductParser(output_directory_path)
##Comment to run single file##
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\givenchy'
#givenchy_parser.parse_directory(directory_path)
#givenchy END




#Canada Goose Start
#canada_goose_parser = CanadaGooseProductParser(output_directory_path)
##Comment to run single file##
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\canada_goose'
#canada_goose_parser.parse_directory(directory_path)

#Canada Goose END


#Isabel Marant Start
#Isabel_Marant_Parser = IsabelMarantParser(output_directory_path)
##Comment to run single file##
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\isabel_marant'
#Isabel_Marant_Parser.parse_directory(directory_path)