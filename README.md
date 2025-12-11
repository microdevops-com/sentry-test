# Sentry Test Environment

Dockerized project to send sample errors, transactions, logs etc to Sentry (self-hosted via DSN) to ensure its features are working properly.

## Overview

This project provides a containerized Python environment for testing Sentry's telemetry capabilities. It includes a comprehensive test script that continuously sends various types of data to your Sentry instance, allowing you to verify that all features are functioning correctly.

## Features

The test script sends the following telemetry data to Sentry:

- **Errors**: Various Python exception types (ZeroDivisionError, ValueError, IndexError, KeyError)
- **Transactions**: Distributed tracing with multiple spans (database queries, HTTP calls, data processing)
- **Profiling**: Continuous profiling of function execution
- **Logs**: Structured logging at different severity levels (INFO, WARNING, ERROR)

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd sentry-test
```

2. Create a `.env` file with your Sentry DSN:
```bash
cp .env.example .env
# Edit .env and add your actual Sentry DSN
```

3. Start the Docker environment:
```bash
docker compose up -d
```

Dependencies are automatically installed when the container starts.

## Usage

### Running the Test Script

To start sending telemetry data to Sentry:

```bash
docker compose exec sentry-test python test_sentry.py
```

The script will:
- Send one sample of each telemetry type (error, trace, profiling, logs) every second
- Display what was sent in the console
- Continue running until you press `Ctrl+C`

### Interactive Development

To access the container shell:

```bash
docker compose exec sentry-test bash
```

### Running Custom Scripts

```bash
docker compose exec sentry-test python your_script.py
```

## Configuration

### Sentry SDK Settings

The test script uses the following Sentry SDK configuration:

- `send_default_pii=True` - Includes user data like request headers and IP addresses
- `enable_logs=True` - Forwards Python logs to Sentry
- `traces_sample_rate=1.0` - Captures 100% of transactions for tracing
- `profile_session_sample_rate=1.0` - Profiles 100% of sessions

### Environment Variables

- `SENTRY_DSN` - Your Sentry Data Source Name (required)

## Project Structure

```
.
├── compose.yaml        # Docker Compose configuration
├── Dockerfile          # Python 3.12 environment with debugging tools
├── entrypoint.sh       # Auto-installs dependencies on container start
├── requirements.txt    # Python dependencies (sentry-sdk)
├── test_sentry.py      # Comprehensive Sentry telemetry test script
├── .env.example        # Example environment variables
└── CLAUDE.md          # Development guide for Claude Code
```

## Docker Environment

- **Base Image**: Python 3.12 (slim-bookworm)
- **Working Directory**: `/app`
- **Volume Mount**: Current directory mounted for live code editing
- **User**: Runs as UID 1000:1000 (non-root)
- **Packages**: Installed locally in `/app/.pip_packages` (persisted via volume)

## Verifying Sentry

After running the test script, check your Sentry instance for:

1. **Issues** - Various error types should appear
2. **Performance** - Transactions with spans should be visible
3. **Profiling** - Function profiling data should be available
4. **Logs** - Log entries at different severity levels

## Stopping the Environment

```bash
docker compose down
```

## License

This project is provided as-is for testing purposes.
