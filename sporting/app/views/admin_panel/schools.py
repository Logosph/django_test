from django.shortcuts import redirect, render

from app import models
from app.forms import DanceSchoolForm, EditDanceSchoolForm
from app.views.helper import check_jwt


def admin_schools(request):
    if request.method != "GET":
        return redirect("/admin/schools?error=Неверный метод запроса")

    error_message = request.GET.get("error")

    schools = models.DanceSchool.objects.all()

    contents = {
        "schools": [],
        "error_message": error_message,
        "school_form": DanceSchoolForm(),
        "edit_school_form": EditDanceSchoolForm()
    }

    for school_id, name, address, phone in schools.values_list("dance_school_id", "dance_school_name", "dance_school_address", "dance_school_address"):
        contents["schools"].append(
            {
                "id": school_id,
                "name": name,
                "address": address,
                "phone": phone
            }
        )

    contents["schools"].sort(key=lambda x: x["name"])

    return check_jwt(request, render(request, "dance_school_list.html", contents))


def add_school(request):
    if request.method != "POST":
        return redirect("/admin/schools?error=Неверный метод запроса")

    form = DanceSchoolForm(request.POST)

    if not form.is_valid():
        return redirect("/admin/schools?error=Неверные данные")

    school = models.DanceSchool.objects.filter(dance_school_name=form.cleaned_data["name"]).first()

    if school is not None:
        return redirect("/admin/schools?error=Такая школа уже существует")

    models.DanceSchool.objects.create(
        dance_school_name=form.cleaned_data["name"],
        dance_school_address=form.cleaned_data["address"],
        phone_number=form.cleaned_data["phone"]
    )
    return redirect("/admin/schools")
