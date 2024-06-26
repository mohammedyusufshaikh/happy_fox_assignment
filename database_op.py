from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base



class DatabaseUtils():
    def __init__(self):
        pass

    def build_conn_obj(self, user, passwd, host, port, db_name, driver):
        self.conn_string = f"{driver}://{user}:{passwd}@{host}:{port}/{db_name}"
        self.engine = create_engine(self.conn_string, echo=True)
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session
    

    def create_tables(self):
        return Base.metadata.create_all(self.engine)

    


    

