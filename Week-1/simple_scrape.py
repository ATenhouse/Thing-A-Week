import requests
from decimal import Decimal
from lxml import html
from operator import itemgetter
from re import sub

page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
tree = html.fromstring(page.content)

buyers = tree.xpath('//div[@title="buyer-name"]/text()')
prices = tree.xpath('//span[@class="item-price"]/text()')

# prices are in string, we really need decimal values for later sorting.
prices[:] = [Decimal(sub(r'[^\d.]', '', value)) for value in prices]

mergedlist = zip(buyers, prices)

# Sorted by first letter of name ...
sorted_by_second = sorted(mergedlist, key=itemgetter(1))

for k, v in sorted_by_second:  # iterating dictionary
    print "{0:<25s} ${1}".format(k, v)
