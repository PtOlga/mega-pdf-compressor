# 📦 MEGA PDF Compressor — Free

Compress PDF files stored in your MEGA cloud using the iLovePDF API.

## 🚀 Quick start

⚡ **[QUICK_START.md](QUICK_START.md)** – cheat sheet with the most important commands and flows.

### Option 1: Local development (without Docker)

📖 **[SETUP_LOCAL.md](SETUP_LOCAL.md)** – run the app locally in a few minutes.

### Option 2: Deploy to production (Railway)

📖 **[DEPLOY_RAILWAY.md](DEPLOY_RAILWAY.md)** – step‑by‑step Railway deployment guide.

### Option 3: Work with Docker locally (optional)

📖 **[SETUP_DOCKER.md](SETUP_DOCKER.md)** – for those who prefer local Docker.

---

## 📦 Features

- ✅ Works directly with your MEGA cloud (login happens in the browser)
- ✅ Lets you choose **three folders** in MEGA:
  - source folder (original PDFs),
  - folder for compressed PDFs,
  - backup folder for originals
- ✅ Batch‑compresses **all PDFs** from the selected source folder
- ✅ Uses the professional iLovePDF API for compression
- ✅ Shows compression statistics (size before/after, reduction percentage)
- ✅ Automatically saves compressed PDFs into the chosen folder in MEGA
- ✅ Automatically moves originals into the backup folder after successful compression

## 🛠 Tech stack

- **Frontend**: MEGA SDK v4 (browser build), vanilla JS
- **Backend**: Flask, pylovepdf
- **Runtime**: Docker, Gunicorn
- **Hosting**: Railway (single container with backend + built‑in static frontend)

---

## 👣 How the web UI works

1. Enter your MEGA email and password in the login form  
   (credentials stay in the browser and are only used by the MEGA SDK).
2. After a successful login, select three folders in MEGA:
   - **Source folder** – where your original PDFs live;
   - **Folder for compressed PDFs** – where compressed versions will be saved;
   - **Backup folder for originals** – where originals will be moved after successful compression.
3. Click **“Compress all PDFs and save to MEGA”** – for each PDF the app will:
   - download the file from the source folder via the MEGA SDK;
   - send it to the backend, which compresses the PDF using iLovePDF;
   - upload the compressed file into the selected folder for compressed PDFs;
   - after a successful upload, move the original file into the backup folder.
4. At the bottom of the page you’ll see a compact log per file  
   (status, sizes before/after, compression percentage).

### 🔁 Typical usage scenario

**Example folder structure in MEGA:**

- `/Cloud Drive/pdf/Input` – source folder with original PDFs;
- `/Cloud Drive/pdf/Compressed` – folder for compressed files;
- `/Cloud Drive/pdf/Backup` – folder for backups of originals.

**Steps:**

1. Create three folders in MEGA, for example:
   - `Cloud Drive/pdf/Input`
   - `Cloud Drive/pdf/Compressed`
   - `Cloud Drive/pdf/Backup`
2. Put all the original PDFs you want to process into `Input`.
3. Open the web app, log into MEGA and select these three folders in the UI.
4. Click **“Compress all PDFs and save to MEGA”**.
5. After the process finishes:
   - `Compressed` will contain compressed versions prefixed with `[Сжато]` (Russian for “[Compressed]”);
   - `Backup` will contain the original files;
   - the `Input` folder will be empty (if every file was processed and moved successfully).

## 💰 Free quotas

- **GitHub Pages**: not used anymore (frontend is now served by the backend container)
- **Railway**: about 500 free hours/month in the hobby tier (check current limits)
- **iLovePDF API**: 250 tasks/month on the free plan (see the official docs)

---

## 📁 Project structure

```
mega-pdf-compressor/
├── backend/
│   ├── app.py              # Flask API
│   ├── Dockerfile          # Alternative Dockerfile for backend-only image
│   ├── requirements.txt    # Python dependencies
│   ├── run_local.py        # Local backend runner
│   └── .env.example        # Template for iLovePDF API keys
├── frontend/
│   └── index.html          # Single-page web UI (MEGA login + folder selection)
├── Dockerfile              # Main Docker image (backend + frontend) for Railway
├── railway.toml            # Railway build and service configuration
├── SETUP_LOCAL.md          # Local development instructions
├── SETUP_DOCKER.md         # Docker usage instructions
├── DEPLOY_RAILWAY.md       # Railway deployment instructions
└── README.md               # This file
```

---

## 🤝 Questions?

If something doesn’t work:
1. Check the corresponding `.md` instruction file.
2. Make sure your iLovePDF API keys are configured correctly.
3. Check logs on Railway (if you are deploying there).

Done! 🎉