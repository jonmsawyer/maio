/*
 * File: dashboard.js
 */

var config;

function change_thumbnail(media_uuid) {
    console.log('Change Thumbnail Config:', config);
    console.log("Media ID:", media_uuid);
    var url = config.get('change_thumbnail_url');
    var csrf_token = config.get('csrf_token');
    var index = config.get('index');
    console.log('Change Thumbnail URL:', url);
    console.log('CSRF Token:', csrf_token);
    console.log('Index:', index);
    console.log('Media UUID:', media_uuid);
    var _jqxhr = $.post(url, {
        'csrfmiddlewaretoken': csrf_token,
        'media_uuid': media_uuid,
        'index': index,
    }, function(response, data) {
        console.log('Response:', response);
        $('#modal_change_thumbnail_'+media_uuid).modal('hide');
        $(`#medium_${media_uuid}`).attr('src', response.slideshow_tn_uri);
    })
    .fail(function(response) {
        console.log('Error Response:', response);
    })
}

function click_thumbnail(media_uuid, index) {
    console.log('Click Thumbnail Config:', config);
    console.log('Index:', index);
    var el = $(`#change_thumbnail_${index}_${media_uuid}`);
    unclick_thumbnail();
    el.addClass('maio-thumbnail-clicked');
    config.set('media_uuid', media_uuid);
    config.set('index', index);
}

function unclick_thumbnail() {
    console.log('Unclick Thumbnail Config:', config);
    $('.maio-thumbnail-clicked').removeClass('maio-thumbnail-clicked');
}

function delete_media(media_uuid) {
    console.log('Delete Media Config:', config);
    console.log("Media ID:", media_uuid);
    var url = config.get('delete_media_url');
    var csrf_token = config.get('csrf_token');
    var delete_all = $('#delete_all_'+media_uuid).is(':checked');
    console.log('Delete media URL', url);
    console.log('CSRF Token:', csrf_token);
    console.log('Delete all?', delete_all);
    var _jqxhr = $.post(url, {
        'csrfmiddlewaretoken': csrf_token,
        'media_uuid': media_uuid,
        'delete_all': delete_all,
    }, function(response, data) {
        console.log('Response:', response);
        console.log('Data:', data);
        $('#modal_'+media_uuid).modal('hide');
        for (var key in response.deleted_media) {
            var uid = response.deleted_media[key];
            console.log('Remove:', response.deleted_media[key]);
            $('#card_'+uid).hide();
        }
    })
    .fail(function(response) {
        console.log('Error Response:', response);
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
