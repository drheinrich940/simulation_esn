#!/usr/bin/env python3


"""
Health check script for Docker container
"""

import sys
import requests
from urllib.parse import urljoin
import time

def check_streamlit_health(base_url="http://localhost:8501", max_retries=5, retry_delay=2):
    """
    Checks if the Streamlit application is running and responding to requests.

    Args:
        base_url (str): Base URL of the Streamlit application
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay between retry attempts in seconds

    Returns:
        bool: True if the application is healthy, False otherwise
    """
    health_endpoint = urljoin(base_url, "/_stcore/health")

    for attempt in range(max_retries):
        try:
            response = requests.get(health_endpoint, timeout=5)
            if response.status_code == 200:
                print(f"✅ L'application Streamlit est en bonne santé (tentative {attempt + 1}/{max_retries})")
                return True
            else:
                print(f"❌ L'application Streamlit a répondu avec le code {response.status_code} (tentative {attempt + 1}/{max_retries})")
        except requests.RequestException as e:
            print(f"❌ Erreur lors de la connexion à l'application Streamlit: {e} (tentative {attempt + 1}/{max_retries})")

        if attempt < max_retries - 1:
            print(f"⏳ Nouvelle tentative dans {retry_delay} secondes...")
            time.sleep(retry_delay)

    return False

if __name__ == "__main__":

    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8501"

    if check_streamlit_health(base_url):
        sys.exit(0)
    else:
        sys.exit(1)
