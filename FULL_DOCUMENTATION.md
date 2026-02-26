# 📔 MAXY: Complete System Documentation

Welcome to the comprehensive technical guide for the **MAXY Chat** repository. This document provides a deep dive into the architecture, core modules, and implementation details that power MAXY.


## 🏗️ 1. High-Level Architecture

MAXY follows a modern **decoupled architecture**:

*   **Frontend**: A high-performance, vanilla JavaScript application focused on premium UX, real-time feedback, and glassmorphic aesthetics.
*   **Backend**: A FastAPI-powered Python engine that handles multi-model routing, heavy file processing, and complex data analysis.
*   **Data Layer**: Integrated with **Supabase** (Auth/Database) and local **SQLite/JSON** for configuration and credit tracking.

### The Intelligence Flow
When a user sends a message, it flows through the following pipeline:
1.  **Intent Detection**: `ModelRouter` analyzes the prompt for keywords (identity, news, code, research).
2.  **Model Selection**: Routing to MAXY 1.1 (Casual), 1.2 (Research), or 1.3 (Technical).
3.  **Synthesis**:
    -   **1.1**: Checks the `SlangManager` and `QuickLookup`.
    -   **1.2**: Triggers `KnowledgeSynthesizer` (Wikipedia + DDG News).
    -   **1.3**: Triggers `FileProcessor` or `DataAnalyzer`.
4.  **Verification**: Responses are cross-referenced for factual consistency before delivery.

---

## 📂 2. Core Modules Breakdown

### 🛠️ Backend Intelligence (`/backend`)

#### [models.py](file:///c:/Users/vinay/Downloads/intern/MAIN%20PROJECT%20CHAT%20BOT/backend/models.py)
The heartbeat of the AI. Contains:
-   **MAXYThinkingEngine**: Manages the multi-step "thinking" process displayed to the user.
-   **KnowledgeSynthesizer**: A scoring engine that ranks search results based on relevance, recency, and factuality.
-   **SlangManager**: An injector that blends localized Bangalore slang into responses.

#### [file_processor.py](file:///c:/Users/vinay/Downloads/intern/MAIN%20PROJECT%20CHAT%20BOT/backend/file_processor.py)
Handles binary and text-based file intelligence:
-   **Images**: Extracts metadata (EXIF), color profiles, and dimensions via PIL.
-   **PDFs**: Multi-page text extraction using PyPDF2.
-   **Structured Data**: Custom CSV/JSON parser that prepares data for analysis.

#### [data_analyzer.py](file:///c:/Users/vinay/Downloads/intern/MAIN%20PROJECT%20CHAT%20BOT/backend/data_analyzer.py)
Advanced statistical suite providing:
-   **Descriptive Stats**: Mean, Median, Variance, Skewness, Kurtosis.
-   **Pattern Detection**: Outlier detection (IQR method) and Trend Analysis (Linear Regression).
-   **Insights Engine**: Converts raw math into human-readable narratives (e.g., "Data shows a strong upward trend").

---

### 🎨 Frontend Experience (`/frontend`)

#### [chat.js](file:///c:/Users/vinay/Downloads/intern/MAIN%20PROJECT%20CHAT%20BOT/frontend/chat.js)
The main controller for the UI:
-   **State Management**: Tracks current chat history, model selection, and credits.
-   **Dynamic UI**: Handles sidebar collapsing, markdown rendering, and auto-scrolling.
-   **API Integration**: Communicates with the Render backend via unified `BACKEND_URL` detection.

#### [common.css](file:///c:/Users/vinay/Downloads/intern/MAIN%20PROJECT%20CHAT%20BOT/frontend/common.css)
Shared UI components including:
-   **Daily Updates Popover**: The hover-based update notification system.
-   **Toast Notifications**: Real-time user feedback for uploads and errors.

---

## 📋 3. API Reference (Partial)

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/chat` | `POST` | The primary endpoint for processing user messages and file analysis. |
| `/health` | `GET` | Returns system uptime, feature status, and metrics. |
| `/api/updates` | `GET` | Fetches the latest news and announcement data (as seen in the UI popover). |
| `/conversations` | `GET/POST` | Management of user chat history (Supabase backed). |
| `/stats` | `GET` | Internal usage and performance statistics. |

---

## ⚙️ 4. Environment & Deployment

### Environment Variables (.env)
-   `ALLOWED_ORIGINS`: Comma-separated list of permitted frontend URLs (Crucial for CORS).
-   `ENABLE_CREDITS`: Boolean flag to turn on the usage limiting system.
-   `DATABASE_URL`: Path to your SQLite file or Supabase connection string.

### Deployment Matrix
-   **Frontend**: Hosted on **Vercel** for lightning-fast asset delivery.
-   **Backend**: Hosted on **Render** (Web Service) to handle computational tasks.
-   **Real-time Logic**: The `news_updater.py` runs on server startup to refresh the `updates.json` file.

---

## 🚨 5. Troubleshooting & Maintenance

*   **CORS Errors**: Always ensure the Vercel URL in `ALLOWED_ORIGINS` does NOT have a trailing slash.
*   **Port Binding**: Render expects the backend to listen on `0.0.0.0:10000` (or the `PORT` env var).
*   **Memory Usage**: MAXY 1.3 can be memory intensive when analyzing large CSVs (>10MB). Adjust `MAX_FILE_SIZE` in `.env` accordingly.
