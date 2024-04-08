from rest_framework import serializers
from .models import Person, PhoneNumber


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ["country_code", "number", "is_primary"]


class PersonSerializer(serializers.ModelSerializer):
    phone_numbers = PhoneNumberSerializer(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ["id", "name", "surname", "phone_numbers"]
