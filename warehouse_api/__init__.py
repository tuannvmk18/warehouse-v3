import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask_restx import Api
from sqlmodel import create_engine, SQLModel
from warehouse_api.models import *

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
debugFileHandler = logging.FileHandler('debug.log')
debugFileHandler.setFormatter(formatter)
logger.addHandler(debugFileHandler)

# Congigure dotenv
load_dotenv()

# Configure database
postgresql_url = f"{os.environ.get('DB_TYPE')}://{os.environ.get('DB_USERNAME')}:{os.environ.get('DB_PASSWORD')}@" \
                 f"{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/" \
                 f"{os.environ.get('DB_NAME')}"
engine = create_engine(url=postgresql_url)

api = Api()


def create_app() -> Flask:
    app = Flask(__name__)
    api.init_app(app)

    from warehouse_api.namespaces import product_ns, warehouse_ns

    api.add_namespace(product_ns)
    api.add_namespace(warehouse_ns)

    SQLModel.metadata.create_all(engine)
    return app
