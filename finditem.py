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

from common import dump

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

    try:

        # SubCategories of Women Accessories
        category_ids = ['163573', '3003', '177651', '168998', '105559',
                        '45220', '167906', '45230', '169285', '45237', '15735',
                        '45238', '150955', '179247', '151486', '105569',
                        '45258', '175634', '106129', '15738', '1063']

        for category_id in category_ids:
            for page in range(1, 100):

                api = finding(debug=opts.debug, appid=opts.appid,
                              config_file=opts.yaml, warnings=True)

                api_request = {
                    'categoryId': '4251',
                    'paginationInput': {'pageNumber': page,
                                        'entriesPerPage': 100}
                }

                response = api.execute('findItemsByCategory', api_request)

                nodes = response.dom().xpath('//itemId')
                item_ids = [n.text for n in nodes]

                shop = Shopping(debug=opts.debug, appid=opts.appid,
                                config_file=opts.yaml, warnings=False)

                prim_resp = shop.execute('GetMultipleItems',
                                         {'IncludeSelector': 'ItemSpecifics',
                                          'ItemID': item_ids[0:20]})

                for j in range(20, 100, 20):
                    sub_resp = shop.execute('GetMultipleItems',
                                            {'IncludeSelector': 'ItemSpecifics',
                                             'ItemID': item_ids[j:j+20]})
                    prim_resp.dom().extend(sub_resp.dom().xpath('//Item'))

                xml_file = open(category_id + '-' + str(page), 'w+')
                stylesheet_tag = '<?xml-stylesheet type="text/xsl" href="xslItemSpecifics.xsl"?>\n'
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