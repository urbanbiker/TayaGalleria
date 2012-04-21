from django.shortcuts import get_object_or_404
from annoying.decorators import render_to

from galleries.models import Gallery

@render_to('galleria_detail.html')
def galleria_detail(request, slug):
    galleria = get_object_or_404(Gallery, slug=slug)
    return locals()

@render_to('galleries_list.html')
def galleries_list(request):
    galleries = Gallery.objects.all()
    return locals()
