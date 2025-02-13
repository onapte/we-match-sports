
document.addEventListener('DOMContentLoaded', (e) => {
    e.preventDefault();

    let chatSendButton = document.querySelector('#chat-send');

    let chatListItems = document.querySelectorAll('.chat-list-item');


    chatSendButton.addEventListener('click', (e) => {
        e.preventDefault();

        let chatContent = document.querySelector('#message-content').value;
        let userId = document.querySelector('.chat-header').getAttribute('data-user-id');

        console.log(`Sending message: ${chatContent}`);

        const currentDatetime = new Date();
        const formattedDatetime = currentDatetime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }) + 
            ', ' + 
            currentDatetime.toISOString().split('T')[0];

        const chatMessagesContainer = document.querySelector('.chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'sent');

        const messageContent = document.createElement('p');
        messageContent.textContent = chatContent;

        const timestampDiv = document.createElement('div');
        timestampDiv.classList.add('message-timestamp');
        timestampDiv.textContent = formattedDatetime;

        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(timestampDiv);
        chatMessagesContainer.appendChild(messageDiv);

        // Clear the input field
        document.querySelector('#message-content').value = '';

        // Scroll to the latest message
        chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;


        fetch('/chats/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token for security
            },
            body: JSON.stringify({'message-content': chatContent, 'user_id': userId}),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })

    })


    chatListItems.forEach((item) => {
        item.addEventListener('click', function (e) {
            // Remove 'active' class from all items
            e.preventDefault();
            console.log('CLICKED');
            chatListItems.forEach((el) => el.classList.remove('active'));

            // Add 'active' class to the clicked item
            this.classList.add('active');

            // Get the user ID from a custom attribute (if used)
            const userId = this.getAttribute('data-user-id');
            
            fetch (`user-messages/${userId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                loadMessages(data);
            })

            
        });
    });

})

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const loadMessages = (data) => {
    // Clear existing messages
    const chatHeader = document.querySelector('.chat-header');
    const chatMessagesContainer = document.querySelector('.chat-messages');
    chatMessagesContainer.innerHTML = '';

    // Update the header
    chatHeader.textContent = `${data.first_name} ${data.last_name}`;
    chatHeader.setAttribute('data-user-id', data._id);

    // Populate new messages
    data.messages.forEach((message) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', message.type);

        const messageContent = document.createElement('p');
        messageContent.textContent = message.content;

        const timestampDiv = document.createElement('div');
        timestampDiv.classList.add('message-timestamp');
        timestampDiv.textContent = message.timestamp;

        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(timestampDiv);

        chatMessagesContainer.appendChild(messageDiv);
    });

    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
}