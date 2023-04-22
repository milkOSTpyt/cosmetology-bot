import json

from utils import config


class FileManager:
    def __init__(self):
        self.data_dict = self.__get_dict()

    @staticmethod
    def __get_dict():
        with open(config.FILE, 'r', encoding='utf-8') as file:
            return json.load(file)

    async def get_description(self):
        return self.data_dict.get('description')

    async def get_categories(self):
        return self.data_dict.get('services').keys()

    async def get_services_of_category(self, category: str):
        services = self.data_dict['services'].get(category)
        return list(service['title'] for service in services)

    async def get_data_on_service(self, category: str, service: str):
        services_of_category = self.data_dict['services'][category]
        for item in services_of_category:
            if item.get('title') == service:
                return item
