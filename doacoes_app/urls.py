from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^login/$', login ),
    #url(r'^check/token/$', check_token ),
    url(r'^doacoes/$', doacoes ),
    url(r'^minhas_doacoes/$', minhas_doacoes ),
    url(r'^cadastro_doacao/$', cadastro_doacao ),
    url(r'^minhas_doacoes_solicitadas/$', minhas_doacoes_solicitadas ),
    url(r'^minhas_doacoes_finalizadas/$', minhas_doacoes_finalizadas ),
    url(r'^doacoes_pedidas/$', doacoes_pedidas ),
    url(r'^doacoes_concluidas/$', doacoes_concluidas ),
    url(r'^pesquisa_doacao/$', pesquisa_doacao ),
    url(r'^estatisticas/$', estatisticas ),
    url(r'^doacoes/(?P<pk>[0-9]+)/$', doacoes_categoria ),
    url(r'^euquero/(?P<id_doacao>[0-9]+)/$', euquero ),
    url(r'^aceitar_doacao/(?P<id_doacao>[0-9]+)/$', aceitar_doacao ),
    url(r'^recusar_doacao/(?P<id_doacao>[0-9]+)/$', recusar_doacao ),
    url(r'^(?P<tabela>[a-z]+)/$', todos_produtos ),
    url(r'^(?P<tabela>[a-z]+)/(?P<pk>[0-9]+)/$', especifico_produto ),
]
