from django.urls import path
# from .views import Welcome
from .views import Error
app_name = 'myUtils'
urlpatterns = [
    path('', Error.as_view(), name='error')
]