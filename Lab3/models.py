from sqlalchemy import (
    Column, Integer, Float, String, DateTime, Time, Enum, ForeignKey, create_engine, Boolean
)
from sqlalchemy.orm import DeclarativeBase, relationship
import enum


class Base(DeclarativeBase):
    pass


class MoonPhaseEnum(enum.Enum):
    New = "New Moon"
    Waxing_Crescent = "Waxing Crescent"
    First_Quarter = "First Quarter"
    Waxing_Gibbous = "Waxing Gibbous"
    Full = "Full Moon"
    Waning_Gibbous = "Waning Gibbous"
    Last_Quarter = "Last Quarter"
    Waning_Crescent = "Waning Crescent"


class WeatherRecord(Base):
    __tablename__ = "weather_record"

    id = Column(Integer, primary_key=True)
    country = Column(String)
    location_name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String)
    last_updated = Column(DateTime)
    humidity = Column(Integer)
    air_quality_carbon_monoxide = Column(Float)
    moon_phase = Column(Enum(MoonPhaseEnum))
    sunrise = Column(Time)

    wind = relationship("Wind", back_populates="weather", uselist=False)


class Wind(Base):
    __tablename__ = "wind"

    id = Column(Integer, primary_key=True)
    weather_id = Column(Integer, ForeignKey('weather_record.id'), unique=True)
    wind_mph = Column(Float)
    wind_kph = Column(Float)
    wind_degree = Column(Integer)
    wind_direction = Column(String)
    gust_mph = Column(Float)
    gust_kph = Column(Float)
    is_good_for_walk = Column(Boolean)
    
    weather = relationship("WeatherRecord", back_populates="wind")
