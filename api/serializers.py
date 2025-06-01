from rest_framework import serializers

from api.enums import SearchType


class SearchParametersSerializer(serializers.Serializer):
    search_type = serializers.ChoiceField(
        choices=SearchType.choices,
        help_text='Search type',
    )

    @staticmethod
    def validate_search_type(value: str) -> SearchType:
        return SearchType(value)


class SearchBodySerializer(serializers.Serializer):
    search_text = serializers.CharField()


class SearchSerializer(SearchParametersSerializer, SearchBodySerializer):
    pass


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    avatar_url = serializers.CharField()
    location = serializers.CharField(allow_null=True)


class RepositorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    owner = serializers.CharField()
    stars = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    url = serializers.CharField()

