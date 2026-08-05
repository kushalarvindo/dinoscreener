import re
with open('screensaver.py', 'r') as f:
    code = f.read()

# 1. Init signature
code = code.replace(
    'def __init__(self, accent_color="#8F96BF", enable_win_key=False, strict_exit=False, show_info=True, preview_mode=False, brightness=100, clock_style=1, clock_scale=0.45):',
    'def __init__(self, accent_color="#8F96BF", enable_win_key=False, strict_exit=False, show_info=True, preview_mode=False, brightness=100, clock_style=1, clock_scales=None, use_24hr=False, leading_zero=False):'
)
code = code.replace(
    'self.clock_scale = clock_scale ',
    'self.clock_scales = clock_scales if clock_scales else {"0": 0.45, "1": 0.45, "2": 0.45}'
)
code = code.replace(
    'self.clock_scale = clock_scale',
    'self.clock_scales = clock_scales if clock_scales else {"0": 0.45, "1": 0.45, "2": 0.45}'
)
code = code.replace(
    'self.preview_mode = preview_mode\n        self.brightness = brightness',
    'self.preview_mode = preview_mode\n        self.brightness = brightness\n        self.use_24hr = use_24hr\n        self.leading_zero = leading_zero'
)
# Add variables for clouds and ground
code = code.replace(
    'self.dino_obstacles = [] \n        self.dino_speed = 8.0',
    'self.dino_obstacles = []\n        self.dino_clouds = []\n        self.ground_x = 0.0\n        self.dino_speed = 8.0'
)
code = code.replace(
    'self.dino_obstacles = []\n        self.dino_speed = 8.0',
    'self.dino_obstacles = []\n        self.dino_clouds = []\n        self.ground_x = 0.0\n        self.dino_speed = 8.0'
)

# 2. Replace clock_scale references
code = code.replace('self.clock_scale', 'self.clock_scales[str(self.clock_style)]')

# 3. Update time formatting logic
code = code.replace(
    '''    def get_time_strings(self, time_obj):
        hour = time_obj.hour()
        minute = time_obj.minute()
        is_pm = hour >= 12
        hour_12 = hour % 12
        if hour_12 == 0: hour_12 = 12
        return str(hour_12), f"{minute:02d}", "PM" if is_pm else "AM"''',
    '''    def get_time_strings(self, time_obj):
        hour = time_obj.hour()
        minute = time_obj.minute()
        is_pm = hour >= 12
        if self.use_24hr:
            hour_str = f"{hour:02d}" if self.leading_zero else str(hour)
            return hour_str, f"{minute:02d}", ""
        else:
            hour_12 = hour % 12
            if hour_12 == 0: hour_12 = 12
            return str(hour_12), f"{minute:02d}", "PM" if is_pm else "AM"'''
)

code = code.replace(
    '''        hour = now.hour()
        hour_12 = hour % 12
        if hour_12 == 0: hour_12 = 12
        hour_str = f"{hour_12:02d}"''',
    '''        hour = now.hour()
        if self.use_24hr:
            hour_str = f"{hour:02d}" if self.leading_zero else str(hour)
        else:
            hour_12 = hour % 12
            if hour_12 == 0: hour_12 = 12
            hour_str = f"{hour_12:02d}"'''
)

code = code.replace(
    '''        now = QTime.currentTime()
        time_str = f"{now.hour():02d}:{now.minute():02d}"''',
    '''        now = QTime.currentTime()
        hour = now.hour()
        if self.use_24hr:
            hour_str = f"{hour:02d}" if self.leading_zero else str(hour)
        else:
            hour_12 = hour % 12
            if hour_12 == 0: hour_12 = 12
            hour_str = str(hour_12)
        time_str = f"{hour_str}:{now.minute():02d}"'''
)

with open('screensaver.py', 'w') as f:
    f.write(code)
