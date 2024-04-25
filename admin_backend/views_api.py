from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import Count
from amaz_products.app_permission import IsSuperAdmin
from amaz_products.models import Permission, StandardProductAsin
from amaz_products.serializers import (
    PermissionSerializer,
    StandardProductAsinSerilizer,
)
from amaz_products.business.amaz_price_and_rank import query_asin_price, query_asin_rank


@api_view()
def inventory_summary(request: Request):
    upc = request.query_params["upc"]
    asins = StandardProductAsin.objects.filter(upc=upc).exclude(asin__exact="")
    data_list = []
    for asin_obj in asins:
        print(asin_obj.asin)
        prices = query_asin_price(asin=asin_obj.asin)
        if prices:
            data = {
                **StandardProductAsinSerilizer(asin_obj).data,
                **prices,
                **query_asin_rank(asin=asin_obj.asin),
            }
            data_list.append(data)
    return Response(data_list)


@api_view()
def upc_asin_count(request: Request):
    asins = (
        StandardProductAsin.objects.exclude(asin__exact="")
        .values("upc")
        .annotate(asin_count=Count("asin"))
    )
    data = {asin_obj["upc"]: asin_obj["asin_count"] for asin_obj in asins}
    return Response({"results": data})


@api_view()
@permission_classes([IsSuperAdmin])
def permissions_button_list(request: Request, parent_id: int):
    button_permissions = Permission.objects.filter(
        parent_id=parent_id, type__exact="BUTTON"
    ).order_by("id")
    data = [PermissionSerializer(p).data for p in button_permissions]
    return Response({"results": data})
