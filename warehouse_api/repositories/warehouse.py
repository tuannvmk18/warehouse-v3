import sys

from sqlmodel import Session, select
from warehouse_api import engine
from warehouse_api.models import WareHouse


# def get_all_fulldoc():
#     with Session(engine) as session:
#         query = "SELECT "
