# 🧬 ScanFlow: The Modular AI Fitness Platform

![Build Status](https://img.shields.io/badge/Build-Passing-success?style=for-the-badge&logo=firebase)
![Stack](https://img.shields.io/badge/Stack-Flutter%20%7C%20Firebase%20%7C%20VertexAI-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

> **Where 3D Body Scanning meets Generative AI Training.**

ScanFlow is a next-generation fitness ecosystem that ingests **3D Body Scans** (Digital Twins) to generate **hyper-personalized** training and nutrition plans using **Google Vertex AI**. Built with a **modular architecture** to support future integrations (Strava, Apple Health, etc.).

---

## ⚡️ Key Features

*   **🧘‍♂️ Digital Twin Engine**: Ingests .obj scans and extracts biometric data (BMR, Body Fat %, Segmental Lean Mass).
*   **🧠 Gemini AI Brain**: Generates weekly workout cycles based on *actual* body composition, not just weight.
*   **🧩 Modular Architecture**: Features (Nutrition, Trainer) are independent plugins. Enable/Disable what you need.
*   **🔄 Adaptive Feedback Loops**: The AI "learns" from your pain reports and cheat meals, adjusting plans in real-time.

---

## 🛠 Tech Stack

*   **Frontend**: Flutter (Mobile - iOS/Android) *[Deferred]*
*   **Backend**: Firebase (Cloud Functions v2, Firestore, Auth)
*   **AI**: Google Vertex AI (Gemini Pro)
*   **Testing**: Local Emulator Suite (No Cloud Bill!)

---

## 🚀 Getting Started

### Prerequisites
*   Node.js (v18+)
*   Java (JDK 11+ for Emulators)
*   Firebase CLI (`npm install -g firebase-tools`)

### 1. Clone & Setup
```bash
git clone https://github.com/tayyipcanbay/scanflow.git
cd scanflow

# Install Backend Dependencies
cd functions && npm install
cd ../scripts && npm install
```

### 2. Run the Live Environment (Emulators)
We use the **Firebase Emulator Suite** to run the entire backend locally. No GCP account required.

```bash
# In Project Root
npx firebase emulators:start --project=demo-scanflow
```
*Wait until you see "All emulators ready".*

### 3. Verify the System
Want to see the AI in action? Run our **Headless Client Script**. It simulates a full user journey (Sign Up -> Upload Scan -> Generate Plan -> Report Injury).

```bash
# In a new terminal window
cd scripts
npm test
```

---

## 📂 Project Structure

```bash
scanflow/
├── docs/                # 📚 Architecture & API Specifications
├── functions/           # 🧠 Cloud Functions (The Backend Brain)
├── scripts/             # 🧪 Test Scripts & Headless Clients
├── assets/              # 📦 Mock Data & 3D Scan Files
├── backend/             # 🐍 FastAPI Backend (3D Body Progress Engine)
├── frontend/            # ⚛️ React Frontend (3D Visualization)
└── firestore.rules      # 🛡 Security Protocols
```

---

## 🎯 3D Body Progress Engine (FastAPI Backend)

This repository also includes a **FastAPI-based 3D Body Progress Engine** that provides:

- **3D Mesh Processing**: Upload and compare GLB, OBJ, FBX files
- **Color-Coded Visualization**: Green for decrease (fat loss), Red for increase (muscle gain)
- **Streamlit Interface**: Interactive web app for mesh comparison
- **AI Insights**: Automated analysis of body changes over time
- **Body Region Detection**: Waist, chest, arms, thighs analysis

### Quick Start (FastAPI Backend)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Streamlit App

```bash
cd backend
streamlit run streamlit_app.py
```

See `QUICK_START.md` and `STREAMLIT_GUIDE.md` for detailed instructions.

---

## 🤝 Contributing
1.  Fork it.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

*Built with ❤️ by the ScanFlow Team*
