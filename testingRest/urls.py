from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', obtain_jwt_token, name='api-login'),
    path('api/postings/', include('postings.api.urls', namespace='api-postings'))
]
