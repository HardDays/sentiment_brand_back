![Soroka](https://pp.userapi.com/c830309/v830309642/107ad1/8NnG9yy_w3A.jpg)

Узнай, хорошо или плохо говорят о тебе или твоей фирме в Интернете! Наша "Сорока" с искусственным интеллектом принесёт тебе это на своём хвосте
“Soroka” – нейросетевой продукт, анализирующий репутацию человека или компании в Интернете.

Для этого вам нужно указать название компании (или имя человека), а также один или несколько интернет-адресов, с которых начнётся анализ веб-контента. Затем с помощью свёрточных нейронных сетей система ищет упоминания заданного имени или названия, после чего анализирует тональность контекста. В результате вы получаете коэффициент сороки – долю положительных, негативных и нейтральных упоминаний в тексте по заданному объекту на заданном сайте (группе сайтов).

“Soroka” поможет вам следить за своей собственной репутацией и репутацией вашей компании, первым узнавать о значимых тенденциях в общественном мнении и вовремя реагировать на любые изменения.

# Как это работает:
В нашем продукте мы используем свёрточные нейронные сети, концепция которых успешно используется для анализа изображений. В последнее время этот подход приобрел популярность в задачах обработки естественного языка. Существует ряд публикаций, доказывающих их преимущества перед другими алгоритмами: например, качество свёрточной сети сравнимо с качеством рекуррентной сети типа LSTM или GRU, при этом время обучения свёрточной нейросети меньше в несколько раз.

Также мы использовали двухслойный персептрон в рамках модели word2vec для решения вспомогательной задачи – формирования векторов слов, которые используются как признаки для свёрточной нейросети.

На первом шаге веб-краулер парсит заданный сайт, от странички к страничке переходя вплоть до установленного уровня вложенности и выкачивая весь текстовый контент.

На втором шаге свёрточная нейронная сеть анализирует полученный текст и находит в нем упоминание о заданном человеке или организации.

На третьем шаге другая свёрточная нейросеть оценивает текст на его семантику и распознает эмоциональность текста – похвалу, критику, нейтральное мнение. В результате “Soroka” возвращает в процентном соотношении уровень положительных, негативных и нейтральных упоминаний искомого объекта в тексте.

# Какие бизнес-задачи можно решать:
=======

- Сравнить, насколько хорошо или плохо пишут о вас и ваших конкурентах;

- Оценить, как изменилось отношение к вам или вашей организации в Интернете после проведения рекламной кампании;

- Узнать, что пишут о компаниях, акциями и облигациями которых вы владеете или собираетесь приобретать;

- Оценить, что пишут о компании, услугами или продуктами которой вы хотите воспользоваться;

- Провести анализ рынков с целью выявления потенциальных конкурентных преимуществ;

- Оперативно реагировать на негативную реакцию о вас или вашей компании в Интернете;

- И любые другие бизнес-кейсы, в которых требуется анализ тональности текста.

# Установка и использование

Перед использованием убедитесь, что все пакеты, перечисленные в файле requirements.txt установлены в вашем окружении.
Кроме того, требуется скачать предобученную модель spacy xx_ent_wiki_sm. Сделать это можно с помощью команды:

`python3 -m spacy download xx_ent_wiki_sm`

Модель доступна для использования с помощью интерфейса командной строки. Вам нужно указать имя/название объекта для поиска,
сущность этого объекта (человек или организация) и ссылки на интересующие интернет-сайты.

К примеру, поиск информации о Сергее Шнурове на lenta.ru в рубрике о культуре выглядел бы так:

`python -u demo.py --name "Сергей Шнуров" --who person --url https://lenta.ru/rubrics/culture/`

Поиск информации об организации "Soroka" на сайте vk.com выглядит так:

`python -u demo.py --name "Soroka" --who organization --url https://vk.com/`

На выход модель выдаст следующие данные:
- Сколько раз на сайте упоминается искомый объект
- Какая доля упоминаний приходится на позитивные/негативные/нейтральные высказывания

*Проект создан командой nsu_ai специально для хакатона neurohive.io*
=======
