from flask import Flask, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':
   app.run()

# MQTT connection details
broker_address = "mosquittobroker.westeurope.azurecontainer.io"
broker_port = 1883  # Change this to the correct port
topic_temp = "MIR/temp"
topic_humi = "MIR/humi"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic_temp)
    client.subscribe(topic_humi)

def on_message(client, userdata, msg):
    print("Received message on topic: " + msg.topic)
    # You can send the message data to the HTML template via WebSockets or any other method of your choice

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, broker_port)

client.loop_start()

