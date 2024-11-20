from utils.logger import logger

class HotelAPI:
    def __init__(self):
        self.decorators = {}
        self.routes = {}

    def __call__(self, route):
        def wrapper(func):
            self.decorators[func.__name__] = (route, func)
            self.routes[func.__name__] = (route, func)
            return func
        return wrapper

    def route(self, name, *args, **kwargs):
        def decorator(func):
            if name in self.decorators:
                route, original_func = self.decorators[name]
                return original_func(func, *args, **kwargs)
            raise ValueError(f"Decorator '{name}' not registered.")
        return decorator

    def __getattr__(self, item):
        if item in self.routes:
            route, func = self.routes[item]

            def wrapped_function(*args, **kwargs):
                logger.log(f"Calling route '{route}' with function '{func.__name__}'.", "info")
                return func(*args, **kwargs)
            return wrapped_function
        raise AttributeError(f"'HotelAPI' object has no attribute '{item}'")
