from celery import shared_task
import time


@shared_task
def process_tarball(tarball_content: bytes):
    # Simulate tarball processing
    time.sleep(5)  # Placeholder for actual processing work
    print(f"Processed tarball of size: {len(tarball_content)} bytes")
    return "Processing complete!"


@shared_task
def simple_task():
    return "Simple task completed!"
