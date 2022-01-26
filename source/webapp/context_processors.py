from webapp.forms import SearchForm


def search_for_processor(request):
    form = SearchForm(request.GET)
    return {"search_form": form}