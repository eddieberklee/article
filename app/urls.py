from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name='article'),
    url(r'^add_article', 'app.views.add_article', name='add_article'),
)
