from collections import defaultdict
from operator import itemgetter
import logging

from django_doctor.staticanalysis import constants, diff, helpers, message_templates

logger = logging.getLogger(__name__)


CODE_SYNTAX_ERROR = 'E0001'


def render_template(template, message):
    # for ...reasons... this message type does not play nice, so special handling here
    if message['message-id'] == CODE_SYNTAX_ERROR:
        return 'Syntax error'
    return template.format(**message['message'])


def read_code_from_message(message):
    return helpers.read_code_from_file(message['path'])


def render_line_centric_advice(messages, settings, settings_modpath, code_style, code_reader=read_code_from_message):
    group = defaultdict(list)

    for message in messages:
        # transformer does not support html yet
        if message['path'].endswith('.py') and message['message-id'] in constants.TRANSFORMABLE_RULES:
            key = f"{message['path']}:{message['line']}"
            group[key].append(message)

    cache = {}
    for key, messages in group.items():
        path = messages[0]['path']
        message_ids = set(message['message-id'] for message in messages)

        if path not in cache:
            path = messages[0]['path']
            cache[path] = helpers.build_atok(
                source=''.join(code_reader(messages[0])),
                modname=helpers.module_path_from_file(path),
                absolute_path=path
            )
        # yes this try catch sucks but get_diff_for_python is running complex code on code in an unknowable state
        # so can break...but we dont want to trash the entire report because one message failed to render the diff...
        try:
            before, after = diff.get_diff_for_python(
                atok=cache[path],
                line=int(messages[0]['line']),  # decimal to int
                message_ids=message_ids,
                code_style=code_style,
                settings_modpath=settings_modpath,
            )
        except Exception as error:
            logger.exception(error)
            continue
        if before == after:
            continue

        context = {}
        for item in messages:
            context.update(item['message'])
        yield {
            'message_ids': message_ids,
            'diff': {'before': before, 'after': after},
            'path': path,
            'line': int(messages[0]['line']),
            'message_type': 'line_centric',
            'context': context,
        }

    cache.clear()  # manually clearing to prevent memory leak on lambda


def render_line_centric_issues(messages, settings, settings_modpath, code_style, code_reader=read_code_from_message):
    # like render_line_centric_advice but for issues that have no suggestion, just problem
    group = defaultdict(list)
    rendered_messages = []

    for message in messages:
        # transformer does not support html yet
        if message['message-id'] not in constants.TRANSFORMABLE_RULES:
            key = f"{message['path']}:{message['line']}"
            group[key].append(message)

    cache = {}

    for key, messages in group.items():
        path = messages[0]['path']
        message_ids = set(message['message-id'] for message in messages)

        context = {}
        for item in messages:
            context.update(item['message'])
        rendered_messages.append({
            'message_ids': message_ids,
            'path': path,
            'line': int(messages[0]['line']),
            'message_type': 'line_centric',
            'context': context,
        })

    cache.clear()  # manually clearing to prevent memory leak on lambda
    return rendered_messages


def render_message_centric_advice(
    messages, settings, settings_modpath, code_style, code_reader=read_code_from_message
):
    message_id_centric_messages = []
    seen = set()
    cache = {}

    for message in messages:
        message_id = message["message-id"]

        template = getattr(message_templates, message_id, None)
        if not template:
            if message_id not in ['C1000', 'E0001']:
                logger.warning(f'No message template for {message_id}')
            continue

        try:
            message_diff = get_message_diff(
                message=message,
                cache=cache,
                seen=seen,
                code_reader=code_reader,
                code_style=code_style,
                settings_modpath=settings_modpath,
                settings=settings,
            )
        except Exception as e:
            logger.error('unable to get message diff', exc_info=e)
            continue

        message_id_centric_messages.append({
            **message,
            'diff': message_diff,
            'message': render_template(template=template['report'], message=message),
            'path': message['path'],
            'message_type': 'message_centric',
        })

    cache.clear()  # manually clearing to prevent memory leak on lambda

    # sort by diff so the first instance the frontend sees of a particular issue has a diff
    return sort_has_diff(message_id_centric_messages)


def get_message_diff(message, cache, seen, code_reader, code_style, settings_modpath, settings):

    message_id = message["message-id"]

    message_diff = None
    if message_id not in seen and message_id in constants.TRANSFORMABLE_RULES:
        path = message['path']
        if path.endswith('.py'):
            if path not in cache:
                cache[path] = helpers.build_atok(
                    source=''.join(code_reader(message)),
                    modname=helpers.module_path_from_file(path),
                    absolute_path=path,
                )
            before, after = diff.get_diff_for_python(
                atok=cache[path],
                line=int(message['line']),
                message_ids={message_id},
                code_style=code_style,
                settings_modpath=settings_modpath,
            )
        else:
            if path not in cache:
                cache[path] = code_reader(message)

            before, after = diff.get_diff_for_html(
                source_lines=cache[path],
                line=int(message['line']),
                message_ids={message_id},
                settings=settings,
            )
        # some transformations bail out early e.g, C2000 when there are choices
        if before != after:
            message_diff = {
                'before': before,
                'after': after,
            }
            seen.add(message_id)
    return message_diff


def render_report_messages(*args, **kwargs):
    return (
        render_message_centric_advice(*args, **kwargs) +
        list(render_line_centric_advice(*args, **kwargs)) +
        render_meta_messages(*args, **kwargs)
    )


def render_meta_messages(messages, *args, **kwargs):
    return [message for message in messages if message.get('message_type') == 'meta']


def sort_path_and_line(commnets):
    return sorted(commnets, key=itemgetter('path', 'line'))


def key_sort_has_diff(item):
    if item.get('diff'):
        return 0
    return 1


def sort_has_diff(messages):
    messages = sort_path_and_line(messages)
    return sorted(messages, key=key_sort_has_diff)
