from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework.routers import DefaultRouter

import nyaural_nyatworks.views
from nyaural_nyatworks import settings
from nyaural_nyatworks.views import *

api_router = DefaultRouter()
api_router.register('reports', ReportViewSet)

handler404 = nyaural_nyatworks.views.handler404

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('reports/', ReportListView.as_view(), name='reports'),
    path('reports/<str:title>/', ReportDetailView.as_view(), name='report'),
    path('predict/', PredictView.as_view(), name='predict'),
    path('results/', PredictResultsView.as_view(), name='results'),


    path('api/', include(api_router.urls)),
    path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

