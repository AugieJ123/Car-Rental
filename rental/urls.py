from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    CarCreateView,
    CarListView,
    CustomLoginView,
    HomeView,
    RentCarView,
    SignUpView,
    UserRentedCarsView,
    CancelRentView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/login"), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("cars/", CarListView.as_view(), name="car_list"),
    path("cars/add/", CarCreateView.as_view(), name="add_car"),
    path("cars/rent/<int:car_id>/", RentCarView.as_view(), name="rent_car"),
    path("user/rented-cars/", UserRentedCarsView.as_view(), name="user_rented_cars"),
    path(
        "user/cancel-rent/<int:rental_id>/",
        CancelRentView.as_view(),
        name="cancel_rent",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
