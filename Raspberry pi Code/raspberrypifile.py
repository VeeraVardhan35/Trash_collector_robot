from picamera2 import Picamera2
from tflite_runtime.interpreter import Interpreter
import numpy as np
import cv2
import time
import serial

# === SERIAL SETUP ===
ser = serial.Serial('/dev/serial0', 9600, timeout=2)
time.sleep(2)  # Wait for Arduino to reset

# === LOAD MODEL ===
interpreter = Interpreter(model_path="model1.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height, width = input_details[0]['shape'][1:3]

labels = {
    0: "cardboard",
    1: "glass",
    2: "metal",
    3: "paper",
    4: "plastic",
    5: "trash"
}

# === CAMERA SETUP ===
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()
time.sleep(1)

print("📷 Starting classification every 15 seconds. Only detecting paper or plastic...")

try:
    while True:
        # Show live preview for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 5:
            preview = picam2.capture_array()
            cv2.imshow("Live Preview - Hold Paper/Plastic", preview)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                raise KeyboardInterrupt

        # Capture and preprocess image
        frame = picam2.capture_array()
        resized = cv2.resize(frame, (width, height))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGRA2RGB)
        input_data = np.expand_dims(rgb, axis=0).astype(np.float32) / 255.0

        # Run inference
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]['index'])

        class_id = int(np.argmax(output[0]))
        confidence = float(output[0][class_id])
        label = labels.get(class_id, "Unknown")

        # Show prediction
        cv2.putText(frame, f"{label}: {confidence:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Prediction", frame)
        cv2.waitKey(1000)

        # Decision logic
        if label == "paper":
            print("🟩 Detected PAPER → Sending '1' to Arduino")
            ser.write(b'1')
        elif label == "plastic":
            print("🟦 Detected PLASTIC → Sending '2' to Arduino")
            ser.write(b'2')
        else:
            print(f"⚠ Detected '{label}', ignoring (not paper/plastic)")

        # Read Arduino response (optional)
        time.sleep(1)
        if ser.in_waiting:
            print("Arduino says:", ser.readline().decode().strip())

        # Wait before next prediction
        print("⏳ Waiting 15 seconds...\n")
        time.sleep(15)

except KeyboardInterrupt:
    print("🛑 Exiting...")

finally:
    ser.close()
    cv2.destroyAllWindows()
    picam2.stop()