from django.urls import path, include



from app.views.admin_panel import choreographers, general, styles, schools
from app import archived_views

admin_patterns = [
    path("", general.admin),
    path("login", general.admin_login),
    path("styles", styles.admin_styles),
    path("add_style", styles.add_style),
    path("delete_style/<int:_id>", styles.delete_style),
    path("edit_style/<int:_id>", styles.edit_style),

    path("choreographers", choreographers.admin_choreographers),
    path("add_choreographer", choreographers.add_choreographer),
    path("delete_choreographer/<int:_id>", choreographers.delete_choreographer),
    path("edit_choreographer/<int:_id>", choreographers.edit_choreographer),

    path("schools", schools.admin_schools),
    path("add_school", schools.add_school),
]


urlpatterns = [
    path("admin/", include(admin_patterns)),
    path("hello/", archived_views.index),
]
