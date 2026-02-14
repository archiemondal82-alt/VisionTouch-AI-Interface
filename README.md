![Project Cover](Vision%20Cover%20iage.png)
# VisionTouch: Contactless HCI Interface 🖱️✋

VisionTouch is a computer vision-based Human-Computer Interaction (HCI) tool that replaces physical input devices with real-time hand gesture recognition. Designed for sterile environments (hospitals) and accessible computing.
![Demo of App](demo.jpg)

## 🚀 Key Features
* **Zero-Hardware Interface:** Uses standard webcams for sub-millimeter precision tracking.
* **Dynamic State Machine:**
    * ☝️ **Index Up:** Cursor Movement (Smoothed)
    * ✌️ **Index + Middle:** Left Click
    * 🤙 **Pinky Up:** Volume Control Mode (Distance-based)
* **Adaptive Smoothing:** Uses a custom interpolation algorithm (`np.interp`) with configurable smoothing factors to eliminate sensor jitter.
* **Configurable Backend:** JSON-based configuration allowing users to tune sensitivity and thresholds without recompiling.

## 🛠️ Tech Stack
* **Core:** Python 3.11
* **Computer Vision:** Google MediaPipe (0.10.9), OpenCV
* **Automation:** PyAutoGUI
* **Deployment:** PyInstaller (Standalone Windows .exe)

## ⚙️ How It Works (The Math)
The system maps the webcam coordinate space $(x_{cam}, y_{cam})$ to the screen resolution $(x_{screen}, y_{screen})$ using linear interpolation:
$$x_{screen} = \text{np.interp}(x_{cam}, [padding, w_{cam}-padding], [0, w_{screen}])$$

## 💿 How to Run
1. Download the latest release from the `dist` folder.
2. Run `ai_mouse.exe`.
3. Press **'q'** to quit the application.

