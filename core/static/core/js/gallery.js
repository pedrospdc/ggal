var Gallery = function(gallery_selector) {
    this.gallery_object = $(gallery_selector);
    this.images = this.gallery_object.find('.container img');
    this.images_length = this.images.length;

    this.onLoad = function()
    {
        console.log(this.images);
        this.images.first().show();
    }
}

$(document).ready(function() {
    var gallery = new Gallery('#gallery');
    gallery.onLoad();
});