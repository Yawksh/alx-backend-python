# Import logging module for file-based logging
import logging # Import datetime for timestamp generation
from datetime import datetime
# Import Django HTTP types for type checking
from django.http import HttpRequest, HttpResponse
# Import typing for type annotations
from typing import Callable
# Configure logging to write to a file
logging.basicConfig(
filename='requests.log', # Log file to store request details
level=logging.INFO, # Log INFO level and above
format='%(message)s' # Custom format for log entries
 )

# Middleware to log user requests
class RequestLoggingMiddleware:
    # Initialize middleware with get_response callable
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) ->None:
        # Store get_response to pass request to next middleware or view
        self.get_response = get_response
        # Initialize logger for request logging
        self.logger = logging.getLogger('request_logger')
        # Alternative: Use RotatingFileHandler for log file size management
    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Get the current timestamp for the log entry
        timestamp = datetime.now()
        # Get the user, default to 'Anonymous' if not authenticated
        user = request.user if request.user.is_authenticated else 'Anonymous'
        # Get the request path (e.g., /api/chats/messages/)
        path = request.path
        # Log the request details in the specified format
        self.logger.info(f"{timestamp} - User: {user} - Path: {path}")
        # Alternative: Sanitize user input to prevent log injection
        # Pass request to next middleware or view and get response
        response = self.get_response(request)
        # Return the response to continue the request-response cycle
        return response