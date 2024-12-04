from django.shortcuts import redirect, render

from app import models
from app.forms.hall_forms import HallForm, EditHallForm
from app.views.helper import check_jwt


def admin_hall(request):
    if request.method != "GET":
        return redirect("/admin/halls?error=Неверный метод запроса")

    error_message = request.GET.get("error")

    halls = models.Hall.objects.all()
    schools = models.DanceSchool.objects.all()

    school_choices = [(school.dance_school_id, school.dance_school_name) for school in schools]
    school_dict = {school.dance_school_id: school.dance_school_name for school in schools}

    school_choices.sort(key=lambda x: x[1])

    add_form = HallForm()
    add_form.update_choices(school_choices)

    edit_form = EditHallForm()
    edit_form.update_choices(school_choices)

    contents = {
        "halls": [],
        "error_message": error_message,
        "hall_form": add_form,
        "edit_hall_form": edit_form
    }

    for hall_id, dance_school_id, hall_name, capacity in halls.values_list(
            "hall_id",
            "dance_school_id",
            "hall_name",
            "capacity",
    ):
        contents["halls"].append(
            {
                "id": hall_id,
                "name": hall_name,
                "school": school_dict[dance_school_id],
                "capacity": capacity
            }
        )

    contents["halls"].sort(key=lambda x: x["name"])

    return check_jwt(request, render(request, "admin/hall_list.html", contents))


def add_hall(request):
    if request.method != "POST":
        return redirect("/admin/halls?error=Неверный метод запроса")

    schools = models.DanceSchool.objects.all()
    school_choices = [(school.dance_school_id, school.dance_school_name) for school in schools]

    form = HallForm(request.POST)
    form.update_choices(school_choices)

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    if not form.is_valid():
        return redirect("/admin/halls?error=Неверные данные")

    halls = models.Hall.objects.filter(hall_name=form.cleaned_data["name"]).first()

    if halls is not None:
        return redirect("/admin/halls?error=Зал с таким именем уже существует")

    models.Hall.objects.create(
        dance_school_id=(
            models
            .DanceSchool
            .objects
            .get(dance_school_id=form.cleaned_data["dance_school"])
        ),
        hall_name=form.cleaned_data["name"],
        capacity=form.cleaned_data["capacity"]
    )
    return redirect("/admin/halls")


def edit_hall(request, _id: int):
    if request.method != "POST":
        return redirect("/admin/halls?error=Неверный метод запроса")

    schools = models.DanceSchool.objects.all()
    school_choices = [(school.dance_school_id, school.dance_school_name) for school in schools]

    form = EditHallForm(request.POST)
    form.update_choices(school_choices)

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    if not form.is_valid():
        return redirect("/admin/halls?error=Неверные данные")

    hall = models.Hall.objects.filter(hall_id=_id)

    if hall is None:
        return redirect("/admin/halls?error=Зал с таким именем уже существует")

    new_name = form.cleaned_data["name"]
    new_capacity = form.cleaned_data["capacity"]
    new_school = form.cleaned_data["dance_school"]

    if new_name:
        hall.update(hall_name=new_name)
    if new_capacity:
        hall.update(capacity=new_capacity)
    if new_school:
        hall.update(dance_school_id=models.DanceSchool.objects.filter(dance_school_id=new_school).first())

    return redirect("/admin/halls")


def delete_hall(request, _id: int):
    if request.method != "POST":
        return redirect("/admin/halls?error=Неверный метод запроса")

    check_result = check_jwt(request.COOKIES.get('access_token'), True)
    if type(check_result) != type(True):
        return redirect("/admin/login")

    hall = models.Hall.objects.filter(hall_id=_id)
    if hall.exists():
        hall.delete()
        return redirect("/admin/halls")
    else:
        return redirect("/admin/halls?error=Такой школы не существует")