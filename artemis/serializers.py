# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import User, Input, Output


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]


class InputSerializer(serializers.ModelSerializer):
    outputs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Input
        # NOTE: Maybe change to
        # fields = "__all__"
        fields = [
            "id", "user", "prompt", "negative_prompt", "image_dimensions", "num_outputs", "num_inference_steps",
            "guidance_scale", "scheduler", "seed", "style", "saturation", "value", "color", "replicate_id", "outputs"
        ]

        # fields = [
        #     "user"
        # ]


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = ["id", "input", "image", "is_public", "favorite_count"]
