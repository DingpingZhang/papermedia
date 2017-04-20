class PresentationRule(object):
    def __init__(self, *, name, xpath, stopwords, is_chinese_word):
        self.name = name
        self.xpath = xpath
        self.stopwords = stopwords
        self.is_chinese_word = is_chinese_word


PRESENTATION_RULES = {
    'doubanmovies': [
        PresentationRule(
            name='quote',
            xpath='//quote/text()',
            stopwords=[

            ],
            is_chinese_word=True
        )
    ],
    'huaxidushibao': [
        PresentationRule(
            name='content',
            xpath='//content/text()',
            stopwords=[

            ],
            is_chinese_word=True
        ),
        PresentationRule(
            name='title',
            xpath='//title/text()',
            stopwords=[

            ],
            is_chinese_word=True
        )
    ],
    'peopledaily': [
        PresentationRule(
            name='content',
            xpath='//content/value/text()',
            stopwords=[

            ],
            is_chinese_word=True
        )
    ],
    'scienceadvances': [
        PresentationRule(
            name='content',
            xpath='//content/value/text()',
            stopwords=[
                'used',
                'using',
                'also',
                'fig',
                'result',
                'one',
                'two'
            ],
            is_chinese_word=False
        ),
        PresentationRule(
            name='abstract',
            xpath='//abstract/text()',
            stopwords=[
                'abstract',
                'also',
                'result',
                'using'
            ],
            is_chinese_word=False
        ),
        PresentationRule(
            name='keywords',
            xpath='//keywords/value/text()',
            stopwords=[

            ],
            is_chinese_word=False
        )
    ],
    'sciencejournal': [
        PresentationRule(
            name='content',
            xpath='//content/value/text()',
            stopwords=[
                'et', 'al',
                'science'
            ],
            is_chinese_word=False
        ),
        PresentationRule(
            name='summary',
            xpath='//summary/text()',
            stopwords=[
                'summary',
                'also',
                'science'
            ],
            is_chinese_word=False
        )
    ]
}
