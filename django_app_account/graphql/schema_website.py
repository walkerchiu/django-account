import graphene

from django_app_account.graphql.website.profile import ProfileMutation, ProfileQuery
from django_app_account.graphql.website.user import UserMutation, UserQuery


class Mutation(
    ProfileMutation,
    UserMutation,
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
