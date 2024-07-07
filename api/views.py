from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Organisation
from auth_core.serializers import UserSerializer
from .serializers import OrganisationSerializer


User = get_user_model()


class UserDetailView(APIView):
    def get(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class OrganisationViewset(viewsets.ModelViewSet):
    serializer_class = OrganisationSerializer
    queryset = Organisation.objects.all()

    def get_queryset(self):
        qs = Organisation.objects.filter(users=self.request.user)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            "status": "success",
            "message": "Organisations retrieved successfully.",
            "data": {"organisations": serializer.data},
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            "status": "success",
            "message": "Organisation retrieved successfully.",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_data = {
                "status": "success",
                "message": "Organisation created successfully.",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    "status": "Bad Request",
                    "message": "Client error",
                    "statusCode": "400",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    def users(self, request, pk=None):
        organisation = self.get_object()

        user_id = request.data.get("userId")

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        organisation.users.add(user)  # assuming there is a many-to-many relationship
        organisation.save()

        return Response(
            {"status": "success", "message": "User added to organisation successfully"},
            status=status.HTTP_200_OK,
        )
