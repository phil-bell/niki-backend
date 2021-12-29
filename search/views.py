from django.views.generic import TemplateView

# Create your views here.

class SearchView(TemplateView):
    template_name = "search/search.html"

    