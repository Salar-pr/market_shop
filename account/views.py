from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreatinForm



class CustomLoginView(LoginView):
    redirect_authenticated_user = True




def signup(request):
    if request.user.is_authenticated:
        return redirect('product:home')
    if request.method == "POST":
        form = CustomUserCreatinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        print(form.errors)
        return render(request,'registration/singup.html',{"form":form})
    form = CustomUserCreatinForm()
    
    context = {
        "form":form,
    }
    
    return render(request,'registration/singup.html',context)
    