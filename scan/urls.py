from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^simple_upload', views.simple_upload, name='simple_upload'),
    url(r'^add', views.add, name='add'),
    url(r'^survey_chart_view', views.survey_chart_view, name='survey_chart_view'),
    url(r'^create_survey', views.create_survey, name='create_survey'),
    url(r'^take_survey', views.take_survey, name='take_survey'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^charts/simple.png$', views.simple, name="simple"),
    url(r'^new-listitem/$', views.additem, name='additem'),
    url(r'^$', views.app_entry, name='app_entry'),

    url(r'^inventory/', views.show_inventory, name="inventory"),
    url(r'^remove_items/', views.remove_items, name="remove_inventory"),
    url(r'^items/$', views.items, name="items"),
]
