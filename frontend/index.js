// import axios from "axios";
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const botMessage = document.getElementById("bot-message");

// Replace with your actual API endpoint
const apiUrl = "http://localhost:5000/assistant";

sendButton.addEventListener("click", async () => {
  const userText = userInput.value.trim();
  if (!userText) {
    return;
  }

  try {
    const response = await axios.get(apiUrl, {
      params: {
        userQuery: userText,
      },
    });

    botMessage.textContent = response.data.message;
    userInput.value = ""; // Clear user input after sending
  } catch (error) {
    console.error("Error fetching response:", error);
    botMessage.textContent = "Error: Could not get response from AI.";
  }
});
