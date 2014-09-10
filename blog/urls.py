from django.conf import settings
from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('blog.views',
    url(r'^$', 'home', name='home'),
    url(r'^post/add/$', 'post_add', name='post-add'),
    url(r'^post/$', 'post_view', name='post-view'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.generic.simple',
        url(r'^500/$', 'direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'direct_to_template', {'template': '404.html'}),
    )
