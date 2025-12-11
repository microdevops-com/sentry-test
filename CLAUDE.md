# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Sentry SDK testing repository using Docker Compose for containerized development. The project is configured to test and develop with the Sentry Python SDK.

## Environment Setup

The repository uses Docker Compose with a Python 3.12 environment. The Sentry DSN is loaded from environment variables (`.env` file or system environment).

Create a `.env` file in the project root with:
```
SENTRY_DSN=your_sentry_dsn_here
```

## Development Commands

### Starting the Environment
```bash
docker compose up -d
docker compose exec sentry-test bash
```

Dependencies from `requirements.txt` are automatically installed when the container starts via the entrypoint script.

### Running Python Scripts
```bash
docker compose exec sentry-test python <script_name>.py
```

### Running the Sentry Test Script
The `test_sentry.py` script sends telemetry data (errors, traces, profiling, logs) to Sentry every second:
```bash
docker compose exec sentry-test python test_sentry.py
```
Press Ctrl+C to stop the script.

## Architecture

### Docker Configuration
- **Base Image**: Python 3.12 (slim-bookworm)
- **Working Directory**: `/app`
- **Volume Mount**: Current directory mounted at `/app` (enables live code editing)
- **User**: Runs as UID 1000:1000 (non-root)
- **Entrypoint**: Automatically runs `pip install -r requirements.txt` on container start
- **Pip Configuration**:
  - Packages installed to `/app/.pip_packages`
  - Cache stored in `/app/.pip_cache`
  - Both directories are volume-mounted for persistence

### Key Environment Variables
- `PYTHONPATH=/app:/app/.pip_packages:$PYTHONPATH`
- `PIP_TARGET=/app/.pip_packages`
- `PIP_CACHE_DIR=/app/.pip_cache`
- `SENTRY_DSN` - Loaded from `.env` file (required for test script)

## Project Structure

- `compose.yaml` - Docker Compose service definition
- `Dockerfile` - Python 3.12 environment with debugging tools (ping, ps, netstat)
- `entrypoint.sh` - Entrypoint script that auto-installs dependencies
- `requirements.txt` - Python dependencies (sentry-sdk)
- `test_sentry.py` - Comprehensive test script that sends errors, traces, profiling data, and logs to Sentry

## Testing with Sentry

### Test Script (`test_sentry.py`)
The repository includes a comprehensive test script that demonstrates all Sentry features:
- **Errors**: Sends various exception types (ZeroDivisionError, ValueError, IndexError, KeyError)
- **Tracing**: Creates transactions with multiple spans (database, HTTP, processing)
- **Profiling**: Profiles function execution using continuous profiling
- **Logs**: Sends logs at different levels (info, warning, error) using both Sentry logger and Python logging

The script sends one sample of each telemetry type every second.

**Note**: The script reads the Sentry DSN from the `SENTRY_DSN` environment variable. Ensure this is set in your `.env` file.

### SDK Configuration
The Sentry SDK is configured with:
- `send_default_pii=True` - Includes user data like headers and IP
- `enable_logs=True` - Forwards logs to Sentry
- `traces_sample_rate=1.0` - Captures 100% of transactions
- `profile_session_sample_rate=1.0` - Profiles 100% of sessions
