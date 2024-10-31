import graphene
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
    missions_by_target_industry = graphene.List(MissionsType, target_industry_id=graphene.Int(required=True))


    def resolve_mission_by_id(self, info, id):
        return db_session.query(MissionsModel).get(id)

    def resolve_missions_by_date_range(self, info, start_date, end_date):
        return db_session.query(MissionsModel).filter(MissionsModel.mission_date >= start_date, MissionsModel.mission_date <= end_date).all()

    def resolve_missions_by_country(self, info, country_id):
        return db_session.query(MissionsModel).filter(MissionsModel.country_id == country_id).all()

    def resolve_missions_by_target_industry(self, info, target_industry_id):
        return db_session.query(MissionsModel).filter(MissionsModel.target_industry_id == target_industry_id).all()




schema = graphene.Schema(query=Query)