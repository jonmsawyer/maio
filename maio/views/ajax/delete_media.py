'''
File: dashboard.py

Module: ``maio.views.dashboard``
'''

from __future__ import annotations

from django.http import HttpRequest, JsonResponse

from maio.models import Media


def delete_media(request: HttpRequest) -> JsonResponse:
    '''Delete the Media for this user for a given UUID.'''
    if request.method == 'POST':
        media_uuid = request.POST.get('media_uuid');
        delete_all = False
        media_deleted = []
        ret = None
        if request.user.is_superuser:
            delete_all = request.POST.get('delete_all')
            if delete_all == 'true':
                delete_all = True
            else:
                delete_all = False
        media = Media.objects.get(pk=media_uuid, owner=request.user)
        if delete_all:
            f = media.file
            for med in f.media_set.all():
                media_deleted.append(med.id)
            ret = f.delete()
        else:
            media_deleted.append(media.id)
            ret = media.delete()
    return JsonResponse({
        'delete_media_uuid': media_uuid,
        'delete_all': delete_all,
        'deleted_media': media_deleted,
        'ret': ret,
    })
