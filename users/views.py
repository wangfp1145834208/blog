from django.shortcuts import render, redirect

from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        redirect_to = request.POST['next']
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            if redirect_to:
                return redirect(redierct_to)
            else:
                return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form})
