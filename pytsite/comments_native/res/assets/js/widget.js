$(window).on('pytsite.widget.init:pytsite.comments_native._widget.Comments', function (e, widget) {
    var em = widget.em;
    var threadUid = em.data('threadId');
    var commentFormContainer = em.find('.comment-form');
    var commentForm = commentFormContainer.find('> form').first();
    var commentsList = em.find('.comments-list');
    var commentsLoadOffset = 0;
    var commentsLoadRemains = 0;
    var commentMaxDepth = em.data('maxDepth');

    function createReplyForm(parentCommentUid) {
        var form = commentForm.clone();

        form.find('.reply-to').val(parentCommentUid);
        form.find('.comment-body').attr('placeholder', t('pytsite.comments_native@enter_your_reply'));

        return form;
    }

    function onFormSubmit(e, form) {
        e.preventDefault();

        var formMessages = form.find('.messages');
        var commentBodyInput = form.find('.comment-body');

        // Clear form's messages
        formMessages.html('');

        pytsite.httpApi.post(em.data('commentSubmitEp'), {
            thread_uid: threadUid,
            parent_uid: form.find('.reply-to').val(),
            body: commentBodyInput.val()
        }).done(function (r) {
            createCommentSlot(r, {create: true});
            commentBodyInput.val('');
            if (form.parent().hasClass('reply-form')) {
                form.remove();
            }

        }).fail(function (e) {
            formMessages.append('<div class="alert alert-danger">' + e.responseJSON.error + '</div>');
        });
    }

    function onBtnReplyClick(btn, commentSlot) {
        // Delete possibly created reply form from other places
        em.find('.reply-form').find('form').remove();

        // Create and add reply form
        var replyForm = createReplyForm(commentSlot.data('uid'));
        replyForm.submit(function (e) {
            e.preventDefault();
            onFormSubmit(e, $(this));
        });
        commentSlot.find('> .right').first().find(' > .reply-form').first().append(replyForm);
        replyForm.find('.comment-body').focus();
    }

    function onBtnDeleteClick(btn, commentSlot) {
        if (confirm(t('pytsite.comments_native@confirm_comment_deletion'))) {
            pytsite.httpApi.delete('comments/comment', {
                uid: commentSlot.data('uid')
            }).done(function (r) {
                if (r['status']) {
                    commentSlot.find('> .left > .author-picture').remove();
                    commentSlot.find('> .right > .body').html('');
                    commentSlot.find('> .right > .header').html(t('pytsite.comments_native@comment_was_deleted'));
                    commentSlot.find('> .right > .reply-form form').remove();
                }
            });
        }
    }

    function onBtnReportClick(commentUid) {
        if (confirm(t('pytsite.comments_native@confirm_comment_report')))
            pytsite.httpApi.post('comments/report', {uid: commentUid}).done(function () {
                alert(t('pytsite.comments_native@comment_report_confirmed'));
            });
    }

    function createCommentSlot(comment, createPermission) {
        var slot = $('<div class="comment-item">');
        slot.attr('id', 'comment-' + comment['uid']);
        slot.attr('data-uid', comment['uid']);
        slot.attr('data-parent-uid', comment['parent_uid']);
        slot.attr('data-depth', comment['depth']);

        if (comment['parent_uid'])
            slot.addClass('reply');
        else
            slot.addClass('top-level');

        if (comment['status'] == 'deleted')
            slot.addClass('deleted');

        // Left container
        var left = $('<div class="left"></div>');
        slot.append(left);

        // Right container
        var right = $('<div class="right"></div>');
        slot.append(right);

        // User picture
        if (comment['status'] == 'published') {
            var userPic = $('<div class="author-picture"><img src="' + comment['author']['picture_url'] + '">');
            left.append(userPic);
        }

        // Comment header
        var header = $('<div class="header"></div>');
        right.append(header);
        if (comment['status'] == 'published') {
            // Author
            header.append($('<div class="author">' + comment['author']['full_name'] + '</div>'));

            // Publish time
            header.append($('<div class="publish-time">' + comment['publish_time']['ago'] + '</div>'));

            // 'Report' button
            var btnReport = $('<div class="report"><a class="report-btn" href="#" title="' +
                t('pytsite.comments_native@report') + '"><i class="fa fa-fw fa-flag"></i></a></div>');
            header.append(btnReport);
            btnReport.click(function (e) {
                e.preventDefault();
                return onBtnReportClick(comment['uid']);
            });


            // 'Delete' button
            if (comment['permissions']['delete']) {
                var btnDelete = $('<div class="delete"><a class="delete-btn" href="#" title="' +
                    t('pytsite.comments_native@delete') + '"><i class="fa fa-fw fa-trash-o"></i></a></div>');
                header.append(btnDelete);
                btnDelete.click(function (e) {
                    e.preventDefault();
                    return onBtnDeleteClick($(this).find('.delete-btn'), slot);
                });
            }

            // 'Reply' button
            if (comment['status'] != 'deleted' && createPermission && comment['depth'] != commentMaxDepth) {
                var btnReply = $('<div class="reply"><a class="reply-btn" href="#"><i class="fa fa-fw fa-reply"></i>&nbsp;' +
                    t('pytsite.comments_native@reply') + '</a></div>');
                header.append(btnReply);

                btnReply.click(function (e) {
                    e.preventDefault();
                    onBtnReplyClick($(this).find('.reply-btn'), slot);
                });
            }
        }
        else if (comment['status'] == 'deleted') {
            header.html(t('pytsite.comments_native@comment_was_deleted'));
        }

        // Comment body
        var body = $('<div class="body">');
        right.append(body);
        if (comment['status'] == 'published') {
            body.html(comment['body']);
        }

        // Placeholder for replies
        right.append($('<div class="replies">'));

        // Placeholder for reply form
        right.append($('<div class="reply-form">'));

        // Place comment slot to the right place
        var parentUid = comment['parent_uid'];
        if (parentUid) {
            // Place in the end of the corresponding parent 'replies' container
            var parentSlot = commentsList.find('.comment-item[data-uid=' + parentUid + ']').first();
            parentSlot.find('.right > .replies').first().append(slot);
        }
        else {
            // Place slot in the end of comments list
            commentsList.append(slot);
        }

        // Remove "No comments yet" notification
        commentsList.find('.no-comments-yet').remove();

        return slot;
    }

    // Load comments
    pytsite.httpApi.get(em.data('commentsLoadEp'), {
        thread_uid: threadUid,
        skip: commentsLoadOffset
    }).success(function (r) {
        commentsList.html('<p class="no-comments-yet">' + t('pytsite.comments_native@no_comments_yet') + '</p>');
        commentsLoadOffset = r['items'].length;
        commentsLoadRemains = parseInt(r['remains']);

        // Create slots and place them to their positions
        for (var i = 0; i < r['items'].length; i++) {
            createCommentSlot(r['items'][i], r['permissions']['create']);
        }
    });

    // Submit new comment handler
    commentForm.submit(function (e) {
        onFormSubmit(e, $(this));
    });
});
