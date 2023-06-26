from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views import View

User = get_user_model()

class LoginView(View):
    """
    A class-based view that handles user authentication and login functionality.
    """

    def get(self, request):
        """
        Handles GET requests and renders the login template.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The response object containing the rendered template.
        """
        return render(request, 'login.html')

    def post(self, request):
        """
        Handles POST requests and performs user authentication and login.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: The response object based on the authentication status.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user using the provided username and password
        user = authenticate(username=username, password=password)

        if user is not None:
            # If authentication is successful, log in the user
            login(request, user)
            return redirect('home')
        else:
            # If authentication fails, render the login template with an error message
            return render(request, 'login.html', {'error': 'Invalid username or password'})
