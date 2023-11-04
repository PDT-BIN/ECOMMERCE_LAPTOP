var chatbox = document.getElementById("chatbox")
var chatboxBtn = document.getElementById("chatboxBtn")
var chatboxClose = document.getElementById("chatboxClose")

chatboxBtn.addEventListener("click", function () {
    chatboxBtn.classList.add("hidden")
    chatbox.classList.remove("hidden")
})
chatboxClose.addEventListener("click", function () {
    chatboxBtn.classList.remove("hidden")
    chatbox.classList.add("hidden")
})

document.addEventListener("DOMContentLoaded", function () {
    const userMessageInput = document.getElementById("user-message");
    const sendButton = document.getElementById("send-button");

    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/getChat/',
        dataType: 'json',
        success: function (response) {
            for (i = 0; i < response.length; i++) {
                addMessageToChat(response[i][0], true, false, false)
                addLabel(response[i][1][3])
                if (typeof response[i][1][1] === 'string') {
                    addMessageToChat(response[i][1], false, false, true)
                }
                else if (response[i][1][1] != 0) {
                    addMessageToChat(response[i][1], false, true, false)
                }
                else {
                    addMessageToChat(response[i][1][0], false, false, false)
                }
            }
        },
        error: function (error) {
            console.log(error)
        }
    });
    function decodeUrlToString(encodedUrl) {
        try {
            const decodedString = decodeURIComponent(encodedUrl);
            return decodedString;
        } catch (error) {
            console.error('Error decoding URL:', error);
            return null; // Return null or handle the error as needed
        }
    }
    function addLabel(messageText) {
        label = document.createElement("p")
        label.innerHTML = messageText
        label.className = "hidden"
        var userTxts = document.getElementsByClassName("message")
        userTxts[userTxts.length - 1].appendChild(label)
    }
    function addMessageToChat(messageText, isUser, hasImage, isLink) {
        const chatMessages = document.getElementById("chat-messages");
        const message = document.createElement("div");
        const container = document.createElement("div");
        if (hasImage) {
            para = document.createElement("p")
            para.innerText = messageText[0];
            message.appendChild(para);
            for (i = 0; i < messageText[1][0].length; i++) {
                message.appendChild(document.createElement("br"))
                numbering = document.createElement("div")
                numbering.innerText = i + 1 + ". " + messageText[1][3][i] + " - " + messageText[1][2][i]
                numbering.classList.add("font-bold", "mb-2")
                message.appendChild(numbering)
                const link = document.createElement("a");
                link.href = '/orders/product/' + messageText[1][1][i];
                const image = document.createElement("img");
                image.src = decodeUrlToString(messageText[1][0][i].replace("/media/https%3A/", "https://"));
                image.classList.add("rounded")
                link.appendChild(image)
                message.appendChild(link)
            }
        }
        else if (isLink) {
            para = document.createElement("p")
            para.innerText = messageText[0];
            message.appendChild(para);
            const link = document.createElement("a");
            link.href = decodeUrlToString(messageText[1].replace("/media/https%3A/", "https://"));
            link.innerText = decodeUrlToString(messageText[1].replace("/media/https%3A/", "https://"));
            message.appendChild(link)
        }
        else {
            para = document.createElement("p")
            para.innerHTML = messageText.replaceAll("\n", "<br>");
            message.appendChild(para);
        }
        if (isUser) {
            container.className = "flex flex-row-reverse mb-2"
            message.className = "message bg-blue-500 text-white rounded-lg p-2 mb-2"
            container.appendChild(message)
        }
        else {
            $("#rating").remove()

            container.className = "flex flex-col mb-2"
            message.className = "bg-gray-300 text-black rounded-lg p-2 mb-2 "
            message.style.borderRadius = "15px";
            message.style.padding = "8px 12px";
            message.style.margin = "5px 0";
            message.style.display = "inline-block";

            rating = document.createElement("div")
            rating.className = "mt-[-1px] inline-block"
            rating.setAttribute("id", "rating")

            ratingTxt = document.createElement("p")
            ratingTxt.className = "text-xs text-slate-500 -tracking-[1px] inline-flex"
            ratingTxt.innerHTML = "Câu trả lời này có hữu ích không?"

            likeButton = document.createElement("button")
            likeButton.setAttribute("id", "likeButton")
            likeButton.addEventListener("click", function () {
                rating.innerHTML = ''
                ratingTxt = document.createElement("p")
                ratingTxt.className = "text-xs text-slate-500 -tracking-[1px] inline-flex"
                ratingTxt.innerHTML = "Cảm ơn bạn đã đóng góp ý kiến!"
                rating.appendChild(ratingTxt)
                const messageText = rating.parentElement.previousSibling.firstChild.firstChild.innerHTML;
                const labelText = rating.parentElement.previousSibling.firstChild.firstChild.nextSibling.innerHTML;
                console.log(labelText)
                var requestData = {
                    message: messageText,
                    label: labelText
                };
                $.ajax({
                    type: 'POST',
                    url: 'http://127.0.0.1:8000/thumbsup/',
                    contentType: 'application/json',
                    dataType: 'json',
                    data: JSON.stringify(requestData),
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    },
                });
            });
            dislikeButton = document.createElement("button")
            dislikeButton.setAttribute("id", "dislikeButton")
            dislikeButton.addEventListener("click", function () {
                rating.textContent = '';
                ratingTxt = document.createElement("p")
                ratingTxt.className = "text-xs text-slate-500 -tracking-[1px] inline-flex"
                ratingTxt.innerHTML = "Cảm ơn bạn đã đóng góp ý kiến!"
                rating.appendChild(ratingTxt)
                const messageText = rating.parentElement.previousSibling.firstChild.firstChild.innerHTML;
                var requestData = {
                    message: messageText,
                };
                $.ajax({
                    type: 'POST',
                    url: 'http://127.0.0.1:8000/thumbsdown/',
                    contentType: 'application/json',
                    dataType: 'json',
                    data: JSON.stringify(requestData),
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    },
                });
            });
            like = document.createElement("i")
            like.className = "fa-solid fa-thumbs-up text-slate-500 ml-[5px] hover:text-blue-500"
            dislike = document.createElement("i")
            dislike.className = "fa-solid fa-thumbs-down text-slate-500  ml-[5px] hover:text-blue-500"
            likeButton.appendChild(like)
            dislikeButton.appendChild(dislike)
            rating.appendChild(ratingTxt)
            rating.appendChild(likeButton)
            rating.appendChild(dislikeButton)
            container.appendChild(message)
            container.appendChild(rating)
        }
        chatMessages.appendChild(container);
    }
    function getCSRFToken() {
        var csrfToken = null;
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.indexOf('csrftoken=') === 0) {
                csrfToken = cookie.substring('csrftoken='.length, cookie.length);
                break;
            }
        }
        return csrfToken;
    }
    sendButton.addEventListener("click", function () {
        const messageText = userMessageInput.value;
        if (messageText.trim() !== "") {
            addMessageToChat(messageText, true, false, false)
            var requestData = {
                message: messageText
            };
            $.ajax({
                type: 'POST',
                url: 'http://127.0.0.1:8000/chatting/',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(requestData),
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                success: function (response) {
                    addLabel(response[3])
                    if (response[1] == 0) {
                        addMessageToChat(response[0], false, false, false)
                    } else if (typeof response[1] === 'string') {
                        addMessageToChat(response, false, false, true)
                    } else {
                        addMessageToChat(response, false, true, false)
                    }
                },
                error: function (error) {
                    console.log(error)
                }
            });
            userMessageInput.value = "";
            userMessageInput.focus();
        }
    });

    userMessageInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            sendButton.click();
        }
    });
});
