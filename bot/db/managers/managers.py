from typing import Optional

from asgiref.sync import sync_to_async

from admin.cosmetology.models import Category, Service, Client, Owner


class CategoryManager:
    @staticmethod
    @sync_to_async
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    @sync_to_async
    def get_category_by_id(category_id):
        category = Category.objects.get(pk=category_id)
        return category


class ServiceManager:
    @staticmethod
    @sync_to_async
    def update_discount(service_id):
        service = Service.objects.get(pk=service_id)
        if service.is_active:
            service.is_active = False
        else:
            service.is_active = True
        service.save()
        return service

    @staticmethod
    @sync_to_async
    def get_all_services():
        return Service.objects.all()

    @staticmethod
    @sync_to_async
    def get_all_active_services():
        return Service.objects.filter(is_active=True)

    @staticmethod
    @sync_to_async
    def get_service_by_id(service_id):
        return Service.objects.get(pk=service_id)

    @staticmethod
    @sync_to_async
    def get_services_by_category(category_id):
        return Service.objects.filter(category_id=category_id)

    @staticmethod
    @sync_to_async
    def get_active_services_by_category(category_id):
        return Service.objects.filter(category_id=category_id, is_active=True, is_discount=False)

    @staticmethod
    @sync_to_async
    def get_active_services_by_discount():
        return Service.objects.filter(is_active=True, is_discount=True)

    @staticmethod
    @sync_to_async
    def get_all_services_by_discount():
        return Service.objects.filter(is_discount=True)


class ClientManager:
    @staticmethod
    @sync_to_async
    def update_or_create(telegram_id, name, telegram_username=None,
                         phone_number=None) -> Optional[Client]:
        obj, created = Client.objects.update_or_create(
            telegram_id=telegram_id,
            defaults={
                "telegram_id": telegram_id,
                "name": name,
                "telegram_username": telegram_username,
                "phone_number": phone_number
            }
        )
        return obj

    @staticmethod
    @sync_to_async
    def get_all_clients():
        return Client.objects.all()

    @staticmethod
    @sync_to_async
    def get_client_by_id(telegram_id):
        return Client.objects.get(telegram_id=telegram_id)


class OwnerManager:
    @staticmethod
    @sync_to_async
    def get_owner():
        return Owner.objects.all().first()
