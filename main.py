from kivy.app import App
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from math import sin, cos, radians
import random
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

ASPECT_RATIO = 8 / 5 

LabelBase.register(name='CustomFont', fn_regular='Ananda Namaste Regular.ttf')

# Disable touch indicators
Config.set('input', 'mouse', 'mouse,disable_multitouch')

Builder.load_string('''
<NoTitlePopup>:
    title: ''
    title_size: 0
    title_font: ''
    separator_color: 0, 0, 0, 0

<RollingHand>:
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'gradient.png'

    Image:
        id: cowrie1
        source: 'cowrie1.png'  # Replace with the actual path to your cowrie1 image
        size: self.parent.width / 1.5, self.parent.height / 1.2
        pos: self.parent.width / 2.2, self.parent.height / 15
                    
    Image:
        id: hand
        source: 'hand.png'  # Replace with the actual path to your hand image
        size: self.parent.width / 1.5, self.parent.height / 1.2
        pos: self.parent.hand_position

    Button:
        size_hint: None, None
        size: self.parent.width / 7, self.parent.height / 13
        pos: root.width * 0.01, root.height * 0.02
        background_normal: 'start.png'  # Image for the button in its normal state
        background_down: 'start_pressed.png'
        on_release: root.start_animation()

    Button:
        size_hint: None, None
        size: self.parent.width / 7, self.parent.height / 13
        pos: root.width * 0.17, root.height * 0.02
        background_normal: 'stop.png'
        background_down: 'stop_pressed.png'
        on_release: root.stop_animation()
                
    Button:
        id: show_rashi_button
        background_normal: 'result.png'
        background_down: 'result_pressed.png'
        size_hint: None, None
        size: self.parent.width / 7, self.parent.height / 13
        opacity: 0
        pos: root.width * 0.68, root.height * 0.02
        on_release: root.show_rashi_popup(root.ids.rashi.text)  # Changed the binding to root

    Label:
        text: root.timer_text
        size_hint: None, None
        size: root.width * 0.15, root.height * 0.05
        pos: root.width * 0.32, root.height * 0.02

    Label:
        text: 'Number: ' + str(root.random_number)
        size_hint: None, None
        size: root.width * 0.2, root.height * 0.05
        pos: root.width * 0.48, root.height * 0.02

    Label:
        id: rashi
        text: ''
        size_hint: None, None
        size: root.width * 0.2, root.height * 0.05
        pos: root.width * 0.7, root.height * 0.02
        opacity:0

    GridLayout:
        cols: 3
        size_hint: None, None
        size: self.parent.width / 2, self.parent.height / 3  # Adjust as needed
        pos: (self.parent.width - self.width) / 4, (self.parent.height - self.height) / 2

        # Add 9 Image widgets (you can customize the appearance as needed)
        BoxLayout:
            orientation: 'vertical'
            Image:
                id: label1
                source: '0.png'  # Initially empty, to be updated dynamically
                size_hint: None, None
                size: self.parent.width / 2, self.parent.height / 2

            Image:
                id: label2
                source: '0.png'
                size_hint: None, None
                size: self.parent.width / 2, self.parent.height / 2

            Image:
                id: label3
                source: '0.png'
                size_hint: None, None
                size: self.parent.width / 2, self.parent.height / 2

        BoxLayout:
            orientation: 'vertical'
            Image:
                id: label4
                source: '0.png'
                size_hint: None, None
                size: self.parent.width / 2, self.parent.height / 2

            Image:
                id: label5
                source: '0.png'
                size_hint: None, None
                size: self.parent.width / 2, self.parent.height / 2

            Image:
                id: label6
                source: '0.png'
                size_hint: None, None
                size: self.parent.width / 2, self.parent.height / 2

        BoxLayout:
            orientation: 'vertical'
            Image:
                id: label7
                source: '0.png'
                size_hint: None, None
                size: self.parent.width / 2, self.parent.height / 2

            Image:
                id: label8
                source: '0.png'
                size_hint: None, None
                size: self.parent.width / 2, self.parent.height / 2

            Image:
                id: label9
                source: '0.png'
                size_hint: None, None
                size: self.parent.width / 2, self.parent.height / 2 
''')

class NoTitlePopup(Popup):
    pass

class RollingHand(Widget):
    angle = NumericProperty(0)
    hand_position = ObjectProperty((0, 0))
    animation = None
    duration = 10  # Initial duration in seconds
    timer_value = NumericProperty(duration)  # Initial timer value
    timer_text = StringProperty(str(duration))  # Displayed timer text
    cowrie_images = ['cowrie1.png', 'cowrie2.png']
    current_cowrie_index = 0
    random_number = NumericProperty(0)
    animation_started = False  # Track if animation has started

    def __init__(self, **kwargs):
        super(RollingHand, self).__init__(**kwargs)
        self.bind(angle=self.on_angle, timer_value=self.update_timer_text)
        self.update_timer_text(self, self.timer_value)

    def on_size(self, instance, value):
        # Called when the widget's size changes
        self.angle = 0  # Set initial angle to 0
        self.on_angle(self, self.angle)  # Manually trigger on_angle once



    def show_rashi_popup(self, rashi_name):
        # Extract the actual Rashi name without the prefix "Rashi: "
        actual_rashi_name = rashi_name.split(":")[1].strip()

        # Create a BoxLayout to contain both the image and the text
        box_layout = BoxLayout(orientation='vertical')

        # Add the label with the Rashi name
        rashi_label = Label(text=f"{rashi_name}", size_hint_y=None, height=50, font_name='CustomFont', font_size=50)
        box_layout.add_widget(rashi_label)

        # Add the corresponding image based on the actual Rashi name
        rashi_image = Image(source=f'{actual_rashi_name}.png')  # Assuming image names match Rashi names
        box_layout.add_widget(rashi_image)

        # Create the popup with the BoxLayout content
        popup = NoTitlePopup(content=box_layout, size_hint=(None, None), size=(400, 300), background_color=(0, 0, 0, 0))
        popup.open()


    def start_animation(self):
        if not self.animation_started:  # Allow start only if animation hasn't started
            self.animation_started = True

            for label_id in range(1, 9):
                label_name = f'label{label_id}'
                setattr(self.ids[label_name], 'source', '0.png')

            t = self.duration
            a = -360 * t
            self.angle = 0
            self.animation = Animation(angle=a, duration=t)
            self.animation.bind(on_complete=self.on_animation_complete)  # Bind on_complete event
            self.animation.start(self)

            # Start the countdown timer
            Clock.schedule_interval(self.update_timer, 0.1)

            # Schedule image update every 0.1 seconds
            Clock.schedule_interval(self.update_images, 0.1)

    def stop_animation(self):
        if self.animation_started:
            self.animation_started = False

            if self.animation:
                self.animation.stop(self)
                self.angle = 0
                random_number = random.randint(12, 35)
                self.random_number = random_number

                # Calculate the number of full groups (4) and the remainder
                full_groups = random_number // 4
                remainder = random_number % 4
                rashirem = random_number % 12



                # Stop the countdown timer
                Clock.unschedule(self.update_images)
                Clock.unschedule(self.update_timer)
                self.timer_value = self.duration  # Reset timer value on stop

        # Schedule a delay before updating images, number, and rashi
                Clock.schedule_once(lambda dt: self.update_information(full_groups, remainder, rashirem), 1)

    def update_information(self, full_groups, remainder, rashirem):
        # Divide the random number into groups of 4 and the remainder
        parts = [str(4) for _ in range(full_groups)]
        if remainder > 0:
            parts.append(str(remainder))

        # Fill the remaining slots to make a total of 9 slots
        while len(parts) < 9:
            parts.append(str(0))

        # Set the parts to the labels with a delay
        for i, part in enumerate(parts):
            Clock.schedule_once(lambda dt, i=i, part=part: self.update_image(i + 1, f'{part}.png'), i/2)

        # Update Rashi with a delay
        Clock.schedule_once(lambda dt: self.identify_rashi(rashirem))

        # Create the Rashi button
        self.create_rashi_button()

    def identify_rashi(self, rashirem):
        # Rashi identification
        if rashirem == 0:
            rashi = 'Meenam'
        elif rashirem == 1:
            rashi = 'Medam'
        elif rashirem == 2:
            rashi = 'Edavam'
        elif rashirem == 3:
            rashi = 'Mithunam'
        elif rashirem == 4:
            rashi = 'Karkidakam'
        elif rashirem == 5:
            rashi = 'Chingam'
        elif rashirem == 6:
            rashi = 'Kanni'
        elif rashirem == 7:
            rashi = 'Thulam'
        elif rashirem == 8:
            rashi = 'Vruschikam'
        elif rashirem == 9:
            rashi = 'Dhanu'
        elif rashirem == 10:
            rashi = 'Makaram'
        elif rashirem == 11:
            rashi = 'Kumbham'
        else:
            # Handle other cases if needed
            rashi = 'Unknown'
        self.ids.rashi.text = f'Rashi: {rashi}'\
        
    def create_rashi_button(self):
        if self.ids.show_rashi_button:  # Check if the button already exists
            self.ids.show_rashi_button.opacity = 1
        else:
            print("Warning: 'show_rashi_button' not found in ids, check the KV string.")


    @mainthread
    def update_image(self, label_id, source):
        # Update the source of the specified label with a delay
        label_name = f'label{label_id}'
        setattr(self.ids[label_name], 'source', source)

    def on_animation_complete(self, animation, widget):
        # Callback when animation is complete
        self.stop_animation()

    def update_timer(self, dt):
        # Update the countdown timer
        self.timer_value -= dt

        if self.timer_value <= 0:
            self.timer_value = 0
            self.stop_animation()

    def update_timer_text(self, instance, value):
        # Update the displayed timer text in mm:ss format
        minutes, seconds = divmod(int(self.timer_value), 60)
        self.timer_text = f"{minutes:02d}:{seconds:02d}"

    def update_images(self, dt):
        # Update the cowrie images interchangeably every second
        self.current_cowrie_index = (self.current_cowrie_index + 1) % len(self.cowrie_images)
        self.ids.cowrie1.source = self.cowrie_images[self.current_cowrie_index]

    def on_angle(self, instance, value):
        # Update hand position based on the oval path equation
        radius_x = self.width / 50
        radius_y = self.height / 45
        center_x = self.parent.width / 2.2
        center_y = self.parent.height / 15
        self.hand_position = (
            center_x + radius_x * cos(radians(value)),
            center_y + radius_y * sin(radians(value))
        )


class Cowrie(App):
    def build(self):
        # Calculate the window height based on the aspect ratio and a fixed width
        fixed_width = 800  # Set your desired width here
        window_height = fixed_width / ASPECT_RATIO

        # Set the window size
        Window.size = (fixed_width, window_height)

        # Return the root widget
        return RollingHand()

if __name__ == '__main__':
    Cowrie().run()
