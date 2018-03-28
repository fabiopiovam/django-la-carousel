from django.template import Library
from django.core.exceptions import ObjectDoesNotExist

from carousel.models import Carousel

register = Library()

@register.inclusion_tag('carousel/carousel.html', takes_context=True)
def generate_carousel(context, carousel=''):
    if not carousel:
        return {'carousel': '',}
    
    try:
        obj = Carousel.activated.get(type=carousel)
        range_carousel = range(obj.images_set().count())
    except ObjectDoesNotExist:
        obj = None
        range_carousel = []
    
    return {'carousel': obj, 'range_carousel': range_carousel}
