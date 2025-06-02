import functools

from drf_spectacular.utils import extend_schema, OpenApiResponse, PolymorphicProxySerializer, OpenApiExample
from api.serializers import SearchParametersSerializer, SearchBodySerializer, UserSerializer, \
    RepositorySerializer

def extend_schema_and_attach(**extend_schema_kwargs):
    @functools.wraps(extend_schema_and_attach)
    def decorator(func):
        func = extend_schema(**extend_schema_kwargs)(func)

        request = extend_schema_kwargs.get('request')
        parameters = extend_schema_kwargs.get('parameters')

        if request is not None:
            setattr(func, "_body_ser", request)
        if parameters is not None:
            setattr(func, "_query_ser", parameters)
        return func

    return decorator

search_extend_schema = extend_schema_and_attach(
    tags=['Search'],
    parameters=[SearchParametersSerializer],
    request=SearchBodySerializer(many=True),
    responses={
        200: OpenApiResponse(
            description="List of Users or Repositories",
            response=PolymorphicProxySerializer(
                component_name="SearchResultList",
                serializers=[
                    UserSerializer,
                    RepositorySerializer,
                ],
                resource_type_field_name=None,
                many=True,
            ),
            examples=[
                OpenApiExample(
                    name="Users list",
                    value=[
                        {
                            "id": 0,
                            "title": "string",
                            "avatar_url": "string",
                            "location": "string"
                        },
                    ],
                ),
                OpenApiExample(
                    name="Repositories list",
                    value=[
                        {
                            "id": 0,
                            "title": "string",
                            "owner": "string",
                            "stars": "string",
                            "description": "string",
                            "url": "string"
                        }
                    ],
                )
            ]
        ),
    },
)