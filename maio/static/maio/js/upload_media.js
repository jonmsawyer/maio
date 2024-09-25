/**
 * File: upload_media.js
 *
 * Progress bar example thanks to: https://jsfiddle.net/41go76g4/
 */

function get_extension(name) {
  var name_arr = name.split('.');
  return name_arr[name_arr.length - 1];
}

function is_restricted_type(config, theFile, maio_type, content_type) {
  var r_mime_type = config.get('restricted_mime_types');
  for (const r_mime_type_idx in r_mime_type) {
    Maio.log(`Comparing restricted MIME type: [${r_mime_type_idx}] ${r_mime_type[r_mime_type_idx]}...`);
    if (`application/${content_type}` == r_mime_type[r_mime_type_idx]) {
      return true;
    }
  }

  var r_extension = config.get('restricted_extensions');
  for (const r_extension_idx in r_extension) {
    Maio.log(`Comparing restricted extension: [${r_extension_idx}] ${r_extension[r_extension_idx]}...`);
    if (get_extension(theFile.name) == r_extension[r_extension_idx]) {
      return true;
    }
  }

  return false;
}

function onload_timer(name, index) {
  var timer_amount = 1000;
  if (maio_conf.get('global_index') > 2000) {
    timer_amount = 5000;
  }
  else if (maio_conf.get('global_index') > 1500) {
    timer_amount = 4000;
  }
  else if (maio_conf.get('global_index') > 1000) {
    timer_amount = 3000;
  }
  else if (maio_conf.get('global_index') > 500) {
    timer_amount = 2000;
  }
  Maio.input_timer($(`.maio-${name}-spinner`)[0], function(evt) {
    $(`.maio-${name}-spinner`).removeClass('visible').addClass('hidden');
    $(`.maio-${name}-progress`).removeClass('visible').addClass('hidden');

    // Enable form attributes
    $('input[name=submit]').removeAttr('disabled');
    $('#upload_label').removeAttr('disabled');
    $('#id_auto_upload_media').removeAttr('disabled');
    $('#id_skip_duplicates').removeAttr('disabled');
    // End enable.

    Maio.update_debug_config();
    update_num_preview_files(maio_conf);
    if (name == 'choose') {
      if ($('#id_auto_upload_media').is(':checked')) {
        upload_files(evt);
      }
    }
  }, timer_amount);
  updateProgress(name, index, 1);
}

function onload_file_reader(theFile, index, config, maio_type, content_type, file_index) {
  return function(e) {
    // Render thumbnail.
    var tn_html = `
              <img src="${maio_conf.get('other_tn')}" alt="${Maio.escape(theFile.name)}" title="${Maio.escape(theFile.name)}" class="maio-upload-image">
    `;
    // Maio.log('tn_html', tn_html);
    if (maio_type == 'image') {
      tn_html = `
              <img src="${e.target.result}" alt="${Maio.escape(theFile.name)}" title="${Maio.escape(theFile.name)}" class="maio-upload-image">
      `;
    }
    if (maio_type == 'audio') {
      tn_html = `
              <img src="${maio_conf.get('audio_tn')}" alt="${Maio.escape(theFile.name)}" title="${Maio.escape(theFile.name)}" class="maio-upload-image"></img>
      `;
    }
    if (maio_type == 'video') {
      tn_html = `
              <img src="${maio_conf.get('video_tn')}" alt="${Maio.escape(theFile.name)}" title="${Maio.escape(theFile.name)}" class="maio-upload-image"></img>
      `;
      if (
        content_type == 'webm' ||
        content_type == 'ogg' ||
        content_type == 'mp4'
      ) {
        tn_html = `
              <video src="${URL.createObjectURL(theFile)}#t=10" alt="${Maio.escape(theFile.name)}" title="${Maio.escape(theFile.name)}" class="maio-upload-image"></video>
        `;
      }
    }
    if (maio_type == 'document') {
      tn_html = `
              <img src="${maio_conf.get('document_tn')}" alt="${Maio.escape(theFile.name)}" title="${Maio.escape(theFile.name)}" class="maio-upload-image">
      `;
      if (content_type == 'text') {
        tn_html = `
              <img src="${maio_conf.get('text_tn')}" alt="${Maio.escape(theFile.name)}" title="${Maio.escape(theFile.name)}" class="maio-upload-image">
        `;
      }
      if (content_type == 'pdf') {
        tn_html = `
              <img src="${maio_conf.get('pdf_tn')}" alt="${Maio.escape(theFile.name)}" title="${Maio.escape(theFile.name)}" class="maio-upload-image">
        `;
      }
    }
    if (maio_type == 'other') {
      tn_html = `
              <img src="${maio_conf.get('other_tn')}" alt="${Maio.escape(theFile.name)}" title="${Maio.escape(theFile.name)}" class="maio-upload-image">
      `;
      if (content_type == 'x-zip-compressed') {
        tn_html = `
              <img src="${maio_conf.get('archive_tn')}" alt="${Maio.escape(theFile.name)}" title="${Maio.escape(theFile.name)}" class="maio-upload-image">
        `;
      }
    }
    var tn_div = document.createElement('div');
    tn_div.innerHTML = tn_html;
    tn_div.style = "display: inline;";
    var maio_div_index = '';
    if (maio_conf.get('render_div_index')) {
      maio_div_index = `<div class="maio-div-index">${file_index}</div>`;
    }
    var div = document.createElement('div');
    var upload_media_view_toggle = config.get('upload_media_view_toggle');
    var upload_media_class = 'bi-caret-up-fill';
    var meta_data_index_class = '';
    if (upload_media_view_toggle == false) {
      upload_media_class = 'bi-caret-down';
      meta_data_index_class = 'hidden';
    }
    var meta_data_html = `
            <button class="btn btn-secondary btn-sm"
                    type="button"
                    style="font-weight: bold;"
                    title="${Maio.escape(theFile.name)}"
                    onclick="toggle(${file_index});"
            >
              ${Maio.trim_filename(theFile.name)} <i id="metadata_caret_${file_index}" class="bi ${upload_media_class}"></i>
            </button>
            <div style="font-size: 10pt;">
              <div id="metadata_index_${file_index}" data-toggle="${upload_media_view_toggle}" class="${meta_data_index_class}">
                <div>${Maio.escape(String(theFile.size.toString()))} Bytes</div>
                <div>${Maio.escape(theFile.type)} (${maio_type})</div>
                <div>${Maio.escape(String(theFile.lastModifiedDate))}</div>
              </div>
              ${maio_div_index}
            </div>
    `;
    if (maio_conf.get('upload_media_view') == 'thumbnails') {
      var meta_data_html = `
          <div class="col" style="font-weight: bold; text-align: center;" title="${Maio.escape(theFile.name)}">
            ${Maio.trim_filename(theFile.name)}
          </div>
      `;
    }
    div.innerHTML = `
      <div class="alert alert-secondary col" style="position: relative;">
        <div style="position: absolute; top: 0px; right: 0px; z-index: 1;">
          <button type="button"
                  class="btn-close btn-sm"
                  aria-label="Close"
                  style="z-index: 1;"
                  onclick="removePreview(${file_index});"
          ></button>
        </div>
        <div class="row">
          <div class="col col-12" style="text-align: center; padding-bottom: 16px; ">
            ${tn_html}
          </div>
          <div class="col col-12" style="text-align: center;">
            ${meta_data_html}
          </div>
        </div>
      </div>
    `;
    $(div).addClass('col');
    $(div).attr('id', `preview_index_${file_index}`);
    $(div).addClass('maio-file-preview');
    $(div).prependTo($('#list'));

    onload_timer('choose', index);
  };
}

/**
 * handleFileSelect
 *
 * @param {domEvent} evt
 */
function handleFileSelect(evt, name) {
  global_index = maio_conf.get('global_index');
  var files = [];
  if (evt.clipboardData && evt.clipboardData.files) {
    files = evt.clipboardData.files; // FileList object
  }
  else if (evt.target && evt.target.files) {
    files = evt.target.files; // FileList object
  }
  else if (evt.dataTransfer && evt.dataTransfer.files) {
    files = evt.dataTransfer.files; // FileList object
  }
  else if (evt.files) {
    files = evt.files;
  } else {
    return;
  }

  initializeProgress(name, files.length);
  var index = 0;

  // Loop through the FileList and render image files as thumbnails.
  for (var i = 0, f; f = files[i]; i++) {
    var mime_type_regex = /^(.+)\/(.+)$/g;
    var mime_type_matches = mime_type_regex.exec(f.type);
    var maio_type = 'other';
    var mime_type = 'other';
    var content_type = 'other';
    var file_index = global_index + index;
    try {
      mime_type = mime_type_matches[1];
      content_type = mime_type_matches[2];
    } catch (error) {
      ; // do nothing
    }

    maio_type = mime_type;

    if (mime_type == 'text') {
      maio_type = 'document';
      content_type = 'text';
    }

    if (
      content_type == 'pdf' ||
      content_type == 'msword' ||
      content_type == 'vnd.kde.kword' ||
      content_type == 'vnd.lotus-wordpro' ||
      content_type == 'vnd.ms-word.document.macroenabled.12' ||
      content_type == 'vnd.ms-word.template.macroenabled.12' ||
      content_type == 'vnd.openxmlformats-officedocument.wordprocessingml.document' ||
      content_type == 'vnd.openxmlformats-officedocument.wordprocessingml.document.glossary+xml' ||
      content_type == 'vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml' ||
      content_type == 'vnd.openxmlformats-officedocument.wordprocessingml.template' ||
      content_type == 'vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml' ||
      content_type == 'vnd.wordperfect' ||
      content_type == 'wordperfect5.1' ||
      content_type == 'x-abiword'
    ) {
      maio_type = 'document';
    }

    if (content_type == 'x-zip-compressed') {
      maio_type = 'other';
    }

    if (is_restricted_type(maio_conf, f, maio_type, content_type)) {
      index += 1;
      onload_timer(name, file_index);
      continue;
    }

    var reader = new FileReader();
    reader.onload = onload_file_reader(f, i, maio_conf, maio_type, content_type, file_index);

    maio_conf.get('files_to_upload').set(file_index, new Config({
      file: f,
      name: Maio.validate_filename(f.name),
      size: f.size,
      type: f.type,
      last_modified: f.lastModified,
      last_modified_date: String(f.lastModifiedDate),
      enabled: true,
      reason: null,
      is_uploaded: false,
      file_index: file_index,
    }));
    update_num_preview_files(maio_conf);

    if (
      maio_type == 'image' ||
      maio_type == 'audio' ||
      maio_type == 'video'
    ) {
      Maio.log(`Reading file \`${maio_type}\` as data URL`);
      reader.readAsDataURL(f);
    } else if (maio_type == 'document' && content_type == 'text') {
      Maio.log('Reading file as `other` as text');
      reader.readAsText(f);
    } else {
      reader.readAsArrayBuffer(f);
      Maio.log('Reading unknown file as an Array Buffer.');
    }

    index += 1;
  }

  global_index = global_index + index;
  maio_conf.set('global_index', global_index);
}

function preventDefaults (evt) {
  evt.preventDefault();
  evt.stopPropagation();
}

function highlight(evt) {
  dropArea.classList.add('highlight');
}

function unhighlight(evt) {
  dropArea.classList.remove('highlight');
}

function handleDrop(evt) {
  handleFileSelect(evt, 'choose');
}

function handlePaste(evt) {
  handleFileSelect(evt, 'choose');
}

function uploadFile(file, idx, config, file_index) {
  var url = maio_conf.get('upload_media_url');
  var formData = new FormData();
  var resp;
  var xhr = new XMLHttpRequest();
  xhr.open('POST', url, true);

  xhr.upload.addEventListener("progress", function(e) {
    updateProgress('upload', idx, (e.loaded / e.total) || 1)
  })

  xhr.addEventListener('readystatechange', function(e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
      Maio.log('Upload success! Response:', xhr);
      resp = JSON.parse(xhr.response);
      Maio.log('Response obj:', resp);
      var prev_index_div = $(`#preview_index_${resp.file_index} > div`);
      if (resp.is_duplicate) {
        prev_index_div
          .removeClass('alert-secondary')
          .removeClass('alert-success')
          .removeClass('alert-danger')
          .addClass('alert-warning');
      } else {
        prev_index_div
          .removeClass('alert-secondary')
          .removeClass('alert-warning')
          .removeClass('alert-danger')
          .addClass('alert-success');
      }
      config.get('files_to_upload').get(file_index).set('is_uploaded', true);
    }
    else if (xhr.readyState == 4 && xhr.status != 200) {
      Maio.log('Upload failed! Response:', xhr);
      resp = JSON.parse(xhr.response);
      Maio.log('Response obj:', resp);
      var prev_index_div = $(`#preview_index_${resp.file_index} > div`);
      prev_index_div
        .removeClass('alert-secondary')
        .removeClass('alert-warning')
        .removeClass('alert-success')
        .addClass('alert-danger');
      prev_index_div.data('uploaded', false);
      }
  })

  formData.append('csrfmiddlewaretoken', config.get('csrf_token'));
  formData.append('skip_duplicates', $('#id_skip_duplicates').is(':checked'));
  formData.append('from_ajax', true);
  formData.append('file_index', file_index);
  formData.append('content_file', file);
  xhr.send(formData);
}

function initializeProgress(name, numFiles) {
  progressBar = $(`#${name}_progress_bar`);
  progressBar.value = 0;
  progressBar.css('width', '5%');
  if (name == 'choose') {
    chooseProgressItems = [];
    progressItems = chooseProgressItems;
  } else if (name == 'upload') {
    uploadProgressItems = [];
    progressItems = uploadProgressItems;
  } else {
    throw Exception(`Indicator with name '${name}' is not valid.`);
  }

  for (let i = numFiles; i > 0; i--) {
    progressItems.push(0);
  }

  // Show spinner and progress.
  $(`.maio-${name}-spinner`).removeClass('hidden').addClass('visible');
  $(`.maio-${name}-progress`).removeClass('hidden').addClass('visible');

  // Disable input form attributes
  $('input[name=submit]').attr('disabled', 'disabled');
  $('#upload_label').attr('disabled', 'disabled');
  $('#id_auto_upload_media').attr('disabled', 'disabled');
  $('#id_skip_duplicates').attr('disabled', 'disabled');

  // Show the previews section.
  $('#maio_preview_files').slideDown();
}

function updateProgress(name, fileNumber, percent) {
  fileNumber = parseInt(fileNumber);
  progressBar = $(`#${name}_progress_bar`);
  if (name == 'choose') {
    progressItems = chooseProgressItems;
  } else if (name == 'upload') {
    progressItems = uploadProgressItems;
  } else {
    throw Exception(`Indicator with name '${name}' is not valid.`);
  }
  progressItems[fileNumber] = percent;
  let total = progressItems.reduce((tot, curr) => tot + curr, 0) / progressItems.length * 100;
  progressBar.value = total;
  $(progressBar).html(`${Math.round(total).toFixed(0)}%`);
  $(progressBar).css('width', `${total}%`);
}

function removePreview(index) {
  var el = $(`#preview_index_${index}`);
  var el_div = $(`#preview_index_${index} > div`)
  el_div.removeClass('alert-secondary').addClass('alert-danger');
  el.fadeOut();
  maio_conf.get('files_to_upload').delete_key(index);
  Maio.update_debug_config();
  update_num_preview_files(maio_conf);
}

function toggle(index) {
  var el = $(`#metadata_index_${index}`);
  if (el.data('toggle')) {
    el.data('toggle', false);
    el.slideUp();
    $(`#metadata_caret_${index}`).removeClass('bi-caret-up-fill').addClass('bi-caret-down');
  } else {
    el.data('toggle', true);
    el.slideDown();
    $(`#metadata_caret_${index}`).removeClass('bi-caret-down').addClass('bi-caret-up-fill');
  }
}

function update_num_preview_files(config) {
  $('#num_preview_files').html(config.get('files_to_upload').length());
}

function upload_files(evt) {
  var files_to_upload = maio_conf.get('files_to_upload');
  initializeProgress('upload', files_to_upload.length());
  var num = 0;
  for (var idx in files_to_upload.config) {
    var f = files_to_upload.config[idx].get('file');
    if (!files_to_upload.config[idx].get('is_uploaded')) {
      uploadFile(f, num, maio_conf, idx);
      onload_timer('upload', idx);
    }
    else {
      Maio.log(`File '${f.name}' has already been uploaded. Not uploading.`);
      onload_timer('upload', num);
    }
    num += 1;
  }
  if (num == 0) {
    onload_timer('upload', num);
  }
}
