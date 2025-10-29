import cv2
import mediapipe as mp
import numpy as np
import json
import os
from datetime import datetime

class GestureAuthenticator:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_face = mp.solutions.face_detection
        self.mp_draw = mp.solutions.drawing_utils
        self.users_db = "users_db.json"
        self.cap = None
        self.load_users()
        
    def load_users(self):
        if os.path.exists(self.users_db):
            with open(self.users_db, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
            
    def save_users(self):
        with open(self.users_db, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def init_camera(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            for _ in range(5):
                self.cap.read()
        return self.cap
    
    def release_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            cv2.destroyAllWindows()
    
    def extract_hand_features(self, hand_landmarks):
        if not hand_landmarks:
            return None
        features = []
        landmarks = hand_landmarks.landmark
        for lm in landmarks:
            features.extend([lm.x, lm.y, lm.z])
        tip_ids = [4, 8, 12, 16, 20]
        for tip_id in tip_ids:
            if tip_id > 0:
                dx = landmarks[tip_id].x - landmarks[tip_id - 2].x
                dy = landmarks[tip_id].y - landmarks[tip_id - 2].y
                features.append(np.arctan2(dy, dx))
        palm_center = landmarks[0]
        for tip_id in tip_ids:
            dx = landmarks[tip_id].x - palm_center.x
            dy = landmarks[tip_id].y - palm_center.y
            features.append(np.sqrt(dx**2 + dy**2))
        return np.array(features)
    
    def extract_two_hands_features(self, multi_hand_landmarks):
        if not multi_hand_landmarks or len(multi_hand_landmarks) < 2:
            return None
        hand1_features = self.extract_hand_features(multi_hand_landmarks[0])
        hand2_features = self.extract_hand_features(multi_hand_landmarks[1])
        if hand1_features is None or hand2_features is None:
            return None
        hand1_center = multi_hand_landmarks[0].landmark[0]
        hand2_center = multi_hand_landmarks[1].landmark[0]
        hand_distance = np.sqrt(
            (hand1_center.x - hand2_center.x)**2 + 
            (hand1_center.y - hand2_center.y)**2 + 
            (hand1_center.z - hand2_center.z)**2
        )
        hand_angle = np.arctan2(
            hand2_center.y - hand1_center.y,
            hand2_center.x - hand1_center.x
        )
        return np.concatenate([hand1_features, hand2_features, [hand_distance, hand_angle]])
    
    def calculate_gesture_similarity(self, features1, features2):
        if features1 is None or features2 is None:
            return 0.0
        f1 = np.array(features1)
        f2 = np.array(features2)
        distance = np.linalg.norm(f1 - f2)
        max_distance = 5.0
        return max(0, 100 * (1 - distance / max_distance))
    
    def record_gesture(self, duration=8, min_frames=60, use_two_hands=True):
        cap = self.init_camera()
        recorded_features = []
        max_hands = 2 if use_two_hands else 1
        with self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        ) as hands:
            start_time = datetime.now()
            frame_count = 0
            
            while (datetime.now() - start_time).seconds < duration:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(rgb)
                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    if use_two_hands:
                        if len(result.multi_hand_landmarks) >= 2:
                            features = self.extract_two_hands_features(result.multi_hand_landmarks)
                            if features is not None:
                                recorded_features.append(features.tolist())
                                frame_count += 1
                            cv2.putText(frame, "TWO HANDS DETECTED!", (10, frame.shape[0] - 60),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        else:
                            cv2.putText(frame, "SHOW BOTH HANDS!", (10, frame.shape[0] - 60),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    else:
                        features = self.extract_hand_features(result.multi_hand_landmarks[0])
                        if features is not None:
                            recorded_features.append(features.tolist())
                            frame_count += 1
                        cv2.putText(frame, "ONE HAND DETECTED!", (10, frame.shape[0] - 60),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                remaining = duration - (datetime.now() - start_time).seconds
                cv2.putText(frame, f"Recording: {remaining}s", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Frames: {frame_count}", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow("Record Gesture", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    cv2.destroyAllWindows()
                    return None
        cv2.destroyAllWindows()
        if len(recorded_features) < min_frames:
            return None
        return np.mean(recorded_features, axis=0).tolist()
    
    def register_user(self, username, use_two_hands=True):
        if username in self.users:
            return False, "Username already exists!"
        gesture_features = self.record_gesture(duration=8, use_two_hands=use_two_hands)
        if gesture_features is None:
            return False, "Gesture recording failed!"
        self.users[username] = {
            "gesture": gesture_features,
            "two_hands": use_two_hands,
            "created_at": datetime.now().isoformat()
        }
        self.save_users()
        return True, "User registered successfully!"
    
    def authenticate_user(self, username, threshold=75):
        if username not in self.users:
            return False, "User not found!"
        use_two_hands = self.users[username].get("two_hands", True)
        gesture_features = self.record_gesture(duration=8, use_two_hands=use_two_hands)
        if gesture_features is None:
            return False, "Gesture authentication failed!"
        stored_gesture = self.users[username]["gesture"]
        similarity = self.calculate_gesture_similarity(gesture_features, stored_gesture)
        if similarity >= threshold:
            return True, f"Authentication successful! (Match: {similarity:.2f}%)"
        else:
            return False, f"Gesture doesn't match! (Match: {similarity:.2f}%)"
    
    def verify_gesture_live(self, username, threshold=75):
        if username not in self.users:
            return False, "User not found!"
        cap = self.init_camera()
        stored_gesture = self.users[username]["gesture"]
        use_two_hands = self.users[username].get("two_hands", True)
        authenticated = False
        similarity_score = 0
        max_hands = 2 if use_two_hands else 1
        with self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        ) as hands:
            stable_frames = 0
            required_stable_frames = 15
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hands.process(rgb)
                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    current_features = None
                    if use_two_hands:
                        if len(result.multi_hand_landmarks) >= 2:
                            current_features = self.extract_two_hands_features(result.multi_hand_landmarks)
                            cv2.putText(frame, "TWO HANDS DETECTED", (10, frame.shape[0] - 60),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        else:
                            cv2.putText(frame, "SHOW BOTH HANDS!", (10, frame.shape[0] - 60),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    else:
                        current_features = self.extract_hand_features(result.multi_hand_landmarks[0])
                        cv2.putText(frame, "ONE HAND DETECTED", (10, frame.shape[0] - 60),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    if current_features is not None:
                        similarity_score = self.calculate_gesture_similarity(current_features.tolist(), stored_gesture)
                        if similarity_score >= threshold:
                            stable_frames += 1
                            color = (0, 255, 0)
                            status = "MATCH!"
                        else:
                            stable_frames = 0
                            color = (0, 0, 255)
                            status = "NO MATCH"
                        cv2.putText(frame, status, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
                        cv2.putText(frame, f"Match: {similarity_score:.1f}%", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                        cv2.putText(frame, f"Stable: {stable_frames}/{required_stable_frames}", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                        if stable_frames >= required_stable_frames:
                            authenticated = True
                            cv2.putText(frame, "AUTHENTICATED!", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                            cv2.imshow("Gesture Authentication", frame)
                            cv2.waitKey(1500)
                            break
                    else:
                        stable_frames = 0
                else:
                    cv2.putText(frame, "Show BOTH hands" if use_two_hands else "No hand detected", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    stable_frames = 0
                cv2.putText(frame, "Press ESC to cancel", (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                cv2.imshow("Gesture Authentication", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        cv2.destroyAllWindows()
        if authenticated:
            return True, f"Authenticated! (Match: {similarity_score:.1f}%)"
        else:
            return False, "Authentication failed!"
    
    def list_users(self):
        return list(self.users.keys())

