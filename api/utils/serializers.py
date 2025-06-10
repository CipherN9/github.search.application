from rest_framework import serializers


def _snake_to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


class CamelCaseSerializerMixin(serializers.Serializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {_snake_to_camel(key): value for key, value in data.items()}
