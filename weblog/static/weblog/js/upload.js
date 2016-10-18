$(document).ready(function() {
    $('#avatar').click(function() {
        upload.image = '';
        upload.url = '';
        upload.isImg = false;
        upload.isURL = false;
    });
});

var upload = new Vue({
    el: '#upload',
    data: {
        image: '',
        url: '',
        isImg: false,
        isURL: false
    },
    methods: {
        onFileChange: function(e) {
            this.url = '';
            this.isURL = false;
            this.isImg = true;
            var file = e.target.files[0];
            if (file.name.length < 1) {
                return;
            } else if (file.size > 1000000) {
                alert("The file is too big, should be at most 1 MB");
                return;
            } else if (file.type != 'image/png' && file.type != 'image/jpg' && file.type != 'image/gif' && file.type != 'image/jpeg' && file.type != 'image/bmp') {
                alert("The file does not match png, jpg, bmp or gif");
                return;
            } else {
                var reader = new FileReader();
                var self = this;
                reader.onload = function(e) {
                    self.image = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        },
        uploadURL: function() {
            var self = this;
            $.ajax('/api/image_from_url/', {
                data: {url: self.image},
                method: "POST"
            });
        },
        addUrl: function() {
            if (this.url === '')
                return;
            this.image = this.url;
            this.url = '';
            this.isImg = false;
            this.isURL = true;
        },
        removeImage: function() {
            this.image = '';
            this.url = '';
            this.isImg = false;
            this.isURL = false;
        }
    }
})