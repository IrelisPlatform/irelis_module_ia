import logging

logger = logging.getLogger(__name__)


def send_email(to: str, subject: str, body: str) -> None:
    """Placeholder email sender that logs payloads."""
    logger.info("Sending email", extra={"to": to, "subject": subject})
    # Hook up your provider (e.g., Sendgrid) here
