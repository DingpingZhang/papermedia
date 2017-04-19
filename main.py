from scrapy import cmdline
from papermedia import settings
from datetime import datetime
from scrapy.crawler import Crawler


def main():
    data_dir = u'file:///E:\Repos\papermedia\data\\'
    spider_name = 'ScienceJournal'  # DoubanMovies PeopleDaily HuaXiDouShiBao ScienceJournal scienceadvances
    today_date = datetime.now().strftime('%Y-%m-%d')
    settings.FEED_URI = '{}{}_{}.xml'.format(data_dir, spider_name, today_date)
    settings.FEED_FORMAT = 'XML'
    cmdline.execute("scrapy crawl {}".format(spider_name.lower()).split())


if __name__ == '__main__':
    main()
