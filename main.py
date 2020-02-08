# Python3.3

import os
import traceback

import sublime
import sublime_plugin

from . import sqlx


class BuildSqlxCommand(sublime_plugin.TextCommand):

    def run(self, edit, to_dist=False):

        file = self.view.file_name() or ''
        print('Building: %s' % file)

        if to_dist:
            if not file:
                sublime.status_message('Please save file first')
                return
            if not file.endswith('.sqlx'):
                sublime.status_message('Only .sqlx files can be built by sqlx')
                return


        self.view.run_command("select_all")
        regions = self.view.sel()
        sqlx_content = self.view.substr(regions[0])
        if len(regions) != 1:
            sublime.status_message('regions error')

        # Another Way
        # selection = sublime.Region(0, self.view.size())
        # sqlx_content = self.view.substr(selection)

        dirname, filename = os.path.split(file)

        try:
            sql_content = sqlx.build(sqlx_content, False, dirname)
        except Exception as e:
            sublime.error_message('Built failed: %s' % e)
            raise e
        
        if to_dist:
            distname = os.path.join(dirname, 'dist')
            filename = os.path.join(distname, filename[:-1])
            if not os.path.isdir(distname):
                os.makedirs(distname)
            open(filename, 'w', encoding='utf8').write(sql_content)
            sublime.status_message('Built success, and saved to `%s`' % distname)
        else:
            sublime.set_clipboard(sql_content)
            sublime.status_message('Built success, and copied the result to clipboard')
            # print(self.view.settings().get('syntax'))
            self.view.set_syntax_file('Sqlx.sublime-syntax')


