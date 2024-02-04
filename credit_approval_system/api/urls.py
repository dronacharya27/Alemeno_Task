from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("register", views.CustomerViewset, basename="register")
router.register("loan", views.LoanViewSet, basename="loan")
urlpatterns = [
    path("", include(router.urls)),
    path(
        "check-eligiblity/",
        views.LoanViewSet.as_view({"post": "check_eligiblity"}),
        name="check-eligiblity",
    ),
    path(
        "create-loan/",
        views.LoanViewSet.as_view({"post": "create_loan"}),
        name="create-loan",
    ),
    path(
        "view-loan/<int:loan_id>/",
        views.LoanViewSet.as_view({"get": "view_loan"}),
        name="view-loan",
    ),
    path(
        "view-loans/<int:customer_id>/",
        views.LoanViewSet.as_view({"get": "view_customer_loans"}),
        name="view-loans",
    ),
]
