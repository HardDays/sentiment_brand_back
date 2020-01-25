# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from crawler.crawler import Crawler
from helper.google_search import GoogleSearch
from ner.spacy_ner import SpacyNamedEntityRecognizer
from sentiment_analyzer.sentiment_analyzer import SentimentAnalyzer
from flask import Flask, Response, request, jsonify
from flask_cors import CORS

import os
import collections
import pickle


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

google = GoogleSearch(os.environ['GOOGLE_SEARCH_KEY'], os.environ['GOOGLE_SEARCH_CX'])

crawler = Crawler(divide_by_sentences=False)

ner = SpacyNamedEntityRecognizer()

cls_name = os.path.join('data', 'senti_cnn_classifier.pkl')
with open(cls_name, 'rb') as cls_fp:
    cls = pickle.load(cls_fp)
        
se = SentimentAnalyzer(cls=cls)

def empty():
    return jsonify(
        {
            'total': 0,
            'negative': 0,
            'neutral': 0,
            'positive': 0,
            'mentions': []
        }
    )

def check(filtered, dates={}):
    if len(filtered) > 0:
        result = se.analyze(filtered)
        if len(result) == 3:
            return jsonify(
                {
                    'total': sum(result),
                    'negative': result[0],
                    'neutral': result[1],
                    'positive': result[2],
                    'mentions': filtered,
                    'dates': dates
                }
            )
        else:
            return empty()
    else:
        return empty()

@app.route('/analyze/content', methods=['POST', 'OPTIONS'])
def analyze_content(): 
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        if 'name' in data and 'is_person' in data and 'content' in data:
            filter_name = 'any'
            if 'fitler_name' in data:
                filter_name = data['filter_name']

            prep_data = data['content'].split('.')
            filtered = ner.filter_content(who=data['name'], is_person=data['is_person'], web_content={'text': prep_data}, filter_name=filter_name)
            filtered = collections.OrderedDict(filtered)
            return check(filtered)
        else:
            return jsonify({'status': 'NO_PARAMETERS'}), 422
            
@app.route('/analyze/url', methods=['POST', 'OPTIONS'])
def analyze_url(): 
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        if 'name' in data and 'is_person' in data and 'url' in data:
            depth = 3
            if 'depth' in data:
                depth = int(data['depth'])
            filter_name = 'any'
            if 'fitler_name' in data:
                filter_name = data['filter_name']
                
            content = crawler.load_and_tokenize([data['url']], depth=depth)   
            filtered = ner.filter_content(who=data['name'], is_person=data['is_person'], web_content=content, filter_name=filter_name)
            return check(filtered)
        else:
            return jsonify({'status': 'NO_PARAMETERS'}), 422

@app.route('/analyze/social', methods=['POST', 'OPTIONS'])
def analyze_social(): 
    if request.method == 'POST':
        data = request.get_json()
        if 'name' in data and 'is_person' in data:
            depth = 1
            if 'depth' in data:
                depth = int(data['depth'])
            pages = 5
            if 'pages' in data:
                pages = min(1, int(data['pages']), 20)
            filter_name = 'any'
            if 'fitler_name' in data:
                filter_name = data['filter_name']
            
            links = google.search(data['name'], pages=pages)
            if len(links) > 0:
                content = crawler.load_and_tokenize(links[0], depth=depth)   
                filtered = ner.filter_content(who=data['name'], is_person=data['is_person'], web_content=content, filter_name=filter_name)
                
                return check(filtered, links[1])
            else:
                return empty()
        else:
            return jsonify({'status': 'NO_PARAMETERS'}), 422


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3002)


# if __name__ == '__main__':
#     parser = ArgumentParser()
#     parser.add_argument('-n', '--name', dest='name', type=str, required=True, help='Name of person or organization.')
#     parser.add_argument('-w', '--who', dest='who', type=str, choices=['person', 'organization'],
#                         default='person', help='Who has to be found: person or organization?')
#     parser.add_argument('-u', '--url', dest='URL', type=str, required=True, help='List of URLs divided by a semicolon.')
#     parser.add_argument('--sentiment', dest='sentiment_analyzer', type=str, choices=['spacy', 'own'], required=False,
#                         default='own',
#                         help='What library has to be base for a sentiment analyzer: the spaCy or own CNN?')
#     args = parser.parse_args()
#     use_spacy_for_sentiment_analysis = (args.sentiment_analyzer == 'spacy')

#     name = args.name.strip()
#     assert len(name) > 0, "Name of person or organization is empty!"
#     is_person = (args.who == 'person')
#     urls = list(filter(lambda it: len(it) > 0, [cur_url.strip() for cur_url in args.URL.split(';')]))
#     assert len(name) > 0, "List of URLs is empty!"

#     print('')
#     print('Сорока летает по следующим сайтам:')
#     for it in sorted(urls):
#         print('  {0}'.format(it))
#     print('')
#     crawler = Crawler(divide_by_sentences=use_spacy_for_sentiment_analysis)
#     full_content = crawler.load_and_tokenize(urls, depth=3)   
#     if len(full_content) == 0:
#         print('По заданным веб-ссылкам ничего не написано :-(')
#     else:
#         ner = SpacyNamedEntityRecognizer()
#         print('Сорока ищет, упоминается ли {0} в текстах на этих сайтах...'.format(name))
#         print('')
#         content_about_name = ner.filter_content(who=name, is_person=is_person, web_content=full_content)
#         if len(content_about_name) == 0:
#             if is_person:
#                 print('Сорока обыскалась везде, но никто не знает, что это за человек - {0} :('.format(name))
#             else:
#                 print('Сорока обыскалась везде, но никто не знает, что это за организация - {0} :('.format(name))
#         else:
#             if use_spacy_for_sentiment_analysis:
#                 from sentiment_analyzer.spacy_sentiment_analyzer import SentimentAnalyzer
#                 se = SentimentAnalyzer()
#             else:
#                 import os
#                 import pickle
#                 from sentiment_analyzer.sentiment_analyzer import SentimentAnalyzer
#                 cls_name = os.path.join('data', 'senti_cnn_classifier.pkl')
#                 with open(cls_name, 'rb') as cls_fp:
#                     cls = pickle.load(cls_fp)
#                 se = SentimentAnalyzer(cls=cls)
#                 print('')
#             print('Сорока оценивает эмоциональность этих упоминаний...')
#             print('')
#             negatives_number, neutral_numbers, positives_number = se.analyze(content_about_name)
#             n = negatives_number + neutral_numbers + positives_number
#             n_as_str = str(n)
#             if n_as_str[-1] in {'2', '3', '4'}:
#                 if len(n_as_str) > 1:
#                     if n_as_str[-2] == '1':
#                         print('{0} упоминается в тексте {1} раз.'.format(name, n))
#                     else:
#                         print('{0} упоминается в тексте {1} раза.'.format(name, n))
#                 else:
#                     print('{0} упоминается в тексте {1} раза.'.format(name, n))
#             else:
#                 print('{0} упоминается в тексте {1} раз.'.format(name, n))
#             print('')
#             print('Коэффициент сороки:')
#             print('  {0:.2%} отрицательных упоминаний;'.format(negatives_number / float(n)))
#             print('  {0:.2%} положительных упоминаний;'.format(positives_number / float(n)))
#             print('  {0:.2%} нейтральных упоминаний.'.format(neutral_numbers / float(n)))
#             print('')
#             if (positives_number > 0) and (negatives_number > 0):
#                 if (negatives_number - positives_number) / float(n) >= 0.1:
#                     print('Сорока узнала, что {0} вызывает много отрицательных эмоций. Нужно поработать над '
#                           'репутацией.'.format(name))
#                 elif (positives_number - negatives_number) / float(n) >= 0.1:
#                     print('Сорока узнала, что {0} приносит много радости людям. Так держать!'.format(name))
#                 else:
#                     print('Сорока узнала, что {0} вызывает неоднозначные эмоции. Вы всегда можете перевесить '
#                           'общественное мнение на свою сторону.'.format(name))
#             else:
#                 if positives_number > 0:
#                     print('Сорока узнала, что {0} приносит много радости людям. Так держать!'.format(name))
#                 elif negatives_number > 0:
#                     print('Сорока узнала, что {0} вызывает много отрицательных эмоций. Нужно поработать над '
#                           'репутацией.'.format(name))
#                 else:
#                     print('Сорока узнала, что {0} не вызывает эмоций. Заявите о себе!'.format(name))
