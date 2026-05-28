from django.urls import path, include

urlpatterns = [

    path(
        '',
        include('jugadores.urls')
    )
]