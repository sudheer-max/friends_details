from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
import kivy.utils


class WorkoutBanner(GridLayout):
    rows = 1

    def __init__(self, **kwargs):
        super(WorkoutBanner, self).__init__(**kwargs)
        with self.canvas.before :
            Color(rgb=(kivy.utils.get_color_from_hex("#808b8e")))
            self.rect = Rectangle(size=self.size, pos=self.pos) 
        self.bind(size=self.update_rect, pos=self.update_rect)

        # Left Floatlayout
        
        left = FloatLayout()
        left_image = Image(source = "icons/" + kwargs['workout_image'], size_hint =( 1, .8), pos_hint = {"top" : 1, "right" : 1})
        left_label = Label(text=kwargs['description'], size_hint =( 1, .2), pos_hint={"top" : .2, "right" : 1})
        left.add_widget(left_image)
        left.add_widget(left_label)

        # middle Floatlayout
        middle = FloatLayout()
        middle_image = Image(source = "icons/" + kwargs['type_image'], size_hint=(1,.8), pos_hint={"top" : 1, "right" : 1})
        middle_label = Label(text=str(kwargs['number']) + " " + kwargs['units'], size_hint=(1, .2), pos_hint={"top" : .2, "right" : 1})
        middle.add_widget(middle_image)
        middle.add_widget(middle_label)

        # right Floatlayout
        right = FloatLayout()
        right_image = Image(source="icons/united.png", size_hint=(1,.8), pos_hint={"top" : 1, "right" : 1})
        right_label = Label(text=str(kwargs['likes']) + " Likes", size_hint=(1, .2), pos_hint={"top" : .2, "right" : 1})
        right.add_widget(right_image)
        right.add_widget(right_label)

        self.add_widget(left)
        self.add_widget(middle)
        self.add_widget(right)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
