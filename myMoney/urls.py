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
]
