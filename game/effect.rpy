## КАК ПОЛЬЗОВАТЬСЯ:

# включить:
# $ tv_on()

# выключить:
# $ tv_off()

# узнать, включен ли режим:
# if tv_mode:

## ПАРАМЕТРЫ:
init -2 python:
    # картинки для имитации телевизора - можно одну:
    # tv_image = "tv"

    # или пустой список, если не нужны совсем:
    # tv_image = [ ]

    # или несколько слоёв списком:
    tv_image = [ "tvnoise" ]

    # подкрашивание ч/б картинки для эффекта кинескопа ("#fff" - не менять цветовую гамму)
    tv_color = "#efd"

    # если заданы звуки включения-выключения, то они прозвучат
    tvon = "audio/tvon.ogg"
    tvoff = "audio/tvoff.ogg"

    ## ДАЛЕЕ НИЧЕГО НЕ МЕНЯТЬ
    tv_mode = False

    # искажения под чёрно-белый телевизор
    def tv_at_f(trans, st, at):
        trans.matrixcolor = TintMatrix(tv_color) * SaturationMatrix(0) * ContrastMatrix(1.5) * BrightnessMatrix(renpy.random.random() * .1)
        return 1/10.

    # включить режим телевизора
    def tv_on(effect=dissolve):
        #renpy.show_layer_at([ tv_at ], "master", camera=True)
        tv = tv_image
        if not isinstance(tv, (list, tuple)):
            tv = [ tv ]
        for i in tv:
            if i:
                renpy.show(i, layer="screens")
        if tvon:
            renpy.play(tvon, channel="audio")
        renpy.transition(effect)
        renpy.restart_interaction()
        store.tv_mode = True

    # выключить режим телевизора
    def tv_off(effect=dissolve):
        #renpy.show_layer_at([ tv_off_at ], "master", camera=True)
        tv = tv_image
        if not isinstance(tv, (list, tuple)):
            tv = [ tv ]
        for i in tv:
            if i:
                renpy.hide(i, layer="screens")
        if tvoff:
            renpy.play(tvoff, channel="audio")
        renpy.transition(effect)
        renpy.restart_interaction()
        store.tv_mode = False

init -2:
    # анимация шума для эффекта видеоплёнки
    image tvnoise = Ani("tvnoise ", 24, zoom=4)

    # режим ч/б
    #transform tv_at:
    #    function tv_at_f

    # отключить режим ч/б
    #transform tv_off_at:
    #    matrixcolor TintMatrix("#fff") * SaturationMatrix(1) * ContrastMatrix(1) * BrightnessMatrix(0)



init -222 python:

    # строку в displayable
    def img2disp(displayable):
        if isinstance(displayable, (str, unicode)):
            return renpy.displayable(displayable)
        return displayable

    # автоматическое объявление анимации
    # описание функции Ani:
    # автоматическое объявление картинки с анимацией,
    # например есть кадры "images/neko%s.png",
    # где %s - числа от 1 до 5, тогда объявляем анимацию так:
    # image neko = Ani("neko", 5, 0.5, reverse = False)
    # где:
    # img_name - имя файла без номера (например, "neko")
    # frames - количество кадров
    # delay - пауза между кадрами в секундах
    # если delay это кортеж, например (1, 2), то скорость будет меняться от 1 до 2 секунд
    # loop - зациклить анимацию (по умолчанию включено)
    # reverse - нужно ли проигрывание анимации в обратную сторону
    # effect - эффект для смены кадров
    # start - с какой цифры начинать отсчет кадров
    # ext - расширение, если оно отлично от Null, то работаем с файлами,
    # при ext=Null - с displayable (уже объявленными или даже измененными изображениями)
    # так же можно добавлять любые стандартные для изображений параметры, типа масштабирования или прозрачности:
    # image neko = Ani("neko", 5, 0.5, zoom=2.0, alpha=0.75)
    def Ani(img_name, frames, delay=.1, loop=True, reverse=False, effect=Dissolve(.1, alpha=True), start=1, ext=None, **properties):
        args = []
        # если пауза переменная, то вычисляем ее шаг
        if isinstance(delay, tuple):
            d0 = delay[0]
            d1 = delay[1]
            f = (frames - 1)
            if f <= 0:
                dp = 0
            else:
                dp = (d1 - d0) * 1. / f
            delay = d0
        else:
            dp = 0
        # перебираем все кадры анимации
        for i in range(start, start + frames):
            if ext:
                img = renpy.display.im.image(img_name + str(i) + "." + ext)
            else:
                img = img2disp(img_name + str(i))
            img = Transform(img, **properties)
            args.append(img)
            if reverse or loop or (i < start + frames - 1):
                args.append(delay)
                delay += dp
                # добавляем эффект для смены кадров
                args.append(effect)
        if reverse: # обратная анимация, если нужна
            dp = -dp
            delay += dp
            for i in range(start + frames - 2, start, -1):
                if ext:
                    img = renpy.display.im.image(img_name + str(i) + "." + ext)
                else:
                    img = img2disp(img_name + str(i))
                img = Transform(img, **properties)
                args.append(img)
                if loop or (i > start + 1):
                    args.append(delay)
                    delay += dp
                    args.append(effect)
        return anim.TransitionAnimation(*args)