from rest_framework import serializers
from .models import Movies, LanguageEnum, GenreEnum

class EnumField(serializers.ChoiceField):
    def __init__(self, enum, **kwargs):
        self.enum = enum
        choices = [(e.name, e.value) for e in enum]
        super().__init__(choices, **kwargs)

    def to_representation(self, obj):
        return obj.value if obj else None

    def to_internal_value(self, data):
        try:
            return self.enum[data]
        except KeyError:
            self.fail('invalid_choice', input=data)

class MovieSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    language = EnumField(enum=LanguageEnum, required=True)
    genre = EnumField(enum=GenreEnum, required=True)
    poster = serializers.ImageField(required=True)  # Changed to ImageField
    release_date = serializers.DateField(required=True)

    def create(self, validated_data):
        return Movies(**validated_data).save()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MovieUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ["title",'description', 'language', 'genre', 'poster', 'release_date']
        
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['id', 'title', 'language', 'genre', 'release_date']
        
class MovieDetailSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    language = EnumField(enum=LanguageEnum)
    genre = EnumField(enum=GenreEnum)
    poster = serializers.ImageField()
    release_date = serializers.DateField()

class MovieSearchSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField(max_length=200)
    language = serializers.ChoiceField(choices=[(lang.value, lang.name) for lang in LanguageEnum])
    genre = serializers.ChoiceField(choices=[(genre.value, genre.name) for genre in GenreEnum])

    def validate(self, data):
        # Add any custom validation logic here
        return data