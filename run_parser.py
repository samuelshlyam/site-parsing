import os
from brand_parser import BottegaVenetaParser, GucciProductParser, BallyProductParser, StellaProductParser, ChloeProductParser, \
    GivenchyProductParser, CanadaGooseProductParser, IsabelMarantProductParser, MCMProductParser, CultGaiaProductParser, \
    GoldenGooseProductParser, FendiProductParser, BalenciagaProductParser, SaintLaurentProductParser, AlexanderMcqueenParser, \
    DolceGabbanaProductParser, StoneIslandProductParser, EtroProductParser, MonclerProductParser, BalmainProductParser, \
    VersaceProductParser, FerragamoProductParser, BurberryProductParser, KenzoProductParser, VejaProductParser, JimmyChooProductParser, \
    BrunelloCucinelliProductParser, DSquaredProductParser, CelineProductParser, LoroPianaProductParser, MarniProductParser, PradaProductParser, TodsProductParser, \
    ValentinoProductParser, JacquemusProductParser, LouboutinProductParser, PalmAngelsProductParser, MooseKnucklesProductParser, AcneStudiosProductParser, \
    TheRowProductParser, ManoloBlahnikProductParser, GianvitoRossiProductParser, MiuMiuProductParser, BirkenstockProductParser, AquazzuraProductParser, \
    OffWhiteProductParser, TomFordProductParser, LoeweProductParser, HernoProductParser, LanvinProductParser


#Folder name for output
output_directory_path = "parser-output"
current_directory= os.getcwd()
main_directory=os.path.join(current_directory,'internal_html')
print(main_directory)


#Bottega Veneta Start
# BottegaParser = BottegaVenetaParser(output_directory_path)
# directory_path = os.path.join(main_directory,'bottega_veneta')
# BottegaParser.parse_directory(directory_path)
#Bottega Veneta End

#Gucci Start
# GucciParser = GucciProductParser()
# combined_gucci_categories = ['men-bags', 'men-bags-luggage','men-readytowear','men-shoes','men-accessories-wallets','men-accessories-hats-and-gloves','men-accessories-belts','men-eyewear','jewelry-watches-watches-men','men-accessories','women-shoes','women-handbags','women-accessories-lifestyle-bags-and-luggage','women-readytowear','women-accessories-wallets','women-accessories','jewelry-watches-watches-women', 'women-accessories-belts','women-accessories-silks-and-scarves','women-accessories-hats-and-gloves']
# locales=['it/it','us/en']
# GucciParser.process_categories(combined_gucci_categories,locales,output_directory_path)
#Gucci End

# START PARSER##
# FendiParser = FendiProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'fendi')
# FendiParser.parse_directory(directory_path)
#Fendi END



#BALLY START
# BallyParser = BallyProductParser()
# category_list = ['men-sale.json', 'women-sale.json', 'men.json', 'women.json']
# BallyParser.process_categories(category_list)
#BALLY END

#STELLA START
#StellParser = StellaProductParser(output_directory_path)
#directory_path = os.path.join(main_directory,'stella_mccartney')
#StellParser.parse_directory(directory_path)
#stella end

# Off White START
# OffWhiteParser = OffWhiteProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'off_white')
# OffWhiteParser.parse_directory(directory_path)
# Off White end

#givenchy START
#GivenchyParser = GivenchyProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'givenchy')
#GivenchyParser.parse_directory(directory_path)
#givenchy END


#Canada Goose Start
#CanadaGooseParser = CanadaGooseProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'canada_goose')
#CanadaGooseParser.parse_directory(directory_path)
#Canada Goose END

#Veja Start
#VejaParser = VejaProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'veja')
#VejaParser.parse_directory(directory_path)
#Veja End



#Isabel Marant Start
#IsabelMarantParser = IsabelMarantProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'isabel_marant')
#IsabelMarantParser.parse_directory(directory_path)
#Isabel Marant End

#Chloe Start
# ChloeParser=ChloeProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'chloe')
# ChloeParser.parse_directory(directory_path)
#Chloe End

#MCM start
#MCMParser=MCMProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'mcm')
#mcm_parser.parse_directory(directory_path)
#MCM End

# #Cult Gaia Start
# CultGaiaParser=CultGaiaProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'cult_gaia')
# CultGaiaParser.parse_directory(directory_path)
# #Cult Gaia end

#Golden Goose Start
#GoldenGooseParser=GoldenGooseProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'canada_goose')
#GoldenGooseParser.parse_directory(directory_path)
#Golden Goose End

#Balenciaga Start
#BalenciagaParser=BalenciagaProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'balenciaga')
#BalenciagaParser.parse_directory(directory_path)
#Balenciaga End

#Old Version
# YSL Start
# SaintLaurentParser=SaintLaurentProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'ysl')
# SaintLaurentParser.parse_directory(directory_path)
# YSL End
#Old Version



#Alexander Mcqueen Start
# women_categories = ['w-ready-to-wear','W-All-Shoes' ,'W-All-Bags','W-All-Accessories','w-jewellery' ]  # Assuming you have a list of categories
# men_categories = ['M-All-Ready-to-Wear','M-Shoes','M-All-Accessories', 'm-jewellery','M-Bags']
# women_base_url = "https://www.alexandermcqueen.com/api/v1/category/women?locale={locale}&categoryIds={clothing_category}&page={page}&hitsPerPage=30"
# men_base_url = "https://www.alexandermcqueen.com/api/v1/category/men?locale={locale}&categoryIds={clothing_category}&page={page}&hitsPerPage=30"
# category_dicts=[{'category_list':women_categories, 'base_url':women_base_url,'gender':'W'},{'category_list':men_categories,'base_url':men_base_url,'gender':'M'}]
# directory_path = '/content/drive/MyDrive/msrp_archive_raw/alexander_mcqueen/2024-07-08_12-45-00/W/'
# locales=['en-it','en-us',]
# AlexandarMcqueenParser=AlexanderMcqueenParser()
# AlexandarMcqueenParser.process_categories(category_dicts,output_directory_path,locales)
#Alexander Mcqueen End

#Dolce Start
# bearer_token= "eyJ2ZXIiOiIxLjAiLCJqa3UiOiJzbGFzL3Byb2QvYmtkYl9wcmQiLCJraWQiOiI4NzNlMTc0ZC03YzU5LTQ5NWMtYTZlNi02MzY3MDhiMDViMjUiLCJ0eXAiOiJqd3QiLCJjbHYiOiJKMi4zLjQiLCJhbGciOiJFUzI1NiJ9.eyJhdXQiOiJHVUlEIiwic2NwIjoic2ZjYy5zaG9wcGVyLW15YWNjb3VudC5iYXNrZXRzIHNmY2Muc2hvcHBlci1kaXNjb3Zlcnktc2VhcmNoIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzIHNmY2Muc2hvcHBlci1jdXN0b21lcnMubG9naW4gc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5vcmRlcnMgc2ZjYy5zaG9wcGVyLXByb2R1Y3RsaXN0cyBzZmNjLnNob3BwZXItcHJvbW90aW9ucyBzZmNjLnNob3BwZXIuc3RvcmVzIHNmY2Mub3JkZXJzLnJ3IHNmY2Muc2Vzc2lvbl9icmlkZ2Ugc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5wYXltZW50aW5zdHJ1bWVudHMucncgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5wcm9kdWN0bGlzdHMgc2ZjYy5zaG9wcGVyLWNhdGVnb3JpZXMgc2ZjYy5zaG9wcGVyLW15YWNjb3VudCBzZmNjLnNob3BwZXItbXlhY2NvdW50LmFkZHJlc3NlcyBzZmNjLnNob3BwZXItcHJvZHVjdHMgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5ydyBzZmNjLnNob3BwZXItY29udGV4dC5ydyBzZmNjLnNob3BwZXItYmFza2V0cy1vcmRlcnMgc2ZjYy5zaG9wcGVyLWN1c3RvbWVycy5yZWdpc3RlciBzZmNjLnNob3BwZXItbXlhY2NvdW50LmFkZHJlc3Nlcy5ydyBzZmNjLnNob3BwZXItbXlhY2NvdW50LnByb2R1Y3RsaXN0cy5ydyBzZmNjLnNob3BwZXItcHJvZHVjdCBzZmNjLnNob3BwZXItYmFza2V0cy1vcmRlcnMucncgc2ZjYy5zaG9wcGVyLWdpZnQtY2VydGlmaWNhdGVzIHNmY2Muc2hvcHBlci1wcm9kdWN0LXNlYXJjaCIsInN1YiI6ImNjLXNsYXM6OmJrZGJfcHJkOjpzY2lkOjAxYzNhMjlmLTMzNmMtNDlkNS04ZWJlLWMxMzNmZjk4Mjk0NTo6dXNpZDo5OTQzNTAwZi1lMmQyLTQyODYtOGYzOC0zM2MwZWU3OTEyYWIiLCJjdHgiOiJzbGFzIiwiaXNzIjoic2xhcy9wcm9kL2JrZGJfcHJkIiwiaXN0IjoxLCJkbnQiOiIwIiwiYXVkIjoiY29tbWVyY2VjbG91ZC9wcm9kL2JrZGJfcHJkIiwibmJmIjoxNzIyODc3MDU0LCJzdHkiOiJVc2VyIiwiaXNiIjoidWlkbzpzbGFzOjp1cG46R3Vlc3Q6OnVpZG46R3Vlc3QgVXNlcjo6Z2NpZDphYm1ySVlrWHNVa2V3UnhyaElrR1lZa0hFMDo6Y2hpZDogIiwiZXhwIjoxNzIyODc4ODg0LCJpYXQiOjE3MjI4NzcwODQsImp0aSI6IkMyQzc3NTc1MzE4MjAtMTYwMDU0NTkwNzE3MjQ5NTk2NzM5NTcyNzEifQ.uhUkPNM4Ro7xxMQltX9YAv2R4vn7LBya5eevXp7JEoLmGc-0OaxxU7nECw1Nq7J7Uud2CP-xl98eRBPcbNQO_Q"
# # categories = ['cgid%3Dwomen-bags', 'cgid%3Dwomen-apparel', 'cgid%3Djewellry-for-her', 'cgid%3Dwomen-shoes',
# #              'cgid%3Dwomen-accessories', 'cgid%3Dwomen-accessories-sunglasses', 'cgid%3Dmen-apparel',
# #              'cgid%3Dmen-tailoring', 'cgid%3Dmen-bags', 'cgid%3Dmen-shoes', 'cgid%3Dmen-accessories',
# #              'cgid%3Dmen-accessories-sunglasses', 'cgid%3Djewellry-for-him']
# categories=['']
# info_dicts=[{'site_id':'dolcegabbana_us','locale':'en','limit':200},{'site_id':'dolcegabbana','locale':'it','limit':200}]
# DolceParser=DolceGabbanaProductParser()
# DolceParser.process_categories(categories,bearer_token,info_dicts)
#Dolce End

#Stone Island Start
#StoneIslandParser = StoneIslandProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'stone_island')
#StoneIslandParser.parse_directory(directory_path)
#Stone Island End


#Etro Start
#EtroParser = EtroProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'etro')
#EtroParser.parse_directory(directory_path)
#Etro End

#Balmain Start
#BalmainParser = BalmainProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'balmain')
#BalmainParser.parse_directory(directory_path)
#Balmain End


#Moncler Start
# categories = ['men','women','children']
# country_codes=['Sites-MonclerEU-Site/en_IT','Sites-MonclerUS-Site/en_US']
# MonclerParser=MonclerProductParser()
# MonclerParser.process_categories(categories,country_codes)
#Moncler End

#Versace Start
#VersaceParser = VersaceProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'versace')
#VersaceParser.parse_directory(directory_path)
#Versace End

#Ferragamo Start
#FerragamoParser = FerragamoProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'ferragamo')
#FerragamoParser.parse_directory(directory_path)
#Ferragamo End


#Burberry Start
#BurberryParser = BurberryProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'burberry')
#BurberryParser.parse_directory(directory_path)
#Burberry End


#Kenzo Start
#KenzoParser = KenzoProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'kenzo')
#KenzoParser.parse_directory(directory_path)
#Kenzo End


#Jimmy Choo Start
#JimmyChooParser = JimmyChooProductParser(output_directory_path)
#directory_path = os.path.join(main_directory,'jimmy_choo')
#JimmyChooParser.parse_directory(directory_path)
#JimmyChoo End


#Brunello Cucinelli Start
#BrunelloCucinelliParser = BrunelloCucinelliProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'brunello_cucinelli')
#BrunelloCucinelliParser.parse_directory(directory_path)
#Brunello Cucinelli End

#DSquared2 Start
#DSquaredParser = DSquaredProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'dsquared2')
#DSquaredParser.parse_directory(directory_path)
#DSquared2 End


#Celine Start
#CelineParser = CelineProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'celine')
#CelineParser.parse_directory(directory_path)
#Celine End


#Loro Piana Start
# categories=['L1_MEN','L1_WOM','L2_MEN_ACCESSORIES','L2_WOM_LG','L2_WOM_ACCESSORIES','L2_SHOES_WOM','L2_WOM_SLG','L2_SHOES_MAN','L2_DIGITALFW24_MAN','L2_DIGITALFW24_WOM','L2_SS23_WOM','L2_SS23_MAN']
# LoroPianaParser=LoroPianaProductParser()
# country_codes=[{'country_code':'it', 'locale':'it'},{'country_code':'en', 'locale':'us'}]
# LoroPianaParser.process_categories(categories, country_codes)
#Loro Piana End


#Marni Start
#MarniParser = MarniProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'marni')
#MarniParser.parse_directory(directory_path)
#Marni End

#Prada Start
#PradaParser = PradaProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'prada')
#PradaParser.parse_directory(directory_path)
#Prada End

#Tods Start
#TodsParser = TodsProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'tods')
#TodsParser.parse_directory(directory_path)
#Tods End

#Valentino Start
#ValentinoParser = ValentinoProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'valentino')
#ValentinoParser.parse_directory(directory_path)
#Valentino End

#Jacquemus Start
#JacquemusParser = JacquemusProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'jacquemus')
#JacquemusParser.parse_directory(directory_path)
#Jacquemus End

#Louboutin Start
# LouboutinParser = LouboutinProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'louboutin')
# LouboutinParser.parse_directory(directory_path)
#Louboutin End

#Palm Angels Start
# PalmAngelsParser = PalmAngelsProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'palm_angels_7-23-24')
# PalmAngelsParser.parse_directory(directory_path)
#PalmAngels End

#Moose Knuckles Start
#MooseKnucklesParser = MooseKnucklesProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'moose_knucles')
#MooseKnucklesParser.parse_directory(directory_path)
#Moose Knuckles End

#Acne Studios Start
# AcneStudiosParser = AcneStudiosProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'acne_studios')
# AcneStudiosParser.parse_directory(directory_path)
#Acne Studios End

#The Row Start
# TheRowParser = TheRowProductParser(output_directory_path)
# directory_path = os.path.join(main_directory, 'the_row')
# TheRowParser.parse_directory(directory_path)
#The Row End

#Manolo Blahnik Start
#ManoloBlahnikParser = ManoloBlahnikProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'manolo_blahnik')
#ManoloBlahnikParser.parse_directory(directory_path)
#Manolo Blahnik End

#Gianvito Rossi Start
#GianvitoRossiParser = GianvitoRossiProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'gianvito_rossi')
#GianvitoRossiParser.parse_directory(directory_path)
#Gianvito Rossi End

#Miu Miu Start
#miuMiuParser = MiuMiuProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'miu_miu')
#miuMiuParser.parse_directory(directory_path)
#Gianvito Rossi End

#Birkenstock Start
#BirkenstockParser = BirkenstockProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'birkenstock')
#BirkenstockParser.parse_directory(directory_path)
#Birkenstock End

#Aquazzura Start
#AquazzuraParser = AquazzuraProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,'aquazzura')
#AquazzuraParser.parse_directory(directory_path)
#Aquazzura End

#Tom Ford Start
# TomFordParser = TomFordProductParser(output_directory_path)
# directory_path = os.path.join(main_directory,"tom_ford")
# TomFordParser.parse_directory(directory_path)
#Tom Ford End

#Loewe Start
# bearer_token= "eyJ2ZXIiOiIxLjAiLCJqa3UiOiJzbGFzL3Byb2QvYmJwY19wcmQiLCJraWQiOiIwMjVjNzdjZS04MGYxLTRjNTEtOTU0NC1lMWFiODMyMTMzNjYiLCJ0eXAiOiJqd3QiLCJjbHYiOiJKMi4zLjQiLCJhbGciOiJFUzI1NiJ9.eyJhdXQiOiJHVUlEIiwic2NwIjoic2ZjYy5zaG9wcGVyLW15YWNjb3VudC5iYXNrZXRzIHNmY2Muc2hvcHBlci1kaXNjb3Zlcnktc2VhcmNoIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzIHNmY2Muc2hvcHBlci1jdXN0b21lcnMubG9naW4gc2ZjYy5zaG9wcGVyLWV4cGVyaWVuY2Ugc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5vcmRlcnMgc2ZjYy5zaG9wcGVyLXByb2R1Y3RsaXN0cyBzZmNjLnNob3BwZXItcHJvbW90aW9ucyBzZmNjLnNlc3Npb25fYnJpZGdlIHNmY2Muc2hvcHBlci1teWFjY291bnQucGF5bWVudGluc3RydW1lbnRzLnJ3IHNmY2Muc2hvcHBlci1teWFjY291bnQucHJvZHVjdGxpc3RzIHNmY2Muc2hvcHBlci1jYXRlZ29yaWVzIHNmY2Muc2hvcHBlci1teWFjY291bnQgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5hZGRyZXNzZXMgc2ZjYy5zaG9wcGVyLXByb2R1Y3RzIHNmY2Muc2hvcHBlci1teWFjY291bnQucncgc2ZjYy5zaG9wcGVyLWNvbnRleHQucncgc2ZjYy5zaG9wcGVyLWJhc2tldHMtb3JkZXJzIHNmY2Muc2hvcHBlci1jdXN0b21lcnMucmVnaXN0ZXIgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5hZGRyZXNzZXMucncgc2ZjYy5zaG9wcGVyLW15YWNjb3VudC5wcm9kdWN0bGlzdHMucncgc2ZjYy5zaG9wcGVyLWJhc2tldHMtb3JkZXJzLnJ3IHNmY2Muc2hvcHBlci1naWZ0LWNlcnRpZmljYXRlcyBzZmNjLnNob3BwZXItcHJvZHVjdC1zZWFyY2ggc2ZjYy5zaG9wcGVyLXNlbyIsInN1YiI6ImNjLXNsYXM6OmJicGNfcHJkOjpzY2lkOjJiNTYzYTRlLWI1MTAtNDE0My05N2UxLWY0NTQxNTk2M2UyMTo6dXNpZDphYjQ3MDZlYS03ODJkLTQ4Y2ItOGMxNy0xODQ0YjYzMDgwZTkiLCJjdHgiOiJzbGFzIiwiaXNzIjoic2xhcy9wcm9kL2JicGNfcHJkIiwiaXN0IjoxLCJkbnQiOiIwIiwiYXVkIjoiY29tbWVyY2VjbG91ZC9wcm9kL2JicGNfcHJkIiwibmJmIjoxNzIyODc4OTI5LCJzdHkiOiJVc2VyIiwiaXNiIjoidWlkbzpzbGFzOjp1cG46R3Vlc3Q6OnVpZG46R3Vlc3QgVXNlcjo6Z2NpZDpiZHd1Z1lsWGEweHVjUmxYRVd4YllZbWVsRzo6Y2hpZDpMT0VfVVNBIiwiZXhwIjoxNzIyODgwNzU5LCJpYXQiOjE3MjI4Nzg5NTksImp0aSI6IkMyQzE3MjI2Mjc5NzgwLTY1MzY3MTExMTE3MjY3NDk0MzA4MjUxMzcifQ.UiMljhre39gXjNOPs81H0Irb3MUXwq2tRM8zl-2DkhRG2F64kPQGXRd-NvRuLF97JRvw4EEtXZ0ecUIiLNh0Rw"
# categories = ['cgid%3Dwomen','cgid%3Dmen','cgid%3Dm_fw_collection','cgid%3Dw_fw_precollection']
# country_dicts=[{'country_code':'IT','locale':'en','limit':200,'site_id':'LOE_EUR'},{'country_code':'USA','locale':'en-US','limit':200,'site_id':'LOE_USA'}]
# LoeweParser=LoeweProductParser()
# LoeweParser.process_categories(categories,bearer_token,country_dicts)
#Loewe End

#Saint Laurent Start
# categories = ['view-all-shoes-women','view-all-rtw-women','view-all-handbags-women','view-all-slg-women','view-all-jewelry-women','view-all-accessories-women','view-all-rtw-men','view-all-shoes-men','view-all-slg-men','view-all-accessories-men','view-all-bags-men','highlights-women-collection','highlights-men-collection',]
# country_code=['en-it','en-us']
# SaintLaurentParser=SaintLaurentProductParser()
# SaintLaurentParser.process_categories(categories,country_code)
#Saint Laurent End

#Tods Start
# TodsParser=TodsProductParser()
# cookie='ftr_ncd=6; mt.v=2.91441120.1720795186835; __attentive_id=9dd8fdfb2a634a25b33a05bddbaea5a4; _attn_=eyJ1Ijoie1wiY29cIjoxNzIwNzk1MTg3MzU5LFwidW9cIjoxNzIwNzk1MTg3MzU5LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcIjlkZDhmZGZiMmE2MzRhMjViMzNhMDViZGRiYWVhNWE0XCJ9In0=; __attentive_cco=1720795187360; OptanonAlertBoxClosed=2024-07-12T14:39:50.226Z; nodeClientToken=TgPITCn5tGqje8P1IHOIdSbrvKA; USER=%7B%22username%22%3A%22anonymous%22%2C%22customerId%22%3A%22anonymous%22%2C%22type%22%3A%22anonymous%22%2C%22accessToken%22%3A%22oXyZLwV-y6eQeBiG130xNZoCpQM%22%7D; nodeSessionId=%22a8b149b3-1990-4cc9-8141-383409795986%22; countryIP=US; AKA_A2=A; _abck=33603576242A74C7496127C28B0E34BE~0~YAAQxMgsFxyITLaQAQAAsdx4vAz7v4KHhurJZlkz46njo3UgqOW0FTcivTzeS4zOIwaVqFY3mrKysCFXEd5hHhnOLdUc807Y73AwEMiujNE3TeCLh6+LPyfBeoTQre39GPsbrvsUUiInpajb1gl0yibi7Noffe6uF78/koZmMOWXOCSyjXx98a7iHPHZzJxMdmPfvFlNNaOmzcg4ubvHfGlZl+ljbpMZjjOKRKmHZsHiJeDqvRrajsJimsPBALa9U1fuJRfDvi2IWDpQMoZKHfN1lsPWokA/k7npRZXZrN4VZ2p+3+yAkd37JjWaMReVjcl9onUCbm/JCXeVSLZq6z5/UyD1FhgCgFEtqO0HEPW9Xg0/S2E89xDeG01xYhA+QvOYPBo3u+27fmWT4669aiQXYNmH1w==~-1~-1~-1; bm_sz=B8F44CA3495E1A73521F76314743EF9F~YAAQxMgsFx+ITLaQAQAAsdx4vBhLG433z000loJxqejKosGvRTFO4/uZadpG5wM7aaDqZiyvNoeubCk2HM9V6tzIdXSkkh7LBaygbZ5efC2FuzKJbfS6vZ54H1PwhWmztzHzEavvEImqhnIPB/LzPsodWyTIaTOriEsDXjX11wtO7Y6WO+dtLiHtvtnRUqlzRsRmS6VFgRIhM8odNnN2tJl5Ril+7ZpjG7X6MZ108n1gFVWp0+1B+Zrs3ecqB6EymP0x7EP7Tl+X+j6URTV3bmN9MYTaGzHR/c4PPNlA4Cx6s+AR6xHTyxB1JkZDfnssFCsOSHoZR9RN4mB6OxWZbKmISWeqANpm1u/mVEQtBbKWFziElAtok6Ojx7i+NRaqfwdmnrPWKis+j5gb7Sg=~4536642~3621174; PIM-SESSION-ID=IAUZPefx620he0If; _cs_mk_ga=0.0739706499717212_1721148957046; _gid=GA1.2.1855863707.1721148957; _ga=GA1.2.1520502800.1720795186; ak_bmsc=A3858ABE0725B00A0AF17AAF79053C7C~000000000000000000000000000000~YAAQxMgsF0CJTLaQAQAATOh4vBiAMseTevUJYssKk+/Hiiffh7Yb/prqOaEQufn7cO6uqUYanYV4iEBhl7Rn7DM9NZWNZD+MSKWaT7QEn83uVL3au+HPR1mnbzLe4n01H4jrhT2i8Ai4JrPNmBQaKGPzhvgRP2sEhrBv5h1h5dY8xWnRj7F69U7O0P9lW1KfKjlc+Tx5ZU7ZoOpLXVZ6eNLZoa4j7gg264NJP6l/jC9DBNsKpvKlcGBKG1BnNVMGAIq0hn8cByMQUzFiqTgCMmo8n562HqgaIC7ZYC9g1nGFR/IyFSaUlUdOJeU+JBcPi98uzRd2U4YNlj8VDtckzmdB1+adD3Ge+BFsLXl22vfd5BQjeriDAwzb+cMMQeSOvuWBncToFqUv6vmEu1Bw4Rh30ADSRnUgg864mjcNYkHLv5dq9sqo3QxoaRzYhA==; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+16+2024+12%3A55%3A58+GMT-0400+(Eastern+Daylight+Time)&version=202405.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=073ae49f-e470-48e1-b404-312cac8c5717&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0&intType=undefined&geolocation=%3B&AwaitingReconsent=false; forterToken=ca43b01699004ab88ab9fccb53451566_1721148956606__UDF43-m4_9ck_; QueueITAccepted-SDFrts345E-V3_tods=EventId%3Dtods%26QueueId%3D77e7644b-2e59-4cfa-a8aa-d3e692510e6f%26RedirectType%3Dsafetynet%26IssueTime%3D1721148959%26Hash%3D15e619f44015c99375b3b5d9fe6654de45f808f4d8353e292ff46ee149787465; __attentive_utm_param_medium=cpc; __attentive_utm_param_source=google; __attentive_utm_param_campaign=W_US_Tods_Search_Brand_Pure_Exact_MS; __attentive_ss_referrer=https://www.google.com/; __attentive_dv=1; __attentive_pv=2; RT="z=1&dm=tods.com&si=2d6b53f5-49d7-4666-97b8-76c5eb97df45&ss=lyonnckv&sl=1&tt=3w7&rl=1&ld=3w9&nu=pmxcb4ms&cl=j7a"; _ga_YMQ83SWR7E=GS1.1.1721148957.2.1.1721148979.0.0.0; bm_sv=B1F13FA6025020E76AB4B3D4137F7FD1~YAAQxMgsF4KNTLaQAQAAmD15vBjIqF+J5NX8tq+eNAievVRfZB6Bz/12ZwQ2tHn8pt7jim6s//uSxD4ZJJYrl7rN6SHeVCCsKlNz/TicQQfEWwVeJnG1c9SAzxWPKIC4CyztE3vtDfEYhd4lW8g3cq6yiFsVnqsLXEUC7hvN9X2FYQH1c56pjkkEnKC3uptSwtFGt/VIZJdO373LjA8B/OB86xwEZpdC2X3EkAtz4EN9lOIXb8FAP9nKN9PJZg==~1'
# categories=TodsProductParser.fetch_categories(cookie)
# print(categories)
# TodsParser.process_categories(categories,cookie)
#Tods End


#Herno Start
#HernoParser = HernoProductParser(output_directory_path)
#directory_path = os.path.join(main_directory, 'herno')
#HernoParser.parse_directory(directory_path)
#Herno End

#Lanvin Start
# LanvinParser = LanvinProductParser(output_directory_path)
# directory_path = os.path.join(main_directory, 'lanvin')
# LanvinParser.parse_directory(directory_path)
#Lanvin End
