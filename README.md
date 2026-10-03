# AI Detection System

An AI-based safety compliance monitoring system that uses **YOLOv8, OpenCV, and Arduino** to detect safety equipment through a webcam and provide a real-time compliance signal.

The system currently supports three detection modes:

* 🪖 Helmet Detection
* 😷 Mask Detection
* 🧤 Glove Detection

When the required safety equipment is detected, the system considers the person **COMPLIANT** and sends a green (`G`) signal to the Arduino.

If the required safety equipment is missing or incorrect, it considers the situation **NON-COMPLIANT** and sends a red (`R`) signal.

---

## Features

* Real-time detection using a webcam
* YOLO-based object detection
* Three detection modes:

  * Helmet
  * Mask
  * Gloves
* Displays detection results using OpenCV
* Shows `COMPLIANT` / `NON-COMPLIANT` status
* Sends compliance signals to Arduino
* Uses separate trained models for each detection mode

---

## Technologies Used

* **Python**
* **YOLOv8 / Ultralytics**
* **OpenCV**
* **PySerial**
* **Arduino Uno**
* **Webcam**

---

## Project Structure

```text
AI_detection_system_project/
│
├── main.py
├── best.pt
├── mask_best.pt
├── gloves_best.pt
├── requirements.txt
├── .gitignore
└── README.md
```

### Model Files

| File             | Purpose                |
| ---------------- | ---------------------- |
| `best.pt`        | Helmet detection model |
| `mask_best.pt`   | Mask detection model   |
| `gloves_best.pt` | Glove detection model  |

---

## How It Works

The system follows these basic steps:

```text
Webcam
   ↓
Capture Video Frame
   ↓
YOLO Model
   ↓
Detect Safety Equipment
   ↓
Check Compliance
   ↓
COMPLIANT / NON-COMPLIANT
   ↓
Arduino Signal
   ↓
Green / Red Indicator
```

---

## Detection Modes

When the program starts, it asks the user to select a detection mode.

```text
Select Detection Mode
1. Helmet
2. Mask
3. Gloves
```

### 1. Helmet Mode

The helmet model detects:

* `head`
* `helmet`

If a head is detected without the required helmet condition, the system marks the situation as:

```text
NON-COMPLIANT
```

If the helmet condition is satisfied:

```text
COMPLIANT
```

---

### 2. Mask Mode

The mask model detects:

* `Masque`
* `PasMasque`
* `Notcorrect`

The system treats `PasMasque` and `Notcorrect` as non-compliant conditions.

---

### 3. Glove Mode

The glove model detects:

* `glove`
* `no_glove`

If `no_glove` is detected, the system marks the situation as:

```text
NON-COMPLIANT
```

If a glove is detected without a `no_glove` detection:

```text
COMPLIANT
```

---

## Arduino Communication

The Python program communicates with an Arduino through a serial connection.

The current code uses:

```python
arduino = serial.Serial("COM11", 9600)
```

The Arduino receives:

| Signal | Meaning        |
| ------ | -------------- |
| `G`    | Compliant      |
| `R`    | Non-compliant  |
| `N`    | Neutral / Stop |

### Important

`COM11` is specific to the computer where the Arduino is connected.

If your Arduino appears on another COM port, change:

```python
"COM11"
```

to your Arduino's actual COM port.

For example:

```python
arduino = serial.Serial("COM5", 9600)
```

---

## Requirements

Install the required Python libraries using:

```bash
pip install -r requirements.txt
```

The project uses:

```text
ultralytics
opencv-python
pyserial
```

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/chanduediga09-boop/AI_detection_system_project.git
```

### 2. Open the project folder

```bash
cd AI_detection_system_project
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Connect the Arduino

Connect the Arduino to the computer and check its COM port.

If required, update the COM port in `main.py`.

### 5. Start the program

```bash
python main.py
```

If `python` is not recognized on Windows, you can use:

```bash
py main.py
```

### 6. Select a detection mode

Choose:

```text
1 → Helmet
2 → Mask
3 → Gloves
```

The webcam will then start the selected detection model.

---

## Controls

Press:

```text
ESC
```

to stop the webcam detection and exit the program.

---

## Hardware

The current project uses:

* Arduino Uno
* Webcam
* Buzzer / LED indicator setup connected to Arduino
* Computer for running the Python detection system

The Python application sends the compliance status to the Arduino through serial communication.

---

## Safety Decision Logic

The system converts the YOLO detections into a simple compliance decision.

```text
Detection
    ↓
Required equipment present?
    ↓
 ┌───────────────┐
 │               │
 YES             NO
 │               │
 ↓               ↓
COMPLIANT     NON-COMPLIANT
 │               │
 ↓               ↓
Send "G"       Send "R"
```

---

## Limitations

* The system currently uses a webcam connected to the computer.
* The Arduino COM port is configured directly in the Python code.
* Detection accuracy depends on the trained YOLO models, camera quality, lighting, distance, and environment.
* The current application supports one selected detection mode at a time.
* The `.pt` model files are included in the repository because they are required by the current application.

---

## Future Improvements

Possible improvements include:

* Add a graphical user interface
* Make the Arduino COM port configurable
* Support multiple PPE types simultaneously
* Add detection statistics and counting
* Add an LCD display for compliance counts
* Store detection results
* Add timestamps and reports
* Improve the model with more training data
* Deploy the system on an edge device such as Raspberry Pi

---

## Author

**Chandu Ediga**

B.Tech — Computer Science / AI & ML

GitHub: [@chanduediga09-boop](https://github.com/chanduediga09-boop)
