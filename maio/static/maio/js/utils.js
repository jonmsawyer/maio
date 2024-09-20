/**
 * utils.js
 * By Jonathan Sawyer <jsawyer@akcourts.gov>
 *
 * Utility objects and functions.
 **/

var config;

/**
 * Config
 *
 * Main Config object used in the OQ Admin. Useful for initializing configuration from a
 * Django template to be used in other static .js scripts.
 */
class Config {
    config = {}

    constructor(config={}){
        this.config = config;
    }

    set(key, value) {
        this.config[key] = value;
    }

    get(key) {
        return this.config[key];
    }

    copy() {
        return this.config.copy()
    }
}

/**
 * Log data to the console if the 'js_debug' flag is set in the `Config`.
 *
 * @param {Array} arguments
 */
function log() {
    if (config.get('js_debug')) {
        console.log(...Object.values(arguments));
    }
}

/**
 * Close the error panel.
 */
function close_error_panel() {
    $('#error-panel').slideUp();
    $('#error').html('');
}

/**
 * Show the error panel with the given `msg`.
 *
 * @param {string} msg
 * @param {any} data
 */
function show_error_panel(msg, data) {
    log('Error:', msg, data);
    $('#error').html(msg);
    $('#error-panel').slideDown();
}

/**
 * Close the info panel.
 */
function close_info_panel() {
    window.info_panel_handle = window.info_panel_handle || 0;
    clearTimeout(window.info_panel_handle);
    $('#info-panel').slideUp();
}

/**
 * Show the info panel with the given `msg`.
 *
 * @param {string} msg
 * @param {any} data
 */
function show_info_panel(msg, data) {
    close_info_panel()
    log('Info:', msg, data);
    window.info_panel_handle = setTimeout(close_info_panel, 5000);
    $('#info').html(msg);
    $('#info-panel').slideDown();
}

/**
 * Call this method and pass the DOM element and callback function as parameters to manage
 * a custom timer to make AJAX calls after some input has been entered in a field. This allows
 * us to make a timed AJAX call once after a buffer of time after input has been entered. If
 * the user adds more data to the field the timer is reset so we don't make premature AJAX calls
 * to the server, which improves usability and performance.
 *
 * @param {DOM element|jQuery element} el
 * @param {function} callback - the callback to execute with `el` as it's first parameter
 * @param {int} timeout - in milliseconds
 * @param {any} param1
 * @param {any} param2
 * @param {any} param3
 */
function input_timer(el, callback, timeout=1000, param1, param2, param3) {
    el = $(el);
    clearTimeout(el.data('timer'));
    el.data('timer', setTimeout(callback, timeout, el, param1, param2, param3));
}

/**
 * fn slugify(el: DOM element or jQuery element) -> None
 *
 * Given an element which contains a value, replace all non slug characters with hyphens.
 * Capital letters are lowercased and then all non slug characters gets replaced. A hyphen
 * before or after the slug is acceptable. The value updates as you type.
 *
 * @param {DOM element|jQuery element} el - DOM element or jQuery element
 */
function slugify(el) {
    el = $(el);

    // My implementation.
    //var val = el.val()
    //  .toLowerCase()
    //  .replace(/[^a-z0-9-]|[-]{2,}/gu, '-')
    //  // replace extra --'s again due to how the above regex is processed
    //  .replace(/[-]{2,}/gu, '-');
    // Django's implementation.
    var val = el.val()
        .replace(/[^\w\s-]/gu, '')
        .toLowerCase()
        .replace(/[-\s]+/gu, '-')
        .replace(/^[-]*/u, '')
        .replace(/[-]*$/u, '');
    el.val(val);
    return el
}
