from rest_framework import serializers
from .models import LipsModel , LooksModel , ColorsPallete ,  EyesModel,FaceModel



class ColorsPalleteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = ColorsPallete
        


class LooksSerializer(serializers.ModelSerializer):
    colors = ColorsPalleteSerializer(read_only=True, many=True)
    class Meta:
        fields = "__all__"
        model = LooksModel




class FaceSerializer(serializers.ModelSerializer):
    colors = ColorsPalleteSerializer(read_only=True, many=True)
    class Meta:
        fields = "__all__"
        model = FaceModel


class EyesSerializer(serializers.ModelSerializer):
    colors = ColorsPalleteSerializer(read_only=True, many=True)
    class Meta:
        fields = "__all__"
        model = EyesModel



class LipsSerializer(serializers.ModelSerializer):
    colors = ColorsPalleteSerializer(read_only=True, many=True)
    class Meta:
        fields = "__all__"
        model = LipsModel