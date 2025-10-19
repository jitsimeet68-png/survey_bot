# Survey Bot

BotX (eXpress) chatbot application built with Flask for handling webhook commands from the BotX platform.

## Architecture

The application uses Docker Compose to orchestrate multiple services:

- **backend** - Flask application (Python 3.11)
  - BotX webhook handler at `/api/v1/command`
  - Health check endpoint at `/healthz`
  - Runs on port 5000 (internal)

- **db** - PostgreSQL 16 database
  - Stores application data
  - Managed via NocoDB interface

- **admin** - NocoDB instance
  - Web-based database admin interface
  - Accessible via proxy_noco

- **proxy_api** - Nginx reverse proxy for backend
  - SSL termination for Flask API
  - Maps external API_PORT to internal backend:5000

- **proxy_noco** - Nginx reverse proxy for NocoDB
  - SSL termination for admin interface
  - Maps external NOCO_PORT to internal admin:8080

## Setup

### Prerequisites

- Docker and Docker Compose installed
- SSL certificates (fullchain.pem, privkey.pem)

### Installation

1. Clone the repository

2. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and configure:
   - PostgreSQL credentials
   - BotX integration settings (CTS_URL, BOT_ID, SECRET)
   - Domain and ports
   - NocoDB JWT secret

4. Place SSL certificates in `proxy/certs/`:
   - `proxy/certs/fullchain.pem`
   - `proxy/certs/privkey.pem`

5. Start services:
   ```bash
   make up
   ```

## Development Commands

### Basic Operations
```bash
make up          # Start all services
make down        # Stop all services
make restart     # Restart all services
make ps          # Show service status
make logs        # Follow logs for all services
```

### Build and Clean
```bash
make build       # Rebuild containers without cache
make clean       # Stop services and remove volumes
```

### Database Access
```bash
docker compose exec db psql -U <POSTGRES_USER> -d <POSTGRES_DB_NAME>
```

### Service-Specific Operations
```bash
# Backend logs and shell
docker compose logs -f backend
docker compose exec backend bash

# NocoDB operations
make noco-restart
make noco-logs
```

## Environment Variables

Required configuration in `.env`:

**PostgreSQL:**
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_DB_NAME` - Database name

**NocoDB:**
- `NC_AUTH_JWT_SECRET` - Long random string for JWT authentication

**BotX Integration:**
- `BOTX_CTS_URL` - BotX server URL (e.g., https://chat.example.ru)
- `BOTX_BOT_ID` - Bot UUID from BotX
- `BOTX_SECRET` - Bot secret for API authentication

**Hosting:**
- `DOMAIN` - Server domain name
- `API_PORT` - External port for backend API (default: 8440)
- `NOCO_PORT` - External port for NocoDB (default: 8441)

## Testing

1. Check health endpoint:
   ```bash
   curl -k https://<DOMAIN>:<API_PORT>/healthz
   ```

2. Send test BotX webhook:
   ```bash
   curl -k -X POST https://<DOMAIN>:<API_PORT>/api/v1/command \
     -H "Content-Type: application/json" \
     -d '{"text":"hello","chat_id":"test-chat"}'
   ```

3. Check logs:
   ```bash
   docker compose logs -f backend
   ```

## Backend Development

The Flask backend runs with auto-reload enabled in development mode. Changes to `backend/app.py` will automatically restart the server.

### Adding Python Dependencies
1. Add package to `backend/requirements.txt`
2. Rebuild container: `make build`

### Database Connection
Connection string format:
```
postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@db:5432/<POSTGRES_DB_NAME>
```

## Key Files

- `backend/app.py` - Main Flask application
- `docker-compose.yml` - Service orchestration
- `Makefile` - Development shortcuts
- `.env` - Environment configuration
- `proxy/nginx-api.conf` - API proxy configuration
- `proxy/nginx-noco.conf` - NocoDB proxy configuration

## Troubleshooting

**Service won't start:** Check `docker compose ps` and `make logs`. Database must be healthy before backend/admin start.

**SSL errors:** Verify certificates exist at `proxy/certs/fullchain.pem` and `proxy/certs/privkey.pem`.

**Port conflicts:** Adjust `API_PORT` and `NOCO_PORT` in `.env` if ports are already in use.

## License

See LICENSE file for details.
