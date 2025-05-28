# apps/utils/json_responses.py

import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def json_error_response(message_user="Ocorreu um erro interno.",
                        exception=None, level="error", context=""):
    if exception:
        log_message = f"[{context}] {str(exception)}"
        if level == "warning":
            logger.warning(log_message)
        else:
            logger.error(log_message)
    return JsonResponse({"success": False, "message": message_user})


def log_exception(exception, context="", level="error"):
    message = f"[{context}] {str(exception)}"
    if level == "warning":
        logger.warning(message)
    else:
        logger.error(message)
