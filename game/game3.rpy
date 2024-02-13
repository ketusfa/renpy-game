# вызов игры из скрипта:
# call t15_game("картинка", ширина в клетках, высота в клетках)

# например:
# call t15_game("t15 1", 4, 3)

init -2 python:

    # размеры поля в клетках
    t15_w, t15_h = 3, 3

    # координаты пустой клетки
    t15_x, t15_y = 0, 0

    # относительные координаты картинки на экране
    t15_ax, t15_ay = .5, .5

    # эффект для ячейки при наведении курсора
    # например, осветление
    t15_hovered_at = brightness(.2)

    # отмена эффекта
    t15_unhovered_at = brightness(0)

    # уменьшение картинки для игры
    t15_z = 2 / 3.

    # длительность перемещения клетки
    t15_t = .15

    # пауза между итерациями быстрого перемешивания
    t15_t_mix = .01

    # время на увеличение картинки после победы
    t15_t_end = 1

    # количество итераций при стартовом перемешивании
    t15_mix_moves = 100

    # по умолчанию подрезание под квадратные клетки включено
    if persistent.t15_cut is None:
        persistent.t15_cut = True

    # по умолчанию числа не отображаются
    if persistent.t15_num is None:
        persistent.t15_num = False

init -2:
    # стиль для текста подсказок
    style t15_text is text:
        size 72
        bold True
        color "#fff"
        outlines [ (4, "#0004", 0, 0), (3, "#0004", 0, 0), (2, "#0004", 0, 0), (1, "#0004", 0, 0) ]
        text_align .5
        align(.5, .5)
        layout "subtitle"

# пример меню, который можно убрать и удалить use t15_menu ниже
screen t15_menu:
    hbox:
        align(1., .0)
        spacing 12
        textbutton "1" action ToggleT15Num()
        textbutton "#" action ToggleT15Cut()
        textbutton "X" action T15Escape()
        
    vbox:
        # флаг подрезания картинок под квадратные клетки можно добавить в настройки или quick_menu:
        textbutton _("КВАДРАТ") action ToggleT15Cut()

        # флаг подсказок в виде номеров клеток:
        textbutton _("ЧИСЛА") action ToggleT15Num()

init -2:
# ДАЛЬШЕ НИЧЕГО МЕНЯТЬ НЕ СТОИТ

    # анимация смещения
    transform t15_move_at(xo, yo):
        offset(xo, yo)
        # звук перемещения
        function renpy.curry(s_play)("move")
        ease t15_t offset(0, 0)

    # анимация появления
    transform t15_show_hide:
        on show:
            alpha 0
            ease t15_t_end alpha 1
        on hide:
            alpha 1
            ease t15_t_end alpha 0

init -2 python:
    # класс для переключения подрезания под квадратные клетки
    class ToggleT15Cut(Action):
        def __init__(self):
            if persistent.t15_cut is None:
                persistent.t15_cut = True

        def __call__(self):
            persistent.t15_cut = not persistent.t15_cut
            renpy.restart_interaction()

        def get_selected(self):
            return persistent.t15_cut

    # класс для переключения отображения номеров клеток
    class ToggleT15Num(Action):
        def __init__(self):
            if persistent.t15_num is None:
                persistent.t15_num = True

        def __call__(self):
            persistent.t15_num = not persistent.t15_num
            renpy.restart_interaction()

        def get_selected(self):
            return persistent.t15_num

    # здесь будет картинка
    t15_spr = "t15 1"

    # здесь будет поле с ячейками
    t15_a = None

    # размеры клетки
    t15_w_side, t15_h_side = 0, 0

    # размеры картинки
    t15_width, t15_height = 0, 0

    # ширина и высота клетки с учётом настроек
    def t15_cur_size():
        w, h = t15_w_side, t15_h_side

        # если в настройках установлено, то подрезаем под квадратные клетки
        if persistent.t15_cut:
            if w > h:
                w = h
            else:
                h = w
        return w, h

    # вырезать прямоугольную часть картинки с заданными координатами
    def t15_crop(ix, iy):
        # размеры клеток с учётом настроек
        w, h = t15_cur_size()

        # если это последняя клетка, то она пустая
        if (ix, iy) == (t15_w - 1, t15_h - 1):
            return Null(w, h)

        # масштабируем перед разбиением на клетки
        spr = At(t15_spr, zoom(t15_z))

        # отступы для подрезания
        x0 = int((t15_width - w * t15_w) / 2)
        y0 = int((t15_height - h * t15_h) / 2)

        # иначе масштабируем и вырезаем
        return Crop((w * ix + x0, h * iy + y0, w, h), spr)

    # создать поле с ячейками-кортежами, в которых содержатся их изначальные координаты
    def t15_new_a():
        return [ [ (x, y) for x in range(t15_w) ] for y in range(t15_h) ]

    # стартовая инициализация игры
    def t15_init(spr=t15_spr, w=4, h=3):
        global t15_spr, t15_a, t15_w, t15_h, t15_x, t15_y, t15_w_side, t15_h_side, t15_move_xy, t15_width, t15_height, t15_act

        # картинка
        t15_spr = spr

        # размеры поля в клетках
        t15_w, t15_h = w, h

        # заполняем поле
        t15_a = t15_new_a()

        # вырезаем последнюю клетку
        t15_x, t15_y = w - 1, h - 1

        # определяем стороны клетки
        spr = At(t15_spr, zoom(t15_z))
        t15_width, t15_height = get_size(spr)
        t15_w_side = int(t15_width / t15_w)
        t15_h_side = int(t15_height / t15_h)

        # сброс перемещений
        t15_move_cur = 0
        t15_move_xy = (-222, -222)

        # начало перемешивания клеток
        t15_act = -t15_mix_moves

    # выделенная наведением курсора ячейка
    t15_hovered_xy = (-222, -222)

    # визуальное выделение клетки по наведению курсора
    def t15_hover(x=-222, y=-222):
        store.t15_hovered_xy = (x, y)
        renpy.restart_interaction()
    T15Hover = renpy.curry(t15_hover)

    # анимация перемещения клетки
    t15_move_cur = 0

    # текущее действие
    t15_act = 0

    # координаты перемещающейся клетки
    t15_move_xy = (-222, -222)

    # делаем ход, по умолчанию отображаем движение
    def t15_move(x, y, move=True):
        global t15_x, t15_y, t15_move_cur, t15_act, t15_a, t15_move_xy

        # перемещение только в пределах поля
        if x in range(t15_w) and y in range(t15_h):

            w, h = t15_cur_size()

            # если нужно, отображаем движение
            if move:
                t15_move_cur = t15_move_at((x - t15_x) * w, (y - t15_y) * h)
                t15_act = 1

            # меняем клетки местами
            t15_a[y][x], t15_a[t15_y][t15_x] = copy(t15_a[t15_y][t15_x]), copy(t15_a[y][x])

            # отмечаем, какая клетка перемещается
            t15_move_xy = t15_x, t15_y

            t15_x, t15_y = x, y

        renpy.restart_interaction()
    T15Move = renpy.curry(t15_move)

    # рандомное перемешивание клеток
    def t15_mix():
        global t15_act
        # рандомное перемещение, пока не кончатся итерации перемешивания
        if t15_act < 0:
            x, y = rnds((t15_x + 1, t15_y), (t15_x - 1, t15_y), (t15_x, t15_y + 1), (t15_x, t15_y - 1) )
            t15_move(x, y, False)
            t15_act += 1
        # если в конце ничего не изменилось, повторить
        elif t15_a == t15_new_a():
            t15_act = -t15_mix_moves
            renpy.restart_interaction()
    T15Mix = renpy.curry(t15_mix)

    # завершение перемещения
    def t15_move_end():
        global t15_act, t15_move_cur, t15_move_xy

        if t15_act != "win":

            # сброс параметров
            t15_act = 0
            t15_move_cur = 0
            t15_move_xy = (-222, -222)

            # победа
            if t15_a == t15_new_a():
                t15_act = "win"

            renpy.restart_interaction()
    T15MoveEnd = renpy.curry(t15_move_end)

    # досрочный выход из игры
    def t15_escape():
        store.t15_act = "lose"
        renpy.restart_interaction()
    T15Escape = renpy.curry(t15_escape)

# экран игры в пятнашки
screen t15:
    # победа
    if t15_act in [ "win", "lose" ]:
        timer .01 action Return()

    # перемешивание
    elif t15_act < 0:
        timer t15_t_mix repeat True action T15Mix()

    # окончание перемещения
    elif t15_act > 0:
        timer t15_t action T15MoveEnd()

    # контейнер для клеток с частями картинки
    frame:
        style "empty"
        align(t15_ax, t15_ay)

        at t15_show_hide

        # сетка
        grid t15_w t15_h:

            # все клетки
            for iy in range(t15_h):
                for ix in range(t15_w):

                    # координаты картинки в клетке
                    $ x, y = t15_a[iy][ix]
                    $ w, h = t15_cur_size()
                    $ num = str(1 + x + y * t15_w)

                    # клетка-кнопка
                    button:
                        style "empty"
                        xysize(w, h)

                        # выводим картинку в клетке
                        if t15_act != "win":
                            add t15_crop(x, y):
                                # при наведении подсвечиваем
                                if (ix, iy) == t15_hovered_xy:
                                    at t15_hovered_at
                                else:
                                    at t15_unhovered_at

                        # текст номера клетки
                        if persistent.t15_num and (x, y) != (t15_w - 1, t15_h - 1):
                            text num style "t15_text" xysize(w, h)

                        # анимация перемещения
                        if t15_move_cur and (ix, iy) == t15_move_xy:
                            at t15_move_cur

                        # если это соседняя с пустой клетка
                        if (ix, iy) in [ (t15_x + 1, t15_y), (t15_x - 1, t15_y), (t15_x, t15_y + 1), (t15_x, t15_y - 1) ] and not t15_act:

                            # подсвечиваем клетку под курсором
                            hovered T15Hover(ix, iy)
                            unhovered T15Hover()

                            # обрабатываем клик
                            action T15Move(ix, iy)

    # меню
    use t15_menu

# вызов игры в пятнашки с параметрами 
label t15_game(spr=t15_spr, w=t15_w, h=t15_h):
    # убрать прежнюю картинку
    hide img
    with dissolve

    # инициализация игры
    $ t15_init(spr, w, h)

    # для сохранений
    $ renpy.retain_after_load()

    # вызов экрана игры
    call screen t15

    # звук победы
    if t15_act == "win":
        $ splay("win")

        # показываем картинку целиком
        show expression spr as img:
            align(t15_ax, t15_ay)
            zoom t15_z
            ease t15_t_end align(.5, .5) zoom 1

    pause t15_t_end

    return
