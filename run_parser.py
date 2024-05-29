import os
from brand_parser import BottegaVenetaParser, GucciParser, FendiParser, BallyParser, StellaProductParser, Chloe_Parser, \
    GivenchyProductParser, CanadaGooseProductParser, IsabelMarantParser, MCM_Parser, CultGaiaProductParser, \
    GoldenGooseProductParser, FendiParser, BalenciagaParser, SaintLaurentParser, AlexanderMcqueenParser, \
    Dolce_Gabbana_Parser, StoneIslandParser

#Folder name for output
output_directory_path = "parser-output"
#directory_path = 'brands_html/bottega_veneta'
##Bottega Veneta Parser METHOD 1##
#bottega_parser = BottegaVenetaParser(output_directory_path)
##SINGLE FILE RUN##
#input_file_path = 'brands_html/bottega_veneta/women_bags.html'
#category = os.path.splitext(input_file_path)[0]  # Use the filename as the category
##Uncomment to run##
#bottega_parser_output = bottega_parser.parse_website(input_file_path, category)
#bottega_parser.write_to_csv(bottega_parser_output)

##MULTIPLE FILE RUN, PASS DIRECTORY PATH
##Comment to run single file##
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\bottega_veneta'
#bottega_parser.parse_directory(directory_path)


#GUCCI PRODUCT FETCH METHOD 2##

#gucci_parser = GucciParser()

#gucci_categories_womens = ['women-shoes','women-handbags','women-accessories-lifestyle-bags-and-luggage','women-readytowear','women-accessories-wallets','women-accessories','jewelry-watches-watches-women', 'women-accessories-belts','women-accessories-silks-and-scarves','women-accessories-hats-and-gloves']
#gucci_categories_mens = ['men-bags', 'men-bags-luggage','men-readytowear','men-shoes','men-accessories-wallets','men-accessories-hats-and-gloves','men-accessories-belts','men-eyewear','jewelry-watches-watches-men','men-accessories']
#combined_gucci_categories = ['men-bags', 'men-bags-luggage','men-readytowear','men-shoes','men-accessories-wallets','men-accessories-hats-and-gloves','men-accessories-belts','men-eyewear','jewelry-watches-watches-men','men-accessories','women-shoes','women-handbags','women-accessories-lifestyle-bags-and-luggage','women-readytowear','women-accessories-wallets','women-accessories','jewelry-watches-watches-women', 'women-accessories-belts','women-accessories-silks-and-scarves','women-accessories-hats-and-gloves']
##UNCOMMENT TO RUN, COMMENT OTHER PARSERS, to avoid multi run##
#gucci_parser.process_categories(combined_gucci_categories)


##START FENDI PARSER##
#directory_path = 'internal_html/fendi'
#fendi_parser = FendiParser(output_directory_path)
#fendi_parser.parse_directory(directory_path)
#Fendi END



###BALLY START
#bally_parser = BallyParser()
#category_list = ['men-sale.json?', 'women-sale.json?', 'men.json?', 'women.json?']
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
#Isabel Marant End

#Chloe Start
#Chloe_parser=Chloe_Parser(output_directory_path)
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_files\chloe_parser_julian\brands_html\chloe'
#Chloe_parser.parse_directory(directory_path)
#Chloe End

#MCM start
#mcm_parser=MCM_Parser(output_directory_path)
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\mcm'
#mcm_parser.parse_directory(directory_path)
#MCM End

#Cult Gaia Start
#cult_gaia_parser=CultGaiaProductParser(output_directory_path)
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\cult_gaia'
#cult_gaia_parser.parse_directory(directory_path)
#Cult Gaia end

#Golden Goose Start
#Golden_Goose_ProductParser=GoldenGooseProductParser(output_directory_path)
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\golden_goose'
#Golden_Goose_ProductParser.parse_directory(directory_path)
#Golden Goose End

#Balenciaga Start
#balenciaga_Parser=BalenciagaParser(output_directory_path)
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\balenciaga'
#balenciaga_Parser.parse_directory(directory_path)
#Balenciaga End


#YSL Start
#YSL_Parser=SaintLaurentParser(output_directory_path)
#directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\saint-laurent'
#YSL_Parser.parse_directory(directory_path)
#YSL End




#Alexander Mcqueen Start
#women_categories = ['w-ready-to-wear','W-All-Shoes' ,'W-All-Bags','W-All-Accessories','w-jewellery' ]  # Assuming you have a list of categories
#men_categories = ['M-All-Ready-to-Wear','M-Shoes','M-All-Accessories', 'm-jewellery','M-Bags']
#women_base_url = "https://www.alexandermcqueen.com/api/v1/category/women?locale=en-us&categoryIds={clothing_category}&page={page}"
#men_base_url = "https://www.alexandermcqueen.com/api/v1/category/men?locale=en-us&categoryIds={clothing_category}&page={page}"
#AlexMcqueenMenParser=AlexanderMcqueenParser(men_base_url)
#AlexMcqueenWomenParser=AlexanderMcqueenParser(women_base_url)
#AlexMcqueenMenParser.process_categories(men_categories)
#AlexMcqueenWomenParser.process_categories(women_categories)
#Alexander Mcqueen End

#Dolce Start
#bearer_token= "eyJ2ZXIiOiIxLjAiLCJqa3UiOiJzbGFzL3Byb2QvYmtkYl9wcmQiLCJraWQiOiI4ZTA2MGIwZi0yYjZlLTQ5NWQtOGY4Ny04NDUxOWE3NmRhOWEiLCJ0eXAiOiJqd3QiLCJjbHYiOiJKMi4zLjQiLCJhbGciOiJFUzI1NiJ9.eyJhdXQiOiJHVUlEIiwic2NwIjoic2ZjYy5zaG9wcGVyLW15YWNjb3VudC5iYXNrZXRzIHNmY2Muc2hvcHBlci1kaXNjb3Zlcnktc2VhcmNoIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzIHNmY2Muc2hvcHBlci1jdXN0b21lcnMubG9naW4gc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5vcmRlcnMgc2ZjYy5zaG9wcGVyLXByb2R1Y3RsaXN0cyBzZmNjLnNob3BwZXItcHJvbW90aW9ucyBzZmNjLnNob3BwZXIuc3RvcmVzIHNmY2Mub3JkZXJzLnJ3IHNmY2Muc2Vzc2lvbl9icmlkZ2Ugc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5wYXltZW50aW5zdHJ1bWVudHMucncgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5wcm9kdWN0bGlzdHMgc2ZjYy5zaG9wcGVyLWNhdGVnb3JpZXMgc2ZjYy5zaG9wcGVyLW15YWNjb3VudCBzZmNjLnNob3BwZXItbXlhY2NvdW50LmFkZHJlc3NlcyBzZmNjLnNob3BwZXItcHJvZHVjdHMgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5ydyBzZmNjLnNob3BwZXItY29udGV4dC5ydyBzZmNjLnNob3BwZXItYmFza2V0cy1vcmRlcnMgc2ZjYy5zaG9wcGVyLWN1c3RvbWVycy5yZWdpc3RlciBzZmNjLnNob3BwZXItbXlhY2NvdW50LmFkZHJlc3Nlcy5ydyBzZmNjLnNob3BwZXItbXlhY2NvdW50LnByb2R1Y3RsaXN0cy5ydyBzZmNjLnNob3BwZXItcHJvZHVjdCBzZmNjLnNob3BwZXItYmFza2V0cy1vcmRlcnMucncgc2ZjYy5zaG9wcGVyLWdpZnQtY2VydGlmaWNhdGVzIHNmY2Muc2hvcHBlci1wcm9kdWN0LXNlYXJjaCIsInN1YiI6ImNjLXNsYXM6OmJrZGJfcHJkOjpzY2lkOjAxYzNhMjlmLTMzNmMtNDlkNS04ZWJlLWMxMzNmZjk4Mjk0NTo6dXNpZDo3NzM1MDMyNi1mNjMxLTQxZjItOWE4MC01MzQ3MjBkNDVlMTEiLCJjdHgiOiJzbGFzIiwiaXNzIjoic2xhcy9wcm9kL2JrZGJfcHJkIiwiaXN0IjoxLCJkbnQiOiIwIiwiYXVkIjoiY29tbWVyY2VjbG91ZC9wcm9kL2JrZGJfcHJkIiwibmJmIjoxNzE3MDIxOTA5LCJzdHkiOiJVc2VyIiwiaXNiIjoidWlkbzpzbGFzOjp1cG46R3Vlc3Q6OnVpZG46R3Vlc3QgVXNlcjo6Z2NpZDpiY2xYQVhscmFYa0h3UnhId1hrcVlZa3V3Vzo6Y2hpZDogIiwiZXhwIjoxNzE3MDIzNzM5LCJpYXQiOjE3MTcwMjE5MzksImp0aSI6IkMyQzc3NTc1MzE4MjAtMTYwMDU0NTkwNzE4MTUwNDA4MzQ1MzE2NDgifQ.cAcmEZb_x-YVfEpSn-MrIcO1UjtaL9wdG9QudX7RpdZHoGQxSNq-OVqKgyJpu3f7wPw1tT4EYN_k_AsBv_GsLg"
#categories = ['cgid%3Dwomen-bags', 'cgid%3Dwomen-apparel', 'cgid%3Djewellry-for-her', 'cgid%3Dwomen-shoes',
#              'cgid%3Dwomen-accessories', 'cgid%3Dwomen-accessories-sunglasses', 'cgid%3Dmen-apparel',
#              'cgid%3Dmen-tailoring', 'cgid%3Dmen-bags', 'cgid%3Dmen-shoes', 'cgid%3Dmen-accessories',
#              'cgid%3Dmen-accessories-sunglasses', 'cgid%3Djewellry-for-him']
#Dolce_Parser=Dolce_Gabbana_Parser()
#Dolce_Parser.process_categories(categories,bearer_token)
#Dolce End

#Stone Island Start
StoneParser = StoneIslandParser(output_directory_path)
directory_path = r'C:\Users\User\PycharmProjects\pythonProject\site-parsing\internal_html\stone_island'
StoneParser.parse_directory(directory_path)
#Stone Island End