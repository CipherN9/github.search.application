from rest_framework import serializers

from api.utils.enums import SearchType


class SearchParametersSerializer(serializers.Serializer):
    search_type = serializers.ChoiceField(
        choices=SearchType.choices,
        help_text="Search type",
    )

    @staticmethod
    def validate_search_type(value: str) -> SearchType:
        return SearchType(value)


class SearchBodySerializer(serializers.Serializer):
    search_text = serializers.CharField()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    avatar_url = serializers.URLField()
    location = serializers.CharField(allow_null=True)


class RepositorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    owner = serializers.CharField()
    stars = serializers.IntegerField()
    description = serializers.CharField(allow_null=True)
    url = serializers.URLField()
