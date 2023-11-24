from flask import Flask, request, Response
import cv2
import numpy as np
import networkx as nx
import json

app = Flask(__name__)

# Algoritma Dijkstra dan graf Anda
graph = {
    'G1': {'C101': 1, 'SAC': 1},
    'C101': {'G1': 1, 'C102': 1},
    'C102': {'C101': 1, 'C102P': 1},
    'C102P': {'C102': 1, 'C103': 1},
    'C103': {'C102P': 1, 'C104': 1},
    'C104': {'C103': 1, 'C105': 1},
    'C105': {'C104': 1, 'C105P': 1},
    'C105P': {'C105': 1, 'TE': 1},
    'TE': {'C105P': 1, 'E105': 1},
    'E105': {'TE': 1, 'E106': 1},
    'E106': {'E105': 1, 'E107': 1},
    'E107': {'E106': 1, 'E108': 1},
    'E108': {'E107': 1, 'CED': 1},
    'CED': {'E108': 1, 'D104': 1},
    'D104': {'CED': 1, 'D103': 1},
    'D103': {'D104': 1, 'D102': 1},
    'D102': {'D103': 1, 'A101': 1},
    'A101': {'D102': 1, 'G2': 1},
    'G2': {'A101': 1, 'A102': 1},
    'A102': {'G2': 1, 'SAC': 1},
    'SAC': {'A102': 1, 'G1': 1},
}

G = nx.Graph()
G.add_nodes_from(graph.keys())
for node, neighbors in graph.items():
    for neighbor, weight in neighbors.items():
        G.add_edge(node, neighbor, weight=weight)

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Fungsi untuk melakukan deteksi objek pada frame
def detect_objects(frame):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 2)
            cv2.putText(frame, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 2)
    return frame

# Fungsi untuk melakukan live detection
def live_detection():
    cap = cv2.VideoCapture(0)  # Membuka kamera

    while True:
        ret, frame = cap.read()  # Membaca frame dari kamera
        if not ret:
            break

        frame = detect_objects(frame)  # Melakukan deteksi objek pada frame

        # Mengubah frame menjadi format yang dapat ditransmisikan melalui HTTP
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(live_detection(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/shortest_path', methods=['POST'])
def shortest_path():
    data = request.get_json()
    source = data['source']
    target = data['target']
    shortest_path = nx.dijkstra_path(G, source, target)
    return json.dumps(shortest_path)

if __name__ == '__main__':
    app.run(host='103.127.97.215:5000', debug=True)