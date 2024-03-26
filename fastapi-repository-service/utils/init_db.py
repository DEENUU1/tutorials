from config.database import Base, engine
from models.region import Region
from models.city import City


def create_tables():
    """
    Creates all database tables defined in the application.
    """
    Region.metadata.create_all(bind=engine)
    City.metadata.create_all(bind=engine)
