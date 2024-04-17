#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A class the defines a place """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)
    reviews = relationship("Review", backref="place", cascade="delete")

    @property
    def reviews(self):
        """Getter attribute reviews that returns the list of Review instances
        with place_id equals to the current Place.id
        """
        from models import storage
        rev_list = []
        amentiy_lists = storage.all('Review').values()
        for rev in amentiy_lists:
            if self.id == rev.place_id:
                rev_list.append(rev)
        return rev_list

    @property
    def amenities(self):
        """Getter attribute that returns the list of Amenity instances."""
        from models import storage
        lists = []
        amenities_lists = storage.all('Amenity').values()
        for amenity in amenities_lists:
            if self.id == amenity.amenity_ids:
                lists.append(amenity)
        return lists

    @amenities.setter
    def amenities(self, obj):
        """Setter attribute that handles appending Amenity instances."""
        if isinstance(obj, Amenity):
            self.amenity_id.append(obj.id)
