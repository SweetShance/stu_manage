from django.urls import path
from .views import Merge, Anomaly, Replenish, Message_edit, Stu_data_list
app_name = 'stu_table'
urlpatterns = [
    path('merge', Merge.as_view(), name="merge"),
    path('anomaly', Anomaly.as_view(), name="anomaly" ),
    path('replenish', Replenish.as_view(), name="replenish"),
    path('edit', Message_edit.as_view(), name='edit'),
    path('data_list', Stu_data_list.as_view(), name="stu_data_list")
]