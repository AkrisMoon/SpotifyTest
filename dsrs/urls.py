from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'dsrs', views.DSRViewSet)
router.register(r'dsrs/<id>', views.DSR_IDViewSet, basename = "dsrs_id")
# router.register(r'resources/percentile/<number>', views.RecordingPercentileViewSet, basename = "resources_percentile")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('resources/percentile/<int:number>/', views.RecordingPercentileViewSet.as_view(), name='resources_percentile'),

]