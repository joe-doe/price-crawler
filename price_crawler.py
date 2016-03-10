import urllib2
from bs4 import BeautifulSoup


class PriceCrawler(object):
    """
    The heart of crawling. Use :meth:get_all to get all results back
    or use individual methods instead
    """

    def __init__(self, config, item):
        self.config = config
        self.item = item

    def get_site_soup(self, url):
        """
        Get back the parsed html file.
        :param url: The URL the bs4 will parse
        :return: BeaulifulSoup object with parsed html
        """
        html_text = urllib2.urlopen(url).read()

        return BeautifulSoup(html_text, 'html.parser')

    def get_plaisio(self):

        try:
            soup = self.get_site_soup(self.config['all_info']
                                      [self.item]['plaisio'])
            price = soup.find('span', {'class': 'productPrice'})
            details = float(price.string.split()[0].replace(',', '.'))
        except KeyError:
            details = 0.0

        data = {
            'name': 'plaisio',
            'details': {
                'price': details
                }
        }
        return data

    def get_media_markt(self):
        try:
            soup = self.get_site_soup(self.config['all_info']
                                 [self.item]
                                 ['media-markt'])
            price = soup.find('div', {'class': 'price big'})
            details = float(price.string.replace(',', '.').replace('-', '0'))
        except KeyError:
            details = 0.0

        data = {
            'name': 'media-markt',
            'details': {
                'price': details
            }
        }
        return data

    def get_kotsovolos(self):
        try:
            soup = self.get_site_soup(self.config['all_info']
                                 [self.item]
                                 ['kotsovolos'])
            price = soup.find('p', {'class': 'price'})
            details = float(price.string.split()[0])
        except KeyError:
            details = 0.0

        data = {
            'name': 'kotsovolos',
            'details': {
                'price': details
            }
        }
        return data

    def get_eshop(self):
        try:
            soup = self.get_site_soup(self.config['all_info']
                                      [self.item]['eshop'])
            price_old_raw = soup.find('span', {'class': 'web-price-value-old'})
            price_old = float(price_old_raw.string.split()[0])
            price_new_raw = soup.find('span', {'class': 'web-price-value-new'})
            price_new = float(price_new_raw.string.split()[0])
        except KeyError:
            price_old = 0.0
            price_new = 0.0

        data = {
            'name': 'eshop',
            'details': {
                'old price': price_old,
                'new price': price_new,
                'price': price_new
            }
        }
        return data

    def get_skroutz(self):

        try:
            soup = self.get_site_soup(self.config['all_info']
                                      [self.item]
                                      ['skroutz'])
            prices = list()
            for item in soup.findAll('a', {'class': 'price_link'}):
                prices.append(float(item.string.split()[0].replace(',', '.')))

            avg = sum(prices) / float(len(prices))

            cheapest = prices[0]
            averege = float('{0:.2f}'.format(avg))
        except KeyError:
            cheapest = 0.0
            averege = 0.0

        data = {
            'name': 'skroutz',
            'details': {
                'cheapest': cheapest,
                'average': averege,
                'price': cheapest
            }
        }
        return data

    def get_best_price(self):

        try:
            soup = self.get_site_soup(self.config['all_info']
                                      [self.item]
                                      ['best_price'])
            prices = list()
            for item in soup.findAll('a',
                                     {'class': 'button tomer title no-img'}):
                prices.append(float(item.string[:-1]
                                    .split()[0]
                                    .replace(',', '.')))
            avg = sum(prices) / float(len(prices))

            cheapest = prices[0]
            averege = float('{0:.2f}'.format(avg))
        except KeyError:
            cheapest = 0.0
            averege = 0.0

        data = {
            'name': 'best_price',
            'details': {
                'cheapest': cheapest,
                'average': averege,
                'price': cheapest
            }
        }
        return data

    def get_all(self):
        return [
            self.get_skroutz(),
            self.get_eshop(),
            self.get_kotsovolos(),
            self.get_media_markt(),
            self.get_plaisio(),
            self.get_best_price()
        ]
