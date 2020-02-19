import datetime

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):    
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True)    
    first_name = sa.Column(sa.Text)    
    last_name = sa.Column(sa.Text)    
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


class Athelete(Base):    
    __tablename__ = "athelete"    
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)    
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)    
    country = sa.Column(sa.Text) 

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def find(user_id, session):    
    query = session.query(User).filter(User.id == user_id)    
    users_cnt = query.count()
    if users_cnt:
        user = query.first()        
        birthdate = datetime.datetime.strptime(user.birthdate, "%Y-%m-%d").date()        
        query = session.query(Athelete.id, Athelete.birthdate, Athelete.height)
        # Распаковывает query на три списка
        lists = list(zip(*query.all()))
        ids = lists[0]
        birthdates = list(map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date(), lists[1]))                         
        heights = lists[2]
        # Ищет индексы ближайших по дате и росту
        closest_birthdate_id = ids[min(enumerate(birthdates), key=lambda x: abs(x[1] - birthdate))[0]]
        closest_height_id = ids[min(enumerate(heights), key=lambda x: abs(x[1] - user.height) if x[1] is not None else float("inf"))[0]]
        # Получает результаты по индексу
        closest_birthdate = session.query(Athelete).filter(Athelete.id == closest_birthdate_id).first()
        closest_height = session.query(Athelete).filter(Athelete.id == closest_height_id).first()
        print("Атлет с ближайшей датой рождения к {}: {} - {}".format(birthdate, closest_birthdate.name, closest_birthdate.birthdate))
        print("Ближайший по росту к {} атлет: {} - {}".format(user.height, closest_height.name, closest_height.height))
    else:
        print("Пользователь не найден.")

if __name__ == "__main__":
    session = connect_db()      
    user_id = input("Введи id пользователя для поиска: ")
    find(user_id, session) 