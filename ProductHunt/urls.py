
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import account.urls, product.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(account.urls)),
    path('product/', include(product.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
