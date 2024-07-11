from .models import UserWall, Fanpage
from django.db.models.functions import Concat
from django.db.models import F, Value, CharField

def most_popular_pages(request):
    walls = UserWall.objects.annotate(
        url = Concat(Value("wall/"), F("user__username"), Value("/"), output_field=CharField())
        ).values("views", "url")

    fanpages = Fanpage.objects.annotate(
        url = Concat(Value("fanpage/"), F("fanpage_name"), Value("/"), output_field=CharField())
    )

    most_popular = walls.union(fanpages).order_by("-views")[:8]
    
    return {"most_popular" : most_popular}