from statistics import mean
from amaz_products.models import Rank, Price


def query_asin_rank(asin: str, sale_rank_reference=541966, tail=3):
    ranks = Rank.objects.filter(
        asin_id__exact=asin, sale_rank_reference=sale_rank_reference
    ).order_by("-date")[:tail]
    print(ranks.query)
    print(ranks)
    values = [r.rank for r in ranks]
    if not values:
        return {}
    stat = (
        values[1],
        round(mean(values), 2),
        max(values),
        min(values),
    )

    return {
        f"rank_{name}": st for name, st in zip(("latest", "mean", "max", "min"), stat)
    }


def query_asin_price(asin: str, tail=3):
    prices = Price.objects.filter(asin_id=asin).order_by("-date")[0:tail]
    values = [p.price for p in prices]
    if not values:
        return {}
    stat = (
        values[1],
        round(mean(values), 2),
        max(values),
        min(values),
    )
    return {
        f"price_{name}": st for name, st in zip(("latest", "mean", "max", "min"), stat)
    }
