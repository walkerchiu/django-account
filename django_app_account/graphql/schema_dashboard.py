import graphene

from django_app_account.graphql.dashboard.profile import ProfileMutation, ProfileQuery
from django_app_account.graphql.dashboard.user import UserQuery


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
