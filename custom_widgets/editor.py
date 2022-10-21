from kivy.uix.gridlayout import GridLayout

class Editor(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(rows = 3, **kwargs)