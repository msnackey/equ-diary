import collections
import logging
import sys
import pathlib

from rich.table import Table
from rich.console import Console
from rich.markup import escape

from django_doctor.staticanalysis.commands import helpers


logger = logging.getLogger(__name__)


def handle(directories, ignore, disable, enable, jobs, output=sys.stdout):
    project_root = pathlib.Path('.').resolve()

    count = 0

    branches = collections.OrderedDict()

    messages = helpers.get_messages(
        directories=directories,
        ignore=ignore,
        enable=enable,
        disable=disable,
        jobs=jobs,
    )
    for message in messages:
        if message['path'] not in branches:
            icon = ':snake' if message["path"].endswith('py') else ':page_facing_up'
            title = f"{icon}: [link file://{message['path']}]{escape(str(pathlib.Path(message['path']).relative_to(project_root)))}"
            branches[message['path']] = table = Table(show_lines=True, title=title)
            table.add_column('Line')
            table.add_column('Message')
            table.add_column('Suggested change', no_wrap=True)
            table.add_column('Reference')

        table.add_row(
            str(message["line"]),
            f"{message['msg']}",
            message.diff or 'N/A',
            '\n'.join(message.documentation_links),
        )
        count += len(message['message_ids'])

    console = Console(file=output, log_path=False, log_time=False)
    console.log('\n')
    for item in branches.values():
        console.log(item)
        console.log('\n')
    sys.exit(0 if count == 0 else 1)
