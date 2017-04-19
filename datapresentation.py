from os import path
import os
import jieba
from lxml import etree
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
import re


def generate_word_cloud(word_text):
    word_cloud = WordCloud(
        mask=imread('assert/background.jpg'),
        font_path='assert/msyh.ttf').generate(word_text)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()


def cut_word_text(word_text):
    return " ".join(jieba.cut(word_text))


def main():
    file_path = r'data\sciencejournal_2017-04-19T13-38-26.xml'
    html = etree.parse(file_path)
    news_content_list = html.xpath('//content/value/text()')
    word_text = ' '.join(news_content_list)
    # word_text = cut_word_text(word_text)
    generate_word_cloud(word_text)


if __name__ == '__main__':
    main()
