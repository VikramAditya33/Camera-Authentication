# Gesture Authentication System

A cutting-edge biometric authentication system that uses hand gestures for secure login. This system leverages MediaPipe and OpenCV to recognize unique hand gestures as a form of authentication, providing a completely password-free and secure login experience using only your camera.

## Features

### Core Features
- **Gesture-Based Authentication** - Login using unique hand gestures only
- **Flexible Hand Options** - Choose between one-handed or two-handed gestures
- **Visual Login Interface** - Modern GUI with camera authentication
- **Real-time Gesture Recognition** - Live feedback during authentication
- **Camera-Only Authentication** - No passwords required, just your camera and hand gestures
- **User Registration** - Easy registration with gesture recording
- **Secure Storage** - Encrypted gesture data storage
- **Match Score Display** - Real-time similarity percentage during authentication

### Security Features
- Gesture feature extraction with 21-point hand landmark analysis
- **One-Hand Mode** - Easier to use, good for quick access
- **Two-Hand Mode** - Enhanced security with more complex gestures
- Similarity threshold verification (minimum 75% match required)
- Stable frame detection (requires 15 consecutive matching frames)
- Unique gesture per user for enhanced security

## Technical Stack

- **Python 3.11**
- **OpenCV** - Computer vision and camera handling
- **MediaPipe** - Hand landmark detection and tracking
- **Tkinter** - Modern GUI interface
- **NumPy** - Mathematical operations and feature comparison
- **Pillow** - Image processing
- **JSON** - Secure credential storage

## Prerequisites

- Python 3.11 or higher
- Webcam/camera access
- Windows/macOS/Linux operating system

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VikramAditya33/Jasoos-Bandar.git
   cd Jasoos-Bandar
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv mediapipe-env
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     mediapipe-env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source mediapipe-env/bin/activate
     ```

4. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Launch the GUI Application

```bash
python gesture_login_gui.py
```

### First-Time Setup (Registration)

1. Click **"Register"** on the login screen
2. Enter your desired username
3. **Choose your gesture type:**
   - 🖐️ **One Hand** - Easier to use, less secure (peace sign, thumbs up, etc.)
   - 🙌 **Two Hands** - More secure, recommended (unique two-hand gestures)
4. Click **"Register with Gesture"**
5. When prompted, perform your unique hand gesture for 8 seconds
6. Hold the gesture steady - the system will record it
7. Once registered, you'll be redirected to the login screen

### Login with Gesture Authentication

1. Enter your username
2. Click **"Login Through Camera"**
3. Perform your registered gesture in front of the camera
   - The system will automatically detect whether you registered with one or two hands
   - You'll see on-screen feedback showing what it expects
4. The system will show real-time match percentage
5. Once your gesture is recognized and authenticated, you'll be logged in successfully!

### Camera-Only Authentication

- **No passwords needed** - Authentication is 100% camera-based using your unique hand gesture
- The system uses advanced hand landmark detection to verify your identity

## How It Works

### Gesture Recording
1. **Hand Detection** - MediaPipe detects 21 hand landmarks
2. **Feature Extraction** - System extracts:
   - 3D coordinates (x, y, z) of all 21 landmarks
   - Finger angles and orientations
   - Distances from palm center
3. **Feature Storage** - Averaged features stored securely

### Gesture Authentication
1. **Live Detection** - Real-time hand tracking
2. **Feature Comparison** - Euclidean distance calculation
3. **Similarity Score** - Percentage match with stored gesture
4. **Stability Check** - Requires 15 consecutive matching frames
5. **Authentication** - Instant login on successful gesture match

## Project Structure

```
Jasoos-Bandar/
├── gesture_login_gui.py     # Main GUI application
├── gesture_auth.py          # Authentication backend
├── users_db.json           # User credentials database (auto-created)
├── main.py                 # Original monkey detection demo
├── requirements.txt        # Python dependencies
├── src/                    # Assets
│   ├── monkey-normal.jpg
│   ├── monkey-thinking.jpg
│   ├── monkey-knowing.jpg
│   ├── monkey-shocked.jpg
│   └── monkey-chill.jpg
└── README.md              # This file
```

## GUI Features

### Modern Dark Theme Interface
- Sleek dark mode design
- Intuitive button layouts
- Real-time status updates
- Professional color scheme

### User Experience
- Clear visual feedback
- Step-by-step guidance
- Error handling and validation
- Smooth transitions

## Customization

### Adjust Authentication Sensitivity

In `gesture_auth.py`, modify:
```python
threshold=75  # Similarity threshold (0-100)
required_stable_frames=15  # Consecutive matching frames
```

### Change Recording Duration

```python
self.record_gesture(duration=3)  # Recording time in seconds
```

### Modify UI Theme

In `gesture_login_gui.py`, customize colors:
```python
bg="#1e1e2e"  # Background color
fg="#cdd6f4"  # Text color
```

## 📊 Gesture Tips

### Best Practices for Gesture Selection

#### One-Hand Gestures
- ✅ Peace sign (✌️) - Easy and distinct
- ✅ Thumbs up (👍) - Simple to perform
- ✅ OK sign (👌) - Clear finger position
- ✅ Rock sign (🤘) - Unique configuration
- ✅ Number signs (1-5 fingers)

#### Two-Hand Gestures (More Secure)
- ✅ Peace signs on both hands (✌️✌️)
- ✅ Thumbs up with different hand positions
- ✅ Heart shape with both hands
- ✅ Mirror gestures (same gesture on both hands)
- ✅ Asymmetric gestures (different on each hand)

### What Makes a Good Gesture?
- Distinct finger configurations
- Easy to reproduce consistently
- Not easily guessable by others
- Comfortable for frequent use
- **Two-hand gestures are significantly more secure**

## Security Considerations

- Gestures are stored as mathematical feature vectors
- Multi-point verification with 21 hand landmarks
- Stability detection prevents random matches
- Threshold-based authentication
- Pure biometric authentication - no passwords to steal or forget

## Troubleshooting

### Camera Not Opening
- Check camera permissions
- Ensure no other application is using the camera
- Verify camera drivers are installed

### Low Match Percentage
- Ensure good lighting conditions
- Position hand clearly in front of camera
- Perform gesture exactly as during registration
- Keep hand steady

### Registration Failed
- Hold gesture steady for full duration
- Ensure hand is clearly visible
- Check camera is working properly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Ideas for Contribution
- Multi-gesture authentication
- Face recognition integration
- Two-factor authentication
- Mobile app version
- Cloud database integration

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- **MediaPipe** - Excellent hand tracking technology
- **OpenCV** - Computer vision capabilities
- **Python community** - Amazing libraries and support

## Contact

- **GitHub**: [VikramAditya33](https://github.com/VikramAditya33)
- **Repository**: [Jasoos-Bandar](https://github.com/VikramAditya33/Jasoos-Bandar)

## Demo

### Original Monkey Reaction Demo
The project also includes the original monkey reaction system. Run:
```bash
python main.py
```

This demonstrates real-time hand gesture detection with animated monkey reactions.

---

**Made with ❤️ and 🔐 by VikramAditya33**

**Transform your security with camera-only gesture authentication - No passwords, just gestures!**
