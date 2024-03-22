# свой экран выборов, но с таймером
# по истечение времени будет выбран последний пункт
screen menu(items, t=10, item=None):
    style_prefix "choice"

    on "hide" action With(dissolve)

    default time_is_up = False

    # если номер ответа по умолчанию не назначен, то пусть это будет последний ответ
    if item is None:
        $ item = len(items) - 1

    # если время для таймера задано, отображаем шкалу и обрабатываем время окончания времени по таймеру
    if t > 0:
        # полупрозрачная рамочка
        frame:
            background "#0128"
            align(.5, .1)

            # индикатор оставшегося времени
            bar value AnimatedValue(value=.0, range=1., delay=t, old_value=1.) xsize gui.choice_button_width

        # таймер, который помечает пункт по умолчанию
        timer t action renpy.curry(renpy.play)("audio/hover.ogg", "audio"), renpy.curry(renpy.set_focus)("menu", item, layer="screens")

        # таймер, который выполняет пункт по умолчанию
        timer t + .25 action renpy.curry(renpy.play)("audio/click.mp3", "audio"), items[item].action

    # все кнопки
    vbox:
        for index in range(len(items)):
            $ i = items[index]
            textbutton i.caption action i.action id index


# игра викторина
label question:

    scene bg_hall4
    play music two
    # если указать наш экран menu вместо обычного choice (который мы не меняли),
    # то будет отображаться именно он, а там есть таймер. по умолчанию 5 секунд,
    # но можно задать другое, а так же указать другой пункт по умолчанию (счёт начинается с нуля!):
    # menu(screen="menu", t=3, item=0):

    "Сейчас начнётся викторина."
    extend " Всего будет 6 вопросов, ответ на каждый нужно дать в течение отведённого времени."
    "Если вы не успеете ответить на вопрос, он отметится как неверный.."
    "Игра начинается, удачи!"

    menu(screen="menu"):

        "Где мы находимся?"

        "Корпус З, 6 этаж":
            pass

        "Корпус Ж, 1 этаж":
            pass

        "Корпус М, 3 этаж":
            $ res = True
            $ qwer = qwer + 1

        "Не знаю":
            pass

    if res:
        "Хорошее начало, так держать!"
    else:
        "Нет.."
    
    $ res = False

    scene mpei
    menu(screen="menu"):

        "Какие корпуса находятся в ГК?"

        "А, Б, В, Г, Д":
            $ res = True
            $ qwer = qwer + 1

        "Д, Е, К, Ж":
            pass

        "С, М, Н":
            pass

        "Не знаю":
            pass

    if res:
        "Молодец, что ты знаешь это!"
    else:
        "Нет, ты не прав."
    
    $ res = False
    
    scene petr
    menu(screen="menu"):

        "Где находится изображенный на фото памятник?"

        "Санкт-Петербург":
            pass

        "Екатеринбург":
            pass

        "Москва":
            $ res = True
            $ qwer = qwer + 1

        "Не знаю":
            pass

    if res:
        "Круто!"
    else:
        "Жалко, что ты не знаешь это.."
    
    $ res = False

    scene water
    menu(screen="menu"):

        "Сколько человек может прожить без воды?"

        "От 4 до 8 дней":
            pass

        "От 3 до 7 дней":
            $ res = True
            $ qwer = qwer + 1

        "Около месяца":
            pass

        "Не знаю":
            pass

    if res:
        "Неплохо!"
    else:
        "Совсем нет."
    
    $ res = False

    scene bathroom
    menu(screen="menu"):

        "Кто находится в ванной?"

        "Белка":
            pass

        "Я":
            pass

        "Крокодил":
            $ res = True
            $ qwer = qwer + 1

        "Не знаю":
            pass

    if res:
        "А ты смекалистый."
    else:
        "Мимо."
    
    $ res = False

    scene bg_hall4
    menu(screen="menu"):

        "Ты думаешь, что сможешь выбраться отсюда?"

        "Да":
            $ h = h+1
            $ qwer = qwer + 1
            pass

        "Нет":
            pass

        "Никогда":
            pass
    
    stop music       
    jump three