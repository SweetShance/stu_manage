from django.urls import path
from .views import Merge, Anomaly, Replenish, Message_edit
app_name = 'stu_table'
urlpatterns = [
    path('merge', Merge.as_view(), name="merge"),
    path('anomaly', Anomaly.as_view(), name="anomaly" ),
    path('replenish', Replenish.as_view(), name="replenish"),
    path('edit', Message_edit.as_view(), name='edit')
]