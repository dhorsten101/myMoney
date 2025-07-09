from django.conf import settings


def version_info(request):
	return {
		"VERSION": getattr(settings, "VERSION", {
			"version": "unknown",
			"commit": "-",
			"branch": "-",
			"message": "",
			"build_date": "-"
		})
	}
