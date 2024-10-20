'''
File: rating.py

Module: ``maio.views.ajax.rating``
'''

from __future__ import annotations

from django.http import HttpRequest, JsonResponse

from maio.models import Media, MaioUser


def _love(request: HttpRequest, media: Media, action: str) -> JsonResponse:
    '''Love the Media.'''
    maio_user = MaioUser.objects.get(user=request.user)
    if action == 'delete':
        num = media.love_set.filter(user=maio_user).delete()
        return JsonResponse({
            'media_uuid': str(media.id),
            'num_deleted': num,
            'status': 'OK',
        })
    elif action == 'create':
        love, is_created = media.love_set.get_or_create(user=maio_user, media=media)
        return JsonResponse({
            'media_uuid': str(media.id),
            'love': str(love),
            'is_created': is_created,
            'status': 'OK',
        })
    return JsonResponse({'error': f'Unknown action: {action}'}, status=400)

def _bookmark(request: HttpRequest, media: Media, action: str) -> JsonResponse:
    '''Like the Media.'''
    maio_user = MaioUser.objects.get(user=request.user)
    if action == 'delete':
        num = media.like_set.filter(user=maio_user).delete()
        return JsonResponse({
            'media_uuid': str(media.id),
            'num_deleted': num,
            'status': 'OK',
        })
    elif action == 'create':
        like, is_created = media.like_set.get_or_create(user=maio_user, media=media)
        return JsonResponse({
            'media_uuid': str(media.id),
            'like': str(like),
            'is_created': is_created,
            'status': 'OK',
        })
    return JsonResponse({'error': f'Unknown action: {action}'}, status=400)

def _star(request: HttpRequest, media: Media, action: str) -> JsonResponse:
    '''Star the Media.'''
    return JsonResponse({'error': 'Rating type "star" is not implemented.'})

def rating(request: HttpRequest) -> JsonResponse:
    '''Set the rating for a given Media.'''
    if request.method == 'POST':
        try:
            media_uuid = request.POST.get('media_uuid');
            media = Media.objects.get(pk=media_uuid)
        except Media.DoesNotExist:
            return JsonResponse({'error': "You do not have access to change this media's rating."}, status=400)
        rating_type = request.POST.get('rating_type')
        action = request.POST.get('action', '')
        if rating_type == 'love':
            return _love(request, media, action)
        elif rating_type == 'bookmark':
            return _bookmark(request, media, action)
        elif rating_type == 'star':
            return _star(request, media, action)
        else:
            return JsonResponse({'error': f"Unknown rating type: {rating_type}"}, status=400)
    return JsonResponse({'error': 'I only understand POST requests.'}, status=400)
