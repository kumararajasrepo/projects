import tomllib

class Config:

    def __init__(self,name):
        self.name=name

    def get_config_data(self):
        with open('news_reader\config.toml','rb') as f:
            toml_data: dict=tomllib.load(f)
            return toml_data