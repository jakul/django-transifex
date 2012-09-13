"""
txpush.py

Push source translations to transifex.
"""

from django.core.management.base import NoArgsCommand, BaseCommand, CommandError
from djangotransifex import app_settings
from djangotransifex.api import DjangoTransifexAPI
import random
import sys
from textwrap import dedent
import inspect


class Command(BaseCommand):
    ## Settings ##
    project_slug = app_settings.PROJECT_SLUG
    resource_prefix = app_settings.RESOURCE_PREFIX
    source_language = app_settings.SOURCE_LANGUAGE_CODE
    username = app_settings.TRANSIFEX_USERNAME
    password = app_settings.TRANSIFEX_PASSWORD
    host = app_settings.TRANSIFEX_HOST

    @property
    def help(self):
        """
        Dynamically generate the help based on the available methods of this
        object
        """
        help_string = getattr(self, '__help', None)
        if help_string is None:
            help_string = dedent("""
            Available Commands:
            """)

            transifex_methods = [
                method for method in dir(self)
                if method.startswith('transifex_')
                and callable(getattr(self, method))
            ]
            for method_name in transifex_methods:
                reduced_method_name = method_name.replace('transifex_', '')
                help_string += ' * %s\n' % (reduced_method_name)

                # Check for a docstring
                method = getattr(self, method_name)
                doc = inspect.getdoc(method)
                for line in doc.split('\n'):
                    help_string += '    %s\n' % (line)

            self.__help = help_string
        return help_string

    def usage(self, subcommand):
        """
        Return a brief description of how to use this command, by
        default from the attribute ``self.help``.
        """
        usage = '%%prog %s command [options] %s' % (subcommand, self.args)
        if self.help:
            return '%s\n\n%s' % (usage, self.help)
        else:
            return usage

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You must give the name of an action to perform')
        command = args[0]
        command_func = getattr(self, 'transifex_%s' % (command), None)
        if command_func is None:
            raise CommandError('Unknown command %r' % (command))

        print('Executing {0} on project {1}'.format(command, self.project_slug))
        command_func(*args[1:], **options)

    @property
    def api(self):
        """
        Create an api instance
        """
        if not hasattr(self, '_api'):
            self._api = DjangoTransifexAPI(
                username=self.username, password=self.password, host=self.host
            )
            #TODO: Do a ping here
        return self._api

    def transifex_upload_source_translations(self, *args, **options):
        """
        Usage: ./manage.py tx upload_source_translation [options]
        Upload the source translation to Transifex.
        """
        self.confirm_command(app_settings.SOURCE_LANGUAGE_CODE)
        self.api.upload_source_translations(project_slug=self.project_slug)

    def transifex_upload_translations(self, *args, **options):
        """
        Usage: ./manage.py tx upload_translations language_code [options]
        Upload the translations for the given language to Transifex.
        This will overwrite any translations made on the Transifex server
        """
        if len(args) == 0:
            raise CommandError('Please provide the language code to upload')
        language_code = args[0]
        self.confirm_command(language_code)

        self.api.upload_translations(
            project_slug=self.project_slug, language_code=language_code
        )

    def _choose_word(self):
        with open('/usr/share/dict/words') as dict_file:
            dict_words = dict_file.readlines()

        word = None
        while word is None:
            word = random.choice(dict_words).replace('\n', '')
            if len(word) < 5:
                word = None

        return word

    def confirm_command(self, language_code):
        safety_word = self._choose_word()

        print((
            'This command will delete the existing "{0}" translations in the '
            '"{1}" project').format(language_code, self.project_slug)
        )
        print(
            'THIS IS NOT REVERSIBLE. YOU MAY LOSE DATA WHICH CANNOT BE '
            'REGENERATED'
        )
        print(
            'To continue, please type this word exactly as it appears - {0}'\
            .format(safety_word)
        )
        typed_word = raw_input('> ')

        if typed_word == safety_word:
            return
        else:
            print('Word entered incorrectly.')
            print('No upload performed.')
            sys.exit(1)

    def transifex_pull_translations(self, *args, **kwargs):
        """
        Usage: ./manage.py tx pull_translations [options]
        Pull all translations from the Transifex server to the local machine.
        This will overwrite any translations made locally
        """
        print(
            'Pulling translations for "{0}" project, in "{1}" source language'\
            .format(self.project_slug, self.source_language)
        )
        self.api.pull_translations(
            project_slug=self.project_slug, source_language=self.source_language
        )
        print('Translations pulled')

    def transifex_ping(self, *args, **kwargs):
        """
        Ping the server to verify connection details and auth details
        """
        print(self.api.ping())

    def transifex_create_project(self, *args, **kwargs):
        """
        Usage: ./manage.py tx create_project
        Create the project on Transifex.
        """
        print(
            'Creating project "{0}" with source language "{1}"'\
            .format(self.project_slug, self.source_language)
            )
        self.api.new_project(
            slug=self.project_slug, name=self.project_slug,
            source_language_code=self.source_language
        )
        print('Project created')

