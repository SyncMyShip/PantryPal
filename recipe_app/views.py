from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    # initialize error message to None
    error_message = None
    # form object with username and password fields
    form = AuthenticationForm()

    # when user hits "login" button, the POST request is generated
    if request.method == 'POST':
        #read data sent by form via POST
        form = AuthenticationForm(data=request.POST)

        # check if form is valid
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # use Django auth function to validate user
            user = authenticate(username=username, password=password)

            if user is not None:
                # then use pre-defined Django function to login
                login(request, user)
                # send user to desired page
                return redirect('recipes:home')
            else:
                error_message = "oops... something went wrong"

    # prep data to send from view to template
    context = {
        'form': form,
        'error_message': error_message
    }

    # load the login page using "context" info
    return render(request, 'auth/login.html', context)


def logout_view(request):
    # user pre-defined Django function to logout
    logout(request)

    # redirect back to login page after login
    return render(request, 'auth/success.html')

