from django.urls import path

from invoicing import views


urlpatterns = [
    path("accounts/", views.accounts_home, name="accounts_home"),
    path("homes/", views.homes_dashboard, name="homes_dashboard"),
    path("invoice/", views.invoice_list, name="invoice_list"),
    path("invoice/new/", views.invoice_create, name="invoice_create"),
    path("invoice/<int:id>/", views.invoice_detail, name="invoice_detail"),
    path("invoice/<int:id>/edit/", views.invoice_update, name="invoice_update"),
    path("invoice/<int:id>/delete/", views.invoice_delete, name="invoice_delete"),
    path("invoice/monthly/", views.invoice_monthly_totals, name="invoice_monthly_totals"),

    path("rental/", views.rental_property_list, name="rental_property_list"),
    path("rental/new/", views.rental_property_create, name="rental_property_create"),
    path("rental/<int:id>/", views.rental_property_detail, name="rental_property_detail"),
    # Inline managing agent assignment could be posted to the same URL via POST
    path("rental/<int:id>/upload_image/", views.rental_property_upload_image, name="rental_property_upload_image"),
    path("rental/<int:id>/edit/", views.rental_property_update, name="rental_property_update"),
    path("rental/<int:id>/delete/", views.rental_property_delete, name="rental_property_delete"),
    path("rental/<int:id>/earnings/", views.rental_property_earnings, name="rental_property_earnings"),
    # Pipeline
    path("rental/pipeline/", views.rental_pipeline_list, name="rental_pipeline_list"),
    path("rental/pipeline/<int:id>/edit/", views.rental_pipeline_edit, name="rental_pipeline_edit"),
    path("rental/pipeline/<int:id>/upload_image/", views.rental_pipeline_upload_image, name="rental_pipeline_upload_image"),
    path("rental/pipeline/<int:id>/detail/", views.rental_pipeline_detail, name="rental_pipeline_detail"),
    path("rental/pipeline/<int:id>/<str:status>/", views.rental_pipeline_update_status, name="rental_pipeline_update_status"),
    path("rental/preview-images/", views.preview_images_from_url, name="preview_images_from_url"),
    # Expenses
    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/monthly/", views.expense_monthly_totals, name="expense_monthly_totals"),
    path("expenses/<int:id>/edit/", views.expense_update, name="expense_update"),
    path("expenses/<int:id>/delete/", views.expense_delete, name="expense_delete"),
    # Agents
    path("agents/", views.agent_list, name="agent_list"),
    path("agents/new/", views.agent_create, name="agent_create"),
    path("agents/<int:id>/", views.agent_detail, name="agent_detail"),
    path("agents/<int:id>/edit/", views.agent_update, name="agent_update"),
    path("agents/<int:id>/delete/", views.agent_delete, name="agent_delete"),

    # Estate Agents
    path("estate-agents/", views.estate_agent_list, name="estate_agent_list"),
    path("estate-agents/new/", views.estate_agent_create, name="estate_agent_create"),
    path("estate-agents/<int:id>/", views.estate_agent_detail, name="estate_agent_detail"),
    path("estate-agents/<int:id>/edit/", views.estate_agent_update, name="estate_agent_update"),
    path("estate-agents/<int:id>/delete/", views.estate_agent_delete, name="estate_agent_delete"),

    # Managing Agents
    path("managing-agents/", views.managing_agent_list, name="managing_agent_list"),
    path("managing-agents/new/", views.managing_agent_create, name="managing_agent_create"),
    path("managing-agents/<int:id>/", views.managing_agent_detail, name="managing_agent_detail"),
    path("managing-agents/<int:id>/edit/", views.managing_agent_update, name="managing_agent_update"),
    path("managing-agents/<int:id>/delete/", views.managing_agent_delete, name="managing_agent_delete"),
]


