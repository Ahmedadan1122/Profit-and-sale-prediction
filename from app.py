from app.database import Base, engine
from app import schemas

Base.metadata.create_all(bind=engine)