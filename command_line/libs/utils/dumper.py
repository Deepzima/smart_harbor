import json
import toml

class FileUtility:
    
    def __init__(self, config_file):
        self.config = self.load_toml(config_file)

    @staticmethod
    def load_json(file_path):
        with open(file_path, "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def dump_json(data, path_dir, invoke):
        with open(path_dir + invoke +"-output.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

    @staticmethod
    def load_toml(file_path):
        return toml.load(file_path)

    @staticmethod
    def dump_toml(data, file_path):
        with open(file_path, "w") as toml_file:
            toml.dump(data, toml_file)
