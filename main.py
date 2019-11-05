# Python3.3

import os
import traceback


import sublime
import sublime_plugin

from . import sqlx


class BuildSqlxCommand(sublime_plugin.TextCommand):

    def run(self, edit):


        file = self.view.file_name()
        print('Building: %s' % file)

        if not file:
            sublime.status_message('Please save file first')
            return

        if not file.endswith('.sqlx'):
            sublime.status_message('Only .sqlx files can be built by sqlx')
            return

        # print(self.view.settings().get('syntax'))
        self.view.set_syntax_file('Packages/SQL/SQL.sublime-syntax')

        dirname, filename = os.path.split(file)

        self.view.run_command("select_all")
        regions = self.view.sel()
        sqlx_content = self.view.substr(regions[0])
        assert len(regions) == 1

        # Another Way
        # selection = sublime.Region(0, self.view.size())
        # sqlx_content = self.view.substr(selection)

        try:
            sql_content = sqlx.build(sqlx_content, False, dirname)
            sublime.set_clipboard(sql_content)
            sublime.status_message('Built success, and copied the result to clipboard')
        except Exception as e:
            sublime.error_message('Built failed: %s' % e)
            raise e
        


