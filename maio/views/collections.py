'''
File: collections.py

Module: ``maio.views.collections``

Collections view.
'''

from __future__ import annotations
from typing import Optional

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.utils import IntegrityError
from django.db.models.manager import BaseManager

from maio.lib import pre_populate_context_dict
from maio.models import Collection


def _get(request: HttpRequest, collection_id: Optional[str] = None) -> JsonResponse | HttpResponse:
    '''Process GET request.'''
    cd = pre_populate_context_dict(request, {})
    collection_list: list[dict[str, Optional[str | int | bool]]] = []

    try:
        collection_list = Collection.get_list(request, collection_id)
    except Collection.DoesNotExist:
        if collection_id:
            return JsonResponse({'error': 'That Collection does not exist for this user.'}, status=404)

    # try:
    #     favorite_list = Collection.get_favorites(request)
    # except:
    if collection_id:
        return JsonResponse({
            'status': 'OK',
            'num_items': len(collection_list),
        })

    cd['collections'] = collection_list
    cd['js_debug'] = 'true'
    return render(request, 'maio/collections.html', cd)

def _post_create(request: HttpRequest) -> JsonResponse:
    '''post add'''
    parent_id = request.POST.get('parent_id') if request.POST.get('parent_id') else None
    parent = None
    if parent_id:
        try:
            parent = Collection.objects.get(id=parent_id, user=request.maio_user)
        except Collection.DoesNotExist:
            return JsonResponse({'error': 'The parent collection with that ID does not exist for this user.'}, status=400)
    try:
        sort = int(request.POST.get('sort')) if request.POST.get('sort') else 0
    except ValueError:
        sort = 0
    name = request.POST.get('name').strip() if request.POST.get('name') else None
    if not name:
        return JsonResponse({'error': 'Name must not be empty.'}, status=400)
    if request.POST.get('is_default', '') == 'true':
        is_default = True
    else:
        is_default = False
    thumbnail = None
    collection, is_created = Collection.objects.get_or_create(
        parent=parent,
        user=request.maio_user,
        name=name,
        defaults={
            'sort': sort,
            'is_default': is_default,
            'thumbnail': thumbnail,
        }
    )
    indent = 0
    current_collection = collection
    while current_collection is not None:
        if current_collection.parent:
            indent += 1
            current_collection = current_collection.parent
        else:
            current_collection = None
    return JsonResponse({
        'status': 'OK',
        'id': str(collection.id),
        'parent_id': str(parent.id) if parent else None,
        'sort': sort,
        'name': name,
        'is_default': is_default,
        'thumbnail_uri': thumbnail.uri if thumbnail else '',
        'date_added': str(collection.date_added),
        'date_modified': str(collection.date_modified),
        'is_created': is_created,
        'div': render_to_string('maio/_collections.html', {
            'collections': [collection],
            'indent': indent,
        }),
    })

def _post_delete(request: HttpRequest) -> JsonResponse:
    '''post delete'''
    collection_id = request.POST.get('id')
    try:
        res = Collection.objects.get(pk=collection_id, user=request.maio_user).delete()
        return JsonResponse({
            'status': 'OK',
            'is_deleted': True,
            'id': collection_id,
            'res': res,
        })
    except Collection.DoesNotExist:
        return JsonResponse({'error': 'This Collection does not exist for this user.'}, status=400)

def _post_make_default(request: HttpRequest) -> JsonResponse:
    '''post make default'''
    collection_id = request.POST.get('id')
    try:
        Collection.objects.filter(pk=collection_id, user=request.maio_user).update(is_default=True)
        return JsonResponse({
            'status': 'OK',
            'action': 'make_default',
            'is_default': True,
            'id': collection_id,
        })
    except Collection.DoesNotExist:
        return JsonResponse({'error': 'This Collection does not exist for this user.'}, status=400)

def _post_unmake_default(request: HttpRequest) -> JsonResponse:
    '''post unmake default'''
    collection_id = request.POST.get('id')
    try:
        Collection.objects.filter(pk=collection_id, user=request.maio_user).update(is_default=False)
        return JsonResponse({
            'status': 'OK',
            'action': 'unmake_default',
            'is_default': False,
            'id': collection_id,
        })
    except Collection.DoesNotExist:
        return JsonResponse({'error': 'This Collection does not exist for this user.'}, status=400)

def _post_make_favorite(request: HttpRequest) -> JsonResponse:
    '''post make favorite'''
    collection_id = request.POST.get('id')
    try:
        Collection.objects.filter(pk=collection_id, user=request.maio_user).update(is_favorite=True)
        return JsonResponse({
            'status': 'OK',
            'action': 'make_favorite',
            'is_favorite': True,
            'id': collection_id,
        })
    except Collection.DoesNotExist:
        return JsonResponse({'error': 'This Collection does not exist for this user.'}, status=400)

def _post_unmake_favorite(request: HttpRequest) -> JsonResponse:
    '''post unmake favorite'''
    collection_id = request.POST.get('id')
    try:
        Collection.objects.filter(pk=collection_id, user=request.maio_user).update(is_favorite=False)
        return JsonResponse({
            'status': 'OK',
            'action': 'unmake_favorite',
            'is_favorite': False,
            'id': collection_id,
        })
    except Collection.DoesNotExist:
        return JsonResponse({'error': 'This Collection does not exist for this user.'}, status=400)

def _post_rename(request: HttpRequest) -> JsonResponse:
    '''post unmake favorite'''
    collection_id = request.POST.get('id')
    if collection_id is None:
        return JsonResponse({'error': 'Missing parameter `id`.'}, status=400)
    name = request.POST.get('new_name')
    if name is None:
        return JsonResponse({'error': 'Missing parameter `new_name`.'}, status=400)
    collection = Collection.objects.get(pk=collection_id, user=request.maio_user)
    parent = collection.parent
    try:
        collection.name = name
        collection.save()
    except IntegrityError:
        return JsonResponse({
            'error': (f'A Collection with name <code>{name}</code> already exists '
                      f'under <code>{parent.name}</code>.')
        })
    return JsonResponse({
        'id': collection_id,
        'new_name': name,
    })

def _sort_collections(request: HttpRequest, collections: Optional[BaseManager[Collection]] = None) -> int:
    '''Sort this collection.'''
    if collections is None:
        collections = Collection.objects.filter(parent=None, user=request.maio_user)

    sort: int = 0
    num_collections: int = 0

    for collection in collections:
        collection.sort = sort
        collection.save()
        sort += 5
        num_collections += 1
        num_collections += _sort_collections(request, collection.collection_set.all())

    return num_collections

def _post_sort(request: HttpRequest) -> JsonResponse:
    '''Sort this collection and all subcollections.'''
    try:
        return JsonResponse({
            'status': 'OK',
            'action': 'sort',
            'num_collections': _sort_collections(request),
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
        })

def _post(request: HttpRequest) -> JsonResponse:
    '''Process POST request.'''
    action = request.POST.get('action')
    if not action:
        return JsonResponse({'error': 'Parameter `action` must be set.'}, status=400)
    if action == 'create':
        return _post_create(request)
    elif action == 'delete':
        return _post_delete(request)
    elif action == 'make_default':
        return _post_make_default(request)
    elif action == 'unmake_default':
        return _post_unmake_default(request)
    elif action == 'make_favorite':
        return _post_make_favorite(request)
    elif action == 'unmake_favorite':
        return _post_unmake_favorite(request)
    elif action == 'rename':
        return _post_rename(request)
    elif action == 'sort':
        return _post_sort(request)
    else:
        return JsonResponse({'error': 'Invalid action.'}, status=400)

def collections(
    request: HttpRequest,
    collection_id: Optional[str] = None,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse | JsonResponse:
    if request.method == 'GET':
        return _get(request, collection_id)
    if request.method == 'POST':
        return _post(request)
