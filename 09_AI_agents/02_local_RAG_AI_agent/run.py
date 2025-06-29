import os
import sys

# Set environment variables before any other imports
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['SSL_VERIFY'] = '0'

# Remove problematic SSL environment variables
env_vars_to_remove = ['SSL_CERT_FILE', 'SSL_CERT_DIR', 'CERT_FILE']
for var in env_vars_to_remove:
    if var in os.environ:
        del os.environ[var]

# Now run the main application
import main
