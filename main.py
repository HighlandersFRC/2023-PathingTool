from kivy.app import App
from kivy.clock import Clock
from pathtool import PathTool

class PathApp(App):
    def build(self):
        #schedule execute callback
        Clock.schedule_interval(self.execute, 1.0  / 60.0)
        self.path_tool = PathTool()
        return self.path_tool

    #called at 60 Hz by Clock
    def execute(self, dt):
        self.path_tool.path.draw_path()

if __name__ == "__main__":
    PathApp().run()