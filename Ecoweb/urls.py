from django.urls import path,include
from .views import(
 HomeView,
 ProductDetailView,
 add_to_cart,
 remove_from_cart,
 OrderSummaryView
)


from .import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


app_name = "Ecoweb"

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='index'),
    path('product/<slug>/',ProductDetailView.as_view(), name='detail'),
    path('add-to-cart/<slug>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug>/',views.remove_from_cart,name='remove-from-cart'),
    path('link/',views.detailitem,name='linkage'),
    path('cart/', OrderSummaryView.as_view(),name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('complete/',views.complete,name='complete'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
