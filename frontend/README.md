# Frontend

This directory contains the React-based frontend for MyAgent.

## Prerequisites
Node.js (v16+) and npm or yarn installed.

## Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   # or yarn install
   ```
2. Start development server:
   ```bash
   npm run dev
   # or yarn dev
   ```
   The app will be available at http://localhost:5173 and will proxy `/chat` requests to the backend.

## Build
```bash
npm run build
# or yarn build
```
Creates a production build in the `dist` directory.

## Project Structure
- index.html       Root HTML file
- package.json     npm scripts and dependencies
- vite.config.js   Vite configuration with proxy settings
- src/
  ├─ main.jsx      App entry point
  ├─ App.jsx       Main app component
  ├─ index.css     Global styles
  └─ components/
      ├─ ChatInput.jsx      Message input component
      └─ MessageList.jsx    Chat history display component