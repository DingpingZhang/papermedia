from scrapy import cmdline
from papermedia import settings


def main():
    settings.FEED_FORMAT = 'xml'
    settings.FEED_URI = u'file:data/%(name)s_%(time)s.' + settings.FEED_FORMAT
    spider_name = 'ScienceAdvances'  # DouBanMovies PeopleDaily huaXiDuShiBao ScienceJournal ScienceAdvances
    cmdline.execute("scrapy crawl {}".format(spider_name.lower()).split())


if __name__ == '__main__':
    main()
