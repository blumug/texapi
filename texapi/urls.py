from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


class TextPlainView(TemplateView):
    def render_to_response(self, context, **kwargs):
        return super(TextPlainView, self).render_to_response(context, content_type='text/plain', **kwargs)


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Examples:
    # url(r'^$', 'ctm.views.home', name='home'),
    # url(r'^ctm/', include('ctm.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # rest-swagger docs
    url(r'^docs/', include('rest_framework_swagger.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^api/v1/text/', include('text.api.urls')),
    (r'^api/v1/', include('api_users.api.urls')),

    url(r'^robots\.txt$', TextPlainView.as_view(template_name='robots.txt')),
)

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
