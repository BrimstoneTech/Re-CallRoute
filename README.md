# Re-CallRoute

An internal call routing system for organizations, using VoIP (SIP) over a local network/VPN to route calls based on personnel roles and network availability.

## Features
- **Role-Based Routing**: Automatically routes calls to "HR", "Support", or "Manager" based on intent.
- **Network Awareness**: Routes calls only when personnel are on the simplified organization network (simulated).
- **Android App**: Dashboard for status, personnel list, and incoming call redirection.
- **Backend API**: FastAPI server for managing users, roles, and logs.

## Installation

### Android App
To install the app on your phone:
1.  **Fork/Clone** this repository to your GitHub account.
2.  Go to the **Actions** tab in your GitHub repository.
3.  Select the **Android Build** workflow.
4.  Download the **app-debug** artifact from the latest successful run.
5.  Extract the zip file and transfer `app-debug.apk` to your Android device.
6.  Install the APK (ensure "Install from unknown sources" is enabled).

### Backend Setup
1.  Navigate to `backend/`.
2.  Create a virtual environment: `python -m venv .venv`
3.  Activate it: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/Mac)
4.  Install dependencies: `pip install -r requirements.txt`
5.  Run the server: `python -m uvicorn main:app --reload`
6.  Access API docs at `http://localhost:8000/docs`

## Development
-   **Backend**: Python 3.10+, FastAPI, SQLAlchemy
-   **Mobile**: Android (Kotlin), Jetpack Compose / XML Layouts