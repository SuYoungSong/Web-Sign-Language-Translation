$(document).ready(function() {
    $('#gpt-input, #send-chat-button').on('keyup click', function(event) {
        if (
            (event.type === 'keyup' && event.key === 'Enter' && event.target.id === 'gpt-input') ||
            (event.type === 'click' && event.target.id === 'send-chat-button')
        ) {
            
            const postData = {
                csrfmiddlewaretoken: $('#send-chat-button').data('csrf-token'),
                question: $('#gpt-input').val()
            };

            $('#chat-zone').append('<div class="message user-message">' + postData.question + '</div>');
            $('#chat-zone').scrollTop($('#chat-zone')[0].scrollHeight);

            $('#gpt-input').val('')
            $('#gpt-input').attr('placeholder','GPT의 답변을 기다리는 동안 메시지를 보낼 수 없습니다.')
            $('#send-chat-button').prop('disabled',true);
            $('#gpt-input').prop('disabled',true);
            $.ajax({
                type: 'POST',
                url: '/api/chatgpt/',
                data: postData,
                dataType: 'json',
                success: function(response) {
                    $('#chat-zone').append('<div class="message gpt-message">' + response.result + '</div>');
                    $('#chat-zone').scrollTop($('#chat-zone')[0].scrollHeight);
                    $('#send-chat-button').prop('disabled',false);
                    $('#gpt-input').prop('disabled',false);
                    $('#gpt-input').focus();
                    $('#gpt-input').attr('placeholder','Message ChatGPT...')
                },
                error: function(error) {
                    console.error('Error:', error);
                    $('#chat-zone').append('<div class="message gpt-message">' + "GPT 응답 오류" + '</div>');
                    $('#chat-zone').scrollTop($('#chat-zone')[0].scrollHeight);
                    $('#send-chat-button').prop('disabled',false);
                    $('#gpt-input').prop('disabled',false);
                    $('#gpt-input').focus();
                    $('#gpt-input').attr('placeholder','Message ChatGPT...')
                }
            });
        }
    });
});