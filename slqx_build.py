import sublime
import sublime_plugin

import subprocess
import threading
import os

from . import sqlx


class SqlxBuildCommand(sublime_plugin.WindowCommand):


    def is_enabled(self):
        return True

    def run(self, to_dist=False):

        # Creating the panel implicitly clears any previous contents
        self.panel = self.window.create_output_panel('exec')
        self.window.run_command('show_panel', {'panel': 'output.exec'})

        self.vars = self.window.extract_variables()
        # working_dir = self.vars.get('file_path')

        self.view = self.window.active_view()

        # as same as main.py

        self.view.run_command("select_all")
        regions = self.view.sel()
        sqlx_content = self.view.substr(regions[0])

        file = self.view.file_name() or ''

        if to_dist:
            if not file:
                self.show_message('Please save file first')
                return
            if not file.endswith('.sqlx'):
                self.show_message('Only .sqlx files can be built by sqlx')
                return

        dirname, filename = os.path.split(file)

        try:
            sql_content = sqlx.build(sqlx_content, False, dirname)
        except Exception as e:
            self.show_message('Built failed: %s' % e)
            raise e
        
        if to_dist:
            distname = os.path.join(dirname, 'dist')
            filename = os.path.join(distname, filename[:-1])
            if not os.path.isdir(distname):
                os.makedirs(distname)
            open(filename, 'w', encoding='utf8').write(sql_content)
            self.show_message('Built success, and saved to `%s`' % distname)
        else:
            sublime.set_clipboard(sql_content)
            self.show_message(sql_content)
            self.show_message('------------------------------------------------------')
            self.show_message('Built success, and copied the result to clipboard')
            # print(self.view.settings().get('syntax'))
            self.view.set_syntax_file('Sqlx.sublime-syntax')

    def show_message(self, text):
        self.panel.run_command('append', {'characters': str(text) + '\n'})

