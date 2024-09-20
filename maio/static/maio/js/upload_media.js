/**
 * File: upload_media.js
 *
 * Thanks to: https://jsfiddle.net/41go76g4/
 */

var config;

function escape(text) {
  return text.replace(/"/g, '&quot;');
}

function process_properties(index, maio_type, maio_subtype) {
  var el = $(`#index_${index}`);
  console.log(` -> Maio Type is ${maio_type}, Maio Subtype is ${maio_subtype}`);
  var by_id = document.getElementById(`index_${index}`);
  if (maio_type == 'image') {
    console.log(`Processing Width and Height for index ${index}.`);
    $(`#width_index_${index}`).html(String(by_id.width));
    $(`#height_index_${index}`).html(String(by_id.height));
  }
}

/**
 * handleFileSelect
 *
 * @param {domEvent} evt
 */
function handleFileSelect(evt, config) {
  console.log('Config:', config);
  var files = evt.target.files; // FileList object
  var index = 0;

  // Loop through the FileList and render image files as thumbnails.
  for (var i = 0, f; f = files[i]; i++) {
    console.log('File:', f);
    var maio_type = 'other';
    var maio_subtype = 'other';

    // Only process image files.
    if (f.type.match('image.*')) {
      maio_type = 'image';
    }

    if (f.type.match('audio.*')) {
      maio_type = 'audio';
    }

    if (f.type.match('video.*')) {
      maio_type = 'video';
    }

    if (f.type.match('text.*')) {
      maio_type = 'document';
      maio_subtype = 'text';
    }

    console.log(`Maio Type: ${maio_type}`, `Maio Subtype: ${maio_subtype}`);

    var reader = new FileReader();

    // Closure to capture the file information.
    reader.onload = (function(theFile, index, config, maio_type, maio_subtype) {
      return function(e) {
        // Render thumbnail.
        var div = document.createElement('div');
        var tn_html = `
                  <img id="index_${index}" src="${config.get('other_tn')}" class="maio-upload-image-index" data-maio-type="other">
                  <img src="${config.get('other_tn')}" alt="${escape(theFile.name)}" class="maio-upload-image">
        `;
        console.log('tn_html', tn_html);
        if (maio_type == 'image') {
          tn_html = `
                  <img id="index_${index}" src="${e.target.result}" alt="${escape(theFile.name)}" class="maio-upload-image-index" data-maio-type="image">
                  <img src="${e.target.result}" alt="${escape(theFile.name)}" class="maio-upload-image">
          `;
        }
        if (maio_type == 'audio') {
          tn_html = `
                  <img id="index_${index}" src="${config.get('audio_tn')}" class="maio-upload-image-index" data-maio-type="audio">
                  <audio src="${e.target.result}" alt="${escape(theFile.name)}" class="maio-upload-image"></audio>
          `;
        }
        if (maio_type == 'video') {
          tn_html = `
                  <img id="index_${index}" src="${config.get('video_tn')}" class="maio-upload-image-index" data-maio-type="video">
                  <video src="${e.target.result}" alt="${escape(theFile.name)}" class="maio-upload-image"></video>
          `;
        }
        if (maio_type == 'document') {
          if (maio_subtype == 'text') {
            tn_html = `
                  <img id="index_${index}" src="${config.get('document_tn')}" alt="${escape(theFile.name)}" class="maio-upload-image-index" data-maio-type="document">
                  <img src="${config.get('document_tn')}" alt="${escape(theFile.name)}" class="maio-upload-image" style="display: none;">
                  <pre class="maio-upload-image-index">${escape(e.target.result)})</pre>
            `;
          } else {
            tn_html = `
                  <img id="index_${index}" src="${config.get('document_tn')}" class="maio-upload-image-index" data-maio-type="document">
                  <img src="${config.get('document_tn')}" alt="${escape(theFile.name)}" class="maio-upload-image">
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
    })(f, index, config, maio_type, maio_subtype);

    $(`#index_${index}`).onload = (function(index) {
      setTimeout(process_properties, 1000, index, maio_type, maio_subtype);
    })(index);

    document.getElementById('list').innerHTML = '';

    if (maio_type == 'image') {
      console.log('Reading file as `image`');
      reader.readAsDataURL(f);
    } else if (maio_type == 'audio') {
      console.log('Reading file as `audio`');
      reader.readAsDataURL(f);
    } else if (maio_type == 'video') {
      console.log('Reading file as `video`');
      reader.readAsDataURL(f);
    } else {
      console.log('Reading file as `other`');
      reader.readAsText(f);
    }
    // Read in the image file as a data URL.

    index += 1;
  }
}
