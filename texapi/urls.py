from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


class TextPlainView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TextPlainView, self).render_to_response(context, content_type='text/plain', **kwargs)


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('texapi.backoffice',),
}


urlpatterns = patterns('',

    # Examples:
    # url(r'^$', 'ctm.views.home', name='home'),
    # url(r'^ctm/', include('ctm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # rest-swagger docs
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    url(r'^docs/', include('rest_framework_swagger.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^backoffice/', include('backoffice.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),

    (r'^api/v1/', include('articles.api.urls')),


    url(r'^robots\.txt$', TextPlainView.as_view(template_name='robots.txt')),

    url(r'^search/', include('search.urls')),
    url(r'^newsletter/', include('newsletter.urls')),
    url(r'^', include('articles.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns = patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    ) + urlpatterns


if settings.LOCAL_MODE:
    urlpatterns += patterns('',

    # if we are in local mode we need django to serve medias
     (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),

    )


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
    ) + urlpatterns
