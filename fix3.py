import re
with open('screensaver.py', 'r') as f:
    code = f.read()

zoom_old = '''        elif event.key() == Qt.Key.Key_Equal or event.key() == Qt.Key.Key_Plus:
            self.clock_scale = min(0.95, self.clock_scale + 0.05)
            self.update()
        elif event.key() == Qt.Key.Key_Minus:
            self.clock_scale = max(0.15, self.clock_scale - 0.05)
            self.update()'''
            
zoom_new = '''        elif event.key() == Qt.Key.Key_Equal or event.key() == Qt.Key.Key_Plus:
            self.clock_scales[str(self.clock_style)] = min(0.95, self.clock_scales[str(self.clock_style)] + 0.05)
            self.update()
        elif event.key() == Qt.Key.Key_Minus:
            self.clock_scales[str(self.clock_style)] = max(0.15, self.clock_scales[str(self.clock_style)] - 0.05)
            self.update()'''

code = code.replace(zoom_old, zoom_new)

with open('screensaver.py', 'w') as f:
    f.write(code)
