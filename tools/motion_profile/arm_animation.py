from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from SplineGeneration import generateSplines

class ArmAnimation(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "horizontal", **kwargs)

        #main widgets
        self.animation = Image()

        #add main widgets
        self.add_widget(self.animation)

        #physical constants (s, deg, in)
        self.UPRIGHT_ARM_ANGLE = 180
        self.MIN_ARM_LENGTH = 24
        self.MAX_ARM_LENGTH = 80

        #setpoints
        #[time (s), arm angle (deg), arm extension (in)]
        self.setpoints = [
            [0, 180, 0],
            [1, 180, 40],
            [2, 180, 0],
            [3, 135, 0],
            [4, 180, 0],
            [5, 135, 40]
        ]