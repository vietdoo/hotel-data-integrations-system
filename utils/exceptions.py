class NormalizerException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class MergerException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class HotelServiceException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class DBException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class CleanerException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class BiasException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    