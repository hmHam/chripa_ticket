from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from chripa.invite.urls import router as invite_router

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += invite_router.urls

urlpatterns += [
    path('', lambda request: redirect('invite-list'))
]
