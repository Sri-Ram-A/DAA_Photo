# run_dev_env.py
import os
import subprocess
import sys
import time

# Get current working directory (root of the project)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

def run_command(command, cwd, new_terminal=False, terminal_title=None):
    if new_terminal:
        if sys.platform.startswith('win'):
            subprocess.Popen(
                f'start cmd /K "title {terminal_title or "Terminal"} && {command}"',
                shell=True, cwd=cwd
            )
        elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            subprocess.Popen([
                'gnome-terminal', '--', 'bash', '-c',
                f'cd "{cwd}" && {command}; exec bash'
            ])
    else:
        subprocess.run(command, cwd=cwd, shell=True)

def main():
    print("🐳 Opening Docker terminal...")
    run_command("docker compose build && docker compose up -d", cwd=BACKEND_DIR, new_terminal=True, terminal_title="Docker Compose")

    time.sleep(2)

    print("🚀 Launching Django server...")
    run_command("python manage.py runserver", cwd=BACKEND_DIR, new_terminal=True, terminal_title="Django Server")

    time.sleep(2)

    print("🌐 Launching frontend (npm run dev)...")
    run_command("npm run dev", cwd=FRONTEND_DIR, new_terminal=True, terminal_title="Frontend")

    print("✅ All services started. Open your browser at http://localhost:3000")

if __name__ == "__main__":
    main()
