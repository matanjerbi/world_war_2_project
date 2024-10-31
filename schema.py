from datetime import datetime
import graphene
from flask import session
from graphene_sqlalchemy import SQLAlchemyObjectType

from database import db_session
from models import TargetModel, TargetTypeModel, MissionsModel, CitiesModel, CountriesModel


class Target(SQLAlchemyObjectType):
    class Meta:
        model = TargetModel
        interfaces = (graphene.relay.Node,)


class TargetType(SQLAlchemyObjectType):
    class Meta:
        model = TargetTypeModel
        interfaces = (graphene.relay.Node,)

class MissionsType(SQLAlchemyObjectType):
    class Meta:
        model = MissionsModel
        interfaces = (graphene.relay.Node,)


class CitiesType(SQLAlchemyObjectType):
    class Meta:
        model = CitiesModel
        interfaces = (graphene.relay.Node,)


class CountrieType(SQLAlchemyObjectType):
    class Meta:
        model = CountriesModel
        interfaces = (graphene.relay.Node,)



class Query(graphene.ObjectType):
    #find mission by id
    mission_by_id = graphene.Field(MissionsType, id=graphene.Int(required=True))
    #find mission by range dates
    missions_by_date_range = graphene.List(MissionsType, start_date=graphene.String(required=True), end_date=graphene.String(required=True))
    #find mission by country
    missions_by_country = graphene.List(MissionsType, country_id=graphene.Int(required=True))
    #find mission by target industry
    missions_by_target_industry = graphene.List(MissionsType, target_industry=graphene.String(required=True))
    #Finding results of an attack by type of attack
    missions_by_target_type_id = graphene.List(MissionsType, target_type_id=graphene.Int(required=True))





    def resolve_mission_by_id(self, info, id):
        return db_session.query(MissionsModel).get(id)

    def resolve_missions_by_date_range(self, info, start_date, end_date):
        session = db_session()
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()

        return (
            session.query(MissionsModel)
            .filter(MissionsModel.mission_date >= start)
            .filter(MissionsModel.mission_date <= end)
            .all()
        )



    def resolve_missions_by_country(self, info, country_id):
        session = db_session()
        return (
            session.query(MissionsModel)
            .join(MissionsModel.targets)
            .join(TargetModel.city)
            .join(CitiesModel.country)
            .filter(CountriesModel.country_id == country_id)
            .all()
        )

    def resolve_missions_by_target_industry(self, info, target_industry):
        session = db_session()
        return (
            session.query(MissionsModel)
            .join(MissionsModel.targets)
            .filter(TargetModel.target_industry == target_industry)
            .all()
        )

    def resolve_missions_by_target_type_id(self, info, target_type_id):
        session = db_session()
        return session.query((MissionsModel.aircraft_returned,
                              MissionsModel.aircraft_failed,
                              MissionsModel.aircraft_damaged)
                             .join(TargetModel).filter(TargetModel.targettype_id == target_type_id)).all()

class Mutation(graphene.ObjectType):
    create_mission = graphene.Field(MissionsType, target_type_id=graphene.Int(required=True), city_id=graphene.Int(required=True), target_industry=graphene.String(required=True))
    create_target = graphene.Field(TargetType, )


    def resolve_create_mission(self, info, target_type_id, city_id, target_industry):
        mission = MissionsModel(target_type_id=target_type_id, city_id=city_id, target_industry=target_industry)
        db_session.add(mission)
        db_session.commit()
        return mission






#

schema = graphene.Schema(query=Query)