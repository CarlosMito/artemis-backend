from rest_framework import serializers
from .models import Profile, Input, Output
from django.contrib.auth.models import User
import logging as log


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["user"]


class InputSerializer(serializers.ModelSerializer):
    outputs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Input
        # NOTE: Maybe change to
        # fields = "__all__"
        fields = [
            "id", "user", "prompt", "negative_prompt", "image_dimensions", "num_outputs", "num_inference_steps", "version",
            "guidance_scale", "scheduler", "seed", "style", "saturation", "value", "color_value", "replicate_id", "outputs"
        ]

    def create(self, validated_data):
        validated_data["user"] = Profile.objects.get(pk=validated_data["user"])
        return Input(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.created = validated_data.get('created', instance.created)
    #     instance.save()
    #     return instance


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = ["id", "input", "image", "is_public", "favorite_count"]


class InputWithProfileSerializer(serializers.ModelSerializer):
    # NOTE: The name should be profile
    user = ProfileSerializer()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Input
        fields = [
            "id", "user", "prompt", "negative_prompt", "image_dimensions", "num_outputs", "num_inference_steps", "version",
            "guidance_scale", "scheduler", "seed", "style", "saturation", "value", "color_value", "replicate_id", "user_id"
        ]

    def get_user_id(self, instance):
        return instance.user.user.id


class OutputWithInputSerializer(serializers.ModelSerializer):
    input = InputWithProfileSerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Output
        fields = ["id", "input", "image", "is_public", "favorite_count"]

    def get_image(self, instance):
        request = self.context.get("request")
        image = instance.image.url
        return request.build_absolute_uri(image)
