
from sqlalchemy import (
    Boolean, 
    Column, 
    Date, 
    DateTime, 
    Float, 
    ForeignKey, 
    Integer, 
    MetaData, 
    Table, 
    Text,
)
from sqlalchemy.orm import mapper, relationship
from football_base.football.domain.entities import League

metadata: MetaData = MetaData()

league_table: Table = Table(
    "leagues",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", Text, nullable=False),
    Column("season", Text, nullable=False),
    Column("details", Text),
    Column("country", Text, nullable=False),
)



def start_mappers() -> None:
    mapper(
        League, 
        league_table, 
        # properties={
        #     "records": relationship(FarmGOWeatherStationRecord, backref="station", lazy="noload", cascade="all,delete")
        # }
    )
    # mapper(
    #     FarmGOWeatherStationRecord, 
    #     record_table,
    # )
    # mapper(
    #     Evapotranspiration,
    #     evapotranspiration_table,
    # )