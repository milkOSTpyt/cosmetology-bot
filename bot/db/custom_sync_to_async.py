from asgiref.sync import SyncToAsync
from django.db import close_old_connections
from loguru import logger


class CustomSyncToAsync(SyncToAsync):
    """
    SyncToAsync version that cleans up old database connections when it exits.
    """

    def thread_handler(self, loop, *args, **kwargs):
        close_old_connections()
        try:
            return super().thread_handler(loop, *args, **kwargs)
        except Exception as error:
            logger.success(f'{error}')
        finally:
            close_old_connections()
