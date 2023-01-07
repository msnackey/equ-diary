import logging
import pathlib
import webbrowser

from django_doctor.staticanalysis.commands import helpers, wsgi
from django_doctor.staticanalysis import constants
from django_doctor.staticanalysis.checker import message_id_symbol_store


logger = logging.getLogger(__name__)


MESSAGE = (
    "Analyzing your Django code.\n"
    "The suggestion engine will soon open in your browser on http://{address}:{port}\n"
    "Use Ctrl+C or Command+C etc to exit."
)


def handle(directories, ignore, address, port, enable, jobs, disable):
    non_autofix_messages = set(message_id_symbol_store.keys()) - constants.TRANSFORMABLE_RULES
    disable = list(non_autofix_messages.union(disable))
    project_root = pathlib.Path('.').resolve()

    logger.info(MESSAGE.format(address=address, port=port))

    messages = list(helpers.get_messages(
        directories=directories,
        ignore=ignore,
        enable=enable,
        disable=disable,
        jobs=jobs,
    ))
    for message in messages:
        if message['message_ids'].intersection(constants.TRANSFORMABLE_RULES):
            break
    else:
        logger.info("\n\nNo autofixable issues detected. Good job.\n")
        return

    server = wsgi.create(
        address=address,
        port=port,
        project_root=project_root,
        messages=messages,
    )
    webbrowser.open_new(f"http://{address}:{port}")
    server.serve_forever()
