import os
import sys
import runpy

# Determine the path to the main application in DBMS PROJECT/Campus Placement System
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(current_dir, "DBMS PROJECT", "Campus Placement System")
app_file = os.path.join(app_dir, "app.py")

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Change directory context if needed
os.chdir(app_dir)

# Execute the main Streamlit application
runpy.run_path(app_file, run_name="__main__")
