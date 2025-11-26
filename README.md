# 📦 MEGA PDF Compressor — Free

Compress PDF files **from your MEGA cloud _or_ from local folders** using the iLovePDF API.

## 📦 Features

### 🔀 Two modes in a single UI

- **Local mode – "Этот компьютер"**
  - ✅ Pick **three local folders** via the browser (Chromium‑based, e.g. Chrome/Edge):
    - source folder (original PDFs),
    - folder for compressed PDFs,
    - backup folder for originals
  - ✅ Batch‑compress **all PDFs** from the selected source folder
  - ✅ Automatically saves compressed PDFs into the chosen local folder (prefixed with `[Сжато]`)
  - ✅ Automatically copies originals into the backup folder and removes them from the source folder (if backup succeeds)

- **Cloud mode – MEGA**
  - ✅ Works directly with your MEGA cloud (login happens in the browser)
  - ✅ Lets you choose **three folders** in MEGA:
    - source folder (original PDFs),
    - folder for compressed PDFs,
    - backup folder for originals
  - ✅ Batch‑compresses **all PDFs** from the selected MEGA source folder
  - ✅ Uses the professional iLovePDF API for compression
  - ✅ Shows compression statistics (size before/after, reduction percentage)
  - ✅ Automatically saves compressed PDFs into the chosen folder in MEGA (prefixed with `[Сжато]`)
  - ✅ Automatically moves originals into the backup folder after successful compression (inside MEGA)

## 🛠 Tech stack

- **Frontend**: MEGA SDK v4 (browser build), vanilla JS
- **Backend**: Flask, pylovepdf
- **Runtime**: Docker, Gunicorn
- **Hosting**: Railway (single container with backend + built‑in static frontend)

---

## 👣 How the web UI works

### 1. Mode selection

On start you see a simple choice between two modes:

- **"Этот компьютер"** – work with local folders on your machine;
- **"Облако MEGA"** – work with folders in your MEGA cloud.

You choose the mode and click **Continue** – then the UI shows the relevant steps for that mode.

### 2. Local mode – "Этот компьютер"

> ⚠️ Requires a Chromium‑based browser (Chrome, Edge, etc.) with the File System Access API.

1. In **Step 1** you choose three local folders via the native folder picker:
   - **Source folder** – where your original PDFs live;
   - **Folder for compressed PDFs** – where compressed versions will be saved;
   - **Backup folder for originals** – where originals will be copied before deletion.
2. After all three folders are selected, **Step 2** becomes active and you can start compression.
3. Click **“Сжать PDF”** – for each PDF in the source folder the app will:
   - read the file from the local source folder via the File System Access API;
   - send it to the backend, which compresses the PDF using iLovePDF (`/compress` endpoint);
   - write the compressed file into the chosen local folder for compressed PDFs (with prefix `[Сжато]`);
   - copy the original into the local backup folder;
   - remove the original from the source folder if the backup copy succeeded.
4. At the bottom of the page you’ll see a detailed log per file  
   (status, sizes before/after, compression percentage, warnings if backup/delete failed).

### 3. Cloud mode – MEGA

1. Enter your MEGA email and password in the login form  
   (credentials stay in the browser and are only used by the MEGA SDK).
2. After a successful login, select three folders in MEGA:
   - **Source folder** – where your original PDFs live;
   - **Folder for compressed PDFs** – where compressed versions will be saved;
   - **Backup folder for originals** – where originals will be moved after successful compression.
3. Click **“Compress all PDFs and save to MEGA”** – for each PDF the app will:
   - download the file from the source folder via the MEGA SDK;
   - send it to the backend, which compresses the PDF using iLovePDF;
   - upload the compressed file into the selected folder for compressed PDFs (with prefix `[Сжато]`);
   - after a successful upload, move the original file into the backup folder.
4. At the bottom of the page you’ll see a compact log per file  
   (status, sizes before/after, compression percentage).

### 🔁 Typical usage scenario (MEGA cloud)

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
3. Open the web app, choose **"Облако MEGA"**, log into MEGA and select these three folders in the UI.
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
	│   └── index.html          # Single-page web UI (mode selector: local folders + MEGA)
├── Dockerfile              # Main Docker image (backend + frontend) for Railway
├── railway.toml            # Railway build and service configuration
└── README.md               # This file
```

Done! 🎉