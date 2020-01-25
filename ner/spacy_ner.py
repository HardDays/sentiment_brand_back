from collections import OrderedDict
import copy
import spacy
import pymorphy2

class SpacyNamedEntityRecognizer(object):
    """ Класс для распознавания именованных сущностей и фильтрации веб-контента только по нужным нам сущностям.

    """
    def __init__(self):
        pass

    def filter_content(self, who: str, is_person: bool, web_content: OrderedDict, filter_name='full') -> OrderedDict:
        """ Отфильтровать входной веб-контент, удалив из него абзацы, где нет упоминаний о нужных нам людях или фирмах.

        Входной веб-контент представляет собой словарь, ключами которого являются строковые описания ранее пропарсенных
        URL-ов, а значениями - списки строк, т.е. текстовый контент каждого URL-а, разбитый на последовательность
        абзацев. Пример:

        {
            "www.abc.com": [
                "мама мыла раму",
                "корова молоко даёт"
            ],
            "https://hello.org": [
                "Здравствуй, мир!",
                "И тебе исполать, добрый молодец!",
                "Доброго здоровьица, девица краса.",
                "Здесь что, все здороваются?"
            ]
        }

        Данный метод вернёт такую же структуру данных, но те абзацы, в которых не будет упоминаний о нужном нам человеке
        или организации, будут удалены. Если получится так, что во всех абзацах какого-то URL-а нет ни одного упоминания
        искомой именованной сущности, то удаляется весь URL.

        :param who: строка с описанием искомой сущности (напр., "Вася Пупкин" или "Рога и копыта")
        :param is_person: искомая сущность - это человек (True) или организация (False)?
        :param web_content: словарь текстового контента, разбитого на абзацы, для всех обойдённых URL-ов

        :return тот же самый словарь, что и web_content, только отфильтрованный.

        """
        trivial = {}
        for url in web_content.keys():
            trivial[url] = []
            for sent in web_content[url]:
                if who.lower() in sent.lower():
                    trivial[url].append(sent)
        nlp = spacy.load('xx_ent_wiki_sm', disable=['parser', 'tagger'])
        morph = pymorphy2.MorphAnalyzer()
        for url in list(web_content.keys()):
            url_fl = 0
            filtered_content = []
            for i in range(len(web_content[url])):
                doc_fl = 0
                doc = nlp(web_content[url][i])
                # if len(doc.ents) > 0:
                #     print('\n doc')
                name_tokens = {unit: 0 for unit in who.split()}
                for ent in doc.ents:
                    #print(ent, ent.label_, type(ent.label_))
                    if is_person:
                        if filter_name == 'any' or filter_name == 'all':
                            for unit in who.split():
                                if ent.label_ == 'PER':
                                    if morph.parse(ent.text.lower())[0].normal_form == morph.parse(unit.lower())[0].normal_form:
                                        name_tokens[unit] += 1
                        else:
                            if ent.label_ == 'PER':
                                if morph.parse(ent.text.lower())[0].normal_form == morph.parse(who.lower())[0].normal_form:
                                    doc_fl += 1
                                    url_fl += 1
                    else:
                        if filter_name == 'any' or filter_name == 'all':
                            for unit in who.split():
                                if ent.label_ == 'ORG' or ent.label_== 'LOC':
                                    if morph.parse(ent.text.lower())[0].normal_form == morph.parse(unit.lower())[0].normal_form:
                                        name_tokens[unit] += 1
                        else:
                            if ent.label_ == 'ORG' or ent.label_== 'LOC':
                                if morph.parse(ent.text.lower())[0].normal_form == morph.parse(who.lower())[0].normal_form:
                                    doc_fl += 1
                                    url_fl += 1
                                    
                if filter_name == 'all' and all(name_tokens[i] > 0 for i in name_tokens):
                    doc_fl += sum(name_tokens[i] for i in name_tokens)
                    url_fl += sum(name_tokens[i] for i in name_tokens)
                elif filter_name == 'any' and any(name_tokens[i] > 0 for i in name_tokens):
                    doc_fl += sum(name_tokens[i] for i in name_tokens)
                    url_fl += sum(name_tokens[i] for i in name_tokens)

                if doc_fl != 0:
                    filtered_content.append(web_content[url][i])
            web_content[url] = copy.copy(filtered_content)
            if url_fl == 0:
                del web_content[url]
        
        for url in trivial.keys():
            if url in web_content:
                for sent in trivial[url]:
                    if not sent in web_content[url]:
                        web_content[url].append(sent)
            elif len(trivial[url]) > 0:
                web_content[url] = trivial[url]

        for i in web_content:
            web_content[i] = list(set(web_content[i]))

        return web_content
