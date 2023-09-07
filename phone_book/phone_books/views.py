from django.shortcuts import get_object_or_404, redirect, render
from phone_books.forms import CategoryCreateForm, CategoryEditForm, PhoneBookForm, PhoneBookEditForm

from phone_books.models import PhoneBook, Category

# Create your views here.


def phone_books(request):
    
    kisiler = PhoneBook.objects.all()
    categories = Category.objects.all()
    context = {
        'kisiler': kisiler,
        'categories': categories,
    }

    return render(request, "phone-books.html", context)

def get_phone_books_by_category(request, id):
    if id:
        kisiler = PhoneBook.objects.filter(category__id=id)
        kategoriler = Category.objects.all()
        

        context = {
            "kisiler":kisiler,
            "kategoriler":kategoriler
    }
    else:
        kisiler = PhoneBook.objects.all()
        categories = Category.objects.all()
        
        context = {
            'kisiler': kisiler,
            'categories': categories,
        }
    return render(request, "person-by-category.html", context)
    


def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q = request.GET["q"]
        kisiler = PhoneBook.objects.filter(ad__icontains=q)
        kategoriler = Category.objects.all()
    else:
        return redirect("/phone_books")
    
    return render(request, 'search.html', {
        "kisiler": kisiler,
        "categories": kategoriler,
    })


def category_list(request):
    kategoriler = Category.objects.all()
    return render(request, "categories-list.html", {
        "kategoriler": kategoriler
    })


def person_details(request, slug):
    kisi = PhoneBook.objects.filter(slug=slug)

    return render(request, "person_details.html", {kisi:kisi})


def create_person(request):
    if request.method == "POST":
        form = PhoneBookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("/phone-books")
        
    else:
        form = PhoneBookForm()
        
    return render(request, "create-person.html", {"form": form})


def create_category(request):
    if request.method == "POST":
        form = CategoryCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("category_list")
        
    else:
        form = CategoryCreateForm()
        
    return render(request, "create-category.html", {"form": form})


def phone_book_list(request):
    kisiler = PhoneBook.objects.all()
    return render(request, "phone-book-list.html", {"kisiler": kisiler})

def phone_book_edit(request, id):
    kisi = get_object_or_404(PhoneBook, pk=id)

    if request.method == "POST":
        form = PhoneBookEditForm(request.POST, request.FILES, instance=kisi)
        form.save()
        return redirect("phone_book_list")

    else:
        form = PhoneBookEditForm(instance=kisi)

    return render(request, "edit-person.html", {"form": form})

def phone_book_delete(request, id):
    kisi = get_object_or_404(PhoneBook, id=id)

    if request.method == "POST":
        kisi.delete()
        return redirect("phone_book_list")
    return render(request, "delete-person.html", {"kisi": kisi})

def category_delete(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        category.delete()
        return redirect("category_list")
    return render(request, "delete-category.html", {"category": category})

def category_edit(request, id):
    category = get_object_or_404(Category, pk=id)

    if request.method == "POST":
        form = CategoryEditForm(request.POST, request.FILES, instance=category)
        form.save()
        return redirect("category_list")

    else:
        form = CategoryEditForm(instance=category)

    return render(request, "edit-category.html", {"form": form})

