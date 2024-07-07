from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrganisationViewset, UserDetailView

routers = DefaultRouter()
routers.register("organisations", OrganisationViewset, basename="organisations")


urlpatterns = [
    path("", include(routers.urls)),
    path("users/<str:pk>/", UserDetailView.as_view()),
]
