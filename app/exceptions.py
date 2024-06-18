def register_handlers(app):
    class APIError(Exception):
        """Custom API Exceptions"""
        pass

