#!/usr/bin/env python3
"""
Sentry Test Script
Sends errors, traces, profiling data, and logs to Sentry every second.
"""

import os
import sys
import time
import random
import logging
import sentry_sdk
from sentry_sdk import start_transaction

# Configure Python's built-in logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get Sentry DSN from environment variable
SENTRY_DSN = os.environ.get("SENTRY_DSN")
if not SENTRY_DSN:
    print("Error: SENTRY_DSN environment variable is not set!")
    print("Please set SENTRY_DSN in your environment or docker-compose.yaml")
    sys.exit(1)

# Initialize Sentry SDK
sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Add data like request headers and IP for users
    send_default_pii=True,
    # Enable sending logs to Sentry
    enable_logs=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profile_session_sample_rate to 1.0 to profile 100%
    # of profile sessions.
    profile_session_sample_rate=1.0,
)

def slow_function():
    """Simulates a slow operation for profiling"""
    time.sleep(0.1)
    return "slow_done"

def fast_function():
    """Simulates a fast operation for profiling"""
    time.sleep(0.05)
    return "fast_done"

def send_error_sample():
    """Send an error to Sentry"""
    try:
        # Intentionally cause different types of errors
        error_type = random.choice([
            lambda: 1 / 0,  # ZeroDivisionError
            lambda: int("not_a_number"),  # ValueError
            lambda: [][5],  # IndexError
            lambda: {"key": "value"}["missing_key"],  # KeyError
        ])
        error_type()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"✓ Error sent: {type(e).__name__}")

def send_trace_sample():
    """Send a transaction trace to Sentry"""
    with start_transaction(op="test", name="test_transaction") as transaction:
        # Create spans within the transaction
        with transaction.start_child(op="db", description="Database query"):
            time.sleep(0.05)

        with transaction.start_child(op="http", description="API call"):
            time.sleep(0.03)

        with transaction.start_child(op="process", description="Data processing"):
            time.sleep(0.02)

    print("✓ Trace sent: test_transaction")

def send_profiling_sample():
    """Send profiling data to Sentry"""
    # Start profiler
    sentry_sdk.profiler.start_profiler()

    # Execute functions to profile
    for _ in range(3):
        slow_function()
        fast_function()

    # Stop profiler
    sentry_sdk.profiler.stop_profiler()
    print("✓ Profiling data sent")

def send_logs_sample(iteration):
    """Send logs to Sentry"""
    # Using Sentry's logger API - send different log levels
    log_messages = [
        ("info", f"Info log sample {iteration}"),
        ("warning", f"Warning log sample {iteration}"),
        ("error", f"Error log sample {iteration}"),
    ]

    message_type, message = random.choice(log_messages)

    if message_type == "info":
        sentry_sdk.logger.info(message)
        logger.info(message)  # Also send via Python logging
    elif message_type == "warning":
        sentry_sdk.logger.warning(message)
        logger.warning(message)
    elif message_type == "error":
        sentry_sdk.logger.error(message)
        logger.error(message)

    print(f"✓ Log sent: [{message_type.upper()}] {message}")

def main():
    """Main loop that sends telemetry data every second"""
    print("Starting Sentry test script...")
    print(f"Sentry DSN: {SENTRY_DSN[:50]}...")
    print("Sending errors, traces, profiling data, and logs every second...")
    print("Press Ctrl+C to stop\n")

    iteration = 0

    try:
        while True:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")

            # Send error sample
            send_error_sample()

            # Send trace sample
            send_trace_sample()

            # Send profiling sample
            send_profiling_sample()

            # Send logs sample
            send_logs_sample(iteration)

            print(f"Waiting 1 second...\n")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nStopping test script...")
        print(f"Total iterations: {iteration}")

        # Flush any remaining events
        sentry_sdk.flush(timeout=2.0)
        print("All events flushed to Sentry. Goodbye!")

if __name__ == "__main__":
    main()
