from scrapy import cmdline
from papermedia import settings
from datetime import datetime


def main():
    data_dir = u'file:///E:\Repos\papermedia\data\\'
    spider_name = 'ScienceJournal'  # DoubanMovies PeopleDaily HuaXiDouShiBao ScienceJournal scienceadvances
    settings.ITEM_PIPELINES = {
        'papermedia.pipelines.CleanListPipeline': 1,
        'papermedia.pipelines.CleanTextPipeline': 2,
        # 'papermedia.pipelines.PeopleDailyPipeline': 3,
        # 'papermedia.pipelines.MongoPipeline': 10
    }
    settings.FEED_FORMAT = 'XML'
    today_date = datetime.now().strftime('%Y-%m-%d')
    settings.FEED_URI = '{}{}_{}.xml'.format(data_dir, spider_name, today_date)
    cmdline.execute("scrapy crawl {}".format(spider_name.lower()).split())


if __name__ == '__main__':
    main()
