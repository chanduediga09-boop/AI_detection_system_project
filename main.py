from ultralytics import YOLO
import cv2
import serial
import time

# -------------------------
# Arduino
# -------------------------

arduino = serial.Serial("COM11", 9600)
time.sleep(2)

# -------------------------
# User Selection
# -------------------------

print("\nSelect Detection Mode")
print("1. Helmet")
print("2. Mask")
print("3. Gloves")

choice = input("\nEnter Choice: ")

# -------------------------
# Load Model
# -------------------------

if choice == "1":
    model = YOLO("best.pt")
    mode = "helmet"

elif choice == "2":
    model = YOLO("mask_best.pt")
    mode = "mask"

elif choice == "3":
    model = YOLO("gloves_best.pt")
    mode = "gloves"

else:
    print("Invalid Choice")
    exit()

# -------------------------
# Webcam
# -------------------------

cap = cv2.VideoCapture(0)

last_signal = None

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, conf=0.5)

    boxes = results[0].boxes

    compliant = False

    # ==================================
    # HELMET MODE
    # ==================================

    if mode == "helmet":

        head_count = 0
        helmet_count = 0

        for box in boxes:

            cls_id = int(box.cls)
            class_name = model.names[cls_id]

            if class_name == "head":
                head_count += 1

            elif class_name == "helmet":
                helmet_count += 1

        print("Heads:", head_count)
        print("Helmets:", helmet_count)

        if head_count > 0:
            compliant = False

        elif helmet_count > 0:
            compliant = True

        else:
            compliant = False

    # ==================================
    # MASK MODE
    # ==================================

    elif mode == "mask":

        masque_count = 0
        pasmasque_count = 0
        notcorrect_count = 0

        for box in boxes:

            cls_id = int(box.cls)
            class_name = model.names[cls_id]

            if class_name == "Masque":
                masque_count += 1

            elif class_name == "PasMasque":
                pasmasque_count += 1

            elif class_name == "Notcorrect":
                notcorrect_count += 1

        print("Masque:", masque_count)
        print("PasMasque:", pasmasque_count)
        print("Notcorrect:", notcorrect_count)

        if pasmasque_count > 0 or notcorrect_count > 0:
            compliant = False

        elif masque_count > 0:
            compliant = True

        else:
            compliant = False

    # ==================================
    # GLOVES MODE
    # ==================================

    elif mode == "gloves":

        glove_count = 0
        no_glove_count = 0

        for box in boxes:

            cls_id = int(box.cls)
            class_name = model.names[cls_id]

            if class_name == "glove":
                glove_count += 1

            elif class_name == "no_glove":
                no_glove_count += 1

        print("Glove:", glove_count)
        print("No Glove:", no_glove_count)

        if no_glove_count > 0:
            compliant = False

        elif glove_count > 0:
            compliant = True

        else:
            compliant = False

    # ==================================
    # FINAL DECISION
    # ==================================

    if compliant:

        status = "COMPLIANT"
        signal = "G"
        color = (0, 255, 0)

    else:

        status = "NON-COMPLIANT"
        signal = "R"
        color = (0, 0, 255)

    # ==================================
    # Arduino
    # ==================================

    if signal != last_signal:

        arduino.write(signal.encode())
        last_signal = signal

    # ==================================
    # Display
    # ==================================

    annotated = results[0].plot()

    cv2.putText(
        annotated,
        status,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.imshow("AI Compliance Monitoring", annotated)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# -------------------------
# Cleanup
# -------------------------

arduino.write(b"N")

cap.release()
arduino.close()

cv2.destroyAllWindows()