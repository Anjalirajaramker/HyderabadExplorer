import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import threading
import http.server
import socketserver
import time

# Global server instance
server = None
server_thread = None
PORT = 8888

@pytest.fixture(scope="session", autouse=True)
def start_server():
    """
    Start a local HTTP server to serve the project files.
    This runs once for the entire test session.
    Uses ThreadingTCPServer for parallel test execution.
    """
    global server, server_thread
    
    # Get project directory
    project_path = os.path.join(os.path.dirname(__file__), "..", "Devops")
    
    # Change to project directory
    os.chdir(project_path)
    
    # Create threaded HTTP server handler
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Use ThreadingTCPServer for handling concurrent requests
    class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True
        daemon_threads = True
    
    try:
        server = ThreadedHTTPServer(("", PORT), Handler)
        print(f"\n🚀 Starting threaded HTTP server on http://localhost:{PORT}")
        
        # Run server in a separate thread
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Give server time to start
        time.sleep(2)
        print(f"✅ Server running at http://localhost:{PORT}")
        
    except OSError as e:
        if e.errno == 10048:  # Port already in use
            print(f"⚠️  Port {PORT} already in use. Using existing server.")
        else:
            raise
    
    yield
    
    # Shutdown server
    if server:
        print(f"\n🛑 Shutting down server...")
        try:
            server.shutdown()
            server.server_close()
        except Exception as e:
            print(f"⚠️  Error shutting down server: {e}")


@pytest.fixture
def browser():
    """
    Setup and teardown for Selenium WebDriver.
    This fixture runs before each test and provides a fresh browser instance.
    """
    # --- Setup ---
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # Allow local file access for CORS
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-file-access-from-files')
    
    # Initialize Chrome driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  # Wait up to 10s for elements to appear
    driver.maximize_window()
    
    # Open via HTTP server
    driver.get(f'http://localhost:{PORT}/index.html')
    
    yield driver  # This is where the test runs
    
    # --- Teardown ---
    driver.quit()  # Close the browser after the test is done


@pytest.fixture
def home_browser():
    """
    Setup for testing the home page.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-file-access-from-files')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get(f'http://localhost:{PORT}/home.html')
    
    yield driver
    
    driver.quit()


@pytest.fixture
def food_browser():
    """
    Setup for testing the food places page.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-file-access-from-files')
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    driver.get(f'http://localhost:{PORT}/food-places.html')
    
    yield driver
    
    driver.quit()
