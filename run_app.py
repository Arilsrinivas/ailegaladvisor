import os
import sys
import shutil
import subprocess
import time
import webbrowser

def ensure_env_file():
    """Ensure .env exists by copying from .env.example if missing."""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("[Setup] Creating .env from .env.example...")
            shutil.copy(".env.example", ".env")
        else:
            with open(".env", "w") as f:
                f.write("SECRET_KEY=nyaya-ai-super-secret-key-2026\nDATABASE_URL=sqlite:///./data/legaladvisor.db\n")
            print("[Setup] Created default .env file.")

def check_python_dependencies():
    """Checks if critical python dependencies are installed."""
    required = ["fastapi", "uvicorn", "sqlalchemy", "sentence_transformers", "pydantic"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
            
    if missing:
        print(f"[Setup] Missing python dependencies ({', '.join(missing)}). Installing requirements.txt...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("[Setup] Python dependencies installed successfully.")

def ensure_frontend_built_or_installed():
    """Ensures node_modules are installed in frontend."""
    frontend_dir = os.path.abspath("frontend")
    node_modules = os.path.join(frontend_dir, "node_modules")
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"

    if not os.path.exists(node_modules):
        print("\n[Setup] Detected fresh clone: Installing frontend npm dependencies...")
        subprocess.run([npm_cmd, "install"], cwd=frontend_dir, check=True)
        print("[Setup] Frontend npm dependencies installed successfully.")

def ensure_db_and_indices():
    """Ensures the SQLite database and FAISS/BM25 indices are initialized."""
    faiss_file = os.path.join("data", "faiss_index", "index.faiss")
    sqlite_db = os.path.join("data", "legaladvisor.db")

    if not os.path.exists(faiss_file) or not os.path.exists(sqlite_db):
        print("\n[Setup] Seeding authoritative legal database & FAISS indices...")
        subprocess.run([sys.executable, "-m", "src.db.init_db"], check=True)
        print("[Setup] Database & indices seeded successfully.")

def main():
    print("=" * 65)
    print("  ⚖️  AI LEGAL ADVISOR (NYAYA AI) - ZERO-CONFIG LAUNCHER")
    print("=" * 65)

    try:
        ensure_env_file()
        check_python_dependencies()
        ensure_frontend_built_or_installed()
        ensure_db_and_indices()
    except Exception as e:
        print(f"\n[Warning during setup check]: {e}")
        print("Proceeding to launch services...")

    print("\n[1/2] Starting FastAPI Backend Server on http://127.0.0.1:8000 ...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.api.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Wait for backend initialization
    time.sleep(3)

    print("[2/2] Starting Vite Frontend Server on http://localhost:5173 ...")
    frontend_dir = os.path.abspath("frontend")
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    frontend_proc = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    print("\n" + "=" * 65)
    print("  🚀  SYSTEM IS FULLY OPERATIONAL!")
    print("  • Frontend Application: http://localhost:5173")
    print("  • Backend REST API:     http://127.0.0.1:8000")
    print("  • Swagger Documentation: http://127.0.0.1:8000/docs")
    print("  Press Ctrl+C at any time to shut down both servers.")
    print("=" * 65 + "\n")

    try:
        # Give Vite a second to bind port, then open default browser
        time.sleep(2)
        webbrowser.open("http://localhost:5173")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Shutdown] Terminating servers gracefully...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("[Shutdown] Completed.")

if __name__ == "__main__":
    main()
