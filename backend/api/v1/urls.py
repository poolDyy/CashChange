from django.urls import include, path


app_name = 'v1'

urlpatterns = [
    path(
        'users/',
        include('api.v1.users.urls'),
        name='users',
    ),
    path(
        'telegram/',
        include('api.v1.telegram.urls'),
        name='telegram',
    ),
    path(
        'offers/',
        include('api.v1.offers.urls'),
        name='offers',
    ),
    path(
        'feedback/',
        include('api.v1.feedback.urls', namespace='feedback'),
        name='feedback',
    ),
]
