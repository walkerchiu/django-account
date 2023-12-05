import graphene

from django_app_account.graphql.hq.profile import ProfileMutation, ProfileQuery
from django_app_account.graphql.hq.user import UserQuery


class Mutation(
    ProfileMutation,
    graphene.ObjectType,
):
    pass


class Query(
    ProfileQuery,
    UserQuery,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
