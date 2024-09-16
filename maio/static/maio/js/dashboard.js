/*
 * File: dashboard.js
 */

function delete_media(media_uuid) {
    console.log("Media ID:", media_uuid);
}

function highlight_media(media_uuid) {
    var el = $(media_uuid);
    el.addClass('highlight_media');
}

function unhighlight_media(media_uuid) {
    var el = $(media_uuid);
    el.removeClass('highlight_media');
}
