from .models import UserWall, Fanpage
from django.db.models.functions import Concat
from django.db.models import F, Value, CharField

def most_popular_pages(request):
    def formated(views):
        if views >= 10**7:
            return str(views//10**6)+" M"
        elif views >= 10**6:
            return str(round(views/10**6, 1))+" M"
        elif views >= 10**4:
            return str(views//10**3)+" K"
        elif views >= 10**3:
            return str(round(views/10**3, 1)) + " K"
        return views

    walls = UserWall.objects.annotate(
        url = Concat(Value("wall/"), F("user__username"), Value("/"), output_field=CharField())
        ).values("views", "url")

    fanpages = Fanpage.objects.annotate(
        url = Concat(Value("fanpage/"), F("fanpage_name"), Value("/"), output_field=CharField())
    )

    most_popular = walls.union(fanpages).order_by("-views")[:8]
    for item in most_popular:
        item["views"] = formated(item["views"])

    return {"most_popular" : most_popular}