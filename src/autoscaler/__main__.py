"""Executable module for the autoscaler."""

from autoscaler import create_app

if __name__ == "__main__":
    import sys
    import uvicorn

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    uvicorn.run(
        create_app,
        port=port,
        factory=True,
    )  # pyright: reportUnknownMemberType=false
