from managers import Manager


def create_manager(func):
    def wrapper(*args, **kwargs):
        manager = Manager()
        return_value = func(*args, manager=manager, **kwargs)
        return return_value
    return wrapper()
