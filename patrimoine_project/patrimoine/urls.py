from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [

    path('home', views.home, name='home'),

    path('', views.dashboard, name='dashboard'),

    # Bureau
    path('bureaux/', views.bureau_list, name='bureau_list'),
    path('bureaux/box/', views.bureau_box, name='bureau_box'),
    path('bureaux/cloisonne/', views.bureau_cloisonne, name='bureau_cloisonne'),
    path('bureaux/open/', views.bureau_open, name='bureau_open'),
    path('bureaux/entier/', views.bureau_entier, name='bureau_entier'),
    path('bureaux/<int:pk>/', views.bureau_detail, name='bureau_detail'),
    path('bureaux/create/', views.bureau_create, name='bureau_create'),
    path('bureaux/<int:pk>/edit/', views.bureau_update, name='bureau_update'),
    path('bureaux/<int:pk>/delete/', views.bureau_delete, name='bureau_delete'),

    # Salle
    path('salles/', views.salle_list, name='salle_list'),
    path('salles/reunion/', views.salle_reunion, name='salle_reunion'),
    path('salles/conference/', views.salle_conference, name='salle_conference'),
    path('salles/pleniere/', views.salle_pleniere, name='salle_pleniere'),
    path('salles/formation/', views.salle_formation, name='salle_formation'),

    path('salles/<int:pk>/', views.salle_detail, name='salle_detail'),
    path('salles/create/', views.salle_create, name='salle_create'),
    path('salles/<int:pk>/edit/', views.salle_update, name='salle_update'),
    path('salles/<int:pk>/delete/', views.salle_delete, name='salle_delete'),

    # Materiel
    path('materiels/', views.materiel_list, name='materiel_list'),

    path('materiels/bon/', views.materiel_bon, name='materiel_bon'),
    path('materiels/moyen/', views.materiel_moyen, name='materiel_moyen'),
    path('materiels/mauvais/', views.materiel_mauvais, name='materiel_mauvais'),
    path('materiels/hs/', views.materiel_hs, name='materiel_hs'),
    path('materiels/autre/', views.materiel_autre, name='materiel_autre'),

    path('materiels/<int:pk>/', views.materiel_detail, name='materiel_detail'),
    path('materiels/create/', views.materiel_create, name='materiel_create'),
    path('materiels/<int:pk>/edit/', views.materiel_update, name='materiel_update'),
    path('materiels/<int:pk>/delete/', views.materiel_delete, name='materiel_delete'),



    path('add_salle/', views.add_salle, name='add_salle'),
    path('list_salle/', views.list_salle, name='list_salle'),
    path('detail_salle/<str:pk>', views.detail_salle, name='detail_salle'),
    path('update_salle/<str:pk>', views.update_salle, name='update_salle'),
    path('delete_salle/<str:pk>', views.delete_salle, name='delete_salle'),

    path('add_bureau/', views.add_bureau, name='add_bureau'),
    path('list_bureau/', views.list_bureau, name='list_bureau'),
    path('detail_bureau/<str:pk>', views.detail_bureau, name='detail_bureau'),
    path('update_bureau/<str:pk>', views.update_bureau, name='update_bureau'),
    path('delete_bureau/<str:pk>', views.delete_bureau, name='delete_bureau'),

    path('add_materiel/', views.add_materiel, name='add_materiel'),
    path('list_materiel/', views.list_materiel, name='list_materiel'),
    path('detail_materiel/<str:pk>', views.detail_materiel, name='detail_materiel'),
    path('update_materiel/<str:pk>', views.update_materiel, name='update_materiel'),
    path('delete_materiel/<str:pk>', views.delete_materiel, name='delete_materiel'),

    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, )
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, )

