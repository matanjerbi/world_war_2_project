from flask import session
from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey, Float, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class TargetModel(Base):
    __tablename__ = 'targets'
    target_id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey('missions.mission_id'))  # תיקון שם העמודה המקושרת
    targettype_id = Column(Integer, ForeignKey('target_type.target_type_id'))
    city_id = Column(Integer, ForeignKey('cities.city_id'))
    target_industry = Column(String)
    target_priority = Column(Integer)

    mission = relationship("Missions", back_populates="targets")
    target_type = relationship("TargetTypeModel", back_populates="targets")
    city = relationship("CitiesModel", back_populates="targets")


#build a missions model from the mission
class MissionsModel(Base):
    __tablename__ = 'missions'
    mission_id = Column(Integer, primary_key=True)
    mission_date = Column(Date)
    airborne_aircraft = Column(Numeric(10, 2))
    attacking_aircraft = Column(Numeric(10, 2))
    bombing_aircraft = Column(Numeric(10, 2))
    aircraft_returned = Column(Numeric(10, 2))
    aircraft_failed = Column(Numeric(10, 2))
    aircraft_damaged = Column(Numeric(10, 2))
    aircraft_lost = Column(Numeric(10, 2))

    targets = relationship("TargetModel", back_populates="mission")


class TargetTypeModel(Base):
    __tablename__ = 'target_type'
    target_type_id = Column(Integer, primary_key=True)
    target_type_name = Column(String)

    targets = relationship("TargetModel", back_populates="target_type")

class CitiesModel(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String)
    country_id = Column(Integer, ForeignKey('countries.country_id'))
    latitude = Column(Numeric)
    longitude = Column(Numeric)

    targets = relationship("TargetModel", back_populates="city")
    country = relationship("CountriesModel", back_populates="cities")


class CountriesModel(Base):
    __tablename__ = 'countries'
    country_id = Column(Integer, primary_key=True)
    country_name = Column(String)

    cities = relationship("CitiesModel", back_populates="country")



