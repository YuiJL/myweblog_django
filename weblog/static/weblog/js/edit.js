new Vue({
    el: '#blog',
    data: {
        url: '/api/blog/',
        blog: {
            title: '',
            tag: '',
            content: ''
        },
        message: ''
    },
    ready: function() {
        var self = this;
        var id = location.pathname.split('/');
        id.pop();
        if (id.pop() === 'edit') {
            var auto_id = id.pop();
            self.url = self.url + auto_id;
            $.getJSON('/api/blog/' + auto_id + '/', function(blog) {
                self.blog = blog;
            });
        }
        $("#navbarleft li:first-child").removeClass("active");
    },
    methods: {
        submit: function() {
            var self = this;
            $.ajax(self.url, {
                data: {
                    title: self.blog.title,
                    tag: self.blog.tag,
                    content: self.blog.content
                },
                method: "POST"
            }).done(function(data) {
                return location.assign(location.pathname.split('blog')[0] + 'blog/' + data.auto_id + '/');
            }).fail(function(xhr) {
                self.message = xhr.responseText;
                return $('.alert').show();
            });
        },
        cancel: function() {
            return location.assign(document.referrer);
        }
    }
})