from django.urls import path
from . import views

#path function defines a url pattern
#'' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.
urlpatterns = [
    path('', views.index, name='index'),
    # View for models
    path('workrequests/', views.WorkRequestListView.as_view(), name='workrequests'),
    path('workrequest/<int:pk>', views.WorkRequestDetailView.as_view(), name='workrequest-detail'),
    # forgot password
    path('forgotpassword/', views.forgotPassword, name='forgot-password'),
    path('delete_requests/', views.deleteWorkRequests, name='delete-requests')
]