from django.urls import path
# from .views import Welcome
from .views import Error, Delete_data, Alert_stu_data, GetClass, GetColleges, AddStu, AddField, ImportDataToexcel, Search, ShareGetClass, CombinedExcel
app_name = 'myUtils'
urlpatterns = [
    path('', Error.as_view(), name='error'),
    path('/delete_stu_data', Delete_data.as_view(), name="delete_stu_data" ),
    path('/alter', Alert_stu_data.as_view(), name="alter"),
    path('/getClass', GetClass.as_view(), name="getClass"),
    path('/getcolleges', GetColleges.as_view(), name='getcolleges'),
    path('/addstu', AddStu.as_view(), name="addstu"),
    path('/addfield', AddField.as_view(), name="addfield"),
    path('/search', Search.as_view(), name='serch'),
    path('/sharegetclass', ShareGetClass.as_view(), name="sharegetclass"),
    path('/combined', CombinedExcel.as_view(), name="combined"),
    path('/import', ImportDataToexcel.as_view(), name='import')
]