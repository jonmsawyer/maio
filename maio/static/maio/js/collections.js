/**
 * File: collections.js
 */

function preventDefaults (evt) {
    evt.preventDefault();
    evt.stopPropagation();
  }

function refresh_default(response) {
    if (response.is_default) {
        $(`#default_${response.id}`)
            .removeClass('btn-secondary')
            .addClass('btn-success')
            .html('<i class="bi bi-check"></i>')
            .prop('title', 'Is Default.');
    }
    else {
        $(`#default_${response.id}`)
            .removeClass('btn-success')
            .addClass('btn-secondary')
            .html('<i class="bi bi-slash-circle"></i>')
            .prop('title', 'Not default. Make Default?');
    }
}

function refresh_favorite(response) {
    if (response.is_favorite) {
        $(`#favorite_${response.id}`)
            .removeClass('btn-secondary')
            .addClass('btn-warning')
            .prop('title', 'Is favorite. Make unfavored?');
    }
    else {
        $(`#favorite_${response.id}`)
            .removeClass('btn-warning')
            .addClass('btn-secondary')
            .prop('title', 'Not favorite. Make favorite?');
    }
}

function new_collection(collection_id, show = false) {
    if (!collection_id) {
        $('#new_sort').val(null);
        $('#new_name').val(null);
        $('#new_default').prop('checked', false);
        $('#new_collection').slideDown();
        return;
    }
    if (collection_id == 'new') {
        var sort = $('#new_sort').val();
        var name = $('#new_name').val();
        var is_default = $('#new_default').prop('checked');

        Maio.log('Collection ID:', collection_id, 'Sort:', sort, 'Name:', name, 'Is Default?', is_default);

        var url = maio_conf.get('collections_uri');
        var data = {
            csrfmiddlewaretoken: maio_conf.get('csrf_token'),
            action: 'create',
            parent_id: null,
            sort: sort,
            name: name,
            is_default: is_default,
        };

        $.post(url, data, function(response) {
            Maio.log('New Collection Response:', response);
            if (response.error) {
                Maio.show_error_panel(response.error);
                return;
            }
            if (response.is_created) {
                $('.card-body').append(response.div);
                refresh_default(response);
            }
            else {
                Maio.show_error_panel(`A Collection with the name <code>${name}</code> already exists.`);
            }
        })
        .fail(function(response) {
            if (response.responseJSON && response.responseJSON.error) {
                Maio.show_error_panel(response.responseJSON.error);
            }
        });
    }
    else {
        if (show) {
            $(`#new_collection_${collection_id}`).slideDown();
        }
        else {
            var sort = $(`#new_sort_${collection_id}`).val();
            var name = $(`#new_name_${collection_id}`).val();
            var is_default = $(`#new_default_${collection_id}`).prop('checked');

            Maio.log('Parent ID:', collection_id, 'Sort:', sort, 'Name:', name, 'Is Default?', is_default);

            var url = maio_conf.get('collections_uri');
            var data = {
                csrfmiddlewaretoken: maio_conf.get('csrf_token'),
                action: 'create',
                parent_id: collection_id,
                sort: sort,
                name: name,
                is_default: is_default,
            };

            $.post(url, data, function(response) {
                Maio.log('New Collection Response:', response);
                if (response.error) {
                    Maio.show_error_panel(response.error);
                    return;
                }
                if (response.is_created) {
                    $(`#children_${collection_id}`).append(response.div);
                    refresh_default(response);
                }
                else {
                    Maio.show_error_panel(`A Collection with the name <code>${name}</code> already exists.`);
                }
            })
            .fail(function(response) {
                if (response.responseJSON && response.responseJSON.error) {
                    Maio.show_error_panel(response.responseJSON.error);
                }
            });
        }
    }
}

function dismiss_new_collection(collection_id) {
    if (!collection_id) {
        $('#new_sort').val(null);
        $('#new_name').val(null);
        $('#new_default').prop('checked', false);
        $('#new_collection').slideUp();
    }
    else {
        $(`#sort_${collection_id}`).val(null);
        $(`#name_${collection_id}`).val(null);
        $(`#default_${collection_id}`).prop('checked', false);
        $(`#new_collection_${collection_id}`).slideUp();
    }
}

function delete_collection(collection_id) {
    Maio.log('Delete Collection:', collection_id);
    var url = maio_conf.get('collections_url');
    var data = {
        csrfmiddlewaretoken: maio_conf.get('csrf_token'),
        action: 'delete',
        id: collection_id,
    };

    $.post(url, data, function(response) {
        Maio.log('Delete Collection Response:', response);
        if (response.error) {
            Maio.show_error_panel(response.error);
        }
        else if (response.is_deleted) {
            $(`#collection_${response.id}`).slideUp();
        }
        else {
            Maio.log('Unexpected response:', response);
        }
    })
    .fail(function(response) {
        if (response.responseJSON && response.responseJSON.error) {
            Maio.show_error_panel(response.responseJSON.error);
        }
    });
}

function make_default(collection_id) {
    Maio.log('Make Default:', collection_id);
    var url = maio_conf.get('collections_url');
    var data = {
        'csrfmiddlewaretoken': maio_conf.get('csrf_token'),
        'action': 'make_default',
        'id': collection_id,
    }
    $.post(url, data, function(response) {
        Maio.log('Make Default Response:', response);
        if (response.error) {
            Maio.show_error_panel(response.error);
        }
        else if (response.status && response.status == 'OK') {
            refresh_default(response);
        }
    })
}

function toggle_default(collection_id) {
    Maio.log('Toggle Default:', collection_id);
    var url = maio_conf.get('collections_url');
    var el = $(`#default_${collection_id}`);
    Maio.log(`data-default="${el.data('default')}"`);
    if (el.data('default')) {
        var data = {
            'csrfmiddlewaretoken': maio_conf.get('csrf_token'),
            'action': 'unmake_default',
            'id': collection_id,
        }
    }
    else {
        var data = {
            'csrfmiddlewaretoken': maio_conf.get('csrf_token'),
            'action': 'make_default',
            'id': collection_id,
        }
    }
    $.post(url, data, function(response) {
        Maio.log('Toggle Default Response:', response);
        if (response.error) {
            Maio.show_error_panel(response.error);
        }
        else if (response.status && response.status == 'OK') {
            if (el.data('default')) {
                el.data('default', false);
            }
            else {
                el.data('default', true);
            }
            refresh_default(response);
        }
    })
}

function toggle_favorite(collection_id) {
    Maio.log('Toggle Favorite:', collection_id);
    var url = maio_conf.get('collections_url');
    var el = $(`#favorite_${collection_id}`);
    Maio.log(`data-favorite="${el.data('favorite')}"`);
    if (el.data('favorite')) {
        var data = {
            'csrfmiddlewaretoken': maio_conf.get('csrf_token'),
            'action': 'unmake_favorite',
            'id': collection_id,
        }
    }
    else {
        var data = {
            'csrfmiddlewaretoken': maio_conf.get('csrf_token'),
            'action': 'make_favorite',
            'id': collection_id,
        }
    }
    $.post(url, data, function(response) {
        Maio.log('Toggle favorite Response:', response);
        if (response.error) {
            Maio.show_error_panel(response.error);
        }
        else if (response.status && response.status == 'OK') {
            if (el.data('favorite')) {
                el.data('favorite', false);
            }
            else {
                el.data('favorite', true);
            }
            refresh_favorite(response);
        }
    })
}

function change_name(collection_id) {
    el = $(`#collection_name_${collection_id}`);
    el_input = $(`#change_name_${collection_id}`);
    var url = maio_conf.get('collections_url');
    var data = {
        csrfmiddlewaretoken: maio_conf.get('csrf_token'),
        action: 'rename',
        id: el.data('id'),
        new_name: el_input.val(),
    }
    $.post(url, data, function(response) {
        Maio.log('Change Name Response:', response);
        if (response.error) {
            Maio.show_error_panel(response.error);
        }
        else {
            el.data('name', response.new_name);
            el.html(response.new_name);
            revert_name(collection_id);
        }
    })
}

function sort_collections() {
    Maio.log('Sort Collections')
    var url = maio_conf.get('collections_url');
    var data = {
        csrfmiddlewaretoken: maio_conf.get('csrf_token'),
        action: 'sort',
    }
    $.post(url, data, function(response) {
        Maio.log('Sort Collections Response:', response);
        if (response.error) {
            Maio.show_error_panel(response.error);
        }
        else {
            window.location.reload();
        }
    })
}

function focus_name(collection_id) {
    $(`#collection_name_${collection_id}`).hide();
    $(`#collection_rename_${collection_id}`).show();
    $(`#change_name_${collection_id}`).focus();
}

function revert_name(collection_id) {
    el = $(`#collection_name_${collection_id}`);
    rename_el = $(`#collection_rename_${collection_id}`);
    el.html(el.data('name'));
    el.show();
    rename_el.hide();
    $(`#change_name_${collection_id}`).val(el.data('name'));
}
