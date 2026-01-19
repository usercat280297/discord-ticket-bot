# Discord Ticket Bot — Architecture Overview

Short summary of recommended architecture, storage, and security for production deployment.

Components
- Bot (discord.py): WebSocket client handling events, interactions, and message components.
- Web service (optional): FastAPI/aiohttp for interaction endpoints, health checks, and signed URL endpoints.
- Storage: External object storage (S3, DigitalOcean Spaces, Backblaze) for user-uploaded files. Use pre-signed URLs.
- Database: Postgres for tickets, mappings, and logs.
- Cache/Queue: Redis for rate-limiting, locks, and background jobs. Use RQ/Celery/APScheduler for scheduled tasks.

Security
- Keep secrets in environment variables; never commit tokens.
- Verify interactions with Discord `PUBLIC_KEY` when using HTTP interactions.
- Serve file links via pre-signed URLs with short expiry and optional one-time tokens.

Deployment
- Run bot as a background worker (Docker, Render background service, or VPS). Run web endpoints as a web service if needed.
- Use managed Postgres (Supabase, RDS) and S3-compatible storage.

Notes
- This repository includes initial helper modules `bot/storage.py` and `bot/db.py` (minimal). Integrate and migrate existing `utils/database.py` when ready.
