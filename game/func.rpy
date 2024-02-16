init -2:

    # масштабирование
    transform zoom(zoom=1):
        subpixel True
        zoom zoom
    transform xzoom(zoom=1):
        subpixel True
        xzoom zoom
    transform yzoom(zoom=1):
        subpixel True
        yzoom zoom

    # прозрачность
    transform alpha(alpha=1.):
        alpha alpha
    transform alphing(alpha1=0, alpha2=1, t=1):
        alpha alpha1
        ease t alpha alpha2

    # размытость
    transform blur(blur=4):
        blur blur
    transform bluring(blur1=0, blur2=16, t=1):
        blur blur1
        ease t blur blur2

    # яркость
    transform brightness(brightness=.25):
        matrixcolor BrightnessMatrix(brightness)

    transform brightnessing(brightness1=0, brightness2=.25, t=2):
        matrixcolor BrightnessMatrix(brightness1)
        ease t matrixcolor BrightnessMatrix(brightness2)


init -2 python:

    # директории для хранение звуков и музыки
    audio_dir = "audio"
    music_dir = "music"

    # автоматическое объявление изображений (вызывается из init)
    def images_auto(folders=["images"]):
        config.automatic_images_minimum_components = 1
        config.automatic_images = [' ', '_', '/']
        config.automatic_images_strip = folders

    # # остановить перемотку
    # def stop_skip():
    #     renpy.config.skipping = None

    # строку в displayable
    def img2disp(displayable):
        if isinstance(displayable, (str, unicode)):
            return renpy.displayable(displayable)
        return displayable

    # узнать текущие размеры изображения типа displayable
    # например, после масштабирования и других операций
    # не работает в разделе init
    def get_size(displayable, w=config.screen_width, h=config.screen_height, st=0, at=0):
        w, h = renpy.render(img2disp(displayable), w, h, st, at).get_size()
        return int(w), int(h)
    def get_width(displayable):
        return get_size(displayable)[0]
    def get_height(displayable):
        return get_size(displayable)[1]

    # если это не список, то сделать единственным элементом списка
    def make_list(param):
        if param is None:
            return None
        if not isinstance(param, list):
            param = [param]
        return param

    # рандомный элемент из параметров на входе
    # просто сокращаем писанину
    def rnds(*args):
        return renpy.random.choice(args)

    # воспроизвести звук для канала audio, который поддерживает многопоточность
    def splay(mname, fadein=0, fadeout=0, channel=config.play_channel, ext="ogg", audio_dir=audio_dir):
        if mname:
            mname = make_list(mname)
            lst = []
            for i in mname:
                lst.append(audio_dir + "/" + i + "." + ext)
            renpy.play(lst, channel=channel, fadein=fadein, fadeout=fadeout)


    # превращаем функции в action для экранов screen
    SPlay = renpy.curry(splay)

    def s_play(sound, trans, st, at):
        if sound:
            splay(sound)

    # полное копирование
    import copy as dcopy
    def copy(*args):
        return dcopy.deepcopy(*args)


init -99 python:
    # список допустимых времён суток
    # "night" - обязательно!
    alldaytime = ["day", "night"]

    # список префиксов-меток для динамических спрайтов,
    # освещение которых будет зависеть от времени суток в curdaytime
    # например, все фоны и пара героев:
    # daytime_prefix = ["bg", "eileen", "pytom"]
    # к таким именам будет добавлен суффикс из daytime_suffix
    # а потом они будут превращены в динамические уже со своими именами без суффикса
    daytime_prefix = []

    # суффикс для динамических спрайтов - первое в списке время суток
    daytime_suffix = alldaytime[0]

    # здесь будут храниться имена изменённых спрайтов, зависимых от curdaytime
    daytime_suffixed = []

# БЛОК ДЛЯ ДОПОЛНЕННОГО АВТООБЪЯВЛЕНИЯ СПРАЙТОВ
# стандартное автообъявление картинок, но с webp
# плюс не разбиваются на теги имена, предназначенные для LayerdImage
# вместо этого объединяются через нижний минус "_"
# префиксы, по которым определяются такие имена берутся из layered_prefixes
# выполняется после всего остального
init 1900 python hide:
    def create_automatic_images():

        seps = config.automatic_images

        if seps is True:
            seps = [ ' ', '/', '_' ]

        for dir, fn in renpy.loader.listdirfiles():

            if fn.startswith("_"):
                continue

            # только .png и .jpg и .jpeg и .webp
            if not (fn.lower().endswith(".png") or fn.lower().endswith(".jpg") or fn.lower().endswith(".jpeg") or fn.lower().endswith(".webp")):
                continue

            # убираем расширения и заменяем слеши.
            if fn.lower().endswith(".jpeg") or fn.lower().endswith(".webp"):
                shortfn = fn[:-5].replace("\\", "/")
            else:
                shortfn = fn[:-4].replace("\\", "/")

            # делим строку на части
            name = ( shortfn, )
            for sep in seps:
                name = tuple(j for i in name for j in i.split(sep))

            # выбрасываем имя папок из тегов
            while name:
                for i in config.automatic_images_strip:
                    if name[0] == i:
                        name = name[1:]
                        break
                else:
                    break

            # для проверки префиксов и суффиксов после
            # возможной склейки тегов
            prefix = name[0]
            suffix = name[len(name) - 1]

            # убираем суффикс, если это первое время суток
            if suffix == daytime_suffix:
                name = name[:-1]

            # имя без суффикса
            name0 = name

            # теги одной строкой
            sname = " ".join(name)

            # добавляем суффикс по умолчанию, если начинается
            # с префикса из списка меток для динамических спрайтов,
            # которые будут менять освещение в зависимости от времени суток
            if prefix in daytime_prefix:
                # нельзя автоматизировать файлы с суффиксами времён суток,
                # потому что они станут частью автоматизированного спрайта
                if not suffix in alldaytime[1:]:
                    if not sname in daytime_suffixed:
                        # запоминаем имя изменённого спрайта
                        store.daytime_suffixed.append(sname)


            # игнорируем, если уже создана одноимённая копия с суффиксом
            if name0 in daytime_suffixed:
                continue

            # игнорируем, если не набирается указанное в переменной количество тегов
            if len(name) < config.automatic_images_minimum_components:
                continue

            # игнорируем, если такой спрайт уже есть
            if name in renpy.display.image.images:
                continue
                
            # объявляем спрайт
            renpy.image(name, fn)

    # если заданы параметры, то объявляем спрайты автоматом
    if config.automatic_images:
        create_automatic_images()

    # функция для динамического освещения спрайтов и фонов
    def def_daytime(st, at, img):
        # ищем картинку для текущего времени суток
        new = img + " " + curdaytime
        if has_image(new):
            return new, None
        # если не нашли, то берем основную
        new = img + " " + daytime_suffix
        # и перекрашиваем в соответствии с настройками
        if img.startswith(bg_prefix):
            return At(new, atdaytime(True)), None
        return At(new, atdaytime()), None

    # если заданы параметры, то создаём динамически освещённые спрайты
    if len(daytime_suffixed) > 0:
        # перебираем все спрайты, для которых нужна реакция на освещение
        for i in daytime_suffixed:
            # создаём такие спрайты
            renpy.image(i, DynamicDisplayable(def_daytime, i))
