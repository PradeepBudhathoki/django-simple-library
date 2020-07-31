from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic 
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin



def index(request):
    """view function for home page of site"""
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    """Available books(status='a')"""
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()

    num_authors=Author.objects.count() #the all is implied by default
    #no of visits to this view as counted in the session variable
    num_visits=request.session.get('num_visits',0) # get the session value assign default if not found
    request.session['num_visits']=num_visits+1


    num_bookswith_the=Book.objects.filter(title__icontains='the').count()

    num_fiction_genre=Book.objects.filter(genre__name__icontains='fiction').count()

    

    context={
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_bookswith_the':num_bookswith_the,
        'num_fiction_genre':num_fiction_genre,
        'num_visits':num_visits,
    }
    #Render the HTML template index.html with the data in the context
    return render(request,'index.html',context=context)

class BookListView(generic.ListView):
    model=Book
    paginate_by=2
    template_name='catalog/book_list.html'

class AuthorListView(generic.ListView):
    model=Author
    paginate_by=10
    template_name='catalog/author_list.html'

class BookDetailView(generic.DetailView):
    model=Book
    template_name='catalog/book_detail.html'

    """function based detail view
    def book_detail_view(request,primary_key):
        book=get_object_or_404(Book,pk=primary_key)
        return render(request,'catalog/book_detail.html',context={'book':book})"""

class AuthorDetailView(generic.DetailView):
    model=Author
    template_name='catalog/author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_user.html'
    paginate_by=2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


"""class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model=BookInstance
    permission_required='catalog.can_mark_returned'
    template_name='catalog/bookinstance_list_borrowed_all.html'
    paginate_by=2

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='0').order_by('due_back')"""





    

