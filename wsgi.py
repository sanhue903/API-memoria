from app import create_app
from config import ProductionConfig

if __name__ == '__main__':
    app = create_app(ProductionConfig)
    app.run()