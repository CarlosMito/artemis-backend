import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets
from pathlib import Path

from artemis.settings import MEDIA_ROOT
from utils.image_processing import change_hue, change_saturation, change_value, argb_to_hsv
from utils.replicate_api import ReplicateAPI
from .models import Profile, Input, Output, User
from .serializers import ProfileSerializer, InputSerializer, OutputSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import logging as log

from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.db.utils import IntegrityError

from cv2 import imread, imwrite


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_csrf_token(request):
    log.debug("Get CSRF Token")
    csrf_token = get_token(request)
    return Response({"csrfToken": csrf_token}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_artemis(request):
    log.debug("Login Artemis")
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({"message": "User Logged in successfully!"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Wrong credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def logout_artemis(request):
    log.debug("Logout Artemis")
    # request.user.auth_token.delete()
    logout(request)
    return Response({"message": "User Logged out successfully!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def signup_artemis(request):
    log.debug("Signup Artemis")
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]

    # user = User.objects.create_user(username, email, password)

    try:
        user = User.objects.create_user(username, email, password)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    profile = Profile(user=user)

    user.save()
    profile.save()

    return Response({"message": "User signed up successfully!"}, status=status.HTTP_201_CREATED)

    # if user is not None:
    #     login(request, user)
    #     return Response({"message": "User Logged in successfully!"}, status=status.HTTP_200_OK)
    # else:
    #     return Response({"error": "Wrong credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the [User] elements on the system
        '''
        users = Profile.objects.all()
        serializer = ProfileSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create a new [User] to the system
        '''
        data = {
            "user": request.data.get("user")
        }

        serializer = ProfileSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InputListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, user_id):
        '''
        List all the [Input] items for given requested user
        '''
        if request.user.is_authenticated and request.user.id == user_id:
            inputs = Input.objects.filter(user_id=user_id)
            serializer = InputSerializer(inputs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unauthorized. Please, try again!"}, status=status.HTTP_403_FORBIDDEN)

    # 2. Create
    def post(self, request):
        '''
        Create the [Input] to a given user
        '''
        data = {
            "user": request.data.get("user"),
            "prompt": request.data.get("prompt"),
            "negative_prompt": request.data.get("negative_prompt"),
            "image_dimensions": request.data.get("image_dimensions"),
            "num_outputs": request.data.get("num_outputs"),
            "num_inference_steps": request.data.get("num_inference_steps"),
            "guidance_scale": request.data.get("guidance_scale"),
            "scheduler": request.data.get("scheduler"),
            "seed": request.data.get("seed"),
            "style": request.data.get("style"),
            "saturation": request.data.get("saturation"),
            "value": request.data.get("value"),
            "color_value": request.data.get("color_value")
        }

        serializer = InputSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OutputListApiView(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer

    # def list(self, request, *args, **kwargs):
    #     ids = list(map(int, request.GET.getlist('id')))
    #     outputs = Output.objects.filter(pk__in=ids) if ids else Output.objects.all()
    #     serializer = OutputSerializer(outputs, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, user_id):
        if request.user.is_authenticated and request.user.id == user_id:
            ids = list(map(int, request.GET.getlist('id')))
            outputs = Output.objects.filter(user_id=user_id, pk__in=ids)
            serializer = OutputSerializer(outputs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unauthorized. Please, try again!"}, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def text2image(request: Request) -> Response:

    if request.method == "GET":
        log.debug("[GET Method] text2image")
        # reqdict = dict(request.query_params.lists())
        # intput_ids = reqdict["id"]
        input_id = request.GET.get("input_id")
        log.debug(input_id)

        input = Input.objects.filter(pk=input_id).first()
        log.debug(input.replicate_id)

        data = ReplicateAPI.status(input.replicate_id)
        log.debug(data)

        if data is None:
            return Response({"error": "Could get status from Replicate API"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if data["percentages"] is None:
            return Response({"error": "This generation is too old to get the results or it doesn't have results"}, status=status.HTTP_410_GONE)

        if data["outputs"] is not None:
            input = Input.objects.filter(replicate_id=input.replicate_id).first()
            log.debug(f"Found input: {input}")

            for output in data["outputs"]:
                splitted = output.split(".")
                extension = splitted[-1]
                number = splitted[-2].split("-")[-1]
                filename = f"{input.replicate_id}-{number}.{extension}"
                filepath = Path(MEDIA_ROOT) / "outputs" / filename
                imagepath = f"outputs/{filename}"

                output_instance = Output.objects.filter(image=imagepath).first()

                if output_instance is not None:
                    log.debug(f"Image [{imagepath}] already on database")
                    continue

                response = requests.get(output)

                if response.status_code == 200 and input is not None:
                    log.debug(f"Saving image at {filepath}")

                    with open(filepath, "wb") as file:
                        file.write(response.content)

                    instance = Output(input=input, image=imagepath)
                    serializer = OutputSerializer(instance=instance, data={}, partial=True)

                    if serializer.is_valid():
                        instance: Output = serializer.save()
                        log.debug(f"Successfully saved image [{imagepath}] in the database")

        return Response(data, status=status.HTTP_200_OK)

    if request.method == "POST":
        log.debug("[POST Method] text2image")
        log.debug(request.data)

        data = {
            "user": request.data.get("user"),
            "prompt": request.data.get("prompt"),
            "negative_prompt": request.data.get("negative_prompt"),
            "image_dimensions": request.data.get("image_dimensions"),
            "num_outputs": request.data.get("num_outputs"),
            "num_inference_steps": request.data.get("num_inference_steps"),
            "guidance_scale": request.data.get("guidance_scale"),
            "scheduler": request.data.get("scheduler"),
            "seed": request.data.get("seed"),
            "style": request.data.get("style"),
            "saturation": request.data.get("saturation"),
            "value": request.data.get("value"),
            "color_value": request.data.get("color_value"),
            "version": request.data.get("version"),
            "replicate_id": request.data.get("replicate_id")
        }

        log.debug(data)

        serializer = InputSerializer(data=data)

        if serializer.is_valid():
            instance = serializer.create(serializer.data)
            log.debug(repr(instance))

            updates = ReplicateAPI.text2image(instance)

            if updates is not None:
                serializer = InputSerializer(instance, data=updates, partial=True)

                if serializer.is_valid():
                    serializer.save()

                    data = {
                        "id": serializer.instance.id,
                        "replicate_id": serializer.instance.replicate_id
                    }

                    return Response(data, status=status.HTTP_201_CREATED)

            return Response({}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def post_processing(request: Request) -> Response:
    log.debug("[POST Method] post_processing")
    log.debug(request.data)

    input_id = request.data.get("input_id")
    log.debug(input_id)

    input = Input.objects.filter(pk=input_id).first()
    outputs = Output.objects.filter(input_id=input_id)

    if input is None:
        return Response({"error": "Couldn't find the given input"}, status=status.HTTP_400_BAD_REQUEST)

    if not outputs:
        return Response({"error": "Couldn't find any output for the given input"}, status=status.HTTP_400_BAD_REQUEST)

    log.debug(f"Color Value: {input.color_value}")
    log.debug(f"Saturation: {input.saturation}")
    log.debug(f"Value: {input.value}")

    needs_post_processing = input.saturation != "random" or input.value != "random" or input.color_value != 0
    log.debug(f"Needs Post Processing: {needs_post_processing}")

    if needs_post_processing:

        scales = {
            "high": 1.5,
            "low": 0.5,
        }

        for output in outputs:

            if output.processed == True:
                log.debug(f"This output has already been processed {output.image}")
                continue

            filepath = str(Path(MEDIA_ROOT) / str(output.image))
            image = imread(filepath)
            log.debug(output.image)

            if image is None:
                log.debug(f"Couldn't read image from path {filepath}")
                continue

            if input.saturation != "random":
                scale = scales[str(input.saturation)]
                image = change_saturation(image, scale)

            if input.value != "random":
                scale = scales[str(input.value)]
                image = change_value(image, scale)

            if input.color_value != 0:
                hsv = argb_to_hsv(input.color_value)
                hue = int(hsv[0] * 255)
                image = change_hue(image, hue)

            imwrite(filepath, image)

            output.processed = True
            output.save()

    return Response({"message": "Post processing applied successfully!"}, status=status.HTTP_201_CREATED)


# image = cv2.imread(image_path)
# assert image is not None, f"Couldn't load image at {image_path}"
# cv2.imwrite(processed_path, result)
# # TODO: Maybe put the post-processing functions here
# instance.processed = True
# instance.save()
