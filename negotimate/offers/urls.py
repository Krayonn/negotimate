from django.urls import path
from . import views

# app_name = 'offers'

urlpatterns = [
    path('<str:user_id>/', views.submit),
    path('<str:offer_id>/<str:user_id>/accept', views.accept),
    path('<str:offer_id>/<str:user_id>/cancel', views.cancel),
    path('<str:offer_id>/<str:user_id>/proposeUpdate', views.proposeUpdate),
    path('<str:offer_id>/<str:user_id>/withdraw', views.withdraw),
    path('<str:offer_id>/<str:user_id>/history', views.getHistory),
]
