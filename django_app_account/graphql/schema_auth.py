import graphene

from django_app_account.graphql.auth.user import UserMutation


class Mutation(
    UserMutation,
    graphene.ObjectType,
):
    pass


class Query(
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
