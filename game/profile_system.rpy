#init python:
#    import renpy.loadsave as _loadsave
#    _loadsave.sync = lambda *args, **kwargs: None

init -1 python:
    import os, json, shutil, re as _re

    _BASE_SAVEDIR = None

    def _profiles_root():
        return _BASE_SAVEDIR

    def _profile_dir(name):
        return os.path.join(_profiles_root(), name)

    def _profile_json_path(name):
        return os.path.join(_profile_dir(name), "profile.json")

    def _profile_saves_dir(name):
        return os.path.join(_profile_dir(name), "saves")

    _PROFILE_NAME_RE = _re.compile(r'^[^\\/:\*\?"<>\|\s][^\\/:\*\?"<>\|]{0,38}$')

    def profile_name_valid(name):
        return bool(name) and bool(_PROFILE_NAME_RE.match(name))

    def profile_list():
        root = _profiles_root()
        if not os.path.isdir(root):
            return []
        result = []
        for folder_name in sorted(os.listdir(root)):
            folder_path = os.path.join(root, folder_name)
            if not os.path.isdir(folder_path):
                continue
            json_path = os.path.join(folder_path, "profile.json")
            if not os.path.isfile(json_path):
                continue
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
            data.setdefault("name", folder_name)
            data.setdefault("difficulty", "normal")
            data.setdefault("difficulty_base_multiplier", 0.03)
            data["_folder"] = folder_name
            result.append(data)
        return result

    def profile_create(name, difficulty="normal", difficulty_base_multiplier=0.03):
        name = name.strip()
        if not profile_name_valid(name):
            return False, u"Недопустимое имя (1-40 символов, без \\ / : * ? \" < > |)"
        if os.path.exists(_profile_dir(name)):
            return False, u"Профиль с таким именем уже существует."
        try:
            os.makedirs(_profile_dir(name), exist_ok=True)
            os.makedirs(_profile_saves_dir(name), exist_ok=True)
            _profile_write_json(name, {
                "name": name,
                "difficulty": difficulty,
                "difficulty_base_multiplier": difficulty_base_multiplier,
            })
        except Exception as e:
            return False, u"Ошибка при создании: {}".format(e)
        return True, ""

    def profile_rename(old_name, new_name):
        new_name = new_name.strip()
        if not profile_name_valid(new_name):
            return False, u"Недопустимое имя (1-40 символов, без \\ / : * ? \" < > |)"
        if not os.path.isdir(_profile_dir(old_name)):
            return False, u"Профиль не найден."
        if os.path.exists(_profile_dir(new_name)):
            return False, u"Профиль с таким именем уже существует."
        try:
            os.rename(_profile_dir(old_name), _profile_dir(new_name))
            data = _profile_read_json(new_name)
            data["name"] = new_name
            _profile_write_json(new_name, data)
        except Exception as e:
            return False, u"Ошибка при переименовании: {}".format(e)
        if persistent.current_profile == old_name:
            _profile_apply(new_name)
        return True, ""

    def profile_delete(name):
        if not os.path.isdir(_profile_dir(name)):
            return False, u"Профиль не найден."
        try:
            shutil.rmtree(_profile_dir(name))
        except Exception as e:
            return False, u"Ошибка при удалении: {}".format(e)
        if persistent.current_profile == name:
            persistent.current_profile = None
            config.savedir = _BASE_SAVEDIR
            flags = load_flags()
            flags["current_profile"] = None
            save_flags(flags)
        return True, ""

    def profile_activate(name):
        _profile_apply(name)
        flags = load_flags()
        flags["current_profile"] = name
        save_flags(flags)

    def _profile_apply(name):
        saves = _profile_saves_dir(name)
        os.makedirs(saves, exist_ok=True)
        persistent.current_profile = name
        config.savedir = saves
        data = _profile_read_json(name)
        renpy.store.difficulty                 = data.get("difficulty", "normal")
        renpy.store.difficulty_base_multiplier = data.get("difficulty_base_multiplier", 0.03)
        
        import renpy.savelocation as _sl
        import renpy.loadsave as _ls
        _sl.init()
        _ls.init()
        _ls.clear_cache()
        renpy.persistent.update()

    def profile_save_difficulty(difficulty, multiplier):
        name = getattr(persistent, "current_profile", None)
        if not name:
            return
        data = _profile_read_json(name)
        data["difficulty"] = difficulty
        data["difficulty_base_multiplier"] = multiplier
        _profile_write_json(name, data)

    def _profile_read_json(name):
        try:
            with open(_profile_json_path(name), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _profile_write_json(name, data):
        with open(_profile_json_path(name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def current_profile_name():
        return getattr(persistent, "current_profile", None) or u"\u2014"

    _DIFFICULTY_LABELS = {
        "easy":   u"Новичок",
        "normal": u"Бывалый",
        "hard":   u"Профессионал",
        "expert": u"Мастер",
    }

    def difficulty_label(key):
        return _DIFFICULTY_LABELS.get(key, key)

    def _profile_system_init():
        global _BASE_SAVEDIR
        if _BASE_SAVEDIR is None:
            _BASE_SAVEDIR = os.path.join(config.gamedir, "profiles")

        flags = load_flags()
        name = flags.get("current_profile", None)

        if name and os.path.isdir(_profile_saves_dir(name)):
            config.savedir = _profile_saves_dir(name)
            persistent.current_profile = name
            data = _profile_read_json(name)
            renpy.store.difficulty                 = data.get("difficulty", "normal")
            renpy.store.difficulty_base_multiplier = data.get("difficulty_base_multiplier", 0.03)
            load_audio_prefs()
            return

        flags["current_profile"] = None
        save_flags(flags)
        persistent.current_profile = None

        existing = profile_list()
        if existing:
            first = existing[0]["name"]
            config.savedir = _profile_saves_dir(first)
            persistent.current_profile = first
            flags["current_profile"] = first
            save_flags(flags)
            data = _profile_read_json(first)
            renpy.store.difficulty                 = data.get("difficulty", "normal")
            renpy.store.difficulty_base_multiplier = data.get("difficulty_base_multiplier", 0.03)
            load_audio_prefs()
        else:
            config.savedir = _BASE_SAVEDIR

    def save_audio_prefs():
        flags = load_flags()
        flags["music_volume"]   = round(renpy.game.preferences.volumes.get("music", 1.0), 2)
        flags["sound_volume"]   = round(renpy.game.preferences.volumes.get("sfx", 1.0), 2)
        flags["mute_music"]     = renpy.game.preferences.mute.get("music", False)
        flags["mute_sfx"]       = renpy.game.preferences.mute.get("sfx", False)
        flags["fullscreen"]     = renpy.game.preferences.fullscreen
        flags["text_speed"]     = round(renpy.game.preferences.text_cps, 2)
        flags["afm_time"]       = round(renpy.game.preferences.afm_time, 2)
        save_flags(flags)

    def load_audio_prefs():
        flags = load_flags()
        p = renpy.game.preferences

        if "music_volume" in flags:
            p.volumes["music"]  = flags["music_volume"]
        if "sound_volume" in flags:
            p.volumes["sfx"]    = flags["sound_volume"]
        if "mute_music" in flags:
            p.mute["music"]     = flags["mute_music"]
        if "mute_sfx" in flags:
            p.mute["sfx"]       = flags["mute_sfx"]
        if "text_speed" in flags:
            p.text_cps          = flags["text_speed"]
        if "afm_time" in flags:
            p.afm_time          = flags["afm_time"]
        if "fullscreen" in flags:
            p.fullscreen        = flags["fullscreen"]

init python:
    def _profile_after_load():
        flags = load_flags()
        name = flags.get("current_profile", None)
        if name and os.path.isdir(_profile_saves_dir(name)):
            config.savedir = _profile_saves_dir(name)
            persistent.current_profile = name
            import renpy.savelocation as _sl
            import renpy.loadsave as _ls
            _sl.init()
            _ls.init()
            _ls.clear_cache()
            renpy.persistent.update()

    config.start_callbacks.append(_profile_system_init)
    config.after_load_callbacks.append(_profile_after_load)

default persistent.current_profile = None
default _sel_profile = None

screen profiles_screen():
    modal True
    zorder 200

    button:
        style "empty"
        xfill True
        yfill True
        action NullAction()
        background "#000000cc"

    add "gui/settings_menu.png"

    frame:
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
                text u"Профили" size 60 color "#fed11b" font "fonts/ARIALBD.ttf" ypos 20 xpos 5

                frame:
                    background None
                    xalign 1.0
                    yalign 0

                    python:
                        ui.imagebutton(
                            idle_image="gui/htabuttons/close_idle.png",
                            hover_image="gui/htabuttons/close_hover.png",
                            activate_image="gui/htabuttons/close_activate.png",
                            clicked=renpy.store.Hide("profiles_screen"),
                            activate_sound="audio/sfx/click.wav"
                        )

            null height 90

            hbox:
                spacing 0

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    xsize 1000
                    ysize 600

                    vbox:
                        spacing 4

                        for _p in profile_list():
                            $ _pn        = _p["name"]
                            $ _is_active = (_pn == current_profile_name())
                            $ _is_sel    = (_pn == _sel_profile)
                            $ _diff_lbl  = difficulty_label(_p.get("difficulty", "normal"))

                            button:
                                xsize 980
                                ypadding 12
                                xpadding 20
                                background ("#ffffff2f" if _is_sel else (
                                    "#ffffff18" if _is_active else "#00000000"
                                ))
                                hover_background "#ffffff15"
                                action [
                                    Function(profile_activate, _pn),
                                    SetVariable("_sel_profile", _pn),
                                ]

                                hbox:
                                    xfill True
                                    spacing 20

                                    text "[_pn]":
                                        size 28
                                        color "#404040"
                                        xmaximum 600

                                    if _is_active:
                                        text u"активен":
                                            size 22
                                            color "#404040"
                                            xalign 1.0
                                            yalign 0.5

                        if not profile_list():
                            text u"Профилей пока нет.\nНажмите «Создать».":
                                size 24
                                color "#606060"

                frame:
                    xsize 300
                    ysize 700
                    background None
                    padding (30, 20)

                    vbox:
                        spacing 20
                        xfill True

                        textbutton u"Создать" activate_sound "audio/sfx/click.wav":
                            style "settings_text_button"
                            action Show("profiles_create_screen")

                        textbutton u"Изменить" activate_sound "audio/sfx/click.wav":
                            style "settings_text_button"
                            sensitive (_sel_profile is not None)
                            action Show("profiles_rename_screen")

                        textbutton u"Удалить" activate_sound "audio/sfx/click.wav":
                            style "settings_text_button"
                            sensitive (_sel_profile is not None)
                            action Show("profiles_delete_screen")

screen profiles_create_screen():
    modal True
    zorder 210

    frame:
        style "name_input_overlay"
        xfill True
        yfill True

    frame:
        style "name_input_frame"
        xalign 0.5
        yalign 0.5
        padding (40, 40)

        default _inp_name = ""

        vbox:
            spacing 30
            xalign 0.5

            text u"Имя профиля:" size 36 xalign 0.5 color "#404040"

            input:
                value ScreenVariableInputValue("_inp_name")
                length 10
                style "centered_input"
                pixel_width 500
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 0

                textbutton u"Создать" activate_sound "audio/sfx/click.wav" action Function(_profiles_do_create, _inp_name, False) style "smaller_button"
                if profile_list():
                    textbutton u"Отмена" activate_sound "audio/sfx/click.wav" action Hide("profiles_create_screen") style "smaller_button"

screen profiles_rename_screen():
    modal True
    zorder 210

    frame:
        style "name_input_overlay"
        xfill True
        yfill True

    frame:
        style "name_input_frame"
        xalign 0.5
        yalign 0.5
        padding (40, 40)

        default _inp_new = (_sel_profile or "")

        vbox:
            spacing 30
            xalign 0.5

            text u"Новое имя профиля:" size 36 xalign 0.5 color "#404040"

            input:
                value ScreenVariableInputValue("_inp_new")
                length 10
                style "centered_input"
                pixel_width 500
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 0

                textbutton u"Сохранить" activate_sound "audio/sfx/click.wav" action Function(_profiles_do_rename, _inp_new) style "smaller_button"
                textbutton u"Отмена"    activate_sound "audio/sfx/click.wav" action Hide("profiles_rename_screen") style "smaller_button"

screen profiles_delete_screen():
    modal True
    zorder 210

    frame:
        style "name_input_overlay"
        xfill True
        yfill True

    frame:
        style "name_input_frame"
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        ysize 260

        vbox:
            spacing 30
            xalign 0.5

            text u"Удалить профиль «[_sel_profile]»?" size 30 xalign 0.5 color "#404040"

            text u"Все сохранения будут удалены безвозвратно." size 22 xalign 0.5 color "#804040"

            hbox:
                xalign 0.5
                spacing 0

                textbutton u"Удалить" activate_sound "audio/sfx/click.wav" action Function(_profiles_do_delete) style "smaller_button"
                textbutton u"Отмена"  activate_sound "audio/sfx/click.wav" action Hide("profiles_delete_screen") style "smaller_button"

screen profiles_error_popup(message):
    modal True
    zorder 300

    add "#00000050"

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 50
        ypadding 40

        vbox:
            spacing 30
            xalign 0.5

            text message:
                size 36
                xalign 0.5
                text_align 0.5
                color "#404040"

            textbutton "OK" activate_sound "audio/sfx/click.wav":
                xalign 0.5
                action Hide("profiles_error_popup")
                style "confirm_button"

init python:
    def _profiles_do_create(name, auto_activate):
        ok, msg = profile_create(name)
        if ok:
            renpy.store._sel_profile = name
            profile_activate(name)
            renpy.hide_screen("profiles_create_screen")
        else:
            renpy.show_screen("profiles_error_popup", msg)

    def _profiles_do_rename(new_name):
        old = renpy.store._sel_profile
        ok, msg = profile_rename(old, new_name)
        if ok:
            renpy.store._sel_profile = new_name.strip()
            renpy.hide_screen("profiles_rename_screen")
        else:
            renpy.show_screen("profiles_error_popup", msg)

    def _profiles_do_delete():
        name = renpy.store._sel_profile
        ok, msg = profile_delete(name)
        if ok:
            renpy.store._sel_profile = None
            renpy.hide_screen("profiles_delete_screen")
            remaining = profile_list()
            if not remaining:
                renpy.show_screen("profiles_create_screen")
            elif persistent.current_profile is None:
                first = remaining[0]["name"]
                profile_activate(first)
                renpy.store._sel_profile = first
        else:
            renpy.show_screen("profiles_error_popup", msg)

style name_input_overlay is default:
    background "#0000007e"

style name_input_frame is default:
    background Frame("gui/frame.png", 20, 20)
    xsize 600
    ysize 300

style centered_input is input:
    xalign 0.5
    textalign 0.5
    size 28
    color "#404040"
    padding (10, 10)

style smaller_button is button:
    size_group "name_button"
    xpadding 30
    ypadding 40
    color "#404040"

style smaller_button_text is button_text:
    size 22
    xalign 0.5
    textalign 0.5
    color "#404040"
    hover_color "#6d6d6d"

style profiles_action_btn is smaller_button:
    xpadding 30
    ypadding 14

style profiles_action_btn_text is smaller_button_text

style profiles_action_btn_accent is profiles_action_btn

style profiles_action_btn_accent_text is profiles_action_btn_text:
    color "#fed11b"
    hover_color "#ffdd55"
    insensitive_color "#fed11b60"

style profiles_action_btn_danger is profiles_action_btn

style profiles_action_btn_danger_text is profiles_action_btn_text:
    color "#ff6666"
    hover_color "#ff9999"
    insensitive_color "#ff666660"
