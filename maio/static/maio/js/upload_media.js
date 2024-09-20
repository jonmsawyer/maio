/**
 * File: upload_media.js
 *
 * Thanks to: https://jsfiddle.net/41go76g4/
 */

var config;

function escape(text) {
  return text.replace(/"/g, '&quot;');
}

function process_properties(index) {
  var index_str = String(index);
  var el = document.getElementById('index_'+index_str);
  console.log(`Processing Width and Height for index ${index}. El:`, el, 'Width:', el.width, 'Height:', el.height);
  $('#width_index_'+index_str).html(String(el.width));
  $('#height_index_'+index_str).html(String(el.height));
}

/**
 * handleFileSelect
 *
 * @param {domEvent} evt
 */
function handleFileSelect(evt) {
  console.log('Config:', config);
  var files = evt.target.files; // FileList object
  var index = 0;

  // Loop through the FileList and render image files as thumbnails.
  for (var i = 0, f; f = files[i]; i++) {
    console.log('File:', f);
    f.maio_type = 'other';
    f.maio_subtype = '';

    // Only process image files.
    if (f.type.match('image.*')) {
      f.maio_type = 'image';
    }

    if (f.type.match('audio.*')) {
      f.maio_type = 'audio';
    }

    if (f.type.match('video.*')) {
      f.maio_type = 'video';
    }

    if (f.type.match('text.*')) {
      f.maio_type = 'document';
      f.maio_subtype = 'text';
    }

    var reader = new FileReader();

    // Closure to capture the file information.
    reader.onload = (function(theFile, index, config) {
      return function(e) {
        // Render thumbnail.
        var div = document.createElement('div');
        var tn_html = `
                  <img id="index_${index}" src="${config.get('other_tn')}" class="maio-upload-image-index">
                  <img src="${config.get('other_tn')}" alt="${escape(theFile.name)}" class="maio-upload-image" data-mime-type="${escape(theFile.type)}">
        `;
        if (theFile.maio_type == 'image') {
          tn_html = `
                  <img id="index_${index}" src="${e.target.result}" alt="${escape(theFile.name)}" class="maio-upload-image-index">
                  <img src="${e.target.result}" alt="${escape(theFile.name)}" class="maio-upload-image" data-mime-type="${escape(theFile.type)}">
          `;
        }
        if (theFile.maio_type == 'audio') {
          tn_html = `
                  <img id="index_${index}" src="${config.get('audio_tn')}" class="maio-upload-image-index">
                  <img src="${config.get('audio_tn')}" alt="${escape(theFile.name)}" class="maio-upload-image" data-mime-type="${escape(theFile.type)}">
          `;
        }
        if (theFile.maio_type == 'video') {
          tn_html = `
                  <img id="index_${index}" src="${config.get('video_tn')}" class="maio-upload-image-index">
                  <img src="${config.get('video_tn')}" alt="${escape(theFile.name)}" class="maio-upload-image" data-mime-type="${escape(theFile.type)}">
          `;
        }
        if (theFile.maio_type == 'document') {
          if (theFile.maio_subtype == 'text') {
            tn_html = `
                  <img id="index_${index}" src="${config.get('document_tn')}" alt="${escape(theFile.name)}" class="maio-upload-image-index">
                  <img src="${config.get('document_tn')}" alt="${escape(theFile.name)}" class="maio-upload-image" data-mime-type="${escape(theFile.type)}" style="display: none;">
                  <pre class="maio-upload-image-index">${escape(e.target.result)})</pre>
            `;
          } else {
            tn_html = `
                  <img id="index_${index}" src="${config.get('document_tn')}" class="maio-upload-image-index">
                  <img src="${config.get('document_tn')}" alt="${escape(theFile.name)}" class="maio-upload-image" data-mime-type="${escape(theFile.type)}">
            `;
          }
        }
        div.innerHTML = `
          <div class="alert alert-secondary" style="position: relative;">
            <h6 class="row maio-upload-image-preview">Preview</h6>
            <div class="row">
              <div class="col" style="position: relative;">
                ${tn_html}
              </div>
              <div class="col">
                <div>Name: ${escape(theFile.name)}</div>
                <div>File Size: ${escape(String(theFile.size.toString()))} Bytes</div>
                <div>File MIME Type: ${escape(theFile.type)}</div>
                <div>Last Modified: ${escape(String(theFile.lastModified))}</div>
                <div>Last Modified Date: ${escape(String(theFile.lastModifiedDate))}</div>
                <div>Width: <span id="width_index_${index}">0</span>px</div>
                <div>Height: <span id="height_index_${index}">0</span>px</div>
                <div class="maio-div-index">${index}</div>
              </div>
            </div>
          </div>
        `;
        document.getElementById('list').insertBefore(div, null);
      };
    })(f, index, document.config);

    $(`#index_${index}`).onload = (function(index) {
      setTimeout(process_properties, 500, index);
    })(index);

    document.getElementById('list').innerHTML = '';

    if (f.maio_type == 'image') {
      reader.readAsDataURL(f);
    } else {
      reader.readAsText(f);
    }
    // Read in the image file as a data URL.

    index += 1;
  }
}
