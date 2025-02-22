from django.urls import include, path

app_name = 'v1'

urlpatterns = [
    path(
        'users/',
        include('api.v1.users.urls'),
        name='users',
    ),

]
