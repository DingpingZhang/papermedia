import os
import jieba
import matplotlib.pyplot as plt

from os import path
from lxml import etree
from wordcloud import WordCloud, STOPWORDS
from wordclouds.settings import PRESENTATION_RULES

IMG_SAVE_PATH_FORMAT = 'imgs/{}.png'


def generate_word_cloud(word_text, stopword_list=list(), is_chinese=False):
    stopword_set = set(STOPWORDS)
    for item in stopword_list:
        stopword_set.add(item)
    word_cloud = WordCloud(
        # mask=np.array(Image.open('assert/background.png')),
        stopwords=stopword_set,
        width=1000,
        height=618,
        max_words=3000,
        prefer_horizontal=0.99,
        # random_state=2333
        # max_font_size=200,
        background_color='#EEEEEE',
    )
    if is_chinese:
        word_cloud.font_path = '../assert/msyh.ttf'
        word_cloud.max_words = 1000
        word_text = ' '.join(jieba.cut(word_text))
    word_cloud.generate(word_text)
    return word_cloud


def generate_all_word_cloud():
    for xml_name in os.listdir('../data'):
        xml_path = '../data/' + xml_name
        spider_name = xml_name.split('_')[0]
        xml = etree.parse(xml_path)
        yield from get_each_word_cloud(spider_name, xml, xml_name.split('.')[0])


def get_each_word_cloud(spider_name, xml, file_name):
    for item in PRESENTATION_RULES[spider_name]:
        info_list = xml.xpath(item.xpath)
        save_path = IMG_SAVE_PATH_FORMAT.format(
            file_name.replace(spider_name, '{}_{}'.format(spider_name, item.name)))
        word_text = ' '.join(info_list)
        yield generate_word_cloud(word_text, item.stopwords, item.is_chinese_word).to_file(save_path)


def main():
    # img_array = np.array(Image.open('alice_color.png'))
    # image_colors = ImageColorGenerator(img_array)
    for word_cloud in generate_all_word_cloud():
        # plt.imshow(word_cloud, interpolation='bilinear')
        # plt.show()
        pass


if __name__ == '__main__':
    main()
