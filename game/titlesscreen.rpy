init python:
    import os, json

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

label splashscreen:
    $ flags = load_flags()

    if not flags["license"]:
        $ renpy.call_screen("license_prompt")
        $ flags["license"] = True
        $ save_flags(flags)

    $ renpy.movie_cutscene("movies/disclaimer.mp4")

    return
