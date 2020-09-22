from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .helpers import get_exports


@login_required
def export(request):
    """Exports instances as a json file."""
    collection = get_exports()
    return JsonResponse(collection, safe=False)
