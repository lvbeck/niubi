from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
  (r'^openid-login/$', 'openidgae.views.LoginPage'),
  (r'^openid-logout/$', 'openidgae.views.LogoutSubmit'),
  (r'^start/$', 'openidgae.views.OpenIDStartSubmit'),
  (r'^finish/$', 'openidgae.views.OpenIDFinish'),
  (r'^rpxrds/$', 'openidgae.views.RelyingPartyXRDS'),
)
