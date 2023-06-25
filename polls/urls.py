from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('api1/',views.api1, name = 'api1'),
    path('getpolls/',views.api2_get, name = 'api2'),
    path('tag/<str:tag_names>/',views.tag_check,name='detail'),
    path('update/<int:id>/',views.update_poll, name='api4'),
    path('get_poll/<int:pk>/',views.get_poll, name='api5'),
    path('get_tag/',views.get_tag, name='api6'),
    path('question/<str:question_text>/', views.get_question_id, name='get_question_id'),

    
]