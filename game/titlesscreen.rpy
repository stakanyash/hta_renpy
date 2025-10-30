init python:
    import os, json, random

    FLAGS_FILE = "hta.json"

    def load_flags():
        if os.path.exists(FLAGS_FILE):
            try:
                with open(FLAGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"license": False, "tutorial": False}

    def save_flags(flags):
        with open(FLAGS_FILE, "w", encoding="utf-8") as f:
            json.dump(flags, f)

    slide_count = 6
    total_time = random.uniform(3.0, 7.0)

    weights = [random.random() for _ in range(slide_count)]
    weight_sum = sum(weights)

    pauses = [total_time * w / weight_sum for w in weights]

label splashscreen:
    $ flags = load_flags()

    if not flags["license"]:
        $ renpy.call_screen("license_prompt")
        $ flags["license"] = True
        $ save_flags(flags)

    $ renpy.movie_cutscene("movies/disclaimer.mp4")

    pause 0.5

    $ slides = ["loading_1", "loading_2", "loading_3", "loading_4", "loading_5", "loading_6"]
    python:
        for i in range(len(slides)):
            renpy.show(slides[i])
            renpy.pause(pauses[i], hard=True)
            renpy.hide(slides[i])

    return
