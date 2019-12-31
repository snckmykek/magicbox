"""
This module is used for synchronization with site/server

Needs a lot of refinement.
"""


def get_global_products():
    """
    Return "global" products (common products, like Apple, Beer, Meat, etc.).

    P.S.For now don't using requests to server, server does not exist =) Now it's stub.
    """

    # f = open('global_products.txt', encoding='utf-8')
    # products_str = f.read()
    products_str = "Баранина,Баранина 1-й категории,Баранина отварная,Бефстроганов,Ветчина,Говядина,Говядина 1-й категории,Говядина нежирная отварная,Говяжий язык отварной,Говяжьи мозги,Говяжья печень жареная,Гусь,Зайчатина,Индейка,Индейка отварная,Колбаса вареная,Колбаса вареная отдельная,Котлеты из свинины,Кролик жареный,Крольчатина,Куриная грудка отварная,Курица,Курица жареная,Куры 1-й категории,Мозги закомпостированные,Омлет,Печенка говяжья,Почки тушеные,Свинина,Свинина жареная,Свинина мясная,Свинина на гриле,Сосиски,Сосиски советские,Телятина,Телятина жирная ,Телятина отварная,Телятина тощая,Утка,Утка жареная,Фазан,Цыплята 1-й категории,Язык говяжий,Яичный белок,Яичный желток,Яичный порошок,Яйца,Белуга,Белуга свежая,Горбуша горячего копчения,Икра белужья зернистая,Икра кетовая,Икра красная,Икра минтая,Икра черная паюсная,Кальмары отварные,Камбала,Карп,Карп жареный,Кефаль отварная,Копченая треска,Котлеты рыбные,Крабовые палочки,Крабы отварные,Креветки,Лещ,Линь,Лосось,Мидии,Морская капуста,Окунь,Окунь жареный,Омар,Осетр,Палтус,Печень трески,Раки отварные,Сайра в масле,Сардина в масле,Сардина отварная,Севрюга свежая,Сельдь,Сельдь атлантическая соленая,Семга отварная,Скумбрия,Скумбрия в масле,Скумбрия холодного копчения,Сом,Ставрида,Стерлядь,Судак,Треска,Треска отварная,Тунец,Тунец в собственном соку,Угорь копченый,Устрицы отварные,Форель отварная,Хек отварной,Хек, мерлуза,Шпроты в масле,Щука,Щука отварная,Кефир,Кефир средний,Майонез,Маргарин,Масло,Масло подсолнечное рафинированное,Масло сливочное несоленое,Масло топленое,Молоко,Молоко коровье,Молоко сгущенное с сахаром,Простокваша,Простокваша жирная,Сливки 20%-ные,Сливки нежирные,Сметана высшего сорта,Сметана жирная,Сыр голландский,Сыр голландский 50%-ный,Сыр козий,Сыр овечий,Творог,Творог жирный,Творог нежирный,ны из муки высшего сорта,Бразильские,Бублик пшеничный,Булочка для хот дога,Булочка сдобная,Вареники с картофелем,Вареники с творогом,Вафли,Геркулес,Горох (зерно),Гренки белые жареные,Гречка,Гречневая каша на воде,Картофельный крахмал,Кедровые,Кешью,Клетчатка пищевая,Крупа гречневая (ядрица),Крупа манная,Крупа овсяная,Крупа перловая,Кукурузные хлопья,Лесные,Макаронные изделия,Макароны высший сорт,Макароны из муки грубого помола,Макароны из твердых сортов пшеницы,Манка,Манная каша молочная,Миндаль,Мука пшеничная 1 сорта,Мука пшеничная 2 сорта,Мюсли,Овсяная каша молочная,Овсяная каша на воде,Овсянка,Овсяные хлопья сырые,Отруби,Пельмени,Перловая каша на воде,Перловка,Печенье крекер,Печенье, пирожные, торты,Пирожок жареный с повидлом,Пирожок печеный с луком и яйцом,Пицца с сыром,Пшенная каша на воде,Пшено,Рис,Рис нешлифованный отварной,Рисовая каша молочная,Рисовая каша на воде,Соевая мука обезжиренная,Сухари сахарные,Сухарики,Фисташки,Фундук,Хлеб Бородинский,Хлеб белый (батон),Хлеб зерновой,Хлеб из муки высшего сорта,Хлеб пшеничный из м.1 с,Хлеб пшеничный из м.2 с,Хлеб ржаной простой формовой,Хлеб ржано-пшеничный,Хлебцы цельнозерновые,Ячневая,Ячневая каша молочная,Абрикосы,Абрикосы свежие,Авокадо,Алыча,Ананас,Апельсины,Арбуз ,Артишоки,Баклажанная икра,Баклажаны,Бананы,Белый гриб,Бобы,Брокколи,Брусника,Брюква,Брюссельская капуста,Виноград,Вишня,Голубика,Гранат,Грейпфрут,Грибы,Грибы белые сушеные,Грибы соленые,Груши,Груши свежие,Дыня,Ежевика,Зеленый горошек,Зеленый горошек свежий,Земляника,Изюм светлый,Изюм темный,Инжир,Кабачки,Кабачки жареные,Кабачковая икра,Капуста белокочанная,Капуста брюссельская,Капуста зеленая,Капуста квашенная,Капуста красная,Капуста пекинская,Капуста савойская,Капуста свежая,Капуста тушеная,Капуста цветная,Картофель,Картофель вареный,Картофель жареный,Картофель свежий,Картофель фри,Картофельное пюре,Картофельные чипсы,Каштаны,Киви,Клубника,Клюква,Кольраби,Корни сельдерея,Крыжовник,Кукуруза,Кукуруза отварная,Курага,Лимон,Лук зеленый,Лук репчатый,Лук репчатый сырой,Лук-порей,Лук-порей,Малина,Манго,Мандарин,Маслины,Маслины черные,Маслята,Морковь свежая,Морковь сырая,Нектарин,Облепиха,Огурцы,Огурцы свежие,Оливки зеленые,Пастернак,Перец зеленый,Перец красный,Перец сладкий,Персики,Петрушка,Петрушка, базилик,Подберезовики,Подосиновики,Помидоры,Помидоры свежие,Рагу овощное,Ревень,Редис,Редька,Репа,Рябина,Салат зеленый,Салат качанный,Салат листовой,Салат цикорий,Свекла,Свекла отварная,Сельдерея зелень,Слива,Смородина,Смородина черная,Спаржа,Тыква,Тыква запеченая,Укроп,Урюк,Фасоль белая,Фасоль вареная,Фасоль стручковая,Фенхель,Финики,Фрукты,Хрен,Хурма,Цветная капуста жареная,Цветная капуста тушеная,Цуккини,Черешня,Черника,Чернослив,Чеснок,Чечевица отварная,Шампиньоны,Шпинат,Щавель,Яблоки,Яблоки свежие,Арахисовое,Горчица,Кетчуп,Кокосовое,Кукурузное,Майонез,Маргарин,Оливковое масло,Растительное масло,Сало свиное,Сливочное масло,Соевое,Соевый соус,Вода чистая негазированная,Чай зеленый (без сахара),Сок томатный,Сок морковный,Сок грейпфрутовый (без сахара),Сок яблочный (без сахара),Сок апельсиновый (без сахара),Сок ананасовый (без сахара),Сок виноградный (без сахара),Вино красное сухое,Вино белое сухое,Квас,Кофе натуральный (без сахара),Какао на молоке (без сахара),Сок в упаковке,Компот из фруктов (без сахара),Десертное вино,Кофе молотый,Газированные напитки,Пиво,Шампанское сухое,Джин с тоником,Ликер,Водка,Коньяк,Шоколад темный,Мед,Варенье,Шоколад молочный,Шоколадный батончики,Халва,Карамель, леденцы,Мармелад,Сахар,Попкорн,Шаверма в лаваше (1шт),Гамбургер (1 шт),Хотдог (1 шт)"
    global_products = products_str.split(",")

    return global_products
