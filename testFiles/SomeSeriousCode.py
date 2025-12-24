import gradio as gr
import requests
from dotenv import load_dotenv
import os

# Load environment variables from a .env file (security best practice)
load_dotenv()
url = os.getenv("url")            # Endpoint for the Chat (LLM)
model_url = os.getenv("model_url") # Endpoint for the Machine Learning model (CSV)
cnn_url = os.getenv("CNN_URL")     # Endpoint for the Computer Vision model (CNN)

def chat(message, history):
    """
    Handles the chatbot logic.
    Converts Gradio's history format into role-based format (user/model) 
    and sends it to an external API.
    """
    messages = []

    # Reconstruct conversation history so the model has context
    for msg, ai_msg in history:
        messages.append({"role" : "user", "content" : msg})
        messages.append({"role" : "model", "content" : ai_msg})

    # Append the user's current message
    messages.append({"role": "user", "content": message})

    try:
        # Send the list of messages via POST to the LLM API
        response = requests.post(url, json=messages)
        response.raise_for_status() # Raises an error if the response is not 200 OK

        data = response.json()
        # Extract the response from JSON or return a default error message
        ai_response = data.get("response", "Error retrieving response")

        return ai_response
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    
def model_prediction(csv_filepath: str) -> str:
    """
    Receives a CSV file, sends it to an ML model, 
    and returns the prediction with an explanation.
    """
    if csv_filepath is None:
        return "Please upload a file"
    try:
        # Open the file in binary read mode to send it via HTTP
        with open(csv_filepath, "rb") as f:
            files = {"csv" : (csv_filepath, f, "text/csv")}

            # Send the file as 'multipart/form-data'
            response = requests.post(model_url, files=files)
            response.raise_for_status()

            data = response.json()

            # Handle specific errors sent back by the API
            if data.get("result") == "Error":
                return f"Error: {data.get('message')}"
            
            prediction = data.get("prediction")
            explanation = data.get("explicacion")

            # Format the output using Markdown for Gradio
            output_text = (
                f"**Model Prediction:** {prediction}\n"
                f"**Explanation:** {explanation}"
            )
            return output_text
        
    except requests.exceptions.RequestException as e:
        return f"Connection error with the model service: {e}"

def cnn_image(image_filepath):
    """
    Receives an image and sends it to a Convolutional Neural Network (CNN)
    for image classification.
    """
    if image_filepath is None:
        return "Please upload an image"
    try:
        with open(image_filepath, "rb") as f:
            files = {'image' : (image_filepath, f, "image/jpeg")}

            # Perform the POST request with the image file
            response = requests.post(cnn_url, files=files)
            response.raise_for_status()

            data = response.json()

            if data.get("result") == "Error":
                return f"Error: {data.get('message')}"
            
            # Extract multiple information fields from the image analysis
            prediction = data.get("prediction")
            confidence = data.get("confidence")
            explanation = data.get("explanation")
            limitations = data.get("limitations")

            # Structure the final report for the user
            output_text = (
                f"Classification Result: {prediction.upper()}\n"
                f"Confidence: {confidence}\n\n"
                f"Explanation: {explanation}\n\n"
                f"System Limitations:\n{limitations}"
            )
            return output_text
        
    except requests.exceptions.RequestException as e:
        return f"Connection error with the CNN service: {e}"

# --- UI DESIGN WITH GRADIO ---
with gr.Blocks() as interface:
    gr.Markdown('# LLM Chat, ML Analysis, and Image Classification')

    # Section 1: Interactive Chatbot
    gr.ChatInterface(chat, title="LLM Chat")

    # Section 2: CSV File Upload and ML Analysis
    gr.Markdown('# ML Analysis')
    inputs=gr.File(label="Upload data file", type="filepath", file_count='single')
    model_output = gr.TextArea(label="Results", interactive=False)
    sendFile = gr.Button("Send")

    # Link the button to the model_prediction function
    sendFile.click(
        fn=model_prediction,
        inputs=[inputs],
        outputs=[model_output]
    )
    
    # Section 3: Image Upload and Classification
    gr.Markdown('# Image Classification')
    image = gr.File(label="Upload your image", type="filepath", file_count='single', file_types=['image'])
    image_output = gr.TextArea(label="Results", interactive=False)
    sendImage = gr.Button("Send")

    # Link the button to the cnn_image function
    sendImage.click(
        fn=cnn_image,
        inputs=[image],
        outputs=[image_output]
    )

# Launch the app (0.0.0.0 allows access from other devices on the network)
interface.launch(server_name="0.0.0.0", server_port=7860)