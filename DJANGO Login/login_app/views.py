from django.shortcuts import render, redirect
from .forms import LoginForm
import subprocess
import os
from django.contrib.auth import authenticate, login

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        # ✅ Path to app.py (adjust this if needed)
        streamlit_script = os.path.abspath(r"C:\Users\HP\Desktop\Hackthon 3\Finance Dashboard\app.py")


        # ✅ Start Streamlit in background
        subprocess.Popen(["streamlit", "run", streamlit_script], shell=True)

        # ✅ Redirect user to Streamlit (default port)
        return redirect("http://localhost:8501")

    return render(request, "login.html", {"form": form})
