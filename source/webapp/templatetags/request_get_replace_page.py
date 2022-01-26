from django import template

register = template.Library()

@register.filter
def replace_request(request, page_num):
    query_args = request.GET.copy()
    query_args['page'] = page_num
    return query_args.urlencode()