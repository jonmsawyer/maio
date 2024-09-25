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
