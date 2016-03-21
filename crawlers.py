import time
from price_crawler import PriceCrawler


class ConsoleCrawler(object):
    """
    Use this for console printout of results
    """

    def __init__(self, config):
        self.config = config

    def print_prices(self):
        for item in self.config['all_info'].keys():
            pc = PriceCrawler(self.config, item)

            interested_in_length = len(item)
            print ('-' * 20) + ('-' * interested_in_length) + ('-' * 20)
            print ('-' * 20) + item + ('-' * 20)
            print ('-' * 20) + ('-' * interested_in_length) + ('-' * 20)

            [self.print_pretty(x) for x in pc.get_all()]
            print ''

    def print_pretty(self, item_dict):
        title = item_dict['name']

        output_format = '| {0:10} | {1:9.2f} |'
        top_and_bottom = '-' * 26
        separator = '|' + '-' * 24 + '|'
        center = '|' + '{0:^23} '.format(title) + '|'

        print top_and_bottom
        print center
        print separator
        for idx, item in enumerate(item_dict['details']):
            print output_format.format(item, item_dict['details'][item])
            if idx != len(item_dict['details']) - 1:
                print separator
        print top_and_bottom
        print ' '


class JsonCrawler(object):
    """
    Use this one to get back results in JSON format
    """

    def __init__(self, config, model):
        self.config = config
        self.model = model

    def get_prices(self):
        """
        Generator method which produces a response dict for every item
        of interest (key in all_info dict)

        :return: response dict every time it is called
        """

        for item in self.model.get_items():
            pc = PriceCrawler(self.config, self.model, item)
            for store in pc.get_stores():
                response = {
                    'timestamp': time.time(),
                    'item_name': item,
                }

                response.update(pc.get_store_price(store))
                yield response
