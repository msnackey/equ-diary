from contextlib import contextmanager
import difflib
import itertools
import logging
import pathlib
import os
import re

from rich.console import Console
from rich.progress import Progress

from django_doctor.staticanalysis import checker, meta, render, transformer, message_templates


logger = logging.getLogger(__name__)


def dedent_diff_lines(lines):
    lines = list(lines)
    if not lines:
        return lines
    match = re.match(r'[\-\+]( +)', lines[0])
    if not match:
        return lines
    return [re.sub(fr'^([\-\+]){match.group(1)}', r'\1 ', line) for line in lines]


def color_diff(line):
    if line.startswith('+'):
        return f'[green]{line}[/green]'
    elif line.startswith('-'):
        return f'[red]{line}[/red]'
    return line


class Message(dict):
    def __getattr__(self, key):
        return self.get(key)

    def _replace(self, **msg):
        self.update(msg)
        return self

    @property
    def documentation_links(self):
        return [get_hyperlink(message_id) for message_id in self['message_ids']]

    @property
    def diff(self):
        if not self.get('diff'):
            return ''
        diff = difflib.unified_diff(
            a=[line for number, line in self['diff']['before']],
            b=[line for number, line in self['diff']['after']],
            lineterm='',
            n=0,
        )
        # skipping the headers "+++" and "---"
        next(diff)
        next(diff)
        next(diff)
        return '\n'.join([color_diff(item) for item in dedent_diff_lines(diff)])


def get_messages(directories, ignore, enable, disable, jobs):
    project_root = str(pathlib.Path('.').resolve())

    console = Console()
    with console.status("[bold green]Collecting Django files to analyze..."):
        files = meta.get_files_to_check_in_project(directories=directories, ignore=ignore)

    logger.debug(f"Collected {len(files)} Django files.")

    config = {}
    if enable:
        config['enable'] = enable
    if disable:
        config['disable'] = disable
    messages = checker.get_messages(project_root=project_root, files=files, config=config, jobs=jobs)

    settings = {"STATIC_URL": meta.get_static_url_setting(project_root)}
    settings_modpath = meta.get_settings_modpath(project_root)
    code_style = meta.get_code_style(project_root)

    suggestions = render.render_line_centric_advice(
        messages=messages,
        settings=settings,
        settings_modpath=settings_modpath,
        code_style=code_style,
    )
    issues = render.render_line_centric_issues(
        messages=messages,
        settings=settings,
        settings_modpath=settings_modpath,
        code_style=code_style,
    )

    with Progress() as progress:
        task = progress.add_task(f"[blue]Rendering {len(messages)} issues...", total=len(messages))

        items = []
        for item in itertools.chain(issues, suggestions):
            progress.update(task, advance=1)
            items.append(item)

        for item in render.sort_path_and_line(items):
            line_messages = []
            for message_id in item["message_ids"]:
                template = getattr(message_templates, message_id)
                line_message = render.render_template(
                    template=template['report'],
                    message={**item, 'message-id': message_id, 'message': item['context']}
                )
                line_messages.append(f'[bold]{line_message}[/bold]')
            yield Message(
                **item,
                msg='\nalso, '.join(f'{item}' for item in sorted(line_messages)),
                module=item["path"],
                C='W'
            )
        progress.update(task, advance=len(messages))


def trasform_files(project_root, whitelist):
    filepaths = transformer.trasform_files_in_place(project_root=project_root, whitelist=whitelist)
    body = ""
    for path in filepaths:
        if 'models.py' in path:
            body = " models.py has changed, so please run `./manage.py makemigrations`."
    logger.info(f"\n\nChanges saved successfully. {body}")


@contextmanager
def chdir(path):
    origin = pathlib.Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)


def get_hyperlink(message_id):
    return f'https://django.doctor/advice/{message_id}'
