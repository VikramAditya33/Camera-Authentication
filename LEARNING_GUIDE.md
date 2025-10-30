# Learning Guide: Camera Gesture Authentication System

## Prerequisites

- Python 3.11 or higher
- Webcam/camera
- Windows/macOS/Linux

## Installation

1. Clone the repository:
```bash
git clone https://github.com/VikramAditya33/Camera-Authentication.git
cd Camera-Authentication
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python gesture_login_gui.py
```

---

## What This Project Does

A login system that uses hand gestures instead of passwords. You register with a gesture, then use that same gesture to login.

**Registration:** Show your gesture for 8 seconds → system saves it  
**Login:** Show the same gesture → system recognizes you → logged in

---

## Technologies Used

### Python
Programming language. The code is written in Python.

### OpenCV (cv2)
Handles camera input and video display.

```python
cap = cv2.VideoCapture(0)  # Opens camera
ret, frame = cap.read()      # Gets frame
cv2.imshow("Video", frame)   # Shows frame
```

### MediaPipe
Detects hands and extracts 21 landmark points per hand.

```python
hands = mp.solutions.hands.Hands()
result = hands.process(frame)  # Detects hands
```

**Configuration used:**
- `max_num_hands=1` or `2` (one-hand or two-hand mode)
- `min_detection_confidence=0.7` (70% confidence required)
- `min_tracking_confidence=0.7` (70% tracking confidence)

### NumPy
Stores hand data as arrays and calculates distances.

```python
features = np.array([0.5, 0.3, 0.2, ...])
distance = np.linalg.norm(features1 - features2)
```

### Tkinter
Creates the GUI (windows, buttons, text fields).

```python
button = tk.Button(window, text="Login", command=login)
button.pack()
```

### JSON
Stores user data in `users_db.json` file.

**Note:** JSON file is created automatically when first user registers. Contains username, gesture features, and registration timestamp.

### Threading
Used in GUI to prevent freezing when camera operations run. Background thread handles camera while UI stays responsive.

```python
thread = threading.Thread(target=authenticate, daemon=True)
thread.start()  # Runs in background
```

---

## How It Works

### Registration Flow

1. User enters username
2. User chooses one-hand or two-hand gesture
3. Camera opens, user shows gesture for 8 seconds
4. System captures ~240 frames (30 fps × 8 seconds)
5. For each frame:
   - MediaPipe detects hand → finds 21 points
   - Extracts features (coordinates, angles, distances)
   - Stores feature array
6. Average all frames → create one signature
7. Save to `users_db.json`

### Login Flow

1. User enters username
2. User clicks "Login Through Camera"
3. Camera opens, user shows gesture
4. System continuously:
   - Captures frame
   - MediaPipe detects hand → extracts features
   - Loads stored signature from JSON
   - Calculates similarity percentage
   - If similarity ≥ 75% for 15 consecutive frames → success
5. Show dashboard

---

## Project Structure

```
Camera-Authentication/
├── gesture_login_gui.py    # GUI (what user sees)
├── gesture_auth.py        # Core logic (how it works)
├── users_db.json          # User database
└── requirements.txt       # Dependencies
```

---

## Code Overview

### gesture_auth.py

**GestureAuthenticator class** - Handles all authentication logic.

**Key functions:**

- `init_camera()` - Opens webcam
- `extract_hand_features()` - Converts hand landmarks to numbers (21 points × 3 coordinates + angles + distances)
- `extract_two_hands_features()` - Same but for two hands
- `record_gesture()` - Records gesture for 8 seconds, averages frames
- `calculate_gesture_similarity()` - Compares two gestures, returns 0-100% match
- `register_user()` - Records gesture and saves to JSON
- `verify_gesture_live()` - Real-time verification during login

### gesture_login_gui.py

**GestureLoginApp class** - Handles user interface.

**Key functions:**

- `show_login_screen()` - Creates login UI
- `show_register_screen()` - Creates registration UI
- `login_with_gesture()` - Handles login button click
- `show_dashboard()` - Success screen after login

---

## Key Concepts

### Hand Landmarks (21 Points)

MediaPipe detects 21 points on each hand:
- Wrist (point 0)
- Each finger: 4 points (base, middle joint, top joint, tip)
- Total: 1 wrist + 5 fingers × 4 = 21 points

Each point has x, y, z coordinates (normalized 0-1).

### Feature Extraction

Converts hand shape to numbers:
- 21 points × 3 coordinates = 63 numbers
- 5 finger angles = 5 numbers
- 5 distances from palm = 5 numbers
- Total: ~73 numbers per hand

**How it works:**
1. Takes 21 landmark points from MediaPipe
2. Extracts x, y, z coordinates for each point
3. Calculates angles for finger tips (using arctan2)
4. Calculates distances from palm center to each fingertip
5. Combines all into one feature array

**For two hands:**
- Same process for both hands
- Adds distance between hands
- Adds angle between hands
- Total: ~146 numbers for two hands

### Similarity Calculation

```python
# Current gesture vs stored gesture
distance = np.linalg.norm(features1 - features2)
similarity = 100 * (1 - distance / max_distance)
```

Smaller distance = more similar. Returns 0-100% match.

### Why These Numbers?

- **8 seconds recording:** Enough time to average out small movements
- **75% threshold:** Balance between security and usability
- **15 consecutive frames:** Prevents accidental matches (0.5 seconds)
- **21 points:** Enough to represent any hand shape accurately

---

## Common Questions

**Q: Can two people have the same gesture?**  
A: Very unlikely. Hand size, finger length, and exact positions are unique.

**Q: Why average frames?**  
A: Hand moves slightly even when trying to stay still. Averaging smooths this out.

**Q: Is it secure?**  
A: More secure than passwords, less secure than fingerprint. Good for medium security.

**Q: Why 21 points?**  
A: MediaPipe's model uses 21 points. It's sufficient for accuracy.

---

## Learning Path

### If you're new to Python:

1. Learn Python basics (variables, functions, classes, lists, dictionaries)
2. Learn about file operations (reading/writing JSON)
3. Install libraries: `pip install opencv-python mediapipe numpy pillow`
4. Try OpenCV basics (open camera, display frames)
5. Try MediaPipe basics (detect hands, draw landmarks)
6. Read through this project's code

### If you know Python:

1. Read `gesture_auth.py` line by line
2. Understand each function
3. Read `gesture_login_gui.py`
4. Run the code and trace execution
5. Modify values (threshold, duration) and see what happens

---

## Code Examples

### Recording a Gesture

```python
def record_gesture(self, duration=8):
    cap = self.init_camera()
    recorded_features = []
    hands = mp.solutions.hands.Hands()
    
    start_time = datetime.now()
    
    while (datetime.now() - start_time).seconds < duration:
        ret, frame = cap.read()
        result = hands.process(frame)
        
        if result.multi_hand_landmarks:
            features = self.extract_hand_features(result.multi_hand_landmarks[0])
            recorded_features.append(features)
        
        cv2.imshow("Record Gesture", frame)
    
    return np.mean(recorded_features, axis=0)  # Average all frames
```

### Comparing Gestures

```python
def calculate_gesture_similarity(self, features1, features2):
    f1 = np.array(features1)
    f2 = np.array(features2)
    distance = np.linalg.norm(f1 - f2)
    max_distance = 5.0
    similarity = 100 * (1 - distance / max_distance)
    return max(0, similarity)
```

---

## File Structure Details

### gesture_auth.py

- `__init__` - Sets up MediaPipe, loads users
- `load_users()` - Reads from users_db.json
- `save_users()` - Writes to users_db.json
- `init_camera()` - Opens camera (640×480, 30fps)
- `extract_hand_features()` - Converts landmarks to feature array
- `extract_two_hands_features()` - Combines two hand features
- `calculate_gesture_similarity()` - Returns match percentage
- `record_gesture()` - Records for 8 seconds, averages frames
- `register_user()` - Records and saves gesture
- `verify_gesture_live()` - Real-time verification loop

### gesture_login_gui.py

- `__init__` - Creates window, sets up styles
- `show_login_screen()` - Login UI
- `show_register_screen()` - Registration UI
- `login_with_gesture()` - Handles login in background thread
- `show_dashboard()` - Success screen

---

## Data Flow

**Registration:**
```
Show gesture → Camera captures frames → MediaPipe detects hand → 
Extract features → Average frames → Save to JSON
```

**Login:**
```
Show gesture → Camera captures frames → MediaPipe detects hand → 
Extract features → Load from JSON → Compare → If match ≥ 75% for 15 frames → Success
```

---

## Data Storage Format

The `users_db.json` file stores data like this:

```json
{
  "username": {
    "gesture": [0.5, 0.3, 0.2, 0.4, ...],
    "two_hands": true,
    "created_at": "2025-10-29T10:30:00"
  }
}
```

- `gesture`: Array of numbers representing hand shape (~73 numbers for one hand, ~146 for two hands)
- `two_hands`: Boolean indicating if user registered with two hands
- `created_at`: ISO timestamp of registration

---

## Troubleshooting

### Camera not opening
- Check if camera is being used by another application
- Verify camera permissions in system settings
- Try changing camera index: `cv2.VideoCapture(1)` instead of `0`

### Low match percentage
- Ensure good lighting
- Keep hand steady during recording and login
- Show gesture exactly as during registration
- Try registering again with better lighting

### Hand not detected
- Check lighting conditions
- Make sure hand is fully visible in frame
- Move closer to camera
- Clean camera lens

### Registration fails
- Hold gesture steady for full 8 seconds
- Ensure hand is clearly visible
- Try with different gesture (more distinct)

### GUI freezes during camera operations
- This shouldn't happen as threading is used, but if it does, check if daemon thread is properly set

---

## Tips for Good Gestures

**One-hand gestures:**
- Peace sign (✌️)
- Thumbs up (👍)
- OK sign (👌)
- Rock sign (🤘)
- Number signs (1-5 fingers)

**Two-hand gestures (more secure):**
- Peace signs on both hands
- Mirror gestures (same on both hands)
- Asymmetric gestures (different on each hand)
- Heart shape with both hands

**What makes a good gesture:**
- Distinct finger configuration
- Easy to reproduce consistently
- Comfortable to hold for 8 seconds
- Not easily guessable

---

## Understanding the Code Flow

### When you click "Register with Gesture":

1. GUI calls `register_user()` from `gesture_auth.py`
2. `register_user()` calls `record_gesture()`
3. `record_gesture()` opens camera loop:
   - Captures frame
   - MediaPipe detects hand
   - Extracts features
   - Stores in array
   - Repeats for 8 seconds
4. Averages all feature arrays
5. Saves to JSON via `save_users()`

### When you click "Login Through Camera":

1. GUI calls `login_with_gesture()` in background thread
2. Calls `verify_gesture_live()` from `gesture_auth.py`
3. `verify_gesture_live()` opens camera loop:
   - Captures frame
   - MediaPipe detects hand
   - Extracts features
   - Loads stored gesture from JSON
   - Calculates similarity
   - If ≥ 75% for 15 frames → success
4. Updates GUI with result

---

## Modifying the Code

### Change similarity threshold:

In `gesture_auth.py`, line 177 or 163:
```python
def verify_gesture_live(self, username, threshold=75):  # Change 75 to your value
```

### Change recording duration:

In `gesture_auth.py`, line 152:
```python
gesture_features = self.record_gesture(duration=8, use_two_hands=use_two_hands)  # Change 8 to your value
```

### Change required stable frames:

In `gesture_auth.py`, line 196:
```python
required_stable_frames = 15  # Change 15 to your value
```

### Change UI colors:

In `gesture_login_gui.py`, modify colors like:
```python
bg="#1e1e2e"  # Background color
fg="#cdd6f4"  # Text color
```

---

## Next Steps

1. Run the code and test it
2. Add print statements to see what's happening
3. Modify threshold values and see effects
4. Try adding new features
5. Read the actual code files alongside this guide
