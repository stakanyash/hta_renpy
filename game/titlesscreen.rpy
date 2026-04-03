init python:
    import os, json, random

    FLAGS_FILE = os.path.join(config.basedir, "config.json")

    def load_flags():
        defaults = {
            "license": False,
            "tutorial": False,
            "current_profile": None,
            "fullscreen": False,
            "music_volume": 1.0,
            "sound_volume": 1.0,
            "mute_music": False,
            "mute_sfx": False,
            "text_speed": 0,
            "afm_time": 0
        }
        if os.path.exists(FLAGS_FILE):
            try:
                with open(FLAGS_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    defaults.update(loaded)
                    return defaults
            except:
                pass
        return defaults

    def save_flags(flags):
        with open(FLAGS_FILE, "w", encoding="utf-8") as f:
            json.dump(flags, f, ensure_ascii=False, indent=2)

    slide_count = 6
    total_time = random.uniform(2.0, 5.0)

    weights = [random.random() for _ in range(slide_count)]
    weight_sum = sum(weights)

    pauses = [total_time * w / weight_sum for w in weights]

    disclaimer_text = ""
    try:
        with open(os.path.join(config.gamedir, "docs/DISCLAIMER.md"), "r", encoding="utf-8") as f :
            disclaimer_text = f.read()
    except Exception as e:
        disclaimer_text = (
            "Ошибка при открытии файла docs/DISCLAIMER.md, либо файл отсутствует!\n\n"
            "{a=https://github.com/stakanyash/hta_renpy/blob/main/DISCLAIMER.md}Текст дисклеймера доступен тут{/a}"
        )

screen license_prompt():
    tag menu
    modal True

    add Solid("#000000", alpha=0.7) at fadeinout

    frame at fadeinout:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 500
        padding (30, 30, 30, 30)

        vbox:
            spacing 20
            xfill True
            yfill True

            null height 20

            text "Для использования требуется лицензия на оригинальную игру Hard Truck Apocalypse/Ex Machina. Нажимая «Принимаю», Вы подтверждаете, что у Вас есть такая лицензия." at fadeinout:
                size 25
                color "#404040"
                line_spacing 5
                text_align 0.5
                xalign 0.5

            null

            frame:
                xpos 30
                xsize 840
                background None
                
                vbox:
                    spacing 10
                    xalign 0.5
                    
                    textbutton "Принимаю" activate_sound "audio/sfx/click.wav":
                        action Return(True)
                        xalign 0.5
                        xminimum 250
                        yminimum 60

                    textbutton "Дисклеймер" activate_sound "audio/sfx/click.wav":
                        action [Hide("license_prompt"), Show("disclaimer_screen")]
                        xalign 0.51
                        xminimum 280
                        yminimum 60

screen disclaimer_screen():
    tag menu
    modal True
    zorder 200

    add "gui/settings_menu.png" at fadeinout

    frame at fadeinout:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        padding (50, 50)
        background None

        vbox:
            spacing 20

            hbox:
                xfill True
                text "Дисклеймер" size 60 color "#fed11b" font "fonts/ARIALBD.ttf" ypos 20 xpos 5

            null height 1

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                ypos 100
                xsize 1300
                ysize 505

                vbox:
                    spacing 20
                    text "[disclaimer_text]" size 24 color "#404040" xsize 1280

            null height 80

            hbox:
                spacing 100
                xalign 0.5

                textbutton "Принять" activate_sound "audio/sfx/click.wav":
                    xminimum 250
                    yminimum 60
                    action Return()

                textbutton "Отказаться" activate_sound "audio/sfx/click.wav":
                    xminimum 250
                    yminimum 60
                    action Quit()

label splashscreen:
    $ flags = load_flags()

    if not flags["license"]:
        $ renpy.call_screen("license_prompt")
        $ flags["license"] = True
        $ save_flags(flags)

    if not flags.get("current_profile"):
        $ renpy.show_screen("profiles_create_screen")
        python:
            while not persistent.current_profile:
                renpy.pause(0.1, hard=True)
        $ renpy.hide_screen("profiles_create_screen")
        $ flags["current_profile"] = persistent.current_profile
        $ save_flags(flags)
    else:
        $ profile_activate(flags["current_profile"])

    $ renpy.movie_cutscene("movies/disclaimer.webm")

    pause 0.5

    $ slides = ["loading_1", "loading_2", "loading_3", "loading_4", "loading_5", "loading_6"]
    python:
        for i in range(len(slides)):
            renpy.show(slides[i])
            renpy.pause(pauses[i], hard=True)
            renpy.hide(slides[i])

    return