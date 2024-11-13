from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Receive the notification from Make
    data = request.json

    # Extract the data from the notification
    image_url = data.get('image_url')  # Assuming the image URL is sent in 'image_url'

    # Download the image from the received URL
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Process the image (for example, crop and enlarge)
    width, height = img.size

    center_width = width // 2
    center_height = height // 2

    # Definir el tamaño del recorte centrado (por ejemplo, un cuadrado de la mitad del tamaño original)
    crop_size = min(width, height) // 2  # Esto hace que sea el 50% del tamaño original

    left = center_width - crop_size // 2
    top = center_height - crop_size // 2
    right = center_width + crop_size // 2
    bottom = center_height + crop_size // 2

    # Recortar la imagen para obtener el centro
    cropped_img = img.crop((left, top, right, bottom))

    # Ampliar la imagen (por ejemplo, duplicar el tamaño)
    enlarged_img = cropped_img.resize((int(cropped_img.width * 2), int(cropped_img.height * 2)))

    # Save the processed image to a temporary file
    processed_image_path = 'processed_image.png'
    enlarged_img.save(processed_image_path)

    # Path of the processed file
    processed_image_path = 'processed_image.png'

    # URL of the Make Webhook
    webhook_url = 'https://hook.us2.make.com/m0hyhqp43nblmg0dhm5pfuinkca25aoo'

    # Open the processed image and prepare it to send
    with open(processed_image_path, 'rb') as img_file:
        files = {
            'image': (processed_image_path, img_file, 'image/png')
        }

        # Send the image to Make using a POST request with multipart/form-data
        response = requests.post(webhook_url, files=files)

    # Check the response from the Webhook
    if response.status_code == 200:
        print("Image sent successfully")
        print(response.text)  # If the Webhook returns data, print it
    else:
        print("Failed to send image")
        print(response.text)

    return jsonify({"message": "Image processed successfully", "processed_image_path": processed_image_path})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
