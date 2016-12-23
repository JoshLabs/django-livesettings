from . import views

urlpatterns = [
    (r'^$', views.site_settings, {}, 'satchmo_site_settings'),
    (r'^export/$', views.export_as_python, {}, 'settings_export'),
    (r'^(?P<group>[^/]+)/$', views.group_settings),
]