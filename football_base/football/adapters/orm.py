
from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, MetaData, Table, Text
from sqlalchemy.orm import mapper, relationship
from weather_station_service.station.domain.entities import Evapotranspiration, FarmGOWeatherStation, FarmGOWeatherStationRecord

metadata = MetaData()

station_table = Table(
    "station",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("station_id", Text, nullable=False, unique=True),
    Column("station_name", Text),
    Column("key", Text, nullable=False),
    Column("active", Boolean),
)

record_table = Table(
    "record",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("weather_station_id", Integer, ForeignKey("station.id")),
    Column("utc_date", DateTime, nullable=False),
    Column("temperature", Float),
    Column("dew_point", Float),
    Column("pressure", Float),
    Column("wind_speed", Float),
    Column("wind_gust", Float),
    Column("wind_direction", Float),
    Column("rain", Float),
    Column("light", Integer),
    Column("solar_radiation", Float),
    Column("soil_temperature", Float),
    Column("soil_moisture", Integer),
    Column("uv", Integer),
    Column("humidity", Integer),
    Column("altitude", Float),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("battery_level", Integer),
    Column("software_type", Text),
    Column("cpu_temperature", Integer),
    Column("signal_intensity", Integer),
    Column("full_network_name", Text),
    Column("short_network_name", Text),
    Column("alphabet", Integer),
    Column("provider_name", Text),
    Column("plmn", Text),
    Column("memory_records", Integer),
    Column("uptime", Integer),
)

evapotranspiration_table = Table(
    "evapotranspiration",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("weather_station_id", Integer, ForeignKey("station.id")),
    Column("day", Date, nullable=False),
    Column("eto", Float),
)

def start_mappers():
    mapper(
        FarmGOWeatherStation, 
        station_table, 
        properties={
            "records": relationship(FarmGOWeatherStationRecord, backref="station", lazy="noload", cascade="all,delete")
        })
    mapper(
        FarmGOWeatherStationRecord, 
        record_table,
    )
    mapper(
        Evapotranspiration,
        evapotranspiration_table,
    )