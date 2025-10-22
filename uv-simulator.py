import gpiod
import time
import random
import paho.mqtt.client as mqtt
import json

# Setup MQTT
client = mqtt.Client()
client.connect("localhost", 1883, 60)

# Setup GPIO (simulated output pin)
chip = gpiod.Chip('gpiochip0')
line = chip.get_line(17)  # use any available GPIO line
line.request(consumer="uv_simulator", type=gpiod.LINE_REQ_DIR_OUT)

while True:
    # Simulate UV index (0–11)
    uv_index = round(random.uniform(0, 11), 2)

    # Convert to HIGH if UV dangerous
    gpio_value = 1 if uv_index > 8 else 0
    line.set_value(gpio_value)

    payload = json.dumps({
        "uv": uv_index,
        "GPIO": gpio_value,
        "timestamp": time.time()
    })

    print(f"UV Index: {uv_index} -> GPIO: {gpio_value}")

    # Publish to MQTT
    client.publish("greenhouse/uv", payload)
    time.sleep(5)