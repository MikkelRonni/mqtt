from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app)

# Define MQTT broker settings
mqtt_broker = "mosquittobroker.westeurope.azurecontainer.io"
mqtt_port = 1883
mqtt_topics = ["MIR/temp", "MIR/humi"]

# Initialize data dictionaries for each topic
mqtt_data = {topic: '' for topic in mqtt_topics}

def on_message(client, userdata, message):
    topic = message.topic
    data = message.payload.decode('utf-8')
    mqtt_data[topic] = data  # Update data dictionary
    socketio.emit('mqtt_message', {'topic': topic, 'data': data})

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.loop_start()  # Start the MQTT client loop

@socketio.on('connect')
def handle_connect():
    for topic in mqtt_topics:
        socketio.emit('mqtt_connected', {'data': 'Connected to MQTT broker'})

@app.route('/')
def index():
    return render_template('index.html', mqtt_data=mqtt_data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
