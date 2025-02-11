# Command to start a worker
celery -A celeryskeleton worker --loglevel info --queues TroubleshootingCelery

# Start aws cli session with correct account