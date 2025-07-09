init python:
    import random
    import math
    from renpy.display.im import MatrixColor

    def apply_boss_attack():
        global player_hp, turn_count, player_max_hp
        if turn_count > 0 and turn_count % 5 == 0:
            damage = int(player_max_hp * 0.075)
            player_hp = max(0, player_hp - damage)

            renpy.sound.play(f"audio/sfx/landing_car_sparkle.wav", channel="damage")

            renpy.show("damage", at_list=[fadeout_damage])

    def attack_boss():
        global boss_hp, boss_max_hp, turn_count, attack_locked
        if attack_locked:
            return
        attack_locked = True

        damage_percent = random.uniform(*damage_range)
        damage = int(boss_max_hp * damage_percent)

        shootsound = random.randint(1, 13)

        renpy.sound.play(f"audio/sfx/bullet{shootsound}.wav", channel="shoot")

        renpy.show("boss", at_list=[center, stretch_in], what=None)
        boss_hp = max(0, boss_hp - damage)
        turn_count += 1
        apply_boss_attack()
        renpy.restart_interaction()

    def heal():
        global player_hp, heal_count, max_heals, player_max_hp
        if heal_count < max_heals:
            heal_per = random.uniform(0.01, 0.08)
            heal_amount = int(player_max_hp * heal_per)
            player_hp = min(player_hp + heal_amount, player_max_hp)
            heal_count += 1

            renpy.sound.play(f"audio/sfx/life.wav", channel="sound")
        renpy.restart_interaction()

    def get_boss_bar_image():
        if boss_hp <= 0:
            return "gui/bossbar/boss_bar_0.png"
        percent = (boss_hp / boss_max_hp) * 100
        level = math.ceil(percent / 10.0) * 10
        level = max(10, min(100, level))
        return f"gui/bossbar/boss_bar_{level}.png"

    def hex_to_rgb(color_str):
        color_str = color_str.lstrip("#")
        return tuple(int(color_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def tint_image(path, hex_color):
        r, g, b = hex_to_rgb(hex_color)

        matrix = [
            r, 0, 0, 0, 0,
            0, g, 0, 0, 0,
            0, 0, b, 0, 0,
            0, 0, 0, 1, 0,
        ]

        return MatrixColor(path, matrix)

    def get_hp_digit_images(hp):
        s = str(hp).rjust(4, "E")
        percent = player_hp / float(player_max_hp)
        color = "#00FF00" if percent >= 0.15 else "#FF0000"

        return [tint_image(f"gui/digits/{c}.png", color) for c in s]

    def get_heal_digit_images(heal):
        s = str(heal).rjust(4, "E")
        color = "#00aeff"

        return [tint_image(f"gui/digits/{c}.png", color) for c in s]

    def get_remain_heals():
        return max_heals - heal_count

    def get_lowheal():
        percent = player_hp / float(player_max_hp)
        level = math.ceil(percent / 10.0) * 10
        level = max(10, min(100, level))
        if percent < 0.15:
            return f"gui/bossbar/redlight_hp.png"
        else:
            return f"gui/bossbar/redlight_blank.png"

    def get_lowhealamount():
        percent = get_remain_heals() / float(max_heals)
        level = math.ceil(percent / 10.0) * 10
        level = max(10, min(100, level))
        if percent < 0.30:
            return f"gui/bossbar/redlight_fuel.png"
        else:
            return f"gui/bossbar/redlight_blank.png"

transform fadeout_damage:
    alpha 1.0
    pause 0.5
    linear 1.5 alpha 0.0

transform blinking:
    alpha 1.0
    pause 0.3
    alpha 0.0
    pause 0.3
    repeat