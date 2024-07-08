from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrganisationViewset, UserDetailView

routers = DefaultRouter(trailing_slash=False)
routers.register("organisations", OrganisationViewset, basename="organisations")


urlpatterns = [
    path("users/<str:pk>", UserDetailView.as_view()),
    path("", include(routers.urls)),
]
