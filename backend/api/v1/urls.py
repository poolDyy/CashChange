from django.urls import include, path


app_name = 'v1'

urlpatterns = [
    path(
        'users/',
        include('api.v1.users.urls', namespace='users'),
        name='users',
    ),
    path(
        'telegram/',
        include('api.v1.telegram.urls', namespace='telegram'),
        name='telegram',
    ),
    path(
        'offers/',
        include('api.v1.offers.urls', namespace='offers'),
        name='offers',
    ),
    path(
        'feedback/',
        include('api.v1.feedback.urls', namespace='feedback'),
        name='feedback',
    ),
    path(
        'centrifugo/',
        include('api.v1.centrifugo.urls', namespace='centrifugo'),
        name='centrifugo',
    ),
    path(
        'chat/',
        include('api.v1.chat.urls', namespace='chat'),
        name='chat',
    ),
]
