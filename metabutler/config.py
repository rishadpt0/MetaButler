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
