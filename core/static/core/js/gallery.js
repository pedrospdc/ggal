var Gallery = function(gallery_selector) {
    this.gallery_object = $(gallery_selector);
    this.images = this.gallery_object.find('.container img');
    this.images_length = this.images.length;
    this.pagination = this.gallery_object.children('.pagination');
    this.pagination_current = this.pagination.find('.current_image');
    this.pagination_total = this.pagination.find('.total_image');
    this.left_arrow = this.gallery_object.children('.left');
    this.right_arrow = this.gallery_object.children('.right');
    this.current_image = this.images.first();
    this.current_index = 0;

    this.onLoad = function()
    {
        this.current_image.show()
        this.pagination_total.text(this.images_length);
        this.left_arrow.click($.proxy(this.previous, this));
        this.right_arrow.click($.proxy(this.next, this));
    }

    this.goToImage = function(index) {
        this.images.hide();
        this.pagination_current.text(index + 1);
        this.current_image = this.images.eq(index);
        this.current_image.show();
        this.current_index = index;
    }

    this.next = function() {
        this.goToImage(Math.min(this.images_length - 1, this.current_index + 1));
    }

    this.previous = function() {
        this.goToImage(Math.max(0, this.current_index - 1));
    }
}

$(document).ready(function() {
    var gallery = new Gallery('#gallery');
    gallery.onLoad();
});