from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    PolymorphicProxySerializer,
    extend_schema,
)

from api.serializers import (
    RepositorySerializer,
    SearchBodySerializer,
    SearchParametersSerializer,
    UserSerializer,
)

search_extend_schema = extend_schema(
    tags=["Search"],
    parameters=[SearchParametersSerializer],
    request=SearchBodySerializer,
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
                            "location": "string",
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
                            "url": "string",
                        }
                    ],
                ),
            ],
        ),
    },
)
