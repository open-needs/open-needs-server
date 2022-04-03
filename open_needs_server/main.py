import os
import logging
import uvicorn
import time

from open_needs_server.config import settings

# Set logger so that initialisation code can use configured loggers.
logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)

log = logging.getLogger(__name__)
log.setLevel(settings.server.log_level)  # Level for root
logging.getLogger('open_needs_server').setLevel(settings.server.log_level)  # Level for server only

from open_needs_server.database import create_db_and_tables

from open_needs_server.version import VERSION

from open_needs_server.app import OpenNeedsServerApp


start_time = time.time()

# Create main app
ons_app = OpenNeedsServerApp(
    title="Open-Needs Server",
    version=VERSION,
    description="REST API Server of Open-Needs",
    license_info={"name": "MIT License",
                  "url": "https://github.com/open-needs/open-needs-server/blob/main/LICENSE"},
    contact={"name": "Open-Needs community",
             "url": "https://github.com/open-needs"}
)

# Load extensions



# Register specific handlers
@ons_app.on_event("startup")
async def on_startup():
    ons_app.load_extensions(settings.server.extensions)
    await create_db_and_tables()
    ons_app.startup_report(start_time)


def start():
    """Start the webserver"""
    uvicorn.run(ons_app, host=settings.server.server, port=settings.server.port)


if __name__ == "__main__":
    start()
