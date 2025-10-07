import numpy as np
import cv2
import time
from picamera2 import Picamera2
import tflite_runtime.interpreter as tflite

# Load TFLite model (optimized for Raspberry Pi)
interpreter = tflite.Interpreter(model_path="quantized_and_pruned_model.tflite")
interpreter.allocate_tensors()

# Get model input/output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Labels (match model training order)
class_names = ["cardboard", "metal", "paper", "plastic"]

# Initialize Picamera2 with lower resolution for faster performance
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"format": 'RGB888', "size": (320, 240)})
picam2.configure(preview_config)
picam2.start()
time.sleep(2)  # Allow camera to warm up

def preprocess(image):
    image = cv2.resize(image, (224, 224))  # Resize to model input
    image = image.astype(np.float32) / 255.0  # Normalize
    return np.expand_dims(image, axis=0)

def predict(image):
    input_data = preprocess(image)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    pred_idx = np.argmax(output_data)
    confidence = output_data[0][pred_idx]
    return class_names[pred_idx], confidence

# Frame skip counter
frame_id = 0
label = ""
confidence = 0

try:
    while True:
        frame = picam2.capture_array()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_id += 1

        if frame_id % 5 == 0:
            label, confidence = predict(frame_rgb)

        text = f"{label} ({confidence*100:.1f}%)"
        cv2.putText(frame, text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Garbage Classifier", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\n[INFO] Exiting...")

finally:
    cv2.destroyAllWindows()
    picam2.close()
