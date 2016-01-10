import re
import time
from operator import itemgetter
from bs4 import BeautifulSoup
from urllib2 import urlopen


def generate_schedule_url(input_url):
    # Redirect from http://www.fxnetworks.com/schedule/
    # isn't working, so we get to generate the full URL!
    # http://www.fxnetworks.com/schedule/2016-01-09/Pacific
    return input_url + time.strftime('%Y-%m-%d') + '/Pacific'


def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "html5lib")


def get_schedule_soup(input_url):
    best_url = generate_schedule_url(input_url)
    return make_soup(best_url)


def clean_me(desc_array):
    output = list()
    for item in desc_array:
        # removing ALL non-unicode characters
        g = re.sub(r'[^\x00-\x7F]+', ' ', item)
        # Not removing the three spaces after character removal. Shoot.
        g = re.sub(' +', ' ', g).replace('\n', "").strip()
        output.append(g)
    return output


def main(start_url):
    gen_soup = get_schedule_soup(start_url)

    big_find = gen_soup.find("div", {'id': 'FXX-schedule'})

    titles = [x.getText() for x in big_find.find_all("h3", {'class': "title"})]
    times = [x.getText()
             for x in big_find.find_all("h3", {'class': "timestamp"})]
    descriptions = [p.getText().encode('utf-8', 'strip')
                    for p in big_find.find_all("p", {'class': "description"})]

    desc_clean = clean_me(descriptions)

    final = zip(times, titles, desc_clean)

    # Sorted by first letter of name ...
    sorted_final = sorted(final, key=itemgetter(0))

    for times, title, desc in sorted_final:  # iterating dictionary
        print "{0}m\t{1}\nSynopsis: {2}\n".format(times, title, desc)

if __name__ == "__main__":
    url = 'http://www.fxnetworks.com/schedule/'
    main(url)
