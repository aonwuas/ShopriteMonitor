from django.http import HttpResponse
from django.db.models import Q
from Shoprite.models import StaticItem, SaleItem
from django.template import RequestContext, loader
# Create your views here.


def search(request):
    search_results = StaticItem.objects.filter(Q(name__icontains="baby") | Q(category__icontains="baby"))
    template = loader.get_template('search_results.html')
    context = RequestContext(request, {
        'search_results': search_results,
    })
    return HttpResponse(template.render(context))


def test(request, item_id):
    item_id = int(item_id)
    item_name = StaticItem.objects.get(id=item_id).name
    sale_items = SaleItem.objects.filter(Q(static_item_id=item_id))
    test = SaleItem.objects.select_related('static_item').get(id=item_id)
    template = loader.get_template('item_info.html')
    context = RequestContext(request, {
        'sale_items': sale_items,
        'item_name': item_name,
        'static_id': test.static_item.id
    })
    return HttpResponse(template.render(context))