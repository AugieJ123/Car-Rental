from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .models import Car, Rental
from .forms import CarForm, CustomUserCreationForm, RentalCarForm
from django.contrib.auth import login
from django.urls import reverse_lazy


class HomeView(generic.ListView):
    model = Car
    template_name = "index.html"


class CustomLoginView(LoginView):
    template_name = "login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome, {self.request.user.username}!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"Welcome, {user.username}!")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error creating the account. Please try again.")
        return super().form_invalid(form)


class CarListView(generic.ListView):
    template_name = "car_list.html"

    def get(self, request):
        cars = Car.objects.all()
        context = {"cars": cars}
        return render(request, self.template_name, context)


class CarCreateView(generic.CreateView):
    model = Car
    form_class = CarForm
    template_name = "car_list.html"
    success_url = reverse_lazy("car_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response


class RentCarView(LoginRequiredMixin, generic.RedirectView):
    permanent = False
    query_string = True
    pattern_name = "car_list"

    def get_redirect_url(self, *args, **kwargs):
        car_id = kwargs["car_id"]
        car = get_object_or_404(Car, id=car_id)

        # Check if the car is available
        if car.available:
            # Rent the car
            Rental.objects.create(user=self.request.user, car=car)
            car.available = False
            car.save()

        # Redirect to 'car_list' without any additional arguments
        return super().get_redirect_url(*args, **kwargs)


class UserRentedCarsView(LoginRequiredMixin, generic.ListView):
    model = Rental
    template_name = "user_rental_car.html"
    context_object_name = "rented_cars"
    ordering = ["-rent_date"]

    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user)


class CancelRentView(generic.View):
    def post(self, request, *args, **kwargs):
        rental_id = kwargs.get("rental_id")
        rental = get_object_or_404(Rental, id=rental_id, user=request.user)

        # Get the associated car and set its availability to True
        car = rental.car
        car.available = True
        car.save()
        
        rental.delete()

        return redirect("user_rented_cars")
