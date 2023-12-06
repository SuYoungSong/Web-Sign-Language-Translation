function addUserMessage() {
    var userMessage = document.getElementById('question-input').value;

    if (userMessage.trim() === '') {
        return; // 입력된 메시지가 없으면 무시
    }

    var chatBox = document.getElementById('chatting');
    var messageContainer = document.createElement('div');
    messageContainer.className = 'message';

    var message = document.createElement('div');
    message.className = 'user-message';
    message.innerText = userMessage;

    messageContainer.appendChild(message);
    chatBox.appendChild(messageContainer);

    adjustUserMessageWidth(messageContainer);

    // 입력창 비우기
    document.getElementById('question-input').value = '';

    // 맨 위로 스크롤
    chatBox.scrollTop = 0;
}

function adjustUserMessageWidth(messageContainer) {
    var messageWidth = messageContainer.querySelector('.message').offsetWidth;
    var maxWidthPercent = 30;

    if (messageWidth < window.innerWidth * (maxWidthPercent / 100)) {
        messageContainer.style.maxWidth = messageWidth + 'px';
    } else {
        messageContainer.style.maxWidth = window.innerWidth * (maxWidthPercent / 100) + 'px';
    }
}