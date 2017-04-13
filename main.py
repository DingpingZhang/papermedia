from scrapy import cmdline
from papermedia import settings
from datetime import datetime


def main():
    # data_dir = u'file:///E:\OtherSourceCode\papermedia\data\\'
    spider_name = 'PeopleDaily'  # DoubanMovies PeopleDaily HuaXiDouShiBao
    settings.ITEM_PIPELINES = {'papermedia.pipelines.' + spider_name + 'Pipeline': 300}
    # today_date = datetime.now().strftime('%Y-%m-%d')
    # settings.FEED_URI = '{}{}_{}.xml'.format(data_dir, spider_name, today_date)
    cmdline.execute("scrapy crawl {}".format(spider_name.lower()).split())


if __name__ == '__main__':
    main()
