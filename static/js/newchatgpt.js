
function show_chat_page(page){
    var allChatPages = document.querySelectorAll('.chat_page');
        allChatPages.forEach(function(chatPage) {
            chatPage.classList.remove('chat-active');            
        });

    var activeChat = document.getElementById('page_'+page);
    activeChat.classList.add('chat-active');

    // 기존 채팅 내역 클리어
    $('#chat-zone').empty();

    postData = {
        'page':page,
    }

    headers = {
        'X-CSRFToken': $('#send-chat-button').data('csrf-token'),
    }
    // 내용 요청
    $.ajax({
        type: 'POST',
        url: '/api/get_previous_chat/',
        data: postData,
        headers: headers,
        dataType: 'json',
        success: function(response) {
            for(var i=0 ; i < response.message.length ; i++ ){
                $('#chat-zone').append('<div class="message user-message">' + response.message[i].user + '</div>');
                $('#chat-zone').append('<div class="message gpt-message">' + response.message[i].gpt + '</div>');
            }
            
            // $('#chat-zone').append('<div class="message gpt-message">' + response.result + '</div>');
            $('#chat-zone').scrollTop($('#chat-zone')[0].scrollHeight);
        },
        error: function(error) {
            console.error('Error:', error);
            $('#chat-zone').append('<div class="message gpt-message">' + "채팅 내역 불러오기 실패" + '</div>');
            $('#chat-zone').scrollTop($('#chat-zone')[0].scrollHeight);
        }
    });
}



$(document).ready(function() {
    $('#gpt-input, #send-chat-button').on('keyup click', function(event) {
        if (
            (event.type === 'keyup' && event.key === 'Enter' && event.target.id === 'gpt-input') ||
            (event.type === 'click' && event.target.id === 'send-chat-button')
        ) {
            // chat-active 클래스를 가진 div 요소를 찾습니다.
            const chatActiveDiv = document.querySelector('.chat-active');

            // chat-active 클래스를 가진 div 요소의 id를 가져옵니다.
            const id = chatActiveDiv ? chatActiveDiv.id : 0;

            // id에서 ** 부분을 추출합니다.
            const page_num = id ? id.split('_')[1] : 0;

            const postData = {
                question: $('#gpt-input').val(),
                page:page_num,
            };

            headers = {
                'X-CSRFToken': $('#send-chat-button').data('csrf-token'),
            }

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
                headers: headers,
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