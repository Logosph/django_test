from django.shortcuts import render


def index(request):
    classes = [
        {"name": "Математика"},
        {"name": "Физика"},
        {"name": "Химия"}
    ]
    return render(request, 'index.html', {'classes': classes})


