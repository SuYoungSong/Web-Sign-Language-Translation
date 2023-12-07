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
    // CSRF 토큰 가져오기
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    // 내용 요청
    $.ajax({
        type: 'POST',
        url: '/api/sign_get_previous_message/',
        data: postData,
        headers: {
            "X-CSRFToken": csrftoken
        },
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


// Dropzone 초기화
Dropzone.autoDiscover = false; // 자동 초기화 비활성화



var openModal = function () {
    var modal = document.getElementById('myModal');
    modal.style.display = 'block';
};
$(document).ready(function () {
    



    var modal = $('#myModal');
    var closeModalBtn = $('#closeModal');
    var submitBtn = $('#submitBtn');
    var myDropzone;

    var requestInProgress = false;
    // X 버튼 또는 모달 외부를 클릭했을 때 모달을 닫도록 이벤트 핸들러 추가
    closeModalBtn.on('click', function () {
        if (!requestInProgress) {
            modal.hide();
            if (myDropzone) {
                myDropzone.removeAllFiles();  // 모달이 닫힐 때 모든 파일을 삭제
            }
        }
    });

    // 모달 외부를 클릭했을 때 모달을 닫도록 이벤트 핸들러 추가
    $(window).on('click', function (event) {
        if (event.target == modal[0] && !requestInProgress) {
            modal.hide();
            if (myDropzone) {
                myDropzone.removeAllFiles();  // 모달이 닫힐 때 모든 파일을 삭제
            }
        }
    });
    
    
    myDropzone = new Dropzone("#myDropzone", {
        url: "/api/signchatgpt/",
        autoProcessQueue: false,  // 자동으로 큐를 처리하지 않도록 설정
        acceptedFiles: 'image/*',
        addRemoveLinks: true,
        paramName: "files",
        parallelUploads: 100,
        maxFiles: 100,
        dictDefaultMessage: "수어 사진을 드래그&드랍 또는 클릭 후 업로드 해주세요!",
        dictFallbackMessage: "브라우저가 드래그 앤 드롭 파일 업로드를 지원하지 않습니다.",
        dictFallbackText: "이전 방식으로 파일을 업로드하려면 아래 폼을 사용하세요.",
        dictFileTooBig: "파일이 너무 큽니다 (최대 파일 크기: {{maxFilesize}}MiB).",
        dictInvalidFileType: "이 유형의 파일은 업로드할 수 없습니다.",
        dictResponseError: "서버에서 오류가 발생했습니다 ({{statusCode}} 코드).",
        dictCancelUpload: "업로드 취소",
        dictCancelUploadConfirmation: "이 업로드를 취소하시겠습니까?",
        dictRemoveFile: "이미지 삭제",
        dictMaxFilesExceeded: "더 이상 파일을 업로드할 수 없습니다."
    });


   // 파일 업로드 버튼 클릭 시 서버로 파일 전송
   submitBtn.on('click', function () {
    requestInProgress = true
    // 비활성화 상태로 변경
    submitBtn.prop('disabled', true);
    submitBtn.text('서버에 수어를 전송하고 있습니다...');

    var formData = new FormData();

    // 모든 파일을 FormData에 추가
    myDropzone.files.forEach(function (file) {
        formData.append("files", file);
    });
    // chat-active 클래스를 가진 div 요소를 찾습니다.
    const chatActiveDiv = document.querySelector('.chat-active');

    // chat-active 클래스를 가진 div 요소의 id를 가져옵니다.
    const id = chatActiveDiv ? chatActiveDiv.id : false;

    // id에서 ** 부분을 추출합니다.
    const page_num = id ? id.split('_')[1] : false;
    formData.append("page", page_num);
    // CSRF 토큰 가져오기
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    // 서버로 직접 Ajax 요청 보내기
    $.ajax({
        url: "/api/signchatgpt/",
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (response) {
            // 성공적으로 업로드되면 모달창 내용을 업데이트하고 A에 결과를 추가
            $('#chat-zone').append('<div class="message user-message">' + response.question + '</div>');
            $('#chat-zone').append('<div class="message gpt-message">' + response.result + '</div>');
            $('#chat-zone').scrollTop($('#chat-zone')[0].scrollHeight);

            // 활성화 상태로 변경
            submitBtn.prop('disabled', false);
            submitBtn.text('전송하기');
            requestInProgress = false;
            modal.hide(); // 모달창 닫기
            myDropzone.removeAllFiles();  // 파일이 성공적으로 업로드되면 모든 파일을 삭제
        },
        error: function () {
            // 파일 업로드 중 에러가 발생하면 모달창 내용을 업데이트
            $('#chat-zone').append('<div class="message user-message">' + "서버에 사진 전송 실패" + '</div>');
            // $('#chat-zone').append('<div class="message gpt-message">' + "GPT 응답 오류" + '</div>');
            $('#chat-zone').scrollTop($('#chat-zone')[0].scrollHeight);

            // 활성화 상태로 변경
            submitBtn.prop('disabled', false);
            submitBtn.text('전송하기');
            requestInProgress = false;
            modal.hide(); // 모달창 닫기
            myDropzone.removeAllFiles();  // 파일 업로드 중 에러가 발생하면 모든 파일을 삭제
        }
    });
});
});