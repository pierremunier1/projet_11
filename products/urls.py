from django.urls import path
from . import views


urlpatterns = [
    path('', views.search, name='home'),
    path('results.html', views.result, name='results'),
    path('<int:product_id>', views.detail, name='detail'),
    path('favorite.html', views.favorite, name='favorite'),
    path('<int:product_original_id>/<int:product_substitute_id>', views.save_substitute, name='save_substitute'),
    path('remove_products/<int:product_original_id>/<int:product_substitute_id>',views.remove_products,name='remove_products'),
    path('mentions_legales', views.mentions_legales, name='mentions_legales'),
    path('my_account',views.my_account, name='my_account'),
    path('search_autocomplete/', views.search_autocomplete, name='search_autocomplete')
]