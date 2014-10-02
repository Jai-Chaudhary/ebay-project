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



    # SubCategories of Women Accessories
    category_ids = {'163573':  'belt-buckles',
                    '3003' :   'belts',
                    '177651' : 'collar-tips',
                    '168998' : 'fascinators-headpieces',
                    '105559' : 'gloves-mittens',
                    '45220' :  'hair-accessories',
                    '167906' : 'handkerchiefs',
                    '45230' :  'hats',
                    '169285' : 'id-document-holders',
                    '45237' :  'key-chains-rings-finders',
                    '15735' :  'organizers-day-planners',
                    '45238' :  'scarves-wraps',
                    '150955' : 'shoe-charms-jibbitz',
                    '179247' : 'sunglasses-fashion-eyewear',
                    '151486' : 'ties',
                    # '105569' : 'umbrellas',
                    '45258' :  'wallets',
                    '175634' : 'wigs-extensions-supplies',
                    # '106129' : 'wristbands',
                    '15738' :  'mixed-items-lots',
                    '1063' :   'other',
                   }

    for category_id, category_name in category_ids.items():
        directory = '/var/www/html/ebay-data/womens-accessories/' + category_name
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