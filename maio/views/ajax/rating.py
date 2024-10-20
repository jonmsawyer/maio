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
    '''Bookmark the Media.'''
    maio_user = MaioUser.objects.get(user=request.user)
    if action == 'delete':
        num = media.bookmark_set.filter(user=maio_user).delete()
        return JsonResponse({
            'media_uuid': str(media.id),
            'num_deleted': num,
            'status': 'OK',
        })
    elif action == 'create':
        bookmark, is_created = media.bookmark_set.get_or_create(user=maio_user, media=media)
        return JsonResponse({
            'media_uuid': str(media.id),
            'bookmark': str(bookmark),
            'is_created': is_created,
            'status': 'OK',
        })
    return JsonResponse({'error': f'Unknown action: {action}'}, status=400)

def _rate(request: HttpRequest, media: Media, action: str) -> JsonResponse:
    '''Rate the Media.'''
    maio_user = MaioUser.objects.get(user=request.user)
    if action == 'delete':
        num = media.rating_set.filter(user=maio_user).delete()
        return JsonResponse({
            'media_uuid': str(media.id),
            'num_deleted': num,
            'status': 'OK',
        })
    elif action == 'create':
        rating_number = request.POST.get('rating_number')
        if not rating_number:
            return JsonResponse({'error': 'Missing parameter `rating_number`.'}, status=400)
        try:
            rating_number = int(rating_number)
            if rating_number < 1 or rating_number > 5:
                raise ValueError('Rating number must an integer between 1 and 5, inclusive.')
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        rated, is_created = media.rating_set.get_or_create(
            user=maio_user,
            media=media,
        )
        rated.rating = int(rating_number)
        rated.save()
        return JsonResponse({
            'media_uuid': str(media.id),
            'rating': rated.rating,
            'is_created': is_created,
            'status': 'OK',
        })

    return JsonResponse({'error': f'Unknown action: {action}'}, status=400)

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
        elif rating_type == 'rate':
            return _rate(request, media, action)
        else:
            return JsonResponse({'error': f"Unknown rating type: {rating_type}"}, status=400)
    return JsonResponse({'error': 'I only understand POST requests.'}, status=400)
