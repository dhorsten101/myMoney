from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
				  path("admin/", admin.site.urls),
				  path("", include("main.urls")),
				  path("", include("api.urls")),
				  path("", include("cryptos.urls")),
				  path("", include("incomes.urls")),
				  path("", include("credits.urls")),
				  path("", include("expenses.urls")),
				  path("", include("worth.urls")),
				  path("", include("history_records.urls")),
				  path("", include("sellables.urls")),
				  path("", include("to_do.urls")),
				  path("", include("ideas.urls")),
				  path("", include("weight.urls")),
				  path("", include('documents.urls')),
				  path("", include('folders.urls')),
				  path("", include('llm.urls')),
				  path("", include('weather.urls')),
				  path("", include('system.urls')),
				  path("", include('monitoring.urls')),
				  path("", include('logs.urls')),
				  path("", include("cameras.urls")),
				  path("", include("pen_tester.urls")),
				  path("", include("reminders.urls")),
				  path("", include("time_tracker.urls")),
				  path("", include("horsten_homes.urls")),
				  path("", include("contractors.urls")),
				  path('ckeditor5/', include('django_ckeditor_5.urls')),
			  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
