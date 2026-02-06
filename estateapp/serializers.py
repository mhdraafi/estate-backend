from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Property, Register,ContactMessage,Enquiry,Cart


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = "__all__"

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class PropertySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Property
        fields = "__all__"


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'



class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(
        source="property.title", read_only=True
    )
    property_price = serializers.IntegerField(
        source="property.price", read_only=True
    )
    property_image = serializers.ImageField(
        source="property.image", read_only=True
    )
    property_location = serializers.CharField(
        source="property.location", read_only=True
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "property",
            "property_title",
            "property_price",
            "property_image",
            "property_location",
            "created_at",
        ]
