from rest_framework import serializers

class ImageUnAutheticatedSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   image = serializers.ImageField()
   