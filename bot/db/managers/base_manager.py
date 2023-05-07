from bot.db.managers import ClientManager, CategoryManager, ServiceManager, OwnerManager


class DbManager:
    def __init__(self):
        self.category = CategoryManager()
        self.client = ClientManager()
        self.service = ServiceManager()
        self.owner = OwnerManager()
