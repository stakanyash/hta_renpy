init python:
    import random
    import math
    from renpy.display.im import MatrixColor

    enemy_damage_multiplier = 1.0
    consecutive_player_hits = 0
    turn_count = 0
    attack_locked = False

    def apply_enemy_attack():
        global player_hp, player_max_hp

        randomDamage = random.random()

        if config.developer:
            renpy.notify(f"Damage Random is: {randomDamage}")

        if randomDamage <= 0.40:
            damage_percent = difficulty_base_multiplier * enemy_damage_multiplier
            damage = int(player_max_hp * damage_percent)

            player_hp = max(0, player_hp - damage)

            renpy.sound.play("audio/sfx/landing_car_sparkle.wav", channel="damage")
            renpy.show(bgname, at_list=[Shake(None, 1.0, dist=7)], what=None)
            renpy.show("damage", at_list=[fadeout_damage, Shake(None, 2.0, dist=5)])

    def attack_enemy():
        global enemy_hp, enemy_max_hp, turn_count
        global attack_locked, enemy_damage_multiplier, consecutive_player_hits
        global player_hp, player_max_hp

        if attack_locked:
            return
        attack_locked = True

        hits_count = random.randint(2, 3) if player_config.gun_type == "Firearm" else 1

        for _ in range(hits_count):
            if random.random() <= 0.7:
                damage = random.randint(*damage_range)
                enemy_hp = max(0, enemy_hp - damage)
                renpy.sound.play(f"audio/sfx/shoot/{player_config.current_gun}_shoot.wav", channel="shoot")
                renpy.show(enemy_image, at_list=[center, stretch_in], what=None)
            else:
                renpy.sound.play("audio/sfx/shoot_miss01.ogg", channel="missshot")

            renpy.timeout(0.3)

        apply_enemy_attack()

        renpy.restart_interaction()

    def heal():
        global player_hp, heal_count, max_heals, player_max_hp

        if heal_count < max_heals:
            heal_per = random.uniform(0.02, 0.1)

            heal_amount = int(player_max_hp * heal_per)

            player_hp = min(player_hp + heal_amount, player_max_hp)

            heal_count += 1

            renpy.notify(f"Восстановлено {heal_amount} здоровья.")
            renpy.sound.play("audio/sfx/life.wav", channel="sound")

        renpy.restart_interaction()

    ## Получение изображения полоски здоровья врага
    def get_enemy_bar_image():
        if enemy_hp <= 0:
            return "gui/bossbar/boss_bar_0.png"
        percent = (enemy_hp / enemy_max_hp) * 100
        level = math.ceil(percent / 10.0) * 10
        level = max(10, min(100, level))
        return f"gui/bossbar/boss_bar_{level}.png"

    ## Вспомогательные функции для цифр HP и лечения
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

    ## Эффекты мигания при низком HP и исцелении
    def get_lowheal():
        percent = player_hp / float(player_max_hp)
        if percent < 0.15:
            return "gui/bossbar/redlight_hp.png"
        else:
            return "gui/bossbar/redlight_blank.png"

    def get_lowhealamount():
        percent = get_remain_heals() / float(max_heals)
        if percent < 0.30:
            return "gui/bossbar/redlight_fuel.png"
        else:
            return "gui/bossbar/redlight_blank.png"

## Эффект затухания урона
transform fadeout_damage:
    alpha 1.0
    pause 0.5
    linear 0.5 alpha 0.0

## Анимация мигания для lowheal и lowhealamount
transform blinking:
    alpha 1.0
    pause 0.3
    alpha 0.0
    pause 0.3
    repeat