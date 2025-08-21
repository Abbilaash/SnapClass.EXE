import os
import threading
import socket
import subprocess
import sys
import time
import webbrowser
import customtkinter as ctk
from tkinter import messagebox
import queue

# --- CONFIG ---
FLASK_PORT = 5000

def get_base_dir():
    if getattr(sys, 'frozen', False):
        # Use the directory next to the executable
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# --- FLASK SERVER LAUNCHER ---
class FlaskServerManager:
    def __init__(self):
        self.process = None
        self.output_queue = queue.Queue()
        self.output_thread = None
        self.running = False

    def start(self):
        if self.process is None or self.process.poll() is not None:
            self.add_custom_log("Starting SnapClass server...")
            # Choose command based on frozen/dev mode
            base_dir = get_base_dir()
            if getattr(sys, 'frozen', False):
                cmd = [sys.executable, "--run-server"]
                cwd = os.path.dirname(sys.executable)
            else:
                app_path = os.path.join(base_dir, "app.py")
                cmd = [sys.executable, app_path]
                cwd = base_dir
            self.process = subprocess.Popen(
                cmd,
                env={**os.environ, "SNAPCLASS_LAUNCHED_BY_DESKTOP": "1"},
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
                cwd=cwd
            )
            self.running = True
            self.output_thread = threading.Thread(target=self.read_output, daemon=True)
            self.output_thread.start()
            self.add_custom_log("Server process started successfully...")

    def stop(self):
        if self.process and self.process.poll() is None:
            self.add_custom_log("Stopping SnapClass server...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
                self.add_custom_log("Server stopped gracefully")
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.add_custom_log("Server force stopped")
            self.running = False

    def is_running(self):
        return self.process is not None and self.process.poll() is None

    def read_output(self):
        try:
            for line in self.process.stdout:
                # Filter out unnecessary logs and only show user-relevant information
                if self.should_display_log(line):
                    self.output_queue.put(line)
            self.process.stdout.close()
        except Exception as e:
            self.output_queue.put(f"[Error reading server output]: {e}\n")
    
    def should_display_log(self, line):
        """Filter logs to only show user-relevant information"""
        line_lower = line.lower()
        
        # Skip Flask framework logs
        if any(skip in line_lower for skip in [
            "flask", "werkzeug", " * running on", " * debug mode", " * reloader", 
            " * serving flask app", " * environment", " * debugger pin"
        ]):
            return False
        
        # Skip model initialization logs
        if any(skip in line_lower for skip in [
            "model", "initializing", "loading", "tensor", "gpu", "cuda", "onnx",
            "llama", "genie", "dll", "library", "backend", "quantization"
        ]):
            return False
        
        # Skip verbose system logs
        if any(skip in line_lower for skip in [
            "info:", "debug:", "warning:", "error:", "critical:", "traceback:",
            "file", "line", "module", "import", "package", "dependency"
        ]):
            return False
        
        # Show important user-relevant logs
        if any(show in line_lower for show in [
            "snapclass", "server", "started", "stopped", "running", "listening",
            "request", "upload", "test", "student", "connected", "disconnected",
            "question", "answer", "result", "score", "time", "completed"
        ]):
            return True
        
        # Show custom formatted logs (lines that start with [ or contain user actions)
        if line.strip().startswith('[') or 'user' in line_lower or 'action' in line_lower:
            return True
        
        return False

    def get_output(self):
        lines = []
        while not self.output_queue.empty():
            lines.append(self.output_queue.get())
        return lines
    
    def add_custom_log(self, message):
        """Add a custom formatted log message to the output queue"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.output_queue.put(formatted_message)

flask_server = FlaskServerManager()

# --- NETWORK UTILS ---
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def open_mobile_hotspot_settings():
    if sys.platform.startswith("win"):
        os.system("start ms-settings:network-mobilehotspot")

def is_hotspot_on():
    ip = get_local_ip()
    return ip.startswith(("192.168.", "172.", "10."))

# --- SIDEBAR ICONS (emoji fallback) ---
ICONS = {
    "Dashboard": "🏠",
    "Server": "🖥️",
    "Hotspot": "📶",
    "Instructions": "📋",
    "About": "ℹ️"
}

# --- MAIN APP ---
class SnapClassDesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SnapClass Desktop")
        self.geometry("1200x750")
        self.minsize(1000, 600)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.selected_section = "Dashboard"
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.font_family = "Segoe UI"
        self.create_widgets()
        self.after(1000, self.update_status)
        self.after(500, self.update_terminal_output)

    def create_widgets(self):
        # Main layout: sidebar + content
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=15, fg_color="#f8fafc", border_width=1, border_color="#e2e8f0")
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=(20, 0), pady=20)
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(6, weight=1)

        # Logo & App Name
        self.logo_label = ctk.CTkLabel(self.sidebar, text="📚", font=("Segoe UI", 42), text_color="#1e40af")
        self.logo_label.grid(row=0, column=0, pady=(25, 5), padx=0)
        self.appname_label = ctk.CTkLabel(self.sidebar, text="SnapClass", font=("Segoe UI", 26, "bold"), text_color="#1e40af")
        self.appname_label.grid(row=1, column=0, pady=(0, 35))

        # Navigation Buttons
        self.nav_buttons = {}
        nav_sections = ["Dashboard", "Server", "Hotspot", "Instructions", "About"]
        for idx, section in enumerate(nav_sections):
            btn = ctk.CTkButton(
                self.sidebar, text=f"{ICONS.get(section, '')}  {section}",
                font=(self.font_family, 16), corner_radius=12, height=45,
                fg_color=("#1e40af" if section=="Dashboard" else "#ffffff"),
                text_color=("white" if section=="Dashboard" else "#374151"),
                hover_color="#3b82f6",
                border_width=1,
                border_color="#e5e7eb",
                command=lambda s=section: self.switch_section(s)
            )
            btn.grid(row=2+idx, column=0, sticky="ew", padx=20, pady=8)
            self.nav_buttons[section] = btn

        # --- Main Content ---
        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#ffffff", border_width=1, border_color="#e5e7eb")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(15, 20), pady=20)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.section_frames = {}
        self.create_section_frames()
        self.show_section("Dashboard")

    def create_card(self, parent, title, content_widgets, width=750, height=None):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color="#ffffff", border_width=1, border_color="#e5e7eb")
        card.grid_columnconfigure(0, weight=1)
        card_title = ctk.CTkLabel(card, text=title, font=(self.font_family, 20, "bold"), text_color="#1f2937")
        card_title.grid(row=0, column=0, sticky="w", padx=25, pady=(20, 15))
        for i, w in enumerate(content_widgets):
            w.grid(row=1+i, column=0, sticky="ew", padx=25, pady=(10 if i==0 else 8, 0))
        if width:
            card.configure(width=width) 
        if height:
            card.configure(height=height)
        return card

    def create_section_frames(self):
        # Dashboard
        dash = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#ffffff")
        dash.grid(row=0, column=0, sticky="nsew")
        dash.grid_rowconfigure(4, weight=1)
        dash.grid_columnconfigure(0, weight=1)
        
        # Welcome title
        dash_title = ctk.CTkLabel(dash, text="Welcome to SnapClass!", font=("Segoe UI", 28, "bold"), text_color="#1f2937")
        dash_title.grid(row=0, column=0, pady=(35, 20))
        
        # Status indicators
        self.dash_status_label = ctk.CTkLabel(dash, text="", font=("Segoe UI", 16), text_color="#374151")
        self.dash_status_label.grid(row=1, column=0, pady=(0, 25))
        
        # Terminal output section
        terminal_label = ctk.CTkLabel(dash, text="Server Output", font=("Segoe UI", 16, "bold"), text_color="#1f2937")
        terminal_label.grid(row=2, column=0, pady=(0, 15))
        
        # Terminal Output Card
        self.terminal_box = ctk.CTkTextbox(
            dash, width=750, height=300, font=("Consolas", 13), corner_radius=12,
            fg_color="#f8fafc", text_color="#1f2937", border_width=2, border_color="#d1d5db"
        )
        self.terminal_box.grid(row=3, column=0, pady=(0, 25), padx=50, sticky="nsew")
        self.terminal_box.insert("1.0", "[SnapClass Server Logs]\n[Ready to start server...]\n\n")
        self.terminal_box.configure(state="disabled")
        self.section_frames["Dashboard"] = dash

        # Server
        server = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#ffffff")
        server.grid(row=0, column=0, sticky="nsew")
        server.grid_rowconfigure(6, weight=1)
        server.grid_columnconfigure(0, weight=1)
        
        server_title = ctk.CTkLabel(server, text="Server Control", font=("Segoe UI", 24, "bold"), text_color="#1f2937")
        server_title.grid(row=0, column=0, pady=(35, 25))
        
        # Server control buttons
        self.server_btn = ctk.CTkButton(
            server, text="Start SnapClass Server", font=("Segoe UI", 16), 
            command=self.toggle_server, height=45, corner_radius=12,
            fg_color="#10b981", text_color="white", hover_color="#059669"
        )
        self.server_btn.grid(row=1, column=0, pady=15)

        
        self.stop_server_btn = ctk.CTkButton(
            server, text="Stop Server", font=("Segoe UI", 16), 
            command=self.stop_server, height=45, corner_radius=12,
            fg_color="#ef4444", text_color="white", hover_color="#dc2626"
        )
        self.stop_server_btn.grid(row=2, column=0, pady=15)
        
        # Server info labels
        self.server_ip_label = ctk.CTkLabel(server, text="Server IP: ...", font=("Segoe UI", 16), text_color="#374151")
        self.server_ip_label.grid(row=3, column=0, pady=12)
        
        self.test_link_label = ctk.CTkLabel(
            server, text="Test Link: ...", font=("Segoe UI", 16, "underline"), 
            cursor="hand2", text_color="#2563eb"
        )
        self.test_link_label.grid(row=4, column=0, pady=12)
        self.test_link_label.bind("<Button-1>", lambda e: self.copy_test_link())
        
        open_browser_btn = ctk.CTkButton(
            server, text="Open in Browser", font=("Segoe UI", 15), 
            command=self.open_in_browser, height=40, corner_radius=12,
            fg_color="#3b82f6", text_color="white", hover_color="#2563eb"
        )
        open_browser_btn.grid(row=5, column=0, pady=15)
        self.section_frames["Server"] = server

        # Hotspot
        hotspot = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#ffffff")
        hotspot.grid(row=0, column=0, sticky="nsew")
        hotspot.grid_rowconfigure(4, weight=1)
        hotspot.grid_columnconfigure(0, weight=1)
        
        hotspot_title = ctk.CTkLabel(hotspot, text="Hotspot Setup", font=("Segoe UI", 24, "bold"), text_color="#1f2937")
        hotspot_title.grid(row=0, column=0, pady=(35, 25))
        
        hotspot_instr = ctk.CTkLabel(
            hotspot, 
            text="1. Open Windows Mobile Hotspot settings.\n2. Enable hotspot.\n3. Share IP with students.", 
            font=("Segoe UI", 15), text_color="#374151", justify="left"
        )
        hotspot_instr.grid(row=1, column=0, pady=15)
        
        open_hotspot_btn = ctk.CTkButton(
            hotspot, text="Open Hotspot Settings", font=("Segoe UI", 15), 
            command=self.open_hotspot_and_update, height=40, corner_radius=12,
            fg_color="#8b5cf6", text_color="white", hover_color="#7c3aed"
        )
        open_hotspot_btn.grid(row=2, column=0, pady=20)
        
        self.hotspot_status_label = ctk.CTkLabel(hotspot, text="Hotspot: Unknown", font=("Segoe UI", 15), text_color="#374151")
        self.hotspot_status_label.grid(row=3, column=0, pady=15)
        self.section_frames["Hotspot"] = hotspot

        # Instructions
        instructions = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#ffffff")
        instructions.grid(row=0, column=0, sticky="nsew")
        instructions.grid_rowconfigure(2, weight=1)
        instructions.grid_columnconfigure(0, weight=1)
        
        instr_title = ctk.CTkLabel(instructions, text="How to Use SnapClass", font=(self.font_family, 24, "bold"), text_color="#1f2937")
        instr_title.grid(row=0, column=0, pady=(35, 25))
        
        self.instructions_text = ctk.CTkLabel(
            instructions,
            text=(
                "SnapClass is designed to be simple and intuitive. Follow these steps to get started:\n\n"
                "1. Go to the Hotspot tab and enable Windows Mobile Hotspot.\n"
                "   This creates a local WiFi network for your students to connect to.\n\n"
                "2. Switch to the Server tab and click 'Start SnapClass Server'.\n"
                "   This launches the local server that will host your tests and manage student connections.\n\n"
                "3. Once the server is running, go to the Dashboard and copy the Test Link.\n"
                "   The link will show your local IP address and port number.\n\n"
                "4. Share the Test Link with your students.\n"
                "   They must connect to your hotspot to access the test.\n\n"
                "5. Students open the link on their devices to join the test/class.\n"
                "   They can use any device with a web browser.\n\n"
                "6. Monitor and manage the class from the Dashboard and Server tabs.\n"
                "   Track participation, view results, and manage the session in real-time.\n\n"
                "Tips:\n"
                "• The app shows live status of both server and hotspot.\n"
                "• You can open the admin page in your browser from the Server tab.\n"
                "• For additional help, see the About section.\n"
                "• Ensure your firewall allows the server to run on the specified port.\n\n"
                "That's it! SnapClass handles the technical complexity so you can focus on teaching."
            ),
            font=(self.font_family, 15),
            justify="left",
            wraplength=700,
            text_color="#374151"
        )
        self.instructions_text.grid(row=1, column=0, pady=15, padx=35)
        self.section_frames["Instructions"] = instructions

        # About
        about = ctk.CTkFrame(self.content_frame, corner_radius=15, fg_color="#ffffff")
        about.grid(row=0, column=0, sticky="nsew")
        about.grid_rowconfigure(2, weight=1)
        about.grid_columnconfigure(0, weight=1)
        
        about_title = ctk.CTkLabel(about, text="About SnapClass", font=(self.font_family, 24, "bold"), text_color="#1f2937")
        about_title.grid(row=0, column=0, pady=(35, 25))
        
        self.about_text = ctk.CTkLabel(
            about,
            text=(
                "SnapClass is a modern classroom management tool designed to simplify and enhance the way teachers conduct tests and manage their classes.\n\n"
                "With SnapClass, you can easily set up a local server, share a test link with students over a secure WiFi hotspot, and monitor participation in real time.\n\n"
                "\u2022 Purpose:\n"
                "  - Seamlessly conduct digital tests in classrooms without internet dependency.\n"
                "  - Ensure privacy and security by keeping all data local to your device.\n"
                "  - Provide a smooth, guided experience for both teachers and students.\n\n"
                "\u2022 How it helps:\n"
                "  - One-click server and hotspot setup.\n"
                "  - Real-time monitoring and feedback.\n"
                "  - Simple, intuitive interface for all users.\n\n"
                "\u2022 Creators:\n"
                "  - A T Abbilaash (Contact: abbilaashat@gmail.com)\n"
                "  - N Nivashini\n\n"
                "SnapClass is built with love for educators everywhere."
            ),
            font=(self.font_family, 15),
            justify="left",
            wraplength=700,
            text_color="#374151"
        )
        self.about_text.grid(row=1, column=0, pady=15, padx=35)
        self.section_frames["About"] = about

    def show_section(self, section):
        for sec, frame in self.section_frames.items():
            frame.grid_remove()
        self.section_frames[section].grid()
        for sec, btn in self.nav_buttons.items():
            if sec == section:
                btn.configure(fg_color="#1e40af", text_color="white")
            else:
                btn.configure(fg_color="#ffffff", text_color="#374151")
        self.selected_section = section

    def switch_section(self, section):
        self.show_section(section)

    def update_status(self):
        # Update dashboard, server, and hotspot status
        try:
            ip = get_local_ip()
            server_running = flask_server.is_running()
            hotspot_on = is_hotspot_on()
            
            # Always show test link
            url = f"http://{ip}:{FLASK_PORT}/"
            self.test_link_label.configure(text=f"Test Link: {url}")
            self.test_link_label.grid()
            
            if server_running:
                self.test_link_label.configure(cursor="hand2", text_color="#2563eb")
            else:
                self.test_link_label.configure(cursor="arrow", text_color="#9ca3af")
            
            # Server section
            self.server_ip_label.configure(text=f"Server IP: http://{ip}:{FLASK_PORT}")
            
            # Hotspot section
            self.hotspot_status_label.configure(text=f"Hotspot: {'ON' if hotspot_on else 'OFF'}")
            
            # Server button states
            if server_running:
                self.server_btn.configure(text="Server Running", state="disabled")
                self.stop_server_btn.configure(state="normal")
            else:
                self.server_btn.configure(text="Start SnapClass Server", state="normal")
                self.stop_server_btn.configure(state="disabled")
        except Exception as e:
            pass
        self.after(2000, self.update_status)

    def update_terminal_output(self):
        lines = flask_server.get_output()
        if lines:
            # Always enable before insert
            self.terminal_box.configure(state="normal")
            for line in lines:
                self.terminal_box.insert("end", line)
                self.terminal_box.see("end")
            self.terminal_box.configure(state="disabled")
        self.after(500, self.update_terminal_output)

    def open_hotspot_and_update(self):
        try:
            open_mobile_hotspot_settings()
        except Exception as e:
            messagebox.showerror("Hotspot Error", f"Error opening hotspot settings:\n{e}")

    def toggle_server(self):
        try:
            if not flask_server.is_running():
                # Disable the start button immediately
                self.server_btn.configure(state="disabled")
                flask_server.start()
        except Exception as e:
            messagebox.showerror("Server Error", f"Error starting server:\n{e}")

    def stop_server(self):
        try:
            if flask_server.is_running():
                flask_server.stop()
                # Force update the button states immediately
                self.server_btn.configure(text="Start SnapClass Server", state="normal")
                self.stop_server_btn.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Server Error", f"Error stopping server:\n{e}")

    def open_in_browser(self):
        try:
            ip = get_local_ip()
            url = f"http://{ip}:{FLASK_PORT}/admin"
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Browser Error", f"Error opening browser:\n{e}")

    def copy_test_link(self):
        try:
            if not flask_server.is_running():
                self.show_custom_messagebox("Server Not Running", "Start the server to copy the test link.", error=True)
                return
            ip = get_local_ip()
            url = f"http://{ip}:{FLASK_PORT}/"
            self.clipboard_clear()
            self.clipboard_append(url)
            self.show_custom_messagebox("Link Copied", f"Test link copied to clipboard:\n{url}")
        except Exception as e:
            self.show_custom_messagebox("Copy Error", f"Error copying link:\n{e}", error=True)

    def show_custom_messagebox(self, title, message, error=False):
        # Custom CTkToplevel popup styled for light theme
        popup = ctk.CTkToplevel(self)
        popup.title(title)
        popup.geometry("450x200")
        popup.resizable(False, False)
        popup.configure(fg_color="#ffffff")
        
        frame = ctk.CTkFrame(popup, fg_color="#ffffff", border_width=3, border_color="#ef4444" if error else "#10b981", corner_radius=15)
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        label = ctk.CTkLabel(frame, text=title, font=(self.font_family, 18, "bold"), text_color="#ef4444" if error else "#10b981")
        label.pack(pady=(15, 5))
        
        msg = ctk.CTkLabel(frame, text=message, font=("Segoe UI", 13), text_color="#374151", wraplength=380, justify="left")
        msg.pack(pady=(0, 20))
        
        ok_btn = ctk.CTkButton(
            frame, text="OK", command=popup.destroy, 
            fg_color="#ef4444" if error else "#10b981", text_color="#ffffff", 
            hover_color="#dc2626" if error else "#059669", corner_radius=10, height=35
        )
        ok_btn.pack(pady=(0, 15))
        
        popup.transient(self)
        popup.grab_set()

    def on_close(self):
        try:
            flask_server.stop()
        except:
            pass
        self.destroy()

if __name__ == "__main__":
    # If launched with --run-server, start Flask server inline (frozen mode helper)
    if len(sys.argv) > 1 and sys.argv[1] == "--run-server":
        try:
            from app import run_server
            run_server()
        except Exception as e:
            print(f"[SnapClass] Failed to start server: {e}", flush=True)
            sys.exit(1)
    else:
        try:
            ctk.set_appearance_mode("light")
            app = SnapClassDesktopApp()
            app.mainloop() 
        except Exception as e:
            messagebox.showerror("App Error", f"Fatal error:\n{e}") 