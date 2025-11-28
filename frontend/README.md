# Jam Server Frontend

React with Vite frontend for Jam Server.

- The frontend uses session-based authentication with cookies.
- React Query handles data caching and refetching.

## Setup

Navigate to the frontend directory and install dependencies:
```bash
cd frontend/
npm install
```

## Development

**Run frontend only:**
```bash
npm run dev
```
Dev server starts at `http://localhost:5173`

**Run frontend + backend together:**
```bash
../scripts/dev.sh
```

## API Integration

Vite proxies `/api/*` requests to the Flask backend at `http://127.0.0.1:5000`

## Building
```bash
npm run build
```

Build output: `dist/`

## Scripts

- `npm run dev` - Start dev server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
