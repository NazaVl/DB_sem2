import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, WeatherRecord, Wind, MoonPhaseEnum
from sqlalchemy.exc import OperationalError, SQLAlchemyError


DATABASE_URL = "postgresql://postgres:postgres/lab3"


def parse_datetime_safe(dt_str):
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except Exception:
        return None


def create_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine


def parse_time(value):
    try:
        return datetime.strptime(value.strip(), "%I:%M %p").time()
    except:
        return None


def parse_enum(value):
    value = value.strip()
    for e in MoonPhaseEnum:
        if e.value == value:
            return e
    return None


def record_exists(session, country, location_name, last_updated):
    return session.query(WeatherRecord).filter_by(
        country=country,
        location_name=location_name,
        last_updated=last_updated
    ).first()


def load_data(session, csv_file):
    df = pd.read_csv(csv_file, delimiter="\t", encoding="utf-8-sig")
    try:
        existing_count = session.query(func.count(WeatherRecord.id)).scalar()

        if existing_count == 0:
            print("Importing")
            df = pd.read_csv("GlobalWeatherRepository.csv")

            for _, row in df.iterrows():
                last_updated = parse_datetime_safe(row.get("last_updated"))
                if not last_updated:
                    continue

                weather = WeatherRecord(
                    country=row["country"],
                    location_name=row["location_name"],
                    latitude=float(row["latitude"]),
                    longitude=float(row["longitude"]),
                    timezone=row["timezone"],
                    last_updated=last_updated,
                    humidity=int(row["humidity"]),
                    air_quality_carbon_monoxide=float(row["air_quality_Carbon_Monoxide"]),
                    moon_phase=parse_enum(str(row["moon_phase"])),
                    sunrise=parse_time(str(row["sunrise"])),
                )

                session.add(weather)
                session.flush()

                wind = Wind(
                    wind_mph=float(row["wind_mph"]),
                    wind_kph=float(row["wind_kph"]),
                    wind_degree=int(row["wind_degree"]),
                    wind_direction=row["wind_direction"],
                    gust_mph=float(row["gust_mph"]),
                    gust_kph=float(row["gust_kph"]),
                    weather=weather
                )

                session.add(wind)

            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print("Err:", str(e))
    finally:
        session.close()


def is_database_empty(session):
    try:
        return session.query(WeatherRecord).first() is None
    except OperationalError:
        return True


def main():
    engine = create_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    if is_database_empty(session):
        load_data(session, "GlobalWeatherRepository.csv")
        print("Done")
    else:
        print("Not empty")


if __name__ == "__main__":
    main()