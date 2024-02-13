# Определение персонажей игры.
define me = Character('Я', color="#c8ffc8")
define G = Character('Генри', color="#4a69aa")
define S = Character('Скотт', color="#a74262")

define n = Character(None, kind=nvl)

# Вставка перед меню игры
label splashscreen:
    scene menu_logo with fade
    pause (2)

    return

#константы для ввода музыки в игру
define audio.start = "audio/another_end.mp3"
define audio.steps = "audio/shagi.mp3"
define audio.one = "audio/game_one.mp3"
define audio.little = "audio/home.mp3"
define audio.two = "audio/fripperies.mp3"
define audio.battle = "audio/battle.mp3"
define audio.frozen = "audio/frozen.mp3"

# для поиска  предметов и викторины
init python:
    res = False

# для секретных реплик в конце
init python:
    h = 0

#позиция для персонажа в локации холл3 и там, где можно расположиться по центру
init:
    $ pos3 = Position(xalign = 0.5, yalign = 0.5) 
    $ pos4 = Position(xalign = 0.55, yalign = 0.7)



init:
    style choice_button:
        activate_sound "audio/click.mp3"
        hover_sound "audio/hover.ogg"


init:
    # пьяный трансформ
    transform drunk():
        parallel:
            ease 1.5 zoom 1.1 align(.5, 1.)
            ease 1.15 zoom 1.05 align(.0, 1.)
            ease 1.5 zoom 1.1 align(1., 1.)
            ease 1.25 zoom 1 align(.0, .5)
            ease 1.15 zoom 1.1 align(1., .0)
            ease 1.25 zoom 1.05 align(.5, .5)
            repeat
        parallel:
            ease 1 blur 24
            ease .5 blur 4
            ease 1.5 blur 16
            ease 1.25 blur 0
            repeat

    # размытость
    transform blur(blur=4):
        blur blur
    transform bluring(blur1=0, blur2=16, t=1):
        blur blur1
        ease t blur blur2
