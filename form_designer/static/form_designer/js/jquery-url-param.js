jQuery(function($) {

    $.urlParam = function(name, defaultValue, url) {
        if (!url) {
            url = window.location.href
        }
        var results = new RegExp('[\\?&]'+name+'=([^&#]*)').exec(url);
        return results ? results[1] : defaultValue;
    }

    $.scriptUrlParam = function(js, name, defaultValue) {
        result = defaultValue;
        $('head script[src]').each(function() {
            if (this.src.match(js)) {
                result = $.urlParam(name, result, this.src);
            }
        });
        return result;
    }

}