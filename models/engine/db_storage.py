#!/usr/bin/Python3
"""A module that defines DBStorage class"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review


class DBStorage:
    """A class that defines the DBStorage """
    __engine = None
    __session = None

    def __init__(self):
        """It Initialize the DBStorage"""
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, passwd, host, database),
                                      pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ It query objects from current database session"""

        object_dict = dict()
        classes = (User, State, City, Amenity, Place, Review)
        if cls is None:
            for c in classes:
                query = self.__session.query(c)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    object_dict[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                object_dict[obj_key] = obj
        return object_dict

    def new(self, obj):
        """It add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """It commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """It deeletes object from current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """It creates all tables in the database and
        create current database session
        """
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine,
                            expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()
