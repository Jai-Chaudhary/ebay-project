# -*- coding: utf-8 -*-
'''
© 2012-2013 eBay Software Foundation
Authored by: Tim Keefer
Licensed under CDDL 1.0
'''

import os
import sys
import lxml

from optparse import OptionParser

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

import ebaysdk
from ebaysdk.soa.finditem import Connection as FindItem
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.utils import getNodeText
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError

def init_options():
        usage = "usage: %prog [options]"
        parser = OptionParser(usage=usage)

        parser.add_option("-d", "--debug",
                                            action="store_true", dest="debug", default=False,
                                            help="Enabled debugging [default: %default]")
        parser.add_option("-y", "--yaml",
                                            dest="yaml", default='ebay.yaml',
                                            help="Specifies the name of the YAML defaults file. [default: %default]")
        parser.add_option("-a", "--appid",
                                            dest="appid", default=None,
                                            help="Specifies the eBay application id to use.")
        parser.add_option("-c", "--consumer_id",
                                            dest="consumer_id", default=None,
                                            help="Specifies the eBay consumer_id id to use.")

        (opts, args) = parser.parse_args()
        return opts, args

def run(opts):



    # # SubCategories of Women Accessories
    # category_ids = {'163573':  'belt-buckles',
    #                 '3003' :   'belts',
    #                 '177651' : 'collar-tips',
    #                 '168998' : 'fascinators-headpieces',
    #                 '105559' : 'gloves-mittens',
    #                 '45220' :  'hair-accessories',
    #                 '167906' : 'handkerchiefs',
    #                 '45230' :  'hats',
    #                 '169285' : 'id-document-holders',
    #                 '45237' :  'key-chains-rings-finders',
    #                 '15735' :  'organizers-day-planners',
    #                 '45238' :  'scarves-wraps',
    #                 '150955' : 'shoe-charms-jibbitz',
    #                 '179247' : 'sunglasses-fashion-eyewear',
    #                 '151486' : 'ties',
    #                 # '105569' : 'umbrellas',
    #                 '45258' :  'wallets',
    #                 '175634' : 'wigs-extensions-supplies',
    #                 # '106129' : 'wristbands',
    #                 '15738' :  'mixed-items-lots',
    #                 '1063' :   'other',
                   # }
    # collectibles category
    # category_ids = {'1': 'general',
    #                 '34'    :  'Advertising', 
    #                 '1335'  :    'Animals', 
    #                 '13658' :   'Animation Art & Characters',  
    #                 '66502' :   'Arcade, Jukeboxes & Pinball', 
    #                 '14429' :   'Autographs',  
    #                 '66503' :   'Banks, Registers & Vending',  
    #                 '3265'  :    'Barware', 
    #                 '156277'    :  'Beads',   
    #                 '29797' :   'Bottles & Insulators',    
    #                 '562'   : 'Breweriana, Beer',    
    #                 '898'   : 'Casino',  
    #                 '397'   : 'Clocks',  
    #                 '63'    :  'Comics',  
    #                 '3913'  :    'Cultures & Ethnicities',  
    #                 '13777' :   'Decorative Collectibles', 
    #                 '137'   : 'Disneyana',   
    #                 '10860' :   'Fantasy, Mythical & Magic',   
    #                 '13877' :   'Historical Memorabilia',  
    #                 '907'   : 'Holiday & Seasonal',  
    #                 '13905' :   'Kitchen & Home',  
    #                 '1401'  :    'Knives, Swords & Blades', 
    #                 '1404'  :    'Lamps, Lighting', 
    #                 '940'   : 'Linens & Textiles (1930-Now)',    
    #                 '1430'  :    'Metalware',   
    #                 '13956' :   'Militaria',   
    #                 '124'   : 'Paper',   
    #                 '966'   : 'Pens & Writing Instruments',  
    #                 '14005' :   'Pez, Keychains, Promo Glasses',   
    #                 '14277' :   'Photographic Images', 
    #                 '39507' :   'Pinbacks, Bobbles, Lunchboxes',   
    #                 '914'   : 'Postcards',   
    #                 '29832' :   'Radio, Phonograph, TV, Phone',    
    #                 '1446'  :    'Religion & Spirituality', 
    #                 '3213'  :    'Rocks, Fossils & Minerals',   
    #                 '152'   : 'Science Fiction & Horror',    
    #                 '412'   : 'Science & Medicine (1930-Now)',   
    #                 '113'   : 'Sewing (1930-Now)',   
    #                 '165800'    :  'Souvenirs & Travel Memorabilia',  
    #                 '593'   : 'Tobacciana',  
    #                 '13849' :   'Tools, Hardware & Locks', 
    #                 '868'   : 'Trading Cards',   
    #                 '417'   : 'Transportation',  
    #                 '597'   : 'Vanity, Perfume & Shaving',   
    #                 '69851' :   'Vintage, Retro, Mid-Century', 
    #                 '45058' :   'Wholesale Lots',  
    #                }

    # category_ids = {
    #                 '137085'    :  'Athletic Apparel',
    #                 '63862' :   'Coats & Jackets',
    #                 '63861' :   'Dresses',
    #                 '11524' :   'Hosiery & Socks',
    #                 '11514' :   'Intimates & Sleep',
    #                 '11554' :   'Jeans',
    #                 '3009'  :    'Jumpsuits & Rompers',
    #                 '169001'    :  'Leggings',
    #                 '172378'    :  'Maternity',
    #                 '63863' :   'Pants',
    #                 '11555' :   'Shorts',
    #                 '63864' :   'Skirts',
    #                 '63865' :   'Suits & Blazers',
    #                 '63866' :   'Sweaters',
    #                 '155226'    :  'Sweats & Hoodies',
    #                 '63867' :   'Swimwear',
    #                 '63869' :   'T-Shirts',
    #                 '53159' :   'Tops & Blouses',
    #                 '15775' :   'Vests',
    #                 '84275' :   'Mixed Items & Lots',
    #                 '314'   : 'Other'
    #                 }

    # category_ids = {
    #     '3034'  :   'general',
    #     '95672' :   'Athletic',
    #     '53557' :   'Boots',
    #     '45333' :   'Flats & Oxfords',
    #     '55793' :   'Heels',
    #     '53548' :   'Occupational',
    #     '62107' :   'Sandals & Flip Flops',
    #     '11632' :   'Slippers',
    #     '63889' :   'Mixed Items & Lots',
    # }

    category_ids = {
                    '220'   : 'general',
                    '246'   : 'Action Figures',
                    '49019' :   'Beanbag Plush',
                    '18991' :   'Building Toys',
                    '19016' :   'Classic Toys',
                    '222'   : 'Diecast & Toy Vehicles',
                    '11731' :   'Educational',
                    '19071' :   'Electronic, Battery & Wind-Up',
                    '19077' :   'Fast Food & Cereal Premiums',
                    '233'   : 'Games',
                    '771'   : 'Marbles',
                    '479'   : 'Model Railroads & Trains',
                    '1188'  :    'Models & Kits',
                    '11743' :   'Outdoor Toys & Structures',
                    '19169' :   'Preschool Toys & Pretend Play',
                    '2613'  :    'Puzzles',
                    '2562'  :    'Radio Control & Control Line',
                    '19192' :   'Robots, Monsters & Space Toys',
                    '2616'  :    'Slot Cars',
                    '436'   : 'Stuffed Animals',
                    '2631'  :    'Toy Soldiers',
                    '2536'  :    'Trading Card Games',
                    '2624'  :    'TV, Movie & Character Toys',
                    '717'   : 'Vintage & Antique Toys',
                    '40149' :   'Wholesale Lots',
                    }
    for category_id, category_name in category_ids.items():
        directory = '/var/www/html/ebay-data/toys-and-hobbies/' + category_name
        for page in range(1, 101):
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(os.path.join(directory, str(page))):
                try:    
                    api = finding(debug=opts.debug, appid=opts.appid,
                                  config_file=opts.yaml, warnings=True)

                    api_request = {
                        'categoryId': category_id,
                        'paginationInput': {'pageNumber': page,
                                            'entriesPerPage': 100}
                    }

                    response = api.execute('findItemsByCategory', api_request)

                    nodes = response.dom().xpath('//itemId')
                    item_ids = [n.text for n in nodes]
                    print category_id, category_name
                    if len(item_ids) > 0:
                        shop = Shopping(debug=opts.debug, appid=opts.appid,
                                        config_file=opts.yaml, warnings=False)

                        prim_resp = shop.execute('GetMultipleItems',
                                                 {'IncludeSelector': 'ItemSpecifics',
                                                  'ItemID': item_ids[0:20]})

                        for j in range(20, len(item_ids), 20):
                            sub_resp = shop.execute('GetMultipleItems',
                                                    {'IncludeSelector': 'ItemSpecifics',
                                                     'ItemID': item_ids[j:j+20]})
                            prim_resp.dom().extend(sub_resp.dom().xpath('//Item'))


                        xml_file = open(os.path.join(directory, str(page)), 'w+')
                        stylesheet_tag = '<?xml-stylesheet type="text/xsl" href="/ebay-data/xslItemSpecifics.xsl"?>\n'
                        xml_file.write(stylesheet_tag)
                        xml_file.write(lxml.etree.tostring(prim_resp.dom(),
                                                           pretty_print=True))
                        xml_file.close()


                except ConnectionError as e:
                        print(e)
                        print(e.response.dict())


if __name__ == "__main__":
        print("FindItem samples for SDK version %s" % ebaysdk.get_version())
        (opts, args) = init_options()
        run(opts)