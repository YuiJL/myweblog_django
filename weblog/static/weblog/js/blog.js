function blackMagic(tag, mode) {
    if (mode === 1) {
        var it = $(tag).parent().find('form');
        if (it.hasClass('replybox')) {
            if (vm.subcomment !== '') {
                vm.subcomment = '';
            } else {
                it.removeClass('replybox');
            }
        }
        $('.replybox').hide();
        $('.replybox').removeClass('replybox');
        it.addClass('replybox');
    } else {
        var it = $(tag).parent().parent().parent().find('form');
        if (!it.hasClass('replybox')) {
            $('.replybox').hide();
            $('.replybox').removeClass('replybox');
            it.addClass('replybox');
        }
    }
}

new Vue({
    el: '#commentsignin',
    methods: {
        clear: function() {
            base.email = '';
            base.password = '';
            base.message = '';
            $('#error').hide();
        }
    }
})

var vm = new Vue({
    el: '#control',
    data: {
        paths: location.pathname.split('/'),
        subcomment: '',
        comment: '',
        comments: [],
        id: 0
    },
    ready: function() {
        var self = this;
        $.getJSON('/api/blog/' + self.paths[self.paths.length-2] + '/comments/', function(data) {
            self.comments = data.comments;
        });
        $("#navbarleft li:first-child").removeClass("active");
    },
    methods: {
        submit: function() {
            var self = this;
            $.ajax('/api/blog/' + self.paths[self.paths.length-2] + '/comments/', {
                data: {content: self.comment},
                method: "POST"
            }).done(function(data) {
                self.comment = '';
                self.comments = data.comments;
            });
        },
        reply: function() {
            var self = this;
            $('.replybox').hide();
            $.ajax('/api/blog/' + self.paths[self.paths.length-2] + '/comments/' + self.id + '/', {
                data: {content: self.subcomment},
                method: "POST"
            }).done(function(data) {
                self.subcomment = '';
                self.comments = data.comments;
            });
        },
        replyBox: function(id, index, mode, name) {
            this.id = id;
            var self = this;
            if (mode === 1) {
                $('.replybox').toggle();
                self.subcomment = '';
            } else {
                $('.replybox').show();
                self.subcomment = 'RE @' + name + ': ';
            }
            $('.replybox textarea').attr('placeholder', 'Write a reply to ' + "#" + (self.comments.length - index));
        },
        delete: function(key, id) {
            var self = this;
            $.ajax('/api/' + key + '/' + id + '/delete/', {
                method: "GET"
            }).done(function(data) {
                self.comments = data.comments;
            });
        }
    }
});