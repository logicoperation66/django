from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    """Rejestracja nowego użytkownika"""
    if request.method != 'POST':
        #Wyświetlanie pustego formularza rejestracji użytkownika
        form = UserCreationForm()
    else:
        #Przetworzenie wypełnionego formularza.
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            #Zalogowanie użytkownika, a następnie przekierowanie go na stronę
            # główną.
            login(request, new_user)
            return redirect('learning_logs:index')

    #Wyświetlanie pustego formularza.
    context = {'form': form}
    return render(request, 'registaration/register.html', context)