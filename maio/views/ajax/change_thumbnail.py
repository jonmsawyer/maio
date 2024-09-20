'''
File: change_thumbnail.py

Module: ``maio.views.ajax.change_thumbnail``
'''

from __future__ import annotations

from django.http import HttpRequest, JsonResponse

from maio.models import Media


def change_thumbnail(request: HttpRequest) -> JsonResponse:
    '''Delete the Media for this user for a given UUID.'''
    if request.method == 'POST':
        try:
            media_uuid = request.POST.get('media_uuid');
            media = Media.objects.get(pk=media_uuid, owner=request.user)
        except Media.DoesNotExist:
            return JsonResponse({'error': 'Media with UUID does not exist for this user.'})
        slideshow = media.file.slideshow_set.get()
        try:
            index = int(request.POST.get('index'))
        except ValueError:
            return JsonResponse({'error': 'Could not parse index into an integer.'}, status=400)
        if index < 0 or index >= slideshow.num_slices:
            return JsonResponse({'error': 'Index value is out of range for this media.'}, status=400)
        prev_index = media.slideshow_index
        media.slideshow_index = index
        media.slideshow_tn_uri = (
            media
                .get_static_thumbnail_uri()
                .replace(f"_{prev_index}.", "_{index}.")
                .format(index=index)
        )
        media.save()
        return JsonResponse({
            'media_uuid': media_uuid,
            'slideshow_index': media.slideshow_index,
            'slideshow_tn_uri': media.slideshow_tn_uri,
            'status': 'OK',
        })
    return JsonResponse({'error': 'I only understand POST requests.'})
