import sys
import os

def get_current_platform():
    # Detect Microsoft Store (MSIX) execution environment
    if os.environ.get("PACKAGE_FULL_NAME"):
        return "microsoft_store"
    
    # Detect Android environment (Kivy/BeeWare/Pyto)
    if hasattr(sys, 'getandroidapilevel'):
        return "google_play"
        
    return "local_dev"
