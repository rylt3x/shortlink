let sendButton = $('#srt-submit-btn');
let sourceField = $('#source-field');

function eventListener (event) {
    let form = $(event.target).parent();
    if (sourceField.val() === ''){
            sourceField.addClass('invalid');
            sourceField.attr('placeholder', 'Введите ссылку!');
        return;
    }
    send_form(form);
}
sendButton.click(eventListener)

sourceField.on('input', function () {
    let currentValue = $(this).val()
    if ((!currentValue.includes('http://') && !currentValue.includes('https://') && !currentValue.startsWith('h') && currentValue.length > 0)){
        $(this).val('https://'+currentValue);
    }
})

sourceField.focus(function (event) {
    let input = $(event.target)
    if (input.hasClass('invalid')){
        input.removeClass('invalid');
        input.attr('placeholder', 'http://yourlink.com')
    }
});

function send_form(form) {
    let data = form.serializeArray();
    $.ajax({
        cache: false,
        method: 'POST',
        data: data,
        url: '/',
        beforeSend: function(xhr, opts){
            let forwardUrl = data[1].value;
            let isValid = isValidUrl(forwardUrl);
            if (!isValid) {
                let source_url = $('#source-field');
                source_url.addClass('invalid');
                source_url.attr('placeholder', 'Введите ссылку!');
                xhr.abort();
                return
            }
            $('#ajax-loader').removeClass('ajax-disabled').addClass('ajax-enabled')
        },
        success: function (data) {
            $('#ajax-loader').removeClass('ajax-enabled').addClass('ajax-disabled')

            let output = window.location.protocol+'//'+window.location.host+'/'+data.link;
            let status_code = data.status;
            $('.srt-notify').hide();
            if (status_code === 'error'){
                let errorModal = $('#err-msg');
                errorModal.fadeIn();
                setTimeout(() => errorModal.fadeOut(), 3000);
                return;
            }

            let output_element = $('#srt-forward-url');
            output_element.val(output);

            $('#output').addClass('enabled');

            let input = $('#source-field');
            if (input.hasClass('invalid')){
                input.removeClass('invalid');
                input.attr('placeholder', 'http://yourlink.com');
            }
            // Цель в метрику
            ym(88522299,'reachGoal','srt-submit-btn')

            let successModal = $('#success-msg');
            successModal.fadeIn()
            setTimeout(() => successModal.fadeOut(), 3000)
        }
    });
}
$('#copy-to-clip').click(function (event) {
    let copyValue = $(event.target).siblings('input').val();
    copyToClipboard(copyValue);
});
$(".g-link-button").click(function (event) {
    console.log(event.target)
    let copyValue = $(event.target).siblings('div').children('a').text()
    copyToClipboard(copyValue);
})

// Копировать в буфер по кнопке
function copyToClipboard(text) {
    let $temp = $("<input>");
    $("body").append($temp);
    $temp.val(text).select();
    document.execCommand("copy");
    $temp.remove();
}

// Проверка введенного урл на доступность
function checkUrl(url) {
    try {
        let request = new XMLHttpRequest();
        request.open("GET", url, true);
        // request.timeout = 500;
        request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        request.onload = function() {
            if(request.readyState === XMLHttpRequest.DONE && request.status === 200) {
                return true;
            }
        }
        request.ontimeout = function (e){
            return false;
        }
        request.send('');
    }
    catch (e) {
        console.log('error')
        return false;
    }
    return false;
}
// Проверка введенного урл на валидность
const isValidUrl = (url) => {
  try {
    new URL(url);
  } catch (e) {
    return false;
  }
  return true;
};

$(document).ready(function () {
    sourceField.focus()
})
