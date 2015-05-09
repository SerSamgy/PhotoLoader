from django.shortcuts import render

def table():
    return None


def root(request):
    return render(request, "loader/index.html")