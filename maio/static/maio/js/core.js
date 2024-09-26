/**
 * Core Maio JavaScript.
 *
 * Included in every page. Requires jQuery to be loaded first.
 */

/**
 * Config
 *
 * Main Config object used in the OQ Admin. Useful for initializing configuration from a
 * Django template to be used in other static .js scripts.
 */
class Config {
    config = {}

    constructor(config = {}){
        this.config = config;
    }

    *[Symbol.iterator]() {
        var keys = this.get_keys();
        for (let index = 0; index < keys.length; index += 1) {
              yield keys[index];
        }
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

    delete_key(key) {
        delete this.config[key];
    }

    length() {
        return Object.keys(this.config).length;
    }

    get_keys() {
        return Object.keys(this.config);
    }
}

let maio_conf = new Config({});

/**
 * Namespaced object for core javascript functionality.
 */
let Maio = {
    FORBIDDEN: {
        /**
         * Forbidden filename characters to restrict across all platforms.
         */
        FILENAME_CHARS: [
            '*', '"', '/', '\\', '<', '>', ':', '|', '?',
            '\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', '\x08', '\x09',
            '\x0a', '\x0b', '\x0c', '\x0d', '\x0e', '\x0f', '\x10', '\x11', '\x12', '\x13',
            '\x14', '\x15', '\x16', '\x17', '\x18', '\x19', '\x1a', '\x1b', '\x1c', '\x1d',
            '\x1e', '\x1f',
        ],

        /**
         * Forbidden filenames to restrict across all platforms.
         */
        FILENAMES: [
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9',
        ],
    },

    config: new Config({}),

    /**
     * Update the debug config, if enabled. Usually only usable by a superuser.
     */
    update_debug_config: function() {
        var el = $('#maio_debug_config pre');
        if (el.length > 0) {
            el.html(JSON.stringify(maio_conf.config, null, 4));
        }
    },

    /**
     * Log data to the console if the 'js_debug' flag is set in the `Config`.
     *
     * @param {Array} arguments
     */
    log: function() {
        if (maio_conf.get('js_debug')) {
            console.log(...Object.values(arguments));
        }
    },

    /**
     * Close the error panel.
     */
    close_error_panel: function() {
        $('#error-panel').slideUp();
        $('#error').html('');
    },

    /**
     * Show the error panel with the given `msg`.
     *
     * @param {string} msg
     * @param {any} data
     */
    show_error_panel: function(msg, data) {
        Maio.close_error_panel();
        Maio.log('Error:', msg, data);
        $('#error').html(msg);
        $('#error-panel').slideDown();
        Maio.input_timer($('#error'), function(el) {
            Maio.close_error_panel();
        }, 10000);
    },

    /**
     * Close the info panel.
     */
    close_info_panel: function() {
        window.info_panel_handle = window.info_panel_handle || 0;
        clearTimeout(window.info_panel_handle);
        $('#info-panel').slideUp();
    },

    /**
     * Show the info panel with the given `msg`.
     *
     * @param {string} msg
     * @param {any} data
     */
    show_info_panel: function(msg, data) {
        Maio.close_info_panel()
        Maio.log('Info:', msg, data);
        window.info_panel_handle = setTimeout(Maio.close_info_panel, 5000);
        $('#info').html(msg);
        $('#info-panel').slideDown();
    },

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
    input_timer: function(el, callback, timeout=1000, param1, param2, param3) {
        el = $(el);
        clearTimeout(el.data('timer'));
        el.data('timer', setTimeout(callback, timeout, el, param1, param2, param3));
    },

    /**
     * Given an element which contains a value, replace all non slug characters with hyphens.
     * Capital letters are lowercased and then all non slug characters gets replaced. A hyphen
     * before or after the slug is acceptable. The value updates as you type.
     *
     * @param {DOM element|jQuery element} el - DOM element or jQuery element
     * @returns {jQuery element}
     */
    slugify: function(el) {
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
    },

    /**
     * Escape literal double quotes in a string with HTML entity double quotes.
     *
     * @param {String} text - A string to escape double quotes from
     * @returns {String}
     */
    escape: function(text) {
        return text.replace(/"/g, '&quot;');
    },

    /**
     * Validate a file name. This function will escape illegal characters and filenames
     * suited for all platforms.
     *
     * @param {String} text - A string to escape double quotes from
     * @returns {String}
     */
    validate_filename: function(text) {
        var forbid_chars = Maio.FORBIDDEN.FILENAME_CHARS.join('');
        var chars_regex = new RegExp(`[${forbid_chars}]`, 'g');
        var forbid_names = Maio.FORBIDDEN.FILENAMES.join('|')
        var names_regex = new RegExp(`^${forbid_names}$`, 'i');
        var name = text
                    .split('.')
                    .slice(0, -1)
                    .join('.')
                    .trim()
                    .replace(chars_regex, '')
                    .replace(names_regex, 'maio_upload');
        let ext = text
                    .split('.')
                    .slice(-1)[0]
                    .trim()
                    .replace(chars_regex, '');
        var validated_name = `${name}.${ext}`;
        if (validated_name.endsWith('.')) {
            validated_name = `${validated_name}file`;
        }
        return validated_name;
    },

    trim_filename: function(text) {
        text = Maio.validate_filename(text);
        var name = text
                    .split('.')
                    .slice(0, -1)
                    .join('.')
                    .trim();
        let ext = text
                    .split('.')
                    .slice(-1)[0]
                    .trim();
        var name_slice = name.slice(0, 18);
        var trimmed_name = `${name}.${ext}`;
        if (name.length != name_slice.length) {
            trimmed_name = `${name_slice}...${ext}`;

        }
        return trimmed_name;
    }
};
