#!/usr/bin/env python3
"""Convenience script to run the EuroForm FastAPI server."""
from __future__ import annotations

import argparse
import sys
import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the EuroForm FastAPI API server.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host IP address to bind server to",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number to bind server to",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=True,
        help="Enable auto-reload on code change (default: enabled)",
    )
    parser.add_argument(
        "--no-reload",
        dest="reload",
        action="store_false",
        help="Disable auto-reload",
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print(" EuroForm FastAPI Server")
    print("=" * 60)
    print(f" * Web Interface:    http://{args.host}:{args.port}/")
    print(f" * Interactive Docs: http://{args.host}:{args.port}/docs")
    print(f" * ReDoc:            http://{args.host}:{args.port}/redoc")
    print(f" * Health Check:     http://{args.host}:{args.port}/health")
    print(f" * JSON Schema:      http://{args.host}:{args.port}/schema")
    print("=" * 60 + "\n")

    uvicorn.run(
        "euroform.api.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
