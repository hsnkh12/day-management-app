
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/",include([

        path('accounts/',include('apps.accounts.api.urls')),

        path('todo/',include('apps.todo.api.urls')),

        path('wallet/',include('apps.wallet.api.urls')),

        path('goals/',include('apps.goals.api.urls')),

        path('notepad/',include('apps.notepad.api.urls')),

        path('health/',include('apps.health.api.urls')),

    ]))

    
]
