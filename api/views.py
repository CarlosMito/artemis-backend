from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets

from artemis.settings import REPLICATE_API_TOKEN
from utils.replicate_api import ReplicateAPI
from .models import Profile, Input, Output
from .serializers import ProfileSerializer, InputSerializer, OutputSerializer
from rest_framework.decorators import api_view, permission_classes
import logging as log


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
    def get(self, request, *args, **kwargs):
        '''
        List all the [Input] items for given requested user
        '''
        # TODO: Should I use the default User Django API Framework entity?
        inputs = Input.objects.filter(user=request.user.id)
        serializer = InputSerializer(inputs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
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
            "color": request.data.get("color")
        }

        serializer = InputSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OutputListApiView(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer

    def list(self, request, *args, **kwargs):
        ids = list(map(int, request.GET.getlist('id')))
        outputs = Output.objects.filter(pk__in=ids) if ids else Output.objects.all()
        serializer = OutputSerializer(outputs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes((permissions.AllowAny,))
def text2image(request: Request) -> Response:

    if request.method == "GET":
        log.debug("[GET Method] text2image")
        reqdict = dict(request.query_params.lists())
        id_list = reqdict["id"]
        log.debug(id_list)

        response = ReplicateAPI.status(id_list)

        print(response)

        if response.status_code == 200:
            return Response({"message": "Hello, world!"})

        return response

    if request.method == "POST":
        log.debug("[POST Method] text2image")
        data = {
            "user": request.data.get("user"),
            "prompt": request.data.get("prompt"),
            "negative_prompt": request.data.get("negativePrompt"),
            "image_dimensions": request.data.get("imageDimensions"),
            "num_outputs": request.data.get("numOutputs"),
            "num_inference_steps": request.data.get("numInferenceSteps"),
            "guidance_scale": request.data.get("guidanceScale"),
            "scheduler": request.data.get("scheduler"),
            "seed": request.data.get("seed"),
            "style": request.data.get("style"),
            "saturation": request.data.get("saturation"),
            "value": request.data.get("value"),
            "color": request.data.get("color"),
            "version": request.data.get("version"),
            "replicate_id": request.data.get("replicateId")
        }

        log.debug(data)

        serializer = InputSerializer(data=data)

        if serializer.is_valid():
            # serializer.save()

            instance = serializer.create(serializer.data)
            log.debug(repr(instance))

            response = ReplicateAPI.text2image(instance)

            if response != None:
                return Response({}, status=status.HTTP_201_CREATED)

            return Response({}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)
