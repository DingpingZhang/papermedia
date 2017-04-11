from scrapy import cmdline
from papermedia import settings
from datetime import datetime


def main():
    data_dir = u'file:///E:\OtherSourceCode\papermedia\data\\'
    current_spider_name = 'doubanmovies'
    settings.ITEM_PIPELINES = {'papermedia.pipelines.DoubanMoviesPipeline': 300}
    # settings.ITEM_PIPELINES = {'papermedia.pipelines.PeopleDailyPipeline': 300}
    today_date = datetime.now().strftime('%Y-%m-%d')
    settings.FEED_URI = '{}{}_{}.xml'.format(data_dir, current_spider_name, today_date)
    cmdline.execute("scrapy crawl {}".format(current_spider_name).split())


if __name__ == '__main__':
    main()
