import os
import toml
from harborapi import HarborAsyncClient

class NestService:
    def __init__(self, config_dir="config"):
        self.credentials = self._load_credentials(config_dir)
        self.client_old_instance = self._create_client(
            self.credentials["base_registry1"]
        )
        self.client_new_instance = self._create_client(
            self.credentials["base_registry2"]
        )

    def _load_credentials(self, config_dir):
        config_path = os.path.join(config_dir, "credentials.toml")
        with open(config_path, "r") as f:
            credentials = toml.load(f)
        return credentials

    def _create_client(self, credentials):
        return HarborAsyncClient(
            url="https://" + credentials["registry_url"] + "/api/v2.0/",
            username=credentials["username"],
            secret=credentials["password"],
            verify=credentials["verify"]
        )

    def get_old_client(self):
        return self.client_old_instance

    def get_new_client(self):
        return self.client_new_instance

    def get_client_by_type(self, type: str):
        if type == 'old':
            return self.get_old_client()
        elif type == 'new':
            return self.get_new_client()
        else:
            raise ValueError("Invalid type. Must be 'old' or 'new'.")
