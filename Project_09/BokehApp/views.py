from django.shortcuts import render
from django.http import HttpResponse
from bokeh.plotting import figure
from bokeh.embed import components

def home(request):
    plot = figure(width=400, height=400)
    plot.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
    script, div = components(plot)
    return render(request, "BokehApp/base.html", {"script":script, "div":div})