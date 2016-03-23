import urllib2
from bs4 import BeautifulSoup


class PriceCrawler(object):
    """
    The heart of crawling. Use :meth:get_all to get all results back
    or use individual methods instead
    """

    def __init__(self, config, model, item):
        self.config = config
        self.item = item
        self.model = model
        self.store_map = {
            'skroutz': self.get_skroutz,
            'eshop': self.get_eshop,
            'kotsovolos': self.get_kotsovolos,
            'media-markt': self.get_media_markt,
            'plaisio': self.get_plaisio,
            'best-price': self.get_best_price
        }

    def get_site_soup(self, url):
        """
        Get back the parsed html file.
        :param url: The URL the bs4 will parse
        :return: BeaulifulSoup object with parsed html
        """
        try:
            html_text = urllib2.urlopen(url).read()
        except urllib2.HTTPError:
            return None
        return BeautifulSoup(html_text, 'html.parser')

    def get_plaisio(self):

        try:
            soup = self.get_site_soup(self.model
                                      .get_url_for_item(self.item, 'plaisio')
                                      .get('url'))

            price = soup.find('span', {'class': 'productPrice'})
            details = float(price.string.split()[0].replace(',', '.'))
        except (KeyError, AttributeError):
            details = 0.0

        data = {
            'store_name': 'plaisio',
            'price': details
        }
        return data

    def get_media_markt(self):
        try:
            soup = self.get_site_soup(self.model
                                      .get_url_for_item(self.item,
                                                        'media-markt')
                                      .get('url'))
            price = soup.find('div', {'class': 'price big'})
            details = float(price.string.replace(',', '.').replace('-', '0'))
        except (KeyError, AttributeError):
            details = 0.0

        data = {
            'store_name': 'media-markt',
            'price': details
        }
        return data

    def get_kotsovolos(self):
        try:
            soup = self.get_site_soup(self.model
                                      .get_url_for_item(self.item,
                                                        'kotsovolos')
                                      .get('url'))
            price = soup.find('p', {'class': 'price'})
            details = float(price.string.split()[0])
        except (KeyError, AttributeError):
            details = 0.0

        data = {
            'store_name': 'kotsovolos',
            'price': details
        }
        return data

    def get_eshop(self):
        try:
            soup = self.get_site_soup(self.model
                                      .get_url_for_item(self.item,
                                                        'eshop')
                                      .get('url'))
            price_old_raw = soup.find('span', {'class': 'web-price-value-old'})
            price_old = float(price_old_raw.string.split()[0])
            price_new_raw = soup.find('span', {'class': 'web-price-value-new'})
            price_new = float(price_new_raw.string.split()[0])
        except (KeyError, AttributeError):
            price_old = 0.0
            price_new = 0.0

        data = {
            'store_name': 'eshop',
            'old price': price_old,
            'new price': price_new,
            'price': price_new
        }
        return data

    def get_skroutz(self):

        try:
            soup = self.get_site_soup(self.model
                                      .get_url_for_item(self.item,
                                                        'skroutz')
                                      .get('url'))
            prices = list()
            for item in soup.findAll('a', {'class': 'price_link'}):
                prices.append(float(item.string.split()[0].replace(',', '.')))

            avg = sum(prices) / float(len(prices))

            cheapest = prices[0]
            average = float('{0:.2f}'.format(avg))
        except (KeyError, AttributeError):
            cheapest = 0.0
            average = 0.0

        data = {
            'store_name': 'skroutz',
            'cheapest': cheapest,
            'average': average,
            'price': cheapest
        }
        return data

    def get_best_price(self):

        try:
            soup = self.get_site_soup(self.model
                                      .get_url_for_item(self.item,
                                                        'best-price')
                                      .get('url'))
            prices = list()
            for item in soup.findAll('a',
                                     {'class': 'button tomer title no-img'}):
                prices.append(float(item.string[:-1]
                                    .split()[0]
                                    .replace(',', '.')))
            avg = sum(prices) / float(len(prices))

            cheapest = prices[0]
            average = float('{0:.2f}'.format(avg))
        except (KeyError, AttributeError, ZeroDivisionError):
            cheapest = 0.0
            average = 0.0

        data = {
            'store_name': 'best-price',
            'cheapest': cheapest,
            'average': average,
            'price': cheapest
        }
        return data

    def get_store_price(self, store):
        return self.store_map[store]()

    def get_all_stores(self):
        return self.store_map.keys()
