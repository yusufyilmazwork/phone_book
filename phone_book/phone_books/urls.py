from django.urls import path
from phone_books import views

urlpatterns = [
    path("", views.phone_books, name="phone_books"),
    path("search", views.search, name="search"),
    path("person-details/<str:slug>", views.person_details, name="person_details"),
    path("create-person", views.create_person, name="create_person"),
    path("create-category", views.create_category, name="create_category"),
    path("phone-book-list", views.phone_book_list, name="phone_book_list"),
    path("categories-list", views.category_list, name="category_list"),
    path("edit-person/<int:id>", views.phone_book_edit, name="phone_book_edit"),
    path("edit-category/<int:id>", views.category_edit, name="category_edit"),
    path("delete-person/<int:id>", views.phone_book_delete, name="phone_book_delete"),
    path("delete-category/<int:id>", views.category_delete, name="category_delete"),
    path("person-by-category/<int:id>", views.get_phone_books_by_category, name="person_by_category"),

]