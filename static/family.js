function sendMessage() {
    var messageInput = document.getElementById('message');
    var message = messageInput.value;
    if (message.trim() === "") return;

    var chatBox = document.getElementById('chat-box');

    // Display the user message
    var userMessageElement = document.createElement('div');
    userMessageElement.className = `message ${currentPerson === 'Rakshit' ? 'blue-bg' : 'gray-bg'}`;
    userMessageElement.innerHTML = `
        <div class="message-sender">${currentPerson}</div>
        <div class="message-text">${message}</div>
        <div class="message-timestamp">${new Date().toLocaleTimeString()}</div>
    `;
    chatBox.appendChild(userMessageElement);

    // Scroll to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Clear the input
    messageInput.value = "";

    // Check if the message contains "@rakumon"
    if (message.includes("@rakumon")) {
        // Send the message to the server
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/send_message_family", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onload = function () {
            var response = JSON.parse(xhr.responseText);

            // Display the bot response
            var botMessageElement = document.createElement('div');
            botMessageElement.className = 'message bot';

            var messageToUser = response.message_to_user;
            var productsAreProduced = response.products_are_produced;
            var products = response.products;

            // Create the response content
            var responseContent = `<div class="text">${messageToUser}</div>`;

            // Add product information if products are produced
            if (productsAreProduced) {
                responseContent += '<div class="product-container">';
                products.forEach(product => {
                    responseContent += `
                        <div class="product">
                            <img src="${product.product_img_url}" alt="${product.product_title}">
                            <div class="product-title">${product.product_title}</div>
                            <div class="product-description">${product.product_description}</div>
                            <div class="product-price">${product.product_price}</div>
                        </div>
                    `;
                });
                responseContent += '</div>';
            }

            botMessageElement.innerHTML = responseContent;
            chatBox.appendChild(botMessageElement);

            // Scroll to the bottom
            chatBox.scrollTop = chatBox.scrollHeight;
        };
        xhr.send("message=" + encodeURIComponent(message));
    }
}

// Add an event listener for the Enter key
document.getElementById('message').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();  // Prevent the default action (form submission or newline)
        sendMessage();        // Call the sendMessage function
    }
});
