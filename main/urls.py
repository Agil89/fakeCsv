from django.urls import path
from .views import HomePage,CustomLoginView,CreateCsvView,DownloadView,TypeList,SchemaDeleteView,SchemaUpdateView
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('main/', HomePage.as_view(), name='home'),
    path('',CustomLoginView.as_view(),name='login'),
    path('create/',CreateCsvView.as_view(),name='create'),
    path('download/',DownloadView.as_view(),name='download'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('types/',TypeList.as_view(),name='types'),
    path('deleteSchema/<int:pk>/',SchemaDeleteView.as_view(),name='delete'),
    path('update/<int:pk>/',SchemaUpdateView.as_view(),name='update'),
]