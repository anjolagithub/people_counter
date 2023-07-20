from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

# Load YOLO model for person detection
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

def count_people(image):
    # Resize image for faster processing (optional)
    # You can experiment with different dimensions for optimization
    resized_image = cv2.resize(image, (416, 416))

    # Preprocess image for YOLO model input
    blob = cv2.dnn.blobFromImage(resized_image, 1/255.0, (416, 416), swapRB=True, crop=False)

    # Set the input for the YOLO model
    net.setInput(blob)
 
    # Get the output layer names
    output_layer_names = net.getUnconnectedOutLayersNames()

    # Run forward pass through the YOLO network
    outputs = net.forward(output_layer_names)

    # Process the outputs to count the number of people
    people_count = 0
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if class_id == 0 and confidence > 0.5: 
                people_count += 1

    return people_count

@app.route('/count_people', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file pr ovided.'}), 400

    try:
        image_file = request.files['image']
        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        people_count = count_people(image)

        return jsonify({'people_count': people_count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
