import argparse
import pathlib
import logging
import sys

from rich.logging import RichHandler

sys.path.insert(0, '.')

from django_doctor.staticanalysis.commands import fix, check

logger = logging.getLogger('django_doctor')  # configure logging for django-doctor in general so it affects module-wide

ignore_help = 'Add <file or directory> to the black list. It should be a base name, not a path.'
jobs_help = (
    'Use multiple processes to speed up Django Doctor. Specifying 0 will auto-detect the number of '
    'processors available to use. [default: 0]'
)
SUPPORT_MESSAGE = 'Please support Django Doctor by buying a licence for commercial use. https://django.doctor/price\n'


def resolve_directory(raw):
    return str(pathlib.Path(raw).resolve())


parser = argparse.ArgumentParser(prog='Django Doctor')

subparsers = parser.add_subparsers()

check_parser = subparsers.add_parser('check')
check_parser.add_argument(
    'directories',
    nargs='*',
    type=resolve_directory,
    default=[resolve_directory('.')],
    help="Directory to collect Django files from. Defaults to current directory"
)
check_parser.add_argument('-d', '--disable', action='append', default=[], help='Checks to disable')
check_parser.add_argument('-e', '--enable', action='append', default=[], help='Checks to enable')
check_parser.add_argument('-i', '--ignore', action='append', default=[], help=ignore_help)
check_parser.add_argument('-l', '--log-level', choices=['debug', 'info'], default='info', type=str)
check_parser.add_argument('-j', '--jobs', default=0, help=jobs_help, type=int)

check_parser.set_defaults(command='check')

fix_parser = subparsers.add_parser('fix')
fix_parser.add_argument(
    'directories',
    nargs='*',
    type=resolve_directory,
    default=[resolve_directory('.')],
    help="Directory to collect Django files from. Defaults to current directory"
)
fix_parser.add_argument('-d', '--disable', action='append', default=[], help='Checks to disable')
fix_parser.add_argument('-e', '--enable', action='append', default=[], help='Checks to enable')
fix_parser.add_argument('-i', '--ignore', action='append', default=[], help=ignore_help)
fix_parser.add_argument('-l', '--log-level', choices=['debug', 'info'], default='info', type=str)
fix_parser.add_argument('-a', '--address', default='localhost', type=str)
fix_parser.add_argument('-p', '--port', default=9000, type=int)
fix_parser.add_argument('-j', '--jobs', default=0, help=jobs_help, type=int)
fix_parser.set_defaults(command='fix')

rich_handler = RichHandler(show_path=False, show_time=False, show_level=False)


def handle(handler=rich_handler, argv=sys.argv[1:]):
    handler.setFormatter(logging.Formatter(fmt="%(message)s", datefmt=None))

    options = parser.parse_args(argv)

    logger.setLevel({'debug': logging.DEBUG, 'info': logging.INFO}[options.log_level])
    logger.addHandler(handler)
    logger.info(SUPPORT_MESSAGE)
    logger.info("HINT: use --log-level=debug to list files --ignore=foo to skip any directories --disable to turn off checks.\n")

    if options.command == 'check':
        multiprocessing_fallback(
            handler=check.handle,
            directories=options.directories,
            ignore=options.ignore,
            disable=options.disable,
            enable=options.enable,
            jobs=options.jobs,
        )
    elif options.command == 'fix':
        multiprocessing_fallback(
            handler=fix.handle,
            directories=options.directories,
            address=options.address,
            port=options.port,
            ignore=options.ignore,
            disable=options.disable,
            enable=options.enable,
            jobs=options.jobs,
        )


def multiprocessing_fallback(handler, jobs, **kwargs):
    # on mac multiprocessing seems to make thins fall over. Handle this case.
    try:
        handler(jobs=jobs, **kwargs)
    except TypeError as exception:
        if "_thread.RLock" in str(exception):
            logger.info("[orange]Failed to run in multiprocessing mode. Retrying as single process.[/orange]")
            handler(jobs=1, **kwargs)
        else:
            raise


def main():
    try:
        handle()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
