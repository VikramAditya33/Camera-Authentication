import tkinter as tk
from tkinter import ttk, messagebox
import threading
from gesture_auth import GestureAuthenticator
from PIL import Image, ImageTk
import cv2

class GestureLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Authentication System")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2e")
        
        self.auth = GestureAuthenticator()
        self.current_user = None
        
        self.setup_styles()
        
        self.show_login_screen()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TButton', background='#89b4fa', foreground='white',
                       borderwidth=0, focuscolor='none', padding=10, font=('Segoe UI', 11, 'bold'))
        style.map('Custom.TButton', background=[('active', '#74c0fc')])
        style.configure('Custom.TEntry', fieldbackground='#313244', foreground='white',
                       borderwidth=2, padding=10)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(main_frame, 
                        text="Gesture Authentication",
                        font=("Segoe UI", 28, "bold"),
                        bg="#1e1e2e",
                        fg="#cdd6f4")
        title.pack(pady=20)
        
        form_frame = tk.Frame(main_frame, bg="#313244", bd=2, relief="solid")
        form_frame.pack(pady=30, padx=40, fill="both")
        
        username_label = tk.Label(form_frame,
                                 text="Username",
                                 font=("Segoe UI", 11),
                                 bg="#313244",
                                 fg="#cdd6f4")
        username_label.pack(pady=(20, 5), padx=20, anchor="w")
        
        self.username_entry = tk.Entry(form_frame,
                                      font=("Segoe UI", 12),
                                      bg="#45475a",
                                      fg="white",
                                      insertbackground="white",
                                      bd=0,
                                      relief="flat")
        self.username_entry.pack(pady=5, padx=20, fill="x", ipady=10)
        
        camera_btn = tk.Button(form_frame,
                              text="Login Through Camera",
                              font=("Segoe UI", 13, "bold"),
                              bg="#89b4fa",
                              fg="white",
                              activebackground="#74c0fc",
                              activeforeground="white",
                              bd=0,
                              cursor="hand2",
                              command=self.login_with_gesture)
        camera_btn.pack(pady=30, padx=20, fill="x", ipady=15)
        
        register_frame = tk.Frame(main_frame, bg="#1e1e2e")
        register_frame.pack(pady=10)
        
        register_label = tk.Label(register_frame,
                                 text="Don't have an account?",
                                 font=("Segoe UI", 10),
                                 bg="#1e1e2e",
                                 fg="#a6adc8")
        register_label.pack(side="left", padx=5)
        
        register_btn = tk.Button(register_frame,
                                text="Register",
                                font=("Segoe UI", 10, "bold"),
                                bg="#1e1e2e",
                                fg="#89b4fa",
                                activebackground="#1e1e2e",
                                activeforeground="#74c0fc",
                                bd=0,
                                cursor="hand2",
                                command=self.show_register_screen)
        register_btn.pack(side="left")
        
        self.status_label = tk.Label(main_frame,
                                    text="",
                                    font=("Segoe UI", 10),
                                    bg="#1e1e2e",
                                    fg="#f38ba8")
        self.status_label.pack(pady=10)
    
    def login_with_gesture(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter your username!")
            return
        self.status_label.config(text="Initializing camera... Please wait", fg="#f9e2af")
        self.root.update()
        def authenticate():
            try:
                self.auth.init_camera()
                self.root.after(0, lambda: self.status_label.config(
                    text="Camera ready! Show your gesture...", fg="#a6e3a1"))
                success, message = self.auth.verify_gesture_live(username)
                def update_gui():
                    if success:
                        self.status_label.config(text=message, fg="#a6e3a1")
                        messagebox.showinfo("Success", f"Welcome back, {username}!\n{message}")
                        self.show_dashboard(username)
                    else:
                        self.status_label.config(text=message, fg="#f38ba8")
                        messagebox.showerror("Failed", message)
                self.root.after(0, update_gui)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Authentication error: {str(e)}"))
        thread = threading.Thread(target=authenticate, daemon=True)
        thread.start()
    
    def show_register_screen(self):
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        title = tk.Label(main_frame,
                        text="Register New User",
                        font=("Segoe UI", 28, "bold"),
                        bg="#1e1e2e",
                        fg="#cdd6f4")
        title.pack(pady=20)
        
        form_frame = tk.Frame(main_frame, bg="#313244", bd=2, relief="solid")
        form_frame.pack(pady=30, padx=40, fill="both")
        
        username_label = tk.Label(form_frame,
                                 text="Username",
                                 font=("Segoe UI", 11),
                                 bg="#313244",
                                 fg="#cdd6f4")
        username_label.pack(pady=(20, 5), padx=20, anchor="w")
        
        username_entry = tk.Entry(form_frame,
                                 font=("Segoe UI", 12),
                                 bg="#45475a",
                                 fg="white",
                                 insertbackground="white",
                                 bd=0,
                                 relief="flat")
        username_entry.pack(pady=5, padx=20, fill="x", ipady=10)
        
        gesture_type_label = tk.Label(form_frame,
                                     text="Select Gesture Type",
                                     font=("Segoe UI", 11),
                                     bg="#313244",
                                     fg="#cdd6f4")
        gesture_type_label.pack(pady=(15, 5), padx=20, anchor="w")
        
        gesture_var = tk.StringVar(value="two")
        
        radio_frame = tk.Frame(form_frame, bg="#313244")
        radio_frame.pack(pady=5, padx=20, fill="x")
        
        one_hand_radio = tk.Radiobutton(radio_frame,
                                       text="One Hand",
                                       variable=gesture_var,
                                       value="one",
                                       font=("Segoe UI", 10),
                                       bg="#313244",
                                       fg="#cdd6f4",
                                       selectcolor="#45475a",
                                       activebackground="#313244",
                                       activeforeground="#cdd6f4")
        one_hand_radio.pack(anchor="w", pady=5)
        
        two_hand_radio = tk.Radiobutton(radio_frame,
                                       text="Two Hands",
                                       variable=gesture_var,
                                       value="two",
                                       font=("Segoe UI", 10),
                                       bg="#313244",
                                       fg="#cdd6f4",
                                       selectcolor="#45475a",
                                       activebackground="#313244",
                                       activeforeground="#cdd6f4")
        two_hand_radio.pack(anchor="w", pady=5)
        
        def register_user():
            username = username_entry.get().strip()
            use_two_hands = gesture_var.get() == "two"
            
            if not username:
                messagebox.showerror("Error", "Please enter a username!")
                return
            
            if use_two_hands:
                gesture_info = (
                    "Click OK and perform your unique TWO-HAND gesture.\n"
                    "This gesture will be used for authentication.\n\n"
                    "Recording Duration: 8 seconds\n"
                    "Enhanced Security: Using BOTH hands!\n\n"
                    "Tips:\n"
                    "- BOTH hands must be visible at all times\n"
                    "- Choose a unique two-hand gesture\n"
                    "- Example: Peace sign on both hands\n"
                    "- Keep both hands steady during recording\n"
                    "- Make sure camera can see both hands clearly\n\n"
                    "Camera will initialize now - please wait..."
                )
                title = "Record Gesture - TWO HANDS"
            else:
                gesture_info = (
                    "Click OK and perform your unique ONE-HAND gesture.\n"
                    "This gesture will be used for authentication.\n\n"
                    "Recording Duration: 8 seconds\n"
                    "One Hand Mode\n\n"
                    "Tips:\n"
                    "- Keep one hand visible at all times\n"
                    "- Choose a unique gesture (peace sign, thumbs up, etc.)\n"
                    "- Example: Peace sign or Thumbs up\n"
                    "- Keep your hand steady during recording\n"
                    "- Make sure camera can see your hand clearly\n\n"
                    "Camera will initialize now - please wait..."
                )
                title = "Record Gesture - ONE HAND"
            
            messagebox.showinfo(title, gesture_info)
            
            def register_thread():
                try:
                    self.auth.init_camera()
                    
                    success, message = self.auth.register_user(username, use_two_hands=use_two_hands)
                    
                    def update_gui():
                        if success:
                            messagebox.showinfo("Success", f"{message}\nYou can now login!")
                            self.show_login_screen()
                        else:
                            messagebox.showerror("Failed", message)
                    
                    self.root.after(0, update_gui)
                    
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Registration error: {str(e)}"))
            
            thread = threading.Thread(target=register_thread, daemon=True)
            thread.start()
        
        register_btn = tk.Button(form_frame,
                                text="Register with Gesture",
                                font=("Segoe UI", 13, "bold"),
                                bg="#a6e3a1",
                                fg="#1e1e2e",
                                activebackground="#94e2d5",
                                activeforeground="#1e1e2e",
                                bd=0,
                                cursor="hand2",
                                command=register_user)
        register_btn.pack(pady=20, padx=20, fill="x", ipady=12)
        
        back_btn = tk.Button(main_frame,
                            text="← Back to Login",
                            font=("Segoe UI", 10),
                            bg="#1e1e2e",
                            fg="#89b4fa",
                            activebackground="#1e1e2e",
                            activeforeground="#74c0fc",
                            bd=0,
                            cursor="hand2",
                            command=self.show_login_screen)
        back_btn.pack(pady=10)
    
    def show_dashboard(self, username):
        self.clear_screen()
        
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        success_label = tk.Label(main_frame,
                                text="✓",
                                font=("Segoe UI", 80, "bold"),
                                bg="#1e1e2e",
                                fg="#a6e3a1")
        success_label.pack(pady=20)
        
        welcome_label = tk.Label(main_frame,
                                text=f"Welcome, {username}!",
                                font=("Segoe UI", 32, "bold"),
                                bg="#1e1e2e",
                                fg="#a6e3a1")
        welcome_label.pack(pady=10)
        
        status_label = tk.Label(main_frame,
                               text="Authentication Successful",
                               font=("Segoe UI", 16),
                               bg="#1e1e2e",
                               fg="#cdd6f4")
        status_label.pack(pady=10)
        
        info_frame = tk.Frame(main_frame, bg="#313244", bd=2, relief="solid")
        info_frame.pack(pady=30, padx=40, fill="both")
        
        gesture_type = "Two-Hand" if self.auth.users.get(username, {}).get("two_hands", True) else "One-Hand"
        
        logout_btn = tk.Button(main_frame,
                              text="Logout",
                              font=("Segoe UI", 12, "bold"),
                              bg="#f38ba8",
                              fg="white",
                              activebackground="#eba0ac",
                              activeforeground="white",
                              bd=0,
                              cursor="hand2",
                              command=self.show_login_screen)
        logout_btn.pack(pady=20, ipadx=30, ipady=10)

def main():
    root = tk.Tk()
    app = GestureLoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

