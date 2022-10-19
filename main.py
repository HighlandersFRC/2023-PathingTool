from kivy.app import App
from kivy.clock import Clock
from pathtool import PathTool

class PathApp(App):
    def build(self):
        Clock.schedule_interval(self.execute, 1.0  / 60.0)
        self.path_tool =  PathTool()
        return self.path_tool.layout

    def execute(self, dt):
        pass

if __name__ == "__main__":
    PathApp().run()