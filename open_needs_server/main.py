import os
import logging
import uvicorn
import time

from open_needs_server.database import create_db_and_tables

from open_needs_server.version import VERSION
from open_needs_server.app import OpenNeedsServerApp
from open_needs_server.extensions import OrganizationExtension, \
    ProjectExtension, NeedExtension, FilterExtension, UserSecurityExtension, \
    ExtensionViewerExtension


start_time = time.time()

logging_conf_path = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
log = logging.getLogger(__name__)

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
org_ext = OrganizationExtension(ons_app, 'Organization', VERSION)
project_ext = ProjectExtension(ons_app, 'Project', VERSION)
need_ext = NeedExtension(ons_app, 'Need', VERSION)
filter_ext = FilterExtension(ons_app, 'Filter', VERSION)
user_security_ext = UserSecurityExtension(ons_app, 'UserSecurity', VERSION)
extension_ext = ExtensionViewerExtension(ons_app, 'ExtensionViewer', VERSION)

# Register specific handlers
@ons_app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    ons_app.startup_report(start_time)


def start():
    """Start the webserver"""
    uvicorn.run(ons_app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()
