/*
 * File: dashboard.js
 */

function change_thumbnail(media_uuid) {
    Maio.log('Change Thumbnail Config:', maio_conf);
    Maio.log("Media ID:", media_uuid);
    var url = maio_conf.get('change_thumbnail_url');
    var csrf_token = maio_conf.get('csrf_token');
    var index = maio_conf.get('index');
    Maio.log('Change Thumbnail URL:', url);
    Maio.log('CSRF Token:', csrf_token);
    Maio.log('Index:', index);
    Maio.log('Media UUID:', media_uuid);
    var _jqxhr = $.post(url, {
        'csrfmiddlewaretoken': csrf_token,
        'media_uuid': media_uuid,
        'index': index,
    }, function(response, data) {
        Maio.log('Response:', response);
        if (response.error) {
            Maio.show_error_panel(response.error);
            return;
        }
        $('#modal_change_thumbnail_'+media_uuid).modal('hide');
        $(`#medium_${media_uuid}`).attr('src', response.slideshow_tn_uri);
        $('.maio-thumbnail-current').removeClass('maio-thumbnail-current');
        $(`#change_thumbnail_${index}_${media_uuid}`).addClass('maio-thumbnail-current');
    })
    .fail(function(response) {
        Maio.log('Error Response:', response);
    })
}

function click_thumbnail(media_uuid, index) {
    Maio.log('Click Thumbnail Config:', maio_conf);
    Maio.log('Index:', index);
    var el = $(`#change_thumbnail_${index}_${media_uuid}`);
    unclick_thumbnail();
    el.addClass('maio-thumbnail-clicked');
    maio_conf.set('media_uuid', media_uuid);
    maio_conf.set('index', index);
}

function unclick_thumbnail() {
    Maio.log('Unclick Thumbnail Config:', maio_conf);
    $('.maio-thumbnail-clicked').removeClass('maio-thumbnail-clicked');
}

function delete_media(media_uuid) {
    Maio.log('Delete Media Config:', maio_conf);
    Maio.log("Media ID:", media_uuid);
    var url = maio_conf.get('delete_media_url');
    var csrf_token = maio_conf.get('csrf_token');
    var delete_all = $('#delete_all_'+media_uuid).is(':checked');
    Maio.log('Delete media URL', url);
    Maio.log('CSRF Token:', csrf_token);
    Maio.log('Delete all?', delete_all);
    var _jqxhr = $.post(url, {
        'csrfmiddlewaretoken': csrf_token,
        'media_uuid': media_uuid,
        'delete_all': delete_all,
    }, function(response, data) {
        Maio.log('Response:', response);
        Maio.log('Data:', data);
        $('#modal_'+media_uuid).modal('hide');
        if (response.error) {
            Maio.show_error_panel(response.error);
            return;
        }
        for (var key in response.deleted_media) {
            var uid = response.deleted_media[key];
            Maio.log('Remove:', response.deleted_media[key]);
            $('#card_'+uid).hide();
        }
    })
    .fail(function(response) {
        Maio.log('Error Response:', response);
    })
}

function highlight_media(media_uuid) {
    var el = $('#card_'+media_uuid);
    el.addClass('maio-highlight-media');
}

function unhighlight_media(media_uuid) {
    var el = $('#card_'+media_uuid);
    el.removeClass('maio-highlight-media');
}

function stop_audio_playback(media_uuid) {
    var el = $('#audio_'+media_uuid);
}

function choose_reset() {
    var url = window.location.href;
    url = Maio.update_url_parameter(url, 'per_page', null); // per_page comes before page due to regex substitution.
    url = Maio.update_url_parameter(url, 'page', null);
    url = Maio.update_url_parameter(url, 'media_type', null);
    url = Maio.update_url_parameter(url, 'love', null);
    url = Maio.update_url_parameter(url, 'bookmark', null);
    url = Maio.update_url_parameter(url, 'star', null);
    window.location.assign(url);
    return;
}


function choose_page(instance, page = null) {
    if (page) {
        url = Maio.update_url_parameter(window.location.href, 'page', page);
        window.location.assign(url);
        return;
    }

    $(`#maio_choose_page_${instance}`).toggle();
}

function choose_media_type(media_type) {
    if (media_type) {
        url = Maio.update_url_parameter(window.location.href, 'media_type', media_type);
        window.location.assign(url);
        return;
    }
}

function choose_love(love) {
    if (love) {
        url = Maio.update_url_parameter(window.location.href, 'love', love);
        window.location.assign(url);
        return;
    }
}

function choose_bookmark(bookmark) {
    if (bookmark) {
        url = Maio.update_url_parameter(window.location.href, 'bookmark', bookmark);
        window.location.assign(url);
        return;
    }
}

function choose_star(star) {
    if (star) {
        url = Maio.update_url_parameter(window.location.href, 'star', star);
        window.location.assign(url);
        return;
    }
}

function choose_per_page(per_page) {
    if (per_page) {
        url = Maio.update_url_parameter(window.location.href, 'per_page', per_page);
        window.location.assign(url);
        return;
    }
}

function love(media_uuid) {
    var el = $(`#rating_${media_uuid} .maio-love`);
    var url = maio_conf.get('rating_url');
    var csrf_token = maio_conf.get('csrf_token');

    if (el.data('loved')) {
        Maio.log('Unloving:', media_uuid);
        $.post(url, {
            csrfmiddlewaretoken: csrf_token,
            rating_type: 'love',
            action: 'delete',
            media_uuid: media_uuid,
        }, function(response) {
            Maio.log('Unloving response:', response);
            if (response.status && response.status == 'OK') {
                el.removeClass('bi-heart-fill').addClass('bi-heart');
                el.data('loved', false);
            }
        });
    } else {
        Maio.log('Loving:', media_uuid);
        $.post(url, {
            csrfmiddlewaretoken: csrf_token,
            rating_type: 'love',
            action: 'create',
            media_uuid: media_uuid,
        }, function(response) {
            Maio.log('Loving response:', response);
            if (response.status && response.status == 'OK') {
                el.addClass('bi-heart-fill').removeClass('bi-heart');
                el.data('loved', true);
            }
        });
    }
}

function bookmark(media_uuid) {
    var el = $(`#rating_${media_uuid} .maio-bookmark`);
    var url = maio_conf.get('rating_url');
    var csrf_token = maio_conf.get('csrf_token');

    if (el.data('bookmarked')) {
        Maio.log('Unbookmarking:', media_uuid);
        $.post(url, {
            csrfmiddlewaretoken: csrf_token,
            rating_type: 'bookmark',
            action: 'delete',
            media_uuid: media_uuid,
        }, function(response) {
            Maio.log('Unbookmarking response:', response);
            if (response.status && response.status == 'OK') {
                el.removeClass('bi-bookmark-check-fill').addClass('bi-bookmark-check');
                el.data('bookmarked', false);
            }
        });
    } else {
        Maio.log('Bookmarking:', media_uuid);
        $.post(url, {
            csrfmiddlewaretoken: csrf_token,
            rating_type: 'bookmark',
            action: 'create',
            media_uuid: media_uuid,
        }, function(response) {
            Maio.log('Bookmarking response:', response);
            if (response.status && response.status == 'OK') {
                el.addClass('bi-bookmark-check-fill').removeClass('bi-bookmark-check');
                el.data('bookmarked', true);
            }
        });
    }
}

function rate(media_uuid, rating) {
    var el = $(`#rating_${media_uuid} .maio-star-${rating}`);
    var starred = $(`#rating_${media_uuid} .maio-star`);
    var url = maio_conf.get('rating_url');
    var csrf_token = maio_conf.get('csrf_token');

    if (el.data('starred')) {
        Maio.log('Unstarring:', media_uuid);
        $.post(url, {
            csrfmiddlewaretoken: csrf_token,
            rating_type: 'rate',
            rating_number: rating,
            action: 'delete',
            media_uuid: media_uuid,
        }, function(response) {
            Maio.log('Unstarring response:', response);
            if (response.status && response.status == 'OK') {
                starred.each(function (index) {
                    var star = $(this);
                    star.data('starred', false);
                    star.data('rating', 0);
                    star.removeClass('bi-star-fill').addClass('bi-star');
                });
            }
        });
    } else {
        Maio.log('Starring:', media_uuid);
        $.post(url, {
            csrfmiddlewaretoken: csrf_token,
            rating_type: 'rate',
            rating_number: rating,
            action: 'create',
            media_uuid: media_uuid,
        }, function(response) {
            Maio.log('Starring response:', response);
            if (response.status && response.status == 'OK') {
                starred.each(function (index) {
                    var star = $(this);
                    star.data('starred', false);
                    star.data('rating', rating);
                    if (star.data('starnum') <= rating) {
                        star.addClass('bi-star-fill').removeClass('bi-star');
                    } else {
                        star.removeClass('bi-star-fill').addClass('bi-star');
                    }
                });
                el.addClass('bi-star-fill').removeClass('bi-star');
                el.data('starred', true);
            }
        });
    }
}
