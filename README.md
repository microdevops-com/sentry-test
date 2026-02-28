# Sentry Test Environment

Dockerized project to send sample errors, transactions, logs etc to Sentry (self-hosted via DSN) to ensure its features are working properly.

## Overview

This project provides a containerized Python environment for testing Sentry's telemetry capabilities.
It includes a comprehensive test script that continuously sends various types of data to your Sentry instance, allowing you to verify that all features are functioning correctly.

## SDK is Non-Blocking

The Sentry SDK is designed to be non-blocking, meaning that it will not interfere with the normal execution of your application.
When you send data to Sentry, it is sent asynchronously in the background, allowing your application to continue running without waiting for the data to be sent.
But that also means that you will not see sending errors in the console output of `sentry-test` container, as they are handled internally by the SDK.

## Features

The test script sends the following telemetry data to Sentry:

- **Errors**: Various Python exception types (ZeroDivisionError, ValueError, IndexError, KeyError)
- **Transactions**: Distributed tracing with multiple spans (database queries, HTTP calls, data processing)
- **Profiling**: Continuous profiling of function execution
- **Logs**: Structured logging at different severity levels (INFO, WARNING, ERROR)

## Prerequisites

- Docker
- Docker Compose

## Setup and Use

1. Clone the repository:
```bash
git clone <repository-url>
cd sentry-test
```

2. Create a `.env` file with your Sentry DSN:
```bash
cp .env.example .env
```
3. Edit `.env` and add your actual Sentry DSN and UID/GID.

4. Start the Docker environment:
```bash
docker compose up
```

Dependencies are automatically installed when the container starts.

The script will:
- Send one sample of each telemetry type (error, trace, profiling, logs) every second
- Display what was sent in the console
- Continue running until you press `Ctrl+C`

## Configuration

### Sentry SDK Settings

The test script uses the following Sentry SDK configuration:

- `send_default_pii=True` - Includes user data like request headers and IP addresses
- `enable_logs=True` - Forwards Python logs to Sentry
- `traces_sample_rate=1.0` - Captures 100% of transactions for tracing
- `profile_session_sample_rate=1.0` - Profiles 100% of sessions

### Environment Variables

- `SENTRY_DSN` - Your Sentry Data Source Name (required)
- `UID` - User ID for running the container (default: 1000)
- `GID` - Group ID for running the container (default: 1000)

## Verifying Sentry

After running the test script, check your Sentry instance for:

1. **Issues** - Various error types should appear
2. **Performance** - Transactions with spans should be visible
3. **Profiling** - Function profiling data should be available
4. **Logs** - Log entries at different severity levels

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
