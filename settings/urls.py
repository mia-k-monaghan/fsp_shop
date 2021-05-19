from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('create-content/<page>/<type>',views.CreateContentView.as_view(),name='create-content'),
    path('update-content/<pk>',views.UpdateContentView.as_view(),name='update-content'),
    path('delete-content/<pk>',views.DeleteContentView.as_view(),name='delete-content'),
    path('add-image/<type>',views.CreateImageView.as_view(),name='add-image'),
    path('update-image/<pk>',views.UpdateImageView.as_view(),name='update-image'),
    path('delete-image/<pk>',views.DeleteImageView.as_view(),name='delete-image'),
    path('icons/',views.IconView.as_view(),name='icons'),
    path('themes/',views.ThemeView.as_view(),name='themes'),
    path('add-theme/<type>',views.CreateThemeView.as_view(),name='add-theme'),
    path('update-theme/<pk>',views.UpdateThemeView.as_view(),name='update-theme'),
    path('delete-theme/<pk>',views.DeleteThemeView.as_view(),name='delete-theme'),
    path('social-accounts/',views.SocialView.as_view(),name='socials'),
    path('add-social/<type>',views.CreateSocialView.as_view(),name='add-social'),
    path('update-social/<pk>',views.UpdateSocialView.as_view(),name='update-social'),
    path('delete-social/<pk>',views.DeleteSocialView.as_view(),name='delete-social'),
    path('optional-pages/',views.OptionalPageView.as_view(),name='pages'),
    path('add-page/<page>',views.CreateDisplayPageView.as_view(),name='add-page'),
    path('update-page/<pk>',views.UpdateDisplayPageView.as_view(),name='update-page'),
]
