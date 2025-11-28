"""
Placeholder seed script.

The former seed data targeted an earlier schema. Update this script with
fixtures that match the tables defined in db/irelis.sql before running it.
"""

from __future__ import annotations

import logging

from app.db.init_db import init_db
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(
        "No seed data loaded. Add seed logic that matches the new schema when ready."
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with SessionLocal() as db:
        init_db(db)
    main()
