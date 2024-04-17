from django.urls import path, include
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
    path('delete_requests/', views.deleteWorkRequests, name='delete-requests'),
    # Forms (CRUD)
    path('workrequest/create_request/', views.createWorkRequests, name='create-requests'),
    path('workrequest/update_request/<int:request_id>', views.updateWorkRequests, name='update-request'),
    path('workrequest/close_request/<int:request_id>', views.closeWorkRequest, name='close-request'),

    # User Auth Stuff
    path('accounts/', include('django.contrib.auth.urls')),  # this will include the login, logout, password_change_(reset/done)
    path('accounts/register', views.registerPage, name='register_page'),
]