import sublime, sublime_plugin
from datetime import datetime 

class ItodoCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # only work on .todo files
    filename = self.view.file_name()
    if filename is None or not filename.endswith('.todo'):
      return False
    
    for region in self.view.sel():
      line = self.view.line(region)
      line_contents = self.view.substr(line).strip()

      # prepend @done if item is ongoing
      if line_contents.startswith('-'):
        self.view.insert(edit, line.end(), " @done (%s)" % datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.view.replace(edit, self.view.word(line.begin()), "+ ")
      # undo @todo
      elif line_contents.startswith('+'):
        #subfix = self.view.find('(\s)*@done(.)+\)$', line.begin())
        subfix = self.view.find('(\s)*@done(.)+\)$', line.begin())
        self.view.erase(edit, subfix)
        self.view.replace(edit, self.view.word(line.begin()), "- ")
      