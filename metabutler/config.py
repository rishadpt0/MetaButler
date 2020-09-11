if not _name_.endswith("sample_config"):
    import sys
    print("The README is there to be read. Extend this sample config to a config file, don't just rename and change "
          "values here. Doing that WILL backfire on you.\nBot quitting.", file=sys.stderr)
    quit(1)


# Create a new config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True

    # REQUIRED
    API_KEY = "1365900902:AAE5UvxO6TXnxDQQX3Q2j_62L9VWTNMkxYU"
    OWNER_ID = "1100580536"  # If you dont know, run the bot and do /id in your private chat with it
    OWNER_USERNAME = "rizuppt"

    


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
