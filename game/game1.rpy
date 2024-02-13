# игра поиск предметов
label qwerty:
    scene black
    play music one

    # заполняем экран игры объектами
    $ InitGame("bg_room", 15.0, (700, 650), "figure1", (1088, 60), "figure2", (850, 500), "figure3", (535, 945), "figure4")

    # показываем экран игры в качестве простого фона
    $ GameAsBG()
    with dissolve

    "Сейчас начнётся игра 'поиск предметов'!"
    "В этой игре необходимо найти все спрятанные предметы: внимательно взгляните на локацию и кликайте правой кнопкой мыши на лежащие предметы."
    "Это игра на время! Будьте внимательны!"
    "Игра начинается!"

    window hide

    # запускаем игру и играем
    $ res_game = False
    $ res = StartGame()

    # снова показываем в качестве фона
    # (но уже без найденных во время игры предметов)
    $ GameAsBG()

    window auto    
    # проверяем результаты игры и обыгрываем их в сценарии
    if oRes:
        "Ура! Вы нашли все спрятанные предметы!"
        #ввести переменную для отличия диалога при проигрыше и выигрыше
        $ res_game = True
    else:
        "Найдено предметов: [oLen] из [maxLen]."
        "Жаль, но не все предметы были найдены!"
        #ввести переменную для отличия диалога при проигрыше и выигрыше
    
    stop music fadeout 0.5
    jump two
    return