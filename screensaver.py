import sys
import math
import ctypes
import json
import os
import random
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QColorDialog, QFormLayout, QSlider, QFileDialog, QStackedWidget, QFrame, QGridLayout, QComboBox, QFontComboBox
from PyQt6.QtCore import Qt, QTimer, QTime, QRectF, QDate, QPointF, QByteArray, QThread, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QRadialGradient, QPainterPath, QFontDatabase, QPixmap, QImage

SPRITE_B64 = 'iVBORw0KGgoAAAANSUhEUgAABNEAAABECAAAAACKI/xBAAAAAnRSTlMAAHaTzTgAAAoOSURBVHgB7J1bdqS4FkSDu7gPTYSh2AOATw1Pn6kBVA2FieiTrlesq6po8lgt0pj02b06E58HlRhXOCQBBcdxHMdxHOfDMeA7BfcIOI4VwISDKQhvK0O4H9iAobeFZSx8WIK0dqz4ztQRg1XdECNfX/CTGUDmNjJDP6MzuMnKKsQ0Y+Amyxnirurmx1KghAvWXoARAErEPUpAB/KzvK6YcAIl8lD2AtsCbENPS1XGwqMTSnvHhNOYgBV3mKlklKDqPUshMUIzsuzlOXFGW9AQS0C/lv/QMWrahOMoiKZL41HyUCRAdcKyDR0tVRkLD0+oV7Q7yLofm6w6rKbdrmNUL6NOyapMtGcUuixZ2WSHbsl+M97BoUX8TrpyrfGbJJ+saBQ0W9I6jnxF/ZO+4nqo66GQneo325keUjth7bFpX38MO6lbM+ZMaeOYETISzYzN9Wiy7shuyj4dI96JSQXuOMSlWcqkgQ2DSlVdUSIbWbVs2vJ41CvadDs0jTE63Y9NWO26r3x9MU3AzDGk1mQWZu2Bht6VaPzEXrl21gjyZRXNPnKFI8+TJnRKLEED24JNpaqqKBGx/C5oWLSlBR0+Pp4J5yM27YVydp8sX4p+SUGe661TuWE5Y78dtcDSX3u+oqWINjLmRm+wTsBUJWpK06pKaXZpJdbmhoH/LcByq6Rq+LMC+7Dl+OFjvzj2ObRJY/tOa1r/uUvDy9d9QaPz4utMP6ZDysxsPeScf3yly6bOfRbcemtPYESvpAn20GSS0efVKOGc4aNQgojj1ZnzvTEnkxqzOVfGllP3y9qnZ0S3pM2mK5jMwQcpiMb1ZVqdkBANl1aCFbBbdOR6Pvwgtjiu9vkx60jrXNpq15E8ywhz/2tbzGQQwQ4b59Zfe7aipVrSEhCP8mZG1UlzZ20tOgw9Hw6hrzCLZiyObqCkVauZFC0OPL8nqUrk/zHN1gopOfkzngH3fv8SQau20jtMQ09VUSmxQUS1OsZSDAWSwKNFq5SylzA6PhFf+Oo4x3m0pEuYKXb4s5WLAAaT1lwfc3Kr6CDZ6JD6hrUCWVhmjHFrzNk17pxWjdGl/Yi9AuBrBqAbusmvGNNCyWpbhvPU82j1aDMi9Q04p8aLaQtiw7plXZ0A7TwDSojO/GsCiAnE6qAGhg45/eAu7csrunGcEUpEN5NsXYDlUY6Mie67UGPTPiiO1xl0vgLYvXt83glmvkux7ke6WdGzz7mKmiSQM2ufmPEoQUv9d2fu3jEazGqc79JUQjRxghoZT9FoiJnjzvbYtDJGOXOcoxUt4hMybAucE3nloJPOSJh5v6cm8gwFWrnn72aj1txnvR+5RrzoXy8kBOAStWBtw/foGvd1NnyX+h2a+LXQUH2XKAFT0uLpi9byzXg2vrzy9Z6eAZmqIUnHoaJ9PlIofwaAYQMWu6XituAE6vWBgifhla/Xp3ClqjpFESRdt5Z+WCIkQ68vHNBAXysZH3CmuufhInRurCagvLk6QNXpbwMDNvouu+Vn/fLeVo3rA084PzAYiwDtzB1jIB3Jmvuc0YqzQRk6W0d8LhIQ9gPkNhSpEGjr2HKW4XyOuznthx/M+8V/W5+7/vRZ9yARQ4L5a18IIBetJbN18/oGYNjRHwyHt6qiJSj9R25zZ55M7Uiq6u3qglDF2KmBCqqTVqhNO0bQSp+gxRJkV9fi68uP/z8TzgYd3tyw9bQOqBUtpmdd9wwlGoGKGzDstMR7LR1EtENp582d1z5jL3yGrc79y83pSsbBZHquNluXZd5DfteKbbhaLc+Ongp1tUslUUvDve1drSPuSFoE2o/8AIL6rspChrbqZkkb0N5yhNa2E3B95Bm2vN+8m/me3lE9WaGp3LbPPDc/u9VZoJFbZ+uoCvaMhAJEDTS2xOO/Tdzp+Xs6C3mG7fXhnXlR4gnx4rXU7dma/FTl0YS29beOjztTx6NOUF2aVrNEe/bZa4m6+nmuEJUAbnFP15xH+/7fHU/FYG6LG+SmVL5bmnFZ/Ho0J4WP4NK4KMCtS7u0p/Bo9ngnXbfWXnVu/DcNdGf9rRgfeab6sWfR1KXZ1Z0kY7+l3rIToQCImiD2U9y4FepFaHm44jpJjDTGlOmfxVbGHMc92nkEW/PrrRSKJiqjF4CiHaqBNqEuLPxDLsGL/+xcvFavbLph6W89TdHCw5wZCW2zXggfe4Sqcc2oBhYYSAc+EY4zGhM5/teid0osBSaaBC3F/vPAjvpxsdDx5Dp1jjsnI7Y+95hT5z+erpZkzB/dpY2wJS0FPfLH0/wsj/AhJS0FJuTaWOPbHWFbN/9VdCUSwtPW5g81j2aMZULDkbtLE+GSBKOCdGiCURtVTXFpp7KCuEtzl3braVVFQ+g/8n6eQil/X24MmjAIe+oYJNqwK2M8uU5mXc8652rXOY6vdZ6NvdyoiXZ1jBqNcC7o0tKVaw2XlltdGs0VUwsYGTpbxwPO1JXcU7gTGLYfrx0tx6tjsW/PsjHd14p2l+YOzXGPdirBDAwdLe9sAf54IEh86zLA2qQj64SGYp9EM674Dk9Rqy4tY58B2MRqVRZOIr2t44FnymfRzlyJSOHBLg2rOzSnn5vxjI3O1hHXxyVNb8zqt2mNi6OrGzR9egPfH1QLREQgFSDs17Ky/zOoS+O7wVJNfN1axjh108L93G8dH3umelx7gGMTCuLbbfJEQZEYha6KGTbN9l2r+zNn2xkwLnzorNWqsLVP0eaGXMZ74pLWDNXLL0N7+GRnAmdqwgNqE4O7tQkREQmp+zMoudWlATcMaIRN28ErA5nv9pF/6PtEnak/1r8H53lRR6bcfuYe0DrCcZxL3vdk19PHBZQz73u6AT0ODZWGbTAY33Ud0nEcZ3hg64gmZjiO81YiCkK1dXytBauO/wwzsmxBqc3VIhP6DVNw5FhFywDS24/cKeHRCdLfoTiO3zMw58+uYUX/HYD2BLETinY4Z5Bk6+jaFo79DFm3LG4Q+pr6r97I5pH7pRsllgiQUEJ7QsSRCdN2aYfjuEczNDnollPLSKm/7EhQ6pgQ2yUKpx3OaQTZOra2gf7P0M/Q3+ScTJlLX6KgECb49h02lFLudPzVzn0lNQwEURQdrfGuc9anX34AIzk21c/xHjLYCo/JU2W1kLTm/7BeP7kkSZIkZbj0JhHZgDdAg5UeAA6f9f8Ar//eMZqUxs8ggs7BhAEarPQAsPm+hwFus4SnG6Mx3pI0xwEX/syoMMDteO0x17QlCd5m/CbX0STs9m3RDggXBLpKWv5S83eSF787y1Wd5apuCcXDHFu0HL1wPGbhz6lL2WL2VYrtE6NPZW7usXAEy1WZ5epGInCMMLhTBsCQ5erTyhXVlAASQROIjO0FvHBFh+evzparEMvVsp8XMGZ5HuHL3cZGzpu884kxZtN/1HLVynL1uiRJkvQFUg1OaKSaqSkAAAAASUVORK5CYII='
class CrispAestheticFlipClock(QWidget):
    def __init__(self, accent_color="#8F96BF", enable_win_key=False, strict_exit=False, show_info=True, preview_mode=False, brightness=100, clock_style=1, clock_scales=None, use_24hr=False, leading_zeros=None, config_path=None, full_config=None, ignore_media_keys=False, dino_font="Bungee", live_weather=False, pixel_shift=False, primary_font="", character_type="dino", custom_character_image=""):
        super().__init__()
        self.last_pos = None
        self.clock_scales = clock_scales if clock_scales else {"0": 0.45, "1": 0.45, "2": 0.45}
        self.config_path = config_path
        self.full_config = full_config if full_config else {}
        
        self.target_time = QTime.currentTime()
        self.old_time = self.target_time
        
        self.animating = False
        self.anim_progress = 0.0
        self.time_elapsed = 0.0 
        self.scale_callback = None
        
        # States
        self.show_bg = False
        self.bg_opacity = 1.0
        self.clock_style = clock_style
        
        # Dino Game State
        self.dino_active = False
        self.dino_y = 0.0 
        self.dino_vy = 0.0
        self.dino_frame = 0
        self.dino_obstacles = []
        self.dino_clouds = []
        self.ground_x = 0.0
        self.dino_speed = 8.0 
        self.dino_dead = False
        self.dino_timer_msec = 0
        self.dino_sound = False
        
        # --- CUSTOMIZATION ---
        self.rotary_accent = QColor(accent_color) 
        self.enable_win_key = enable_win_key
        self.strict_exit = strict_exit
        self.show_info = show_info
        self.preview_mode = preview_mode
        self.preview_mode = preview_mode
        self.brightness = brightness
        self.use_24hr = use_24hr
        if leading_zeros is None:
            self.leading_zeros = {"0": False, "1": False, "2": False}
        elif isinstance(leading_zeros, bool):
            self.leading_zeros = {"0": leading_zeros, "1": leading_zeros, "2": leading_zeros}
        else:
            self.leading_zeros = leading_zeros
        self.ignore_media_keys = ignore_media_keys
        self.dino_font = dino_font
        self.live_weather = live_weather
        self.pixel_shift = pixel_shift
        self.primary_font = primary_font
        self.primary_font_family = getattr(self, "primary_font_family", "Google Sans")
        
        self.character_type = character_type
        self.custom_character_image = custom_character_image
        self.custom_char_pixmap = QPixmap()
        if self.custom_character_image:
            import os
            if os.path.exists(self.custom_character_image):
                self.custom_char_pixmap.load(self.custom_character_image)
        
        if self.primary_font:
            import os
            if os.path.exists(self.primary_font):
                font_id = QFontDatabase.addApplicationFont(self.primary_font)
                if font_id != -1:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    if families:
                        self.primary_font_family = families[0]
                        
        self.weather_temp = 72
        self.weather_code = 0  # 0 is clear sky
        self.weather_loaded = False
        
        if getattr(self, "live_weather", False):
            self.weather_thread = WeatherWorker()
            self.weather_thread.weather_updated.connect(self.on_weather_updated)
            self.weather_thread.start()

        
        self.sprite_pixmap = QPixmap()
        try:
            ba = QByteArray.fromBase64(SPRITE_B64.encode('utf-8'))
            self.sprite_pixmap.loadFromData(ba)
            image = self.sprite_pixmap.toImage()
            image.invertPixels(QImage.InvertMode.InvertRgb)
            self.sprite_pixmap = QPixmap.fromImage(image)
        except Exception as e:
            print("Sprite load failed", e)
            
        self.initUI()
        
    def set_accent_color(self, hex_col):
        self.rotary_accent = QColor(hex_col)
        self.update()
        
    def set_show_info(self, show):
        self.show_info = show
        self.update()
        
    def set_brightness(self, val):
        self.brightness = val
        self.update()
        
    def set_custom_character(self, path):
        self.custom_character_image = path
        if path:
            import os
            if os.path.exists(path):
                self.custom_char_pixmap.load(path)
            else:
                self.custom_char_pixmap = QPixmap()
        else:
            self.custom_char_pixmap = QPixmap()
        self.update()
        
    def on_weather_updated(self, data):
        self.weather_temp = data.get("temp", 0)
        self.weather_code = data.get("code", 0)
        self.weather_loaded = True
        self.update()

    def initUI(self):
        if not self.preview_mode:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
            self.showFullScreen()
            self.setCursor(Qt.CursorShape.BlankCursor)
            self.setMouseTracking(True)
        
        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.checkTime)
        self.sync_timer.start(200)

        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.updateAnimation)
        self.anim_timer.start(16)


    def save_live_config(self):
        if not self.preview_mode and self.config_path and self.full_config is not None:
            self.full_config["clock_scales"] = self.clock_scales
            self.full_config["clock_style"] = self.clock_style
            import json, os
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            try:
                with open(self.config_path, 'w') as f:
                    json.dump(self.full_config, f)
            except Exception:
                pass
    def checkTime(self):
        now = QTime.currentTime()
        if now.minute() != self.target_time.minute():
            self.old_time = self.target_time
            self.target_time = QTime(now.hour(), now.minute())
            self.animating = True
            self.anim_progress = 0.0

    def updateAnimation(self):
        if self.show_bg and self.bg_opacity < 1.0:
            self.bg_opacity = min(1.0, self.bg_opacity + 0.04)
        elif not self.show_bg and self.bg_opacity > 0.0:
            self.bg_opacity = max(0.0, self.bg_opacity - 0.04)
            
        self.time_elapsed += 0.016 
        
        # Dino Game Loop
        if self.clock_style == 2:
            self.dino_timer_msec += 16
            
            if not self.dino_dead:
                # Physics
                self.dino_y += self.dino_vy
                if self.dino_y > 0:
                    self.dino_vy -= 0.6 # gravity
                else:
                    self.dino_y = 0
                    self.dino_vy = 0
                
                # Obstacle Generation
                # Ground scroll
                self.ground_x -= self.dino_speed
                if self.ground_x <= -1200:
                    self.ground_x += 1200

                # Clouds
                if len(self.dino_clouds) < 3:
                    if random.random() < 0.01:
                        self.dino_clouds.append({'x': self.width() + 100, 'y': random.randint(int(self.height()*0.5), int(self.height()*0.75)), 'speed': self.dino_speed * 0.2})
                for c in self.dino_clouds:
                    c['x'] -= c['speed']
                self.dino_clouds = [c for c in self.dino_clouds if c['x'] > -100]

                if len(self.dino_obstacles) == 0:
                    self.dino_obstacles.append({'x': self.width() + 200, 'w': 25, 'h': 50, 'type': 'large1'})
                else:
                    last_obs = self.dino_obstacles[-1]
                    if self.width() - last_obs['x'] > 400 + random.randint(0, 400):
                        obs_type = random.randint(0, 8)
                        if obs_type == 0:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 17, 'h': 35, 'type': 'small1'})
                        elif obs_type == 1:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 34, 'h': 35, 'type': 'small2'})
                        elif obs_type == 2:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 51, 'h': 35, 'type': 'small3'})
                        elif obs_type == 3:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 25, 'h': 50, 'type': 'large1'})
                        elif obs_type == 4:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 50, 'h': 50, 'type': 'large2'})
                        elif obs_type == 5:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 75, 'h': 50, 'type': 'large3'})
                        elif obs_type == 6:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 46, 'h': 40, 'type': 'crow', 'y_off': 20})
                        elif obs_type == 7:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 46, 'h': 40, 'type': 'crow', 'y_off': 50})
                        elif obs_type == 8:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 46, 'h': 40, 'type': 'crow', 'y_off': 80})
                
                for obs in self.dino_obstacles:
                    obs['x'] -= self.dino_speed
                
                self.dino_obstacles = [o for o in self.dino_obstacles if o['x'] > -100]
                
                # Auto-play AI
                dino_x = self.width() * 0.2
                dino_w = 40
                
                next_obs = None
                for obs in self.dino_obstacles:
                    if obs['x'] + obs['w'] > dino_x:
                        next_obs = obs
                        break
                        
                if next_obs:
                    dist = next_obs['x'] - (dino_x + dino_w)
                    if dist < 120 and self.dino_y == 0:
                        if next_obs.get('type') == 'crow' and next_obs.get('y_off', 0) >= 47:
                            pass # run under it
                        else:
                            self.dino_vy = 12.0
                                
            self.dino_frame = (self.dino_frame + 1) % 20
        
        if self.animating:
            self.anim_progress += 0.035 
            if self.anim_progress >= 1.0:
                self.anim_progress = 1.0
                self.animating = False
                self.old_time = self.target_time
        self.update() 

    def get_time_strings(self, time_obj):
        hour = time_obj.hour()
        minute = time_obj.minute()
        is_pm = hour >= 12
        lz = self.leading_zeros.get(str(self.clock_style), False)
        if self.use_24hr:
            hour_str = f"{hour:02d}" if lz else str(hour)
            return hour_str, f"{minute:02d}", ""
        else:
            hour_12 = hour % 12
            if hour_12 == 0: hour_12 = 12
            hour_str = f"{hour_12:02d}" if lz else str(hour_12)
            return hour_str, f"{minute:02d}", "PM" if is_pm else "AM"

    # ==========================================
    # DESIGN 1: FLIPCLOCK
    # ==========================================
    def draw_card_base(self, painter, x, y, w, h, text, ampm):
        rect = QRectF(x, y, w, h)
        radius = h * 0.06 

        painter.setBrush(QColor(16, 20, 26, 180)) 
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        border_pen = QPen(QColor(255, 255, 255, 20), 1.0) 
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)

        painter.setPen(QColor(250, 250, 250, 255))
        font = QFont()
        font.setFamilies(["Google Sans", "Product Sans", "Segoe UI", "Arial"]) 
        font.setPixelSize(int(h * 0.65)) 
        font.setWeight(QFont.Weight.Black) 
        font.setStretch(90) 
        painter.setFont(font)
        
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

        if ampm:
            font_ampm = QFont()
            font_ampm.setFamilies(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
            font_ampm.setPixelSize(int(h * 0.09))
            font_ampm.setWeight(QFont.Weight.Bold)
            painter.setFont(font_ampm)
            
            padding_x = w * 0.08
            padding_y = h * 0.06
            ampm_rect = QRectF(x + padding_x, y + h - (h*0.15) - padding_y, w, h*0.15)
            painter.drawText(ampm_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom, ampm)

    def draw_half_card(self, painter, x, y, w, h, text, ampm, is_top):
        painter.save()
        if is_top:
            painter.setClipRect(QRectF(x, y, w, h / 2))
        else:
            painter.setClipRect(QRectF(x, y + h / 2, w, h / 2))
        self.draw_card_base(painter, x, y, w, h, text, ampm)
        painter.restore()

    def drawMechanicalSplit(self, painter, x, y, w, h):
        split_thickness = max(4.0, h * 0.015)
        painter.setBrush(QColor(0, 0, 0, 255)) 
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(QRectF(x, y + (h / 2) - (split_thickness / 2), w, split_thickness))

    def drawStaticCard(self, painter, x, y, w, h, text, ampm):
        self.draw_half_card(painter, x, y, w, h, text, ampm, is_top=True)
        self.draw_half_card(painter, x, y, w, h, text, ampm, is_top=False)
        self.drawMechanicalSplit(painter, x, y, w, h)

    def drawFlippingCard(self, painter, x, y, w, h, old_text, new_text, ampm):
        center_y = y + h / 2
        self.draw_half_card(painter, x, y, w, h, new_text, ampm, is_top=True)
        self.draw_half_card(painter, x, y, w, h, old_text, ampm, is_top=False)

        painter.save()
        painter.translate(x + w / 2, center_y)

        if self.anim_progress < 0.5:
            p = self.anim_progress * 2.0
            scale_y = max(0.001, 1.0 - p) 
            painter.scale(1.0, scale_y)
            painter.translate(-(x + w / 2), -center_y)
            self.draw_half_card(painter, x, y, w, h, old_text, ampm, is_top=True)
            painter.setClipRect(QRectF(x, y, w, h / 2))
            painter.fillRect(QRectF(x, y, w, h / 2), QColor(0, 0, 0, int(180 * p)))
        else:
            p = (self.anim_progress - 0.5) * 2.0
            scale_y = max(0.001, p)
            painter.scale(1.0, scale_y)
            painter.translate(-(x + w / 2), -center_y)
            self.draw_half_card(painter, x, y, w, h, new_text, ampm, is_top=False)
            painter.setClipRect(QRectF(x, center_y, w, h / 2))
            painter.fillRect(QRectF(x, center_y, w, h / 2), QColor(0, 0, 0, int(180 * (1.0 - p))))

        painter.restore()
        self.drawMechanicalSplit(painter, x, y, w, h)

    def draw_flipclock_style(self, painter, w, h):
        card_h = int(h * self.clock_scales[str(self.clock_style)])
        card_w = int(card_h * 0.85) 
        spacing = int(card_w * 0.08) 
        
        center_x = w // 2
        center_y = h // 2
        half_spacing = spacing // 2
        
        hour_x = int(center_x - half_spacing - card_w)
        minute_x = int(center_x + half_spacing)
        card_y = int(center_y - (card_h // 2))

        old_h_str, old_m_str, old_ampm = self.get_time_strings(self.old_time)
        new_h_str, new_m_str, new_ampm = self.get_time_strings(self.target_time)

        if self.animating and old_h_str != new_h_str:
            self.drawFlippingCard(painter, hour_x, card_y, card_w, card_h, old_h_str, new_h_str, new_ampm)
        else:
            self.drawStaticCard(painter, hour_x, card_y, card_w, card_h, new_h_str, new_ampm)

        if self.animating:
            self.drawFlippingCard(painter, minute_x, card_y, card_w, card_h, old_m_str, new_m_str, "")
        else:
            self.drawStaticCard(painter, minute_x, card_y, card_w, card_h, new_m_str, "")

    # ==========================================
    # DESIGN 2: MODERN PIXEL ROTARY (DUAL RING)
    # ==========================================
    def draw_rotary_style(self, painter, w, h):
        now = QTime.currentTime()
        msec = now.msec()
        
        sec_val = now.second() + msec / 1000.0
        min_val = now.minute() + sec_val / 60.0
        
        hour = now.hour()
        lz = self.leading_zeros.get(str(self.clock_style), False)
        if self.use_24hr:
            hour_str = f"{hour:02d}" if lz else str(hour)
        else:
            hour_12 = hour % 12
            if hour_12 == 0: hour_12 = 12
            hour_str = f"{hour_12:02d}" if lz else str(hour_12)

        cx = float(w) * 0.10 
        cy = float(h) * 0.5
        R_min = float(w) * 0.22 
        R_sec = float(w) * 0.32 
        
        accent_color = self.rotary_accent
        pure_white = QColor(255, 255, 255)
        off_white = QColor("#F5F4EE")
        muted_grey = QColor(145, 150, 155) 

        # --- MINUTE WHEEL ---
        def draw_minute_wheel(radius, val_float, font_size):
            font = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
            font.setPixelSize(int(font_size))
            font.setWeight(QFont.Weight.Medium)
            
            tick_offset = w * 0.045 
            
            for i in range(60):
                angle_deg = (val_float - i) * 6.0
                norm_angle = (angle_deg + 180) % 360 - 180
                dist = abs(norm_angle)
                
                opacity = max(0.0, 1.0 - dist / 75.0) 
                if opacity <= 0.01: continue
                
                if dist < 8.0:
                    text_opacity = 0.0
                elif dist < 18.0:
                    text_opacity = (dist - 8.0) / 10.0 
                else:
                    text_opacity = max(0.0, 1.0 - (dist - 18.0) / 67.0)
                
                painter.save()
                painter.translate(cx, cy)
                painter.rotate(angle_deg)
                
                if i % 5 == 0 and text_opacity > 0.01:
                    painter.save()
                    painter.translate(radius, 0)
                    painter.rotate(-angle_deg) 
                    
                    color = QColor(muted_grey)
                    color.setAlpha(int(255 * text_opacity))
                    painter.setPen(color)
                    painter.setFont(font)
                    
                    box_size = w * 0.1
                    text_rect = QRectF(-box_size/2, -box_size/2, box_size, box_size)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, f"{i:02d}")
                    painter.restore()

                painter.translate(radius + tick_offset, 0)
                tick_color = QColor(120, 125, 130)
                
                if i % 5 == 0:
                    tick_color.setAlpha(int(200 * opacity))
                    painter.setPen(QPen(tick_color, 2.5)) 
                    tick_len = w * 0.005 
                else:
                    tick_color.setAlpha(int(150 * opacity))
                    painter.setPen(QPen(tick_color, 1.5)) 
                    tick_len = w * 0.002
                    
                painter.drawLine(int(-tick_len), 0, int(tick_len), 0)
                painter.restore()

        # --- SECOND WHEEL (Perfect Unified Single-Track) ---
        def draw_second_wheel(radius, val_float, font_size):
            font = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
            font.setPixelSize(int(font_size))
            font.setWeight(QFont.Weight.Medium)
            
            tick_offset = w * 0.022 
            
            for i in range(60):
                angle_deg = (val_float - i) * 6.0
                norm_angle = (angle_deg + 180) % 360 - 180
                
                opacity = max(0.0, 1.0 - abs(norm_angle) / 75.0) 
                if opacity <= 0.01: continue
                
                painter.save()
                painter.translate(cx, cy)
                painter.rotate(angle_deg)
                
                if i % 5 == 0:
                    painter.save()
                    painter.translate(radius, 0)
                    painter.rotate(-angle_deg) 
                    
                    # Blue accent text matching the image design
                    color = QColor(accent_color)
                    color.setAlpha(int(255 * opacity))
                    painter.setPen(color)
                    painter.setFont(font)
                    
                    box_size = w * 0.1
                    text_rect = QRectF(-box_size/2, -box_size/2, box_size, box_size)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, f"{i:02d}")
                    painter.restore()

                painter.translate(radius + tick_offset, 0)
                tick_color = QColor(120, 125, 130)
                
                if i % 5 == 0:
                    tick_color.setAlpha(int(200 * opacity))
                    painter.setPen(QPen(tick_color, 2.5)) 
                    tick_len = w * 0.005 
                else:
                    tick_color.setAlpha(int(150 * opacity))
                    painter.setPen(QPen(tick_color, 1.5)) 
                    tick_len = w * 0.002
                    
                painter.drawLine(int(-tick_len), 0, int(tick_len), 0)
                painter.restore()

        # 1. Draw flush rings 
        draw_minute_wheel(R_min, min_val, h * 0.050) 
        draw_second_wheel(R_sec, sec_val, h * 0.035) 

        # 2. The Pill Enclosure
        pill_h = h * 0.14
        pill_left = cx + R_min - w * 0.055 
        pill_right = cx + R_sec + w * 0.045
        pill_rect = QRectF(pill_left, cy - pill_h/2, pill_right - pill_left, pill_h)

        painter.setPen(QPen(QColor(accent_color.red(), accent_color.green(), accent_color.blue(), 220), 2.5)) 
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(pill_rect, pill_h/2, pill_h/2)

        # 3. Fixed Exact Minute inside Pill overlay
        font_min_fixed = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
        font_min_fixed.setPixelSize(int(h * 0.070))
        font_min_fixed.setWeight(QFont.Weight.Bold)
        
        painter.setFont(font_min_fixed)
        painter.setPen(pure_white)
        min_rect = QRectF(cx + R_min - w*0.05, cy - h*0.05, w*0.1, h*0.1)
        painter.drawText(min_rect, Qt.AlignmentFlag.AlignCenter, f"{now.minute():02d}")

        # 4. Hard-Anchored Left Hour
        font_hr = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
        font_hr.setPixelSize(int(h * 0.28))
        painter.setFont(font_hr)
        painter.setPen(off_white)
        
        hr_rect = QRectF(cx - w * 0.15, cy - h * 0.25, w * 0.30, h * 0.50)
        painter.drawText(hr_rect, Qt.AlignmentFlag.AlignCenter, hour_str)

        # 5. Right Side Date, Weather & Battery Display
        date_now = QDate.currentDate()
        date_str_1 = date_now.toString("dd MMM yyyy").upper()
        date_str_2 = date_now.toString("dddd").upper()
        
        box_w = w * 0.3
        date_x = pill_right + w * 0.10
        center_x = date_x + box_w / 2
        
        if self.show_info:
            offset_y = cy - h * 0.02
        else:
            offset_y = cy + h * 0.015
        
        # Draw Center Aligned Date Text
        font_date_1 = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
        font_date_1.setPixelSize(int(h * 0.022))
        font_date_1.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 4.0)
        
        font_date_2 = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
        font_date_2.setPixelSize(int(h * 0.038))
        font_date_2.setWeight(QFont.Weight.Bold)
        font_date_2.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 3.0)
        
        painter.setFont(font_date_1)
        painter.setPen(accent_color)
        painter.drawText(QRectF(date_x, offset_y - h * 0.10, box_w, h * 0.08), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom, date_str_1)
        
        painter.setFont(font_date_2)
        painter.setPen(pure_white)
        painter.drawText(QRectF(date_x, offset_y - h * 0.01, box_w, h * 0.08), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, date_str_2)
        
        if self.show_info:
            # Unified Weather & Battery Display
            info_y = offset_y + h * 0.05 # Reduced spacing (closer to date)
            info_h = h * 0.04
            
            # Center dot
            font_info = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
            font_info.setPixelSize(int(h * 0.016))
            font_info.setWeight(QFont.Weight.Medium)
            font_info.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.0)
            painter.setFont(font_info)
            painter.setPen(QColor(120, 125, 130))
            painter.drawText(QRectF(center_x - w*0.01, info_y, w*0.02, info_h), Qt.AlignmentFlag.AlignCenter, "\u2022")
            
            # Weather
            weather_text = f"{getattr(self, 'weather_temp', 26)}\u00B0C" if getattr(self, "live_weather", False) else "26\u00B0C"
            fm = painter.fontMetrics()
            w_text_width = fm.horizontalAdvance(weather_text)
            
            weather_end = center_x - w * 0.02 # Pushed out a bit
            weather_text_x = weather_end - w_text_width
            
            # Dynamic Weather Icon
            emoji_w = w * 0.012
            weather_icon_x = weather_text_x - emoji_w - w * 0.003
            
            painter.save()
            painter.translate(weather_icon_x + emoji_w/2, info_y + info_h/2)
            w_icon_size = h * 0.016
            painter.setPen(Qt.PenStyle.NoPen)
            
            code = getattr(self, 'weather_code', 0) if getattr(self, "live_weather", False) else 0
            
            # WMO Code Mapping
            if code in [0, 1]: # Clear / Mostly Clear
                painter.setBrush(QColor(255, 210, 80)) # Sun
                painter.drawEllipse(QRectF(-w_icon_size*0.4, -w_icon_size*0.4, w_icon_size*0.8, w_icon_size*0.8))
            elif code in [2, 3, 45, 48]: # Cloudy / Fog
                painter.setBrush(QColor(180, 190, 200)) # Cloud
                painter.drawEllipse(QRectF(-w_icon_size*0.4, -w_icon_size*0.2, w_icon_size*0.8, w_icon_size*0.5))
                painter.drawEllipse(QRectF(-w_icon_size*0.2, -w_icon_size*0.4, w_icon_size*0.5, w_icon_size*0.5))
            elif 50 <= code <= 67 or 80 <= code <= 82: # Rain
                painter.setBrush(QColor(100, 150, 255)) # Raindrop
                path = QPainterPath()
                path.moveTo(0, -w_icon_size*0.4)
                path.lineTo(-w_icon_size*0.3, w_icon_size*0.1)
                path.arcTo(QRectF(-w_icon_size*0.3, -w_icon_size*0.2, w_icon_size*0.6, w_icon_size*0.6), 180, 180)
                path.closeSubpath()
                painter.drawPath(path)
            elif 70 <= code <= 77 or 85 <= code <= 86: # Snow
                painter.setPen(QPen(QColor(255, 255, 255), 2))
                painter.drawLine(int(-w_icon_size*0.3), 0, int(w_icon_size*0.3), 0)
                painter.drawLine(0, int(-w_icon_size*0.3), 0, int(w_icon_size*0.3))
                painter.drawLine(int(-w_icon_size*0.2), int(-w_icon_size*0.2), int(w_icon_size*0.2), int(w_icon_size*0.2))
                painter.drawLine(int(-w_icon_size*0.2), int(w_icon_size*0.2), int(w_icon_size*0.2), int(-w_icon_size*0.2))
            elif 95 <= code <= 99: # Thunder
                painter.setBrush(QColor(200, 100, 255))
                path = QPainterPath()
                path.moveTo(0, -w_icon_size*0.4)
                path.lineTo(-w_icon_size*0.3, w_icon_size*0.1)
                path.lineTo(0, 0)
                path.lineTo(0, w_icon_size*0.4)
                path.lineTo(w_icon_size*0.3, -w_icon_size*0.1)
                path.lineTo(0, 0)
                path.closeSubpath()
                painter.drawPath(path)
            else:
                # Default Sun
                painter.setBrush(QColor(255, 210, 80))
                painter.drawEllipse(QRectF(-w_icon_size*0.4, -w_icon_size*0.4, w_icon_size*0.8, w_icon_size*0.8))
                
            painter.restore()
            
            # Weather Temp
            painter.setFont(font_info)
            painter.setPen(QColor(230, 235, 240)) # Crisp almost white
            painter.drawText(QRectF(weather_text_x, info_y, w_text_width, info_h), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, weather_text)
            
            # Battery
            bat_text = "100%"
            bat_val = 100
            is_charging = False
            try:
                class SYSTEM_POWER_STATUS(ctypes.Structure):
                    _fields_ = [
                        ('ACLineStatus', ctypes.c_byte),
                        ('BatteryFlag', ctypes.c_byte),
                        ('BatteryLifePercent', ctypes.c_byte),
                        ('SystemStatusFlag', ctypes.c_byte),
                        ('BatteryLifeTime', ctypes.c_ulong),
                        ('BatteryFullLifeTime', ctypes.c_ulong),
                    ]
                sys_pwr = SYSTEM_POWER_STATUS()
                ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(sys_pwr))
                if sys_pwr.BatteryLifePercent == 255:
                    bat_text = "PWR"
                else:
                    bat_text = f"{sys_pwr.BatteryLifePercent}%"
                    bat_val = sys_pwr.BatteryLifePercent
                    if sys_pwr.ACLineStatus == 1:
                        is_charging = True
            except Exception:
                pass
                
            bat_start = center_x + w * 0.02
            bat_icon_w = w * 0.019
            bat_icon_h = h * 0.015
            bat_icon_x = bat_start
            bat_text_x = bat_icon_x + bat_icon_w + w * 0.005
            bat_icon_y = info_y + info_h/2 - bat_icon_h/2
            
            # Professional Battery Shell (White, solid border)
            painter.setPen(QPen(QColor(255, 255, 255), 1.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(QRectF(bat_icon_x, bat_icon_y, bat_icon_w, bat_icon_h), 2, 2)
            # Battery Cap
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawRoundedRect(QRectF(bat_icon_x + bat_icon_w + 1.5, bat_icon_y + bat_icon_h*0.3, w*0.0015, bat_icon_h*0.4), 1, 1)
            
            # Battery Fill
            fill_margin = 2.5
            fill_w = (bat_icon_w - fill_margin * 2) * (bat_val / 100.0)
            fill_h = bat_icon_h - fill_margin * 2
            if bat_val <= 20:
                painter.setBrush(QColor(255, 80, 80)) # Red alert
            else:
                painter.setBrush(QColor(160, 230, 160)) # Professional light green
            if fill_w > 0:
                painter.drawRoundedRect(QRectF(bat_icon_x + fill_margin, bat_icon_y + fill_margin, fill_w, fill_h), 1, 1)
            
            if is_charging:
                painter.save()
                painter.translate(bat_icon_x + bat_icon_w/2, bat_icon_y + bat_icon_h/2)
                bolt = QPainterPath()
                bw = bat_icon_w * 0.15
                bh = bat_icon_h * 0.35
                bolt.moveTo(bw*0.3, -bh)
                bolt.lineTo(-bw*0.8, 0)
                bolt.lineTo(0, 0)
                bolt.lineTo(-bw*0.3, bh)
                bolt.lineTo(bw*0.8, 0)
                bolt.lineTo(0, 0)
                bolt.closeSubpath()
                painter.setBrush(QColor(255, 255, 255)) # Pure white bolt
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawPath(bolt)
                painter.restore()
                
            painter.setFont(font_info)
            painter.setPen(QColor(230, 235, 240))
            # Align text exactly with the battery icon height
            painter.drawText(QRectF(bat_text_x, bat_icon_y, w*0.1, bat_icon_h), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, bat_text)

    # ==========================================
    # DESIGN 3: DINO GAME CLOCK
    # ==========================================
    def draw_dino_style(self, painter, w, h):
        now = QTime.currentTime()
        hour = now.hour()
        lz = self.leading_zeros.get(str(self.clock_style), False)
        if self.use_24hr:
            hour_str = f"{hour:02d}" if lz else str(hour)
        else:
            hour_12 = hour % 12
            if hour_12 == 0: hour_12 = 12
            hour_str = f"{hour_12:02d}" if lz else str(hour_12)
        time_str = f"{hour_str}:{now.minute():02d}"
        
        base_size = int(h * 0.18)
        scaled_size = int(base_size * (self.clock_scales[str(self.clock_style)] / 0.45))
        font_time = QFont([self.dino_font, "Bungee", "Arial Black"])
        font_time.setPixelSize(scaled_size)
        font_time.setWeight(QFont.Weight.Bold)
        
        painter.setFont(font_time)
        painter.setPen(QColor(255, 255, 255))
        time_rect = QRectF(0, h * 0.05, w, scaled_size * 1.2)
        painter.drawText(time_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, time_str)
        
        base_date = int(h * 0.025)
        scaled_date = int(base_date * (self.clock_scales[str(self.clock_style)] / 0.45))
        date_str = QDate.currentDate().toString("dddd, d MMMM")
        font_date = QFont(["Google Sans", "Product Sans", "Segoe UI"])
        font_date.setPixelSize(scaled_date)
        font_date.setWeight(QFont.Weight.Medium)
        
        painter.setFont(font_date)
        date_y = h * 0.05 + scaled_size * 1.30
        date_rect = QRectF(0, date_y, w, scaled_date * 2)
        painter.drawText(date_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, date_str)
        
        if self.dino_sound:
            painter.setPen(QColor(100, 100, 100))
            painter.setFont(QFont("Segoe UI", 12))
            painter.drawText(QRectF(w - 100, 20, 80, 30), Qt.AlignmentFlag.AlignRight, "Sound: ON")
            
        ground_y = h * 0.95
        
        dino_x = w * 0.2
        dino_w = 44
        dino_h = 47
        
        if not self.sprite_pixmap.isNull():
            # Draw ground
            ground_rect = QRectF(2, 54, 1200, 12)
            gx = self.ground_x
            while gx < w:
                painter.drawPixmap(QRectF(gx, ground_y - 10, 1200, 12), self.sprite_pixmap, ground_rect)
                gx += 1200
                
            # Draw clouds
            cloud_rect = QRectF(86, 2, 46, 14)
            for c in self.dino_clouds:
                painter.drawPixmap(QRectF(c['x'], c['y'], 46, 14), self.sprite_pixmap, cloud_rect)
                
            dino_w = 44
            dino_h = 47
            if getattr(self, "character_type", "dino") == "custom" and getattr(self, "custom_char_pixmap", None) and not self.custom_char_pixmap.isNull():
                orig_w = self.custom_char_pixmap.width()
                orig_h = self.custom_char_pixmap.height()
                target_h = 47
                target_w = max(20, min(65, int(orig_w * (target_h / orig_h)))) if orig_h > 0 else 44
                char_x = dino_x + (dino_w - target_w) / 2
                target_rect = QRectF(char_x, ground_y - self.dino_y - target_h, target_w, target_h)
                painter.drawPixmap(target_rect, self.custom_char_pixmap, QRectF(self.custom_char_pixmap.rect()))
            else:
                if self.dino_y > 0:
                    dino_rect = QRectF(848, 2, 44, 47) 
                else:
                    if self.dino_frame < 10:
                        dino_rect = QRectF(936, 2, 44, 47) 
                    else:
                        dino_rect = QRectF(980, 2, 44, 47)
                        
                target_rect = QRectF(dino_x, ground_y - self.dino_y - dino_h, dino_w, dino_h)
                painter.drawPixmap(target_rect, self.sprite_pixmap, dino_rect)
            
            for obs in self.dino_obstacles:
                t = obs.get('type', 'large1')
                if t == 'crow':
                    if (self.dino_frame // 10) % 2 == 0:
                        obs_rect = QRectF(134, 2, 46, 40)
                    else:
                        obs_rect = QRectF(180, 2, 46, 40)
                    obs_target = QRectF(obs['x'], ground_y - obs.get('y_off', 0) - obs['h'], obs['w'], obs['h'])
                else:
                    if t == 'small1': obs_rect = QRectF(228, 2, 17, 35)
                    elif t == 'small2': obs_rect = QRectF(228, 2, 34, 35)
                    elif t == 'small3': obs_rect = QRectF(228, 2, 51, 35)
                    elif t == 'large1': obs_rect = QRectF(332, 2, 25, 50)
                    elif t == 'large2': obs_rect = QRectF(332, 2, 50, 50)
                    elif t == 'large3': obs_rect = QRectF(332, 2, 75, 50)
                    else: obs_rect = QRectF(332, 2, 25, 50)
                    obs_target = QRectF(obs['x'], ground_y - obs['h'], obs['w'], obs['h'])
                
                painter.drawPixmap(obs_target, self.sprite_pixmap, obs_rect)
            
        if self.dino_dead:
            font_dead = QFont(["Google Sans", "Segoe UI"])
            font_dead.setPixelSize(24)
            font_dead.setWeight(QFont.Weight.Bold)
            painter.setFont(font_dead)
            painter.setPen(QColor(255, 50, 50))
            painter.drawText(QRectF(0, ground_y - 150, w, 50), Qt.AlignmentFlag.AlignHCenter, "G A M E   O V E R")
            font_dead.setPixelSize(16)
            painter.setPen(QColor(150, 150, 150))
            painter.drawText(QRectF(0, ground_y - 100, w, 50), Qt.AlignmentFlag.AlignHCenter, "Press SPACE to restart")

    # ==========================================
    # AMBIENT ORBS & MAIN PAINT EVENT
    # ==========================================
    def draw_ambient_orb(self, painter, w, h, duration, start_x, start_y, start_size, end_x, end_y, end_size, color):
        if self.bg_opacity <= 0.0:
            return 
            
        phase = (math.sin(self.time_elapsed * (math.pi / duration) - (math.pi / 2)) + 1) / 2.0
        current_x = start_x + (end_x - start_x) * phase
        current_y = start_y + (end_y - start_y) * phase
        current_size = start_size + (end_size - start_size) * phase
        
        current_alpha = int(color.alpha() * self.bg_opacity)
        
        grad = QRadialGradient(current_x, current_y, current_size / 2)
        grad.setColorAt(0.0, QColor(color.red(), color.green(), color.blue(), current_alpha))
        grad.setColorAt(1.0, QColor(color.red(), color.green(), color.blue(), 0))
        
        painter.setBrush(grad)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(QRectF(current_x - current_size/2, current_y - current_size/2, current_size, current_size))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing) 
        
        w = self.width()
        h = self.height()
        
        painter.fillRect(self.rect(), QColor(0, 0, 0))
        
        self.draw_ambient_orb(
            painter, w, h, duration=12.0,
            start_x=0.45*w, start_y=0.25*h + 0.15*w, start_size=0.30*w,
            end_x=0.70*w, end_y=-0.10*h + 0.40*w, end_size=0.80*w,
            color=QColor(12, 119, 255, 76) 
        )
        self.draw_ambient_orb(
            painter, w, h, duration=11.5,
            start_x=0.55*w, start_y=0.30*h + 0.10*w, start_size=0.20*w,
            end_x=0.40*w, end_y=-0.10*h + 0.40*w, end_size=0.80*w,
            color=QColor(0, 56, 255, 76) 
        )
        self.draw_ambient_orb(
            painter, w, h, duration=15.0,
            start_x=0.45*w, start_y=0.30*h + 0.10*w, start_size=0.20*w,
            end_x=0.40*w, end_y=-0.50*h + 0.60*w, end_size=1.20*w,
            color=QColor(65, 56, 210, 127) 
        )
        
        if self.clock_style == 0:
            self.draw_flipclock_style(painter, w, h)
        elif self.clock_style == 1:
            self.draw_rotary_style(painter, w, h)
        else:
            self.draw_dino_style(painter, w, h)
            
        # Apply brightness overlay
        if self.brightness < 100:
            overlay_alpha = 255 - int((self.brightness / 100.0) * 255)
            painter.fillRect(self.rect(), QColor(0, 0, 0, overlay_alpha))

    def keyPressEvent(self, event):
        media_keys = [Qt.Key.Key_MediaPlay, Qt.Key.Key_MediaStop, Qt.Key.Key_MediaPrevious, Qt.Key.Key_MediaNext, Qt.Key.Key_VolumeUp, Qt.Key.Key_VolumeDown, Qt.Key.Key_VolumeMute, Qt.Key.Key_MediaPause, Qt.Key.Key_MediaTogglePlayPause]
        if self.ignore_media_keys and event.key() in media_keys:
            return
            
        if self.strict_exit and event.key() == Qt.Key.Key_Z and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            if not self.preview_mode:
                self.close()
            return
            
        if event.key() == Qt.Key.Key_Equal or event.key() == Qt.Key.Key_Plus:
            self.clock_scales[str(self.clock_style)] = min(0.95, self.clock_scales[str(self.clock_style)] + 0.05)
            self.update()
            self.save_live_config()
        elif event.key() == Qt.Key.Key_Minus:
            self.clock_scales[str(self.clock_style)] = max(0.15, self.clock_scales[str(self.clock_style)] - 0.05)
            self.update()
            self.save_live_config()
        elif event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
            self.clock_style = (self.clock_style + (1 if event.key() == Qt.Key.Key_Up else -1)) % 3 
            self.update()
            self.save_live_config()
        elif event.key() in (Qt.Key.Key_Space, Qt.Key.Key_F23):
            if self.clock_style == 2 and self.dino_dead:
                self.dino_dead = False
                self.dino_obstacles = []
                self.dino_timer_msec = 0
            else:
                self.show_bg = not self.show_bg
        elif self.enable_win_key and event.key() in (Qt.Key.Key_Meta, Qt.Key.Key_Super_L, Qt.Key.Key_Super_R):
            self.show_bg = not self.show_bg
        else:
            if not self.strict_exit and not self.preview_mode:
                self.close()

    def mouseMoveEvent(self, event):
        if self.preview_mode: return
        if self.strict_exit: return
        if self.last_pos is None:
            self.last_pos = event.pos()
            return
        diff = event.pos() - self.last_pos
        if abs(diff.x()) > 5 or abs(diff.y()) > 5:
            self.close()

    def mousePressEvent(self, event):
        if self.preview_mode: return
        if self.strict_exit: return
        self.close()

    def wheelEvent(self, event):
        if self.preview_mode:
            delta = event.angleDelta().y()
            if delta != 0:
                step = 0.05 if delta > 0 else -0.05
                style_key = str(self.clock_style)
                current_scale = self.clock_scales.get(style_key, 0.45)
                new_scale = max(0.15, min(0.95, round(current_scale + step, 2)))
                self.clock_scales[style_key] = new_scale
                self.update()
                if callable(getattr(self, 'scale_callback', None)):
                    self.scale_callback(int(new_scale * 100))
                event.accept()
                return
        super().wheelEvent(event)


import urllib.request
import threading
import json
import traceback

class WeatherWorker(QThread):
    weather_updated = pyqtSignal(dict)

    def run(self):
        try:
            # 1. Get Location
            req = urllib.request.Request("http://ip-api.com/json/", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                ip_data = json.loads(response.read().decode())
                lat = ip_data.get("lat")
                lon = ip_data.get("lon")
            
            if lat and lon:
                # 2. Get Weather
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&temperature_unit=celsius"
                req2 = urllib.request.Request(weather_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req2, timeout=5) as response2:
                    weather_data = json.loads(response2.read().decode())
                    current = weather_data.get("current_weather", {})
                    self.weather_updated.emit({
                        "temp": current.get("temperature", 0),
                        "code": current.get("weathercode", 0)
                    })
        except Exception as e:
            print("Weather fetch failed:", e)

class SpatialStageFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("spatialStage")
        self.accent_color = QColor("#0078D4")
        self.clock_style = 0
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
    def set_stage_theme(self, clock_style, accent_hex):
        self.clock_style = clock_style
        self.accent_color = QColor(accent_hex)
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        
        # Soft ambient back-glow matching the active mode/color
        if self.clock_style == 0:
            glow_col = QColor(245, 158, 11) # Warm incandescent amber
        elif self.clock_style == 1:
            glow_col = self.accent_color    # Custom accent color
        else:
            glow_col = QColor(56, 189, 248) # Electric cyan
            
        cx = w / 2.0
        cy = h / 2.0
        r = max(w, h) * 0.58
        glow = QRadialGradient(cx, cy, r)
        glow.setColorAt(0.0, QColor(glow_col.red(), glow_col.green(), glow_col.blue(), 75))
        glow.setColorAt(0.40, QColor(glow_col.red(), glow_col.green(), glow_col.blue(), 28))
        glow.setColorAt(1.0, QColor(glow_col.red(), glow_col.green(), glow_col.blue(), 0))
        
        painter.setBrush(glow)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(QRectF(0, 0, w, h), 14, 14)
        
        # Fine glass specular border
        border_pen = QPen(QColor(255, 255, 255, 30), 1)
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(1, 1, w - 2, h - 2), 14, 14)


def get_or_create_check_icon():
    import tempfile
    temp_path = os.path.join(tempfile.gettempdir(), "dinoscreener_chk.png").replace("\\", "/")
    if not os.path.exists(temp_path):
        pix = QPixmap(16, 16)
        pix.fill(Qt.GlobalColor.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor("#FFFFFF"), 2.2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        p.setPen(pen)
        path = QPainterPath()
        path.moveTo(3.5, 8.5)
        path.lineTo(6.5, 11.5)
        path.lineTo(12.5, 4.5)
        p.drawPath(path)
        p.end()
        pix.save(temp_path, "PNG")
    return temp_path


class SettingsDialog(QDialog):
    def __init__(self, config_path):
        super().__init__()
        self.setWindowTitle("Dinoscreener Settings — Spatial Studio")
        self.setFixedSize(920, 645)
        self.setAcceptDrops(True)
        
        # Apply Windows 11 DWM Acrylic backdrop & Dark Mode
        try:
            hwnd = int(self.winId())
            dark_mode = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(dark_mode), ctypes.sizeof(dark_mode))
            backdrop_type = ctypes.c_int(3) # DWMSBT_TRANSIENTWINDOW (Acrylic blur)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 38, ctypes.byref(backdrop_type), ctypes.sizeof(backdrop_type))
        except Exception:
            pass

        check_icon_path = get_or_create_check_icon()

        # Spatial Studio Modern Glass Stylesheet
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #0E121A;
            }}
            QLabel {{
                color: #FFFFFF;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', -apple-system, sans-serif;
            }}
            QFrame#bentoCard {{
                background: rgba(255, 255, 255, 0.035);
                border: 1px solid rgba(255, 255, 255, 0.07);
                border-radius: 12px;
            }}
            QFrame#previewCard {{
                background: #000000;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 10px;
            }}
            /* Fluent Checkbox with Authentic Checkmark */
            QCheckBox {{
                color: #CBD5E1;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
                font-size: 11.5px;
                spacing: 8px;
                background: transparent;
            }}
            QCheckBox:hover {{
                color: #FFFFFF;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid rgba(255, 255, 255, 0.22);
                border-radius: 4px;
                background: rgba(255, 255, 255, 0.05);
            }}
            QCheckBox::indicator:hover {{
                border-color: rgba(255, 255, 255, 0.45);
                background: rgba(255, 255, 255, 0.09);
            }}
            QCheckBox::indicator:checked {{
                background-color: #0078D4;
                border-color: #0078D4;
                image: url("{check_icon_path}");
            }}
            /* Modern Slider */
            QSlider {{
                background: transparent;
            }}
            QSlider::groove:horizontal {{
                height: 4px;
                background: rgba(255, 255, 255, 0.15);
                border-radius: 2px;
            }}
            QSlider::sub-page:horizontal {{
                background: #0078D4;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: #FFFFFF;
                border: 2px solid #0078D4;
                width: 14px;
                height: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }}
            /* Comboboxes */
            QComboBox, QFontComboBox {{
                background: rgba(255, 255, 255, 0.06);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 6px;
                padding: 3px 8px;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
                font-size: 11px;
            }}
            QComboBox:hover, QFontComboBox:hover {{
                background: rgba(255, 255, 255, 0.09);
                border-color: rgba(255, 255, 255, 0.25);
            }}
            QComboBox::drop-down, QFontComboBox::drop-down {{
                border: none;
                width: 18px;
            }}
            QComboBox QAbstractItemView, QFontComboBox QAbstractItemView {{
                background: #181C26;
                color: #FFFFFF;
                selection-background-color: #0078D4;
                selection-color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                padding: 4px;
            }}
        """)
        
        self.config_path = config_path
        self.config = self.load_config()
        
        saved_prim = self.config.get("primary_font", "")
        self.saved_primary_font = saved_prim if (saved_prim and os.path.exists(saved_prim)) else ""
        self.saved_dino_font = self.config.get("dino_font", "Bungee")
        
        saved_char = self.config.get("custom_character_image", "")
        self.saved_char_image = saved_char if (saved_char and os.path.exists(saved_char)) else ""
        self.saved_char_type = self.config.get("character_type", "dino").capitalize()
        if self.saved_char_type not in ["Dino", "Custom"]:
            self.saved_char_type = "Dino"
        if self.saved_char_type == "Custom" and not self.saved_char_image:
            self.saved_char_type = "Dino"
            
        bungee_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Bungee-Regular.ttf")
        if getattr(sys, 'frozen', False):
            bungee_path = os.path.join(sys._MEIPASS, "Bungee-Regular.ttf")
        if os.path.exists(bungee_path):
            QFontDatabase.addApplicationFont(bungee_path)
            
        self.initUI()
        self.installEventFilter(self)
        self.check_font_changed()
        self.check_char_changed()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for u in event.mimeData().urls():
                ext = os.path.splitext(u.toLocalFile())[1].lower()
                if ext in ['.ttf', '.otf', '.png', '.jpg', '.jpeg', '.bmp', '.webp']:
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for u in event.mimeData().urls():
                path = u.toLocalFile()
                ext = os.path.splitext(path)[1].lower()
                if ext in ['.ttf', '.otf']:
                    self.handle_font_import(path)
                    self.set_mode(2)
                    event.acceptProposedAction()
                    return
                elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']:
                    self.handle_character_import(path)
                    self.set_mode(2)
                    event.acceptProposedAction()
                    return

    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
                new_style = (self.preview.clock_style + (1 if event.key() == Qt.Key.Key_Up else -1)) % 3
                self.set_mode(new_style)
                return True
            elif event.key() in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
                self.step_scale(5)
                return True
            elif event.key() in (Qt.Key.Key_Minus, Qt.Key.Key_Underscore):
                self.step_scale(-5)
                return True
        return super().eventFilter(obj, event)

    def load_config(self):
        default_config = {
            "accent_color": "#0078D4",
            "show_info": True,
            "strict_exit": False,
            "enable_win_key": False,
            "brightness": 100,
            "clock_style": 0,
            "clock_scales": {"0": 0.45, "1": 0.45, "2": 0.45},
            "use_24hr": False,
            "leading_zero": False,
            "leading_zeros": {"0": False, "1": False, "2": False},
            "live_weather": False,
            "pixel_shift": False,
            "primary_font": "",
            "ignore_media_keys": False,
            "dino_font": "Bungee",
            "character_type": "dino",
            "custom_character_image": ""
        }
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    default_config.update(json.load(f))
            except Exception:
                pass
        return default_config

    def save_config(self):
        self.config["show_info"] = self.info_cb.isChecked()
        self.config["strict_exit"] = self.strict_cb.isChecked()
        self.config["enable_win_key"] = self.win_cb.isChecked()
        self.config["brightness"] = self.bright_slider.value()
        self.config["clock_style"] = self.preview.clock_style
        self.config["clock_scales"] = self.preview.clock_scales
        self.config["use_24hr"] = self.use_24hr_cb.isChecked()
        self.config["leading_zeros"] = self.preview.leading_zeros
        self.config["live_weather"] = self.live_weather_cb.isChecked()
        self.config["pixel_shift"] = self.pixel_shift_cb.isChecked()
        self.config["primary_font"] = getattr(self, 'primary_font', "")
        self.config["ignore_media_keys"] = self.ignore_media_cb.isChecked()
        self.config["dino_font"] = self.font_cb.currentFont().family()
        self.config["character_type"] = self.char_cb.currentText().lower()
        self.config["custom_character_image"] = getattr(self, 'custom_character_image', "")
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        self.accept()

    def test_fullscreen(self):
        try:
            self.test_clock = CrispAestheticFlipClock(
                accent_color=self.config.get("accent_color", "#0078D4"),
                enable_win_key=self.win_cb.isChecked(),
                strict_exit=False,
                show_info=self.info_cb.isChecked(),
                preview_mode=False,
                brightness=self.bright_slider.value(),
                clock_style=self.preview.clock_style,
                clock_scales=self.preview.clock_scales,
                use_24hr=self.use_24hr_cb.isChecked(),
                leading_zeros=self.preview.leading_zeros,
                ignore_media_keys=self.ignore_media_cb.isChecked(),
                dino_font=self.font_cb.currentFont().family(),
                primary_font=getattr(self, 'primary_font', ""),
                character_type=self.char_cb.currentText().lower(),
                custom_character_image=getattr(self, 'custom_character_image', ""),
                live_weather=self.live_weather_cb.isChecked(),
                pixel_shift=self.pixel_shift_cb.isChecked()
            )
            self.test_clock.showFullScreen()
        except Exception as e:
            print("Error launching fullscreen test:", e)

    def reset_defaults(self):
        if os.path.exists(self.config_path):
            try:
                os.remove(self.config_path)
            except Exception:
                pass
        self.config = self.load_config()
        self.preview.clock_scales = self.config["clock_scales"]
        self.scale_slider.setValue(int(self.preview.clock_scales.get("0", 0.45) * 100))
        self.bright_slider.setValue(100)
        self.use_24hr_cb.setChecked(False)
        self.leading_zero_cb.setChecked(False)
        self.flip_leading_cb.setChecked(False)
        self.strict_cb.setChecked(False)
        self.ignore_media_cb.setChecked(False)
        self.win_cb.setChecked(False)
        self.pixel_shift_cb.setChecked(False)
        self.info_cb.setChecked(True)
        self.live_weather_cb.setChecked(False)
        self.revert_font()
        self.revert_character()
        self.set_accent_color("#0078D4")
        self.set_mode(0)

    def on_preview_scale_scrolled(self, val):
        if hasattr(self, 'scale_slider'):
            self.scale_slider.blockSignals(True)
            self.scale_slider.setValue(val)
            self.scale_slider.blockSignals(False)
            self.lbl_scale_pct.setText(f"{val}%")

    def initUI(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(18, 14, 18, 14)
        root_layout.setSpacing(10)
        
        # 1. TOP HEADER (App branding & Status Indicator)
        header_row = QHBoxLayout()
        header_row.setContentsMargins(2, 0, 2, 0)
        
        brand_box = QVBoxLayout()
        brand_box.setSpacing(1)
        lbl_app_name = QLabel("Dinoscreener")
        lbl_app_name.setStyleSheet("font-size: 15px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.2px;")
        lbl_app_sub = QLabel("Spatial Ambient Studio")
        lbl_app_sub.setStyleSheet("font-size: 11px; color: #94A3B8;")
        brand_box.addWidget(lbl_app_name)
        brand_box.addWidget(lbl_app_sub)
        header_row.addLayout(brand_box)
        
        header_row.addStretch()
        
        status_pill = QLabel("● LIVE PREVIEW")
        status_pill.setStyleSheet("""
            QLabel {
                background: rgba(16, 185, 129, 0.12);
                color: #34D399;
                border: 1px solid rgba(16, 185, 129, 0.25);
                border-radius: 10px;
                padding: 3px 10px;
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
        """)
        header_row.addWidget(status_pill)
        root_layout.addLayout(header_row)
        
        # 2. SPATIAL AMBIENT STAGE
        self.stage_frame = SpatialStageFrame()
        stage_layout = QVBoxLayout(self.stage_frame)
        stage_layout.setContentsMargins(8, 7, 8, 7)
        
        self.preview_card = QFrame()
        self.preview_card.setObjectName("previewCard")
        preview_layout = QVBoxLayout(self.preview_card)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        start_style = self.config.get("clock_style", 0)
        self.preview = CrispAestheticFlipClock(
            accent_color=self.config.get("accent_color", "#0078D4"),
            enable_win_key=self.config.get("enable_win_key", False),
            strict_exit=self.config.get("strict_exit", False),
            show_info=self.config.get("show_info", True),
            preview_mode=True,
            brightness=self.config.get("brightness", 100),
            clock_style=start_style,
            clock_scales=self.config.get("clock_scales", {"0": 0.45, "1": 0.45, "2": 0.45}),
            use_24hr=self.config.get("use_24hr", False),
            leading_zeros=self.config.get("leading_zeros", self.config.get("leading_zero", False)),
            ignore_media_keys=self.config.get("ignore_media_keys", False),
            dino_font=self.config.get("dino_font", "Bungee"),
            primary_font=self.config.get("primary_font", ""),
            character_type=self.config.get("character_type", "dino"),
            custom_character_image=self.config.get("custom_character_image", "")
        )
        self.preview.scale_callback = self.on_preview_scale_scrolled
        preview_layout.addWidget(self.preview)
        stage_layout.addWidget(self.preview_card)
        root_layout.addWidget(self.stage_frame, stretch=1)
        
        # 3. FLOATING CAPSULE MODE SELECTOR
        capsule_row = QHBoxLayout()
        capsule_row.setContentsMargins(0, 0, 0, 0)
        capsule_row.addStretch()
        
        capsule_frame = QFrame()
        capsule_frame.setFixedHeight(34)
        capsule_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.045);
                border: 1px solid rgba(255, 255, 255, 0.09);
                border-radius: 17px;
                padding: 2px;
            }
        """)
        capsule_layout = QHBoxLayout(capsule_frame)
        capsule_layout.setContentsMargins(3, 1, 3, 1)
        capsule_layout.setSpacing(4)
        
        self.mode_buttons = []
        modes = [
            ("Flip Clock", 0),
            ("Rotary Modern", 1),
            ("Dino Runner", 2)
        ]
        for label, idx in modes:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #94A3B8;
                    border: none;
                    border-radius: 14px;
                    padding: 4px 18px;
                    font-size: 11.5px;
                    font-weight: 500;
                    min-width: 95px;
                    font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
                }
                QPushButton:hover {
                    color: #FFFFFF;
                    background: rgba(255, 255, 255, 0.05);
                }
                QPushButton:checked {
                    background: rgba(255, 255, 255, 0.14);
                    color: #FFFFFF;
                    font-weight: 600;
                }
            """)
            btn.clicked.connect(lambda checked, i=idx: self.set_mode(i))
            capsule_layout.addWidget(btn)
            self.mode_buttons.append(btn)
            
        capsule_row.addWidget(capsule_frame)
        capsule_row.addStretch()
        root_layout.addLayout(capsule_row)
        
        # 4. THREE BALANCED SPATIAL BENTO CARDS
        cards_row = QHBoxLayout()
        cards_row.setSpacing(12)
        cards_row.setContentsMargins(0, 0, 0, 0)
        
        # === CARD 1: Mode Parameters ===
        card_mode = QFrame()
        card_mode.setObjectName("bentoCard")
        card_mode_layout = QVBoxLayout(card_mode)
        card_mode_layout.setContentsMargins(14, 12, 14, 12)
        card_mode_layout.setSpacing(8)
        
        header_mode = QVBoxLayout()
        header_mode.setSpacing(1)
        self.lbl_mode_title = QLabel("Flip Clock Studio")
        self.lbl_mode_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #FFFFFF;")
        self.lbl_mode_sub = QLabel("Scale & Typography")
        self.lbl_mode_sub.setStyleSheet("font-size: 10.5px; color: #94A3B8;")
        header_mode.addWidget(self.lbl_mode_title)
        header_mode.addWidget(self.lbl_mode_sub)
        card_mode_layout.addLayout(header_mode)
        
        self.pages = QStackedWidget()
        
        # --- Page 0: Flip Clock ---
        page_flip = QWidget()
        flip_layout = QVBoxLayout(page_flip)
        flip_layout.setContentsMargins(0, 2, 0, 0)
        flip_layout.setSpacing(8)
        
        scale_box = QHBoxLayout()
        scale_box.setSpacing(8)
        lbl_scale_title = QLabel("Scale:")
        lbl_scale_title.setStyleSheet("color: #E2E8F0; font-size: 11.5px; font-weight: 500;")
        scale_box.addWidget(lbl_scale_title)
        
        btn_step_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.06);
                color: #CBD5E1;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 5px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.12);
                color: #FFFFFF;
            }
        """
        self.btn_scale_minus = QPushButton("−")
        self.btn_scale_minus.setFixedSize(22, 22)
        self.btn_scale_minus.setStyleSheet(btn_step_style)
        self.btn_scale_minus.clicked.connect(lambda: self.step_scale(-5))
        scale_box.addWidget(self.btn_scale_minus)
        
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(15, 95)
        init_scale = int(self.preview.clock_scales.get("0", 0.45) * 100)
        self.scale_slider.setValue(init_scale)
        self.scale_slider.valueChanged.connect(self.update_scale)
        scale_box.addWidget(self.scale_slider)
        
        self.btn_scale_plus = QPushButton("+")
        self.btn_scale_plus.setFixedSize(22, 22)
        self.btn_scale_plus.setStyleSheet(btn_step_style)
        self.btn_scale_plus.clicked.connect(lambda: self.step_scale(5))
        scale_box.addWidget(self.btn_scale_plus)
        
        self.lbl_scale_pct = QLabel(f"{init_scale}%")
        self.lbl_scale_pct.setFixedWidth(36)
        self.lbl_scale_pct.setStyleSheet("color: #60CDFF; font-size: 11.5px; font-weight: 600;")
        scale_box.addWidget(self.lbl_scale_pct)
        flip_layout.addLayout(scale_box)
        
        self.flip_leading_cb = QCheckBox("Leading Zero (e.g. 09:00)")
        self.flip_leading_cb.setChecked(self.preview.leading_zeros.get("0", False))
        self.flip_leading_cb.stateChanged.connect(self.on_flip_leading_changed)
        flip_layout.addWidget(self.flip_leading_cb)
        
        tip_frame = QFrame()
        tip_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.025);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 6px;
                padding: 4px 6px;
            }
        """)
        tip_layout = QVBoxLayout(tip_frame)
        tip_layout.setContentsMargins(4, 3, 4, 3)
        tip_layout.setSpacing(2)
        lbl_tip1 = QLabel("Tip: Scroll mouse on preview to scale directly.")
        lbl_tip1.setStyleSheet("color: #94A3B8; font-size: 10.5px;")
        lbl_tip2 = QLabel("Shortcut: Press + or − anytime while screensaver runs.")
        lbl_tip2.setStyleSheet("color: #64748B; font-size: 10px;")
        tip_layout.addWidget(lbl_tip1)
        tip_layout.addWidget(lbl_tip2)
        flip_layout.addWidget(tip_frame)
        flip_layout.addStretch()
        self.pages.addWidget(page_flip)
        
        # --- Page 1: Rotary Modern ---
        page_rotary = QWidget()
        rot_layout = QVBoxLayout(page_rotary)
        rot_layout.setContentsMargins(0, 2, 0, 0)
        rot_layout.setSpacing(8)
        
        accent_box = QHBoxLayout()
        accent_box.setSpacing(6)
        lbl_dial = QLabel("Accent:")
        lbl_dial.setStyleSheet("color: #E2E8F0; font-size: 11.5px; font-weight: 500;")
        accent_box.addWidget(lbl_dial)
        
        self.swatch_buttons = []
        preset_colors = ["#0078D4", "#60CDFF", "#10B981", "#F59E0B", "#F43F5E"]
        for c in preset_colors:
            s_btn = QPushButton()
            s_btn.setFixedSize(18, 18)
            s_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            s_btn.clicked.connect(lambda checked, col=c: self.set_accent_color(col))
            accent_box.addWidget(s_btn)
            self.swatch_buttons.append((c, s_btn))
            
        btn_custom = QPushButton("Custom...")
        btn_custom.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_custom.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.06);
                color: #CBD5E1;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 5px;
                padding: 2px 7px;
                font-size: 10.5px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.12);
                color: #FFFFFF;
            }
        """)
        btn_custom.clicked.connect(self.pick_color)
        accent_box.addWidget(btn_custom)
        accent_box.addStretch()
        rot_layout.addLayout(accent_box)
        
        self.info_cb = QCheckBox("Weather && Battery Status Ring")
        self.info_cb.setChecked(self.config.get("show_info", True))
        self.info_cb.stateChanged.connect(lambda s: self.preview.set_show_info(self.info_cb.isChecked()))
        rot_layout.addWidget(self.info_cb)
        
        self.live_weather_cb = QCheckBox("Live Weather Updates (Open-Meteo)")
        self.live_weather_cb.setChecked(self.config.get("live_weather", False))
        self.live_weather_cb.stateChanged.connect(self.update_live_weather)
        rot_layout.addWidget(self.live_weather_cb)
        
        rot_note = QLabel("Dual orbital dials with live astronomical & charge status.")
        rot_note.setStyleSheet("color: #64748B; font-size: 10px;")
        rot_layout.addWidget(rot_note)
        rot_layout.addStretch()
        self.pages.addWidget(page_rotary)
        
        # --- Page 2: Dino Runner ---
        page_dino = QWidget()
        dino_layout = QVBoxLayout(page_dino)
        dino_layout.setContentsMargins(0, 2, 0, 0)
        dino_layout.setSpacing(6)
        
        btn_action_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.06);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 5px;
                padding: 3px 8px;
                font-size: 10.5px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.12);
            }
        """
        undo_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.06);
                color: #94A3B8;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
                color: #FFFFFF;
            }
        """
        
        # Font Row
        font_row1 = QHBoxLayout()
        font_row1.setSpacing(6)
        lbl_dino_font = QLabel("Font:")
        lbl_dino_font.setFixedWidth(40)
        lbl_dino_font.setStyleSheet("color: #E2E8F0; font-size: 11px;")
        font_row1.addWidget(lbl_dino_font)
        self.font_cb = QFontComboBox()
        self.font_cb.setCurrentFont(QFont(self.config.get("dino_font", "Bungee")))
        self.font_cb.currentFontChanged.connect(self.update_dino_font)
        font_row1.addWidget(self.font_cb)
        dino_layout.addLayout(font_row1)
        
        font_row2 = QHBoxLayout()
        font_row2.setSpacing(6)
        self.primary_font = self.config.get("primary_font", "")
        self.primary_font_btn = QPushButton("Import TTF...")
        self.primary_font_btn.setStyleSheet(btn_action_style)
        self.primary_font_btn.clicked.connect(self.import_primary_font)
        font_row2.addWidget(self.primary_font_btn)
        
        self.undo_font_btn = QPushButton("↺")
        self.undo_font_btn.setFixedSize(20, 20)
        self.undo_font_btn.setStyleSheet(undo_style)
        self.undo_font_btn.clicked.connect(self.revert_font)
        self.undo_font_btn.hide()
        font_row2.addWidget(self.undo_font_btn)
        
        self.primary_font_label = QLabel(os.path.basename(self.primary_font) if self.primary_font else "Default")
        self.primary_font_label.setStyleSheet("color: #94A3B8; font-size: 10.5px;")
        font_row2.addWidget(self.primary_font_label)
        font_row2.addStretch()
        dino_layout.addLayout(font_row2)
        
        # Sprite Row
        char_row1 = QHBoxLayout()
        char_row1.setSpacing(6)
        lbl_sprite = QLabel("Sprite:")
        lbl_sprite.setFixedWidth(40)
        lbl_sprite.setStyleSheet("color: #E2E8F0; font-size: 11px;")
        char_row1.addWidget(lbl_sprite)
        self.char_cb = QComboBox()
        self.char_cb.addItems(["Dino", "Custom"])
        char_init = "Custom" if (self.config.get("character_type", "dino").lower() == "custom" and self.config.get("custom_character_image", "") and os.path.exists(self.config.get("custom_character_image", ""))) else "Dino"
        self.char_cb.setCurrentText(char_init)
        self.char_cb.currentTextChanged.connect(self.update_character_type)
        char_row1.addWidget(self.char_cb)
        dino_layout.addLayout(char_row1)
        
        char_row2 = QHBoxLayout()
        char_row2.setSpacing(6)
        self.custom_character_image = self.config.get("custom_character_image", "")
        self.char_btn = QPushButton("Import Sprite...")
        self.char_btn.setStyleSheet(btn_action_style)
        self.char_btn.clicked.connect(self.import_character)
        char_row2.addWidget(self.char_btn)
        
        self.undo_char_btn = QPushButton("↺")
        self.undo_char_btn.setFixedSize(20, 20)
        self.undo_char_btn.setStyleSheet(undo_style)
        self.undo_char_btn.clicked.connect(self.revert_character)
        self.undo_char_btn.hide()
        char_row2.addWidget(self.undo_char_btn)
        
        self.char_label = QLabel(os.path.basename(self.custom_character_image) if self.custom_character_image else "Default")
        self.char_label.setStyleSheet("color: #94A3B8; font-size: 10.5px;")
        char_row2.addWidget(self.char_label)
        char_row2.addStretch()
        dino_layout.addLayout(char_row2)
        
        tip_dino = QLabel("Tip: Drop .ttf or .png directly onto window.")
        tip_dino.setStyleSheet("color: #64748B; font-size: 10px;")
        dino_layout.addWidget(tip_dino)
        dino_layout.addStretch()
        self.pages.addWidget(page_dino)
        
        card_mode_layout.addWidget(self.pages)
        cards_row.addWidget(card_mode, stretch=1)
        
        # === CARD 2: Display & Atmosphere ===
        card_disp = QFrame()
        card_disp.setObjectName("bentoCard")
        card_disp_layout = QVBoxLayout(card_disp)
        card_disp_layout.setContentsMargins(14, 12, 14, 12)
        card_disp_layout.setSpacing(8)
        
        header_disp = QVBoxLayout()
        header_disp.setSpacing(1)
        lbl_disp_title = QLabel("Display & Atmosphere")
        lbl_disp_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #FFFFFF;")
        lbl_disp_sub = QLabel("Luminance & Protection")
        lbl_disp_sub.setStyleSheet("font-size: 10.5px; color: #94A3B8;")
        header_disp.addWidget(lbl_disp_title)
        header_disp.addWidget(lbl_disp_sub)
        card_disp_layout.addLayout(header_disp)
        
        # Brightness Row
        bright_box = QHBoxLayout()
        bright_box.setSpacing(8)
        lbl_bright_title = QLabel("Brightness:")
        lbl_bright_title.setStyleSheet("color: #E2E8F0; font-size: 11.5px; font-weight: 500;")
        bright_box.addWidget(lbl_bright_title)
        
        self.bright_slider = QSlider(Qt.Orientation.Horizontal)
        self.bright_slider.setRange(10, 100)
        self.bright_slider.setValue(self.config.get("brightness", 100))
        self.bright_slider.valueChanged.connect(self.update_brightness)
        bright_box.addWidget(self.bright_slider)
        
        self.bright_val_label = QLabel(f"{self.config.get('brightness', 100)}%")
        self.bright_val_label.setFixedWidth(36)
        self.bright_val_label.setStyleSheet("color: #60CDFF; font-size: 11.5px; font-weight: 600;")
        bright_box.addWidget(self.bright_val_label)
        card_disp_layout.addLayout(bright_box)
        
        # Display Toggles
        self.use_24hr_cb = QCheckBox("24-Hour Time Format")
        self.use_24hr_cb.setChecked(self.config.get("use_24hr", False))
        self.use_24hr_cb.stateChanged.connect(self.update_24hr)
        card_disp_layout.addWidget(self.use_24hr_cb)
        
        self.pixel_shift_cb = QCheckBox("OLED Pixel Shift")
        self.pixel_shift_cb.setChecked(self.config.get("pixel_shift", False))
        self.pixel_shift_cb.stateChanged.connect(self.update_pixel_shift)
        card_disp_layout.addWidget(self.pixel_shift_cb)
        
        self.leading_zero_cb = QCheckBox("Leading Zero Display")
        self.leading_zero_cb.setChecked(self.preview.leading_zeros.get(str(start_style), False))
        self.leading_zero_cb.stateChanged.connect(self.update_leading_zero)
        card_disp_layout.addWidget(self.leading_zero_cb)
        
        lbl_burnin_info = QLabel("OLED shift subtly repositions pixels over time to prevent burn-in.")
        lbl_burnin_info.setWordWrap(True)
        lbl_burnin_info.setStyleSheet("color: #64748B; font-size: 10px;")
        card_disp_layout.addWidget(lbl_burnin_info)
        card_disp_layout.addStretch()
        cards_row.addWidget(card_disp, stretch=1)
        
        # === CARD 3: System & Security ===
        card_sys = QFrame()
        card_sys.setObjectName("bentoCard")
        card_sys_layout = QVBoxLayout(card_sys)
        card_sys_layout.setContentsMargins(14, 12, 14, 12)
        card_sys_layout.setSpacing(8)
        
        header_sys = QVBoxLayout()
        header_sys.setSpacing(1)
        lbl_sys_title = QLabel("System & Security")
        lbl_sys_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #FFFFFF;")
        lbl_sys_sub = QLabel("Keyboard & Intercepts")
        lbl_sys_sub.setStyleSheet("font-size: 10.5px; color: #94A3B8;")
        header_sys.addWidget(lbl_sys_title)
        header_sys.addWidget(lbl_sys_sub)
        card_sys_layout.addLayout(header_sys)
        
        self.strict_cb = QCheckBox("Lock Screen on Exit (Ctrl+Z)")
        self.strict_cb.setChecked(self.config.get("strict_exit", False))
        self.strict_cb.stateChanged.connect(lambda s: setattr(self.preview, 'strict_exit', self.strict_cb.isChecked()))
        card_sys_layout.addWidget(self.strict_cb)
        
        self.ignore_media_cb = QCheckBox("Ignore Media Keys")
        self.ignore_media_cb.setChecked(self.config.get("ignore_media_keys", False))
        self.ignore_media_cb.stateChanged.connect(lambda s: setattr(self.preview, 'ignore_media_keys', self.ignore_media_cb.isChecked()))
        card_sys_layout.addWidget(self.ignore_media_cb)
        
        self.win_cb = QCheckBox("Enable Windows Key")
        self.win_cb.setChecked(self.config.get("enable_win_key", False))
        self.win_cb.stateChanged.connect(lambda s: setattr(self.preview, 'enable_win_key', self.win_cb.isChecked()))
        card_sys_layout.addWidget(self.win_cb)
        
        lbl_sys_info = QLabel("Screensaver dismisses smoothly on mouse movement or custom unlock key.")
        lbl_sys_info.setWordWrap(True)
        lbl_sys_info.setStyleSheet("color: #64748B; font-size: 10px;")
        card_sys_layout.addWidget(lbl_sys_info)
        card_sys_layout.addStretch()
        cards_row.addWidget(card_sys, stretch=1)
        
        root_layout.addLayout(cards_row)
        
        # 5. FOOTER ACTIONS
        footer_row = QHBoxLayout()
        footer_row.setContentsMargins(4, 2, 4, 0)
        
        btn_test = QPushButton("Test Fullscreen")
        btn_test.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_test.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                color: #CBD5E1;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 11.5px;
                font-weight: 500;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
                color: #FFFFFF;
                border-color: rgba(255, 255, 255, 0.25);
            }
        """)
        btn_test.clicked.connect(self.test_fullscreen)
        footer_row.addWidget(btn_test)
        footer_row.addStretch()
        
        btn_reset = QPushButton("Reset Defaults")
        btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reset.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94A3B8;
                border: none;
                padding: 6px 12px;
                font-size: 11.5px;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                color: #F87171;
            }
        """)
        btn_reset.clicked.connect(self.reset_defaults)
        footer_row.addWidget(btn_reset)
        
        btn_apply = QPushButton("Apply")
        btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                padding: 6px 26px;
                font-size: 11.5px;
                font-weight: 600;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
            QPushButton:pressed {
                background-color: #005A9E;
            }
        """)
        btn_apply.clicked.connect(self.save_config)
        footer_row.addWidget(btn_apply)
        root_layout.addLayout(footer_row)
        
        self.set_mode(start_style)

    def set_mode(self, idx):
        self.preview.clock_style = idx
        self.preview.update()
        if hasattr(self, 'stage_frame'):
            self.stage_frame.set_stage_theme(idx, self.config.get("accent_color", "#0078D4"))
        for i, btn in enumerate(self.mode_buttons):
            btn.blockSignals(True)
            btn.setChecked(i == idx)
            btn.blockSignals(False)
        self.pages.setCurrentIndex(idx)
        titles = ["Flip Clock Studio", "Rotary Modern Studio", "Dino Runner Studio"]
        subtitles = ["Scale & Typography", "Colors & Orbital Telemetry", "Sprites & Custom Type"]
        if idx < len(titles):
            self.lbl_mode_title.setText(titles[idx])
            self.lbl_mode_sub.setText(subtitles[idx])
        self.update_swatch_highlights()
        if hasattr(self, 'leading_zero_cb'):
            self.leading_zero_cb.blockSignals(True)
            self.leading_zero_cb.setChecked(self.preview.leading_zeros.get(str(idx), False))
            self.leading_zero_cb.blockSignals(False)

    def update_swatch_highlights(self):
        if not hasattr(self, 'swatch_buttons'):
            return
        curr = self.config.get("accent_color", "#0078D4").upper()
        for hex_code, btn in self.swatch_buttons:
            if hex_code.upper() == curr:
                btn.setStyleSheet(f"background-color: {hex_code}; border: 2px solid #FFFFFF; border-radius: 9px;")
            else:
                btn.setStyleSheet(f"background-color: {hex_code}; border: 1px solid rgba(255, 255, 255, 0.25); border-radius: 9px;")

    def set_accent_color(self, hex_code):
        self.config["accent_color"] = hex_code
        self.preview.set_accent_color(hex_code)
        if hasattr(self, 'stage_frame'):
            self.stage_frame.set_stage_theme(self.preview.clock_style, hex_code)
        self.update_swatch_highlights()

    def pick_color(self):
        color = QColorDialog.getColor(QColor(self.config.get("accent_color", "#0078D4")), self, "Select Accent Color")
        if color.isValid():
            self.set_accent_color(color.name())

    def update_scale(self, val):
        self.lbl_scale_pct.setText(f"{val}%")
        self.preview.clock_scales["0"] = val / 100.0
        self.config["clock_scales"]["0"] = val / 100.0
        if self.preview.clock_style == 0:
            self.preview.update()

    def step_scale(self, delta):
        if hasattr(self, 'scale_slider'):
            new_val = max(15, min(95, self.scale_slider.value() + delta))
            self.scale_slider.setValue(new_val)

    def on_flip_leading_changed(self, state):
        self.leading_zero_cb.setChecked(self.flip_leading_cb.isChecked())

    def update_leading_zero(self, state=None):
        val = self.leading_zero_cb.isChecked()
        self.preview.leading_zeros[str(self.preview.clock_style)] = val
        if self.preview.clock_style == 0:
            self.flip_leading_cb.blockSignals(True)
            self.flip_leading_cb.setChecked(val)
            self.flip_leading_cb.blockSignals(False)
        self.preview.update()

    def update_brightness(self, val):
        self.bright_val_label.setText(f"{val}%")
        self.preview.set_brightness(val)

    def update_24hr(self, state=None):
        self.preview.use_24hr = self.use_24hr_cb.isChecked()
        self.preview.update()

    def update_live_weather(self, state=None):
        self.preview.live_weather = self.live_weather_cb.isChecked()
        self.preview.update()

    def update_pixel_shift(self, state=None):
        self.preview.pixel_shift = self.pixel_shift_cb.isChecked()
        self.preview.update()

    def handle_font_import(self, path):
        self.primary_font = path
        self.primary_font_label.setText(os.path.basename(path))
        font_id = QFontDatabase.addApplicationFont(path)
        self.font_cb.setFontFilters(QFontComboBox.FontFilter.AllFonts)
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                self.font_cb.setCurrentFont(QFont(families[0]))
                self.preview.primary_font_family = families[0]
        self.preview.primary_font = path
        self.preview.update()
        self.check_font_changed()

    def import_primary_font(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Font File", "", "Font Files (*.ttf *.otf)")
        if file:
            self.handle_font_import(file)

    def update_dino_font(self, font):
        self.preview.dino_font = font.family()
        self.preview.update()
        self.check_font_changed()

    def check_font_changed(self):
        if not hasattr(self, 'undo_font_btn') or not hasattr(self, 'saved_dino_font') or not hasattr(self, 'font_cb'):
            return
        current_primary = getattr(self, 'primary_font', "")
        current_dino = self.font_cb.currentFont().family()
        has_changed = (current_primary != self.saved_primary_font) or (current_dino != self.saved_dino_font)
        self.undo_font_btn.setVisible(has_changed)

    def revert_font(self):
        if self.saved_primary_font and os.path.exists(self.saved_primary_font):
            self.primary_font = self.saved_primary_font
            self.primary_font_label.setText(os.path.basename(self.primary_font))
            font_id = QFontDatabase.addApplicationFont(self.primary_font)
            self.font_cb.setFontFilters(QFontComboBox.FontFilter.AllFonts)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    self.preview.primary_font_family = families[0]
            self.preview.primary_font = self.primary_font
        else:
            self.saved_primary_font = ""
            self.primary_font = ""
            self.primary_font_label.setText("Default")
            self.preview.primary_font = ""
            self.preview.primary_font_family = "Google Sans"

        all_families = QFontDatabase.families()
        if self.saved_dino_font and self.saved_dino_font in all_families:
            target_dino = self.saved_dino_font
        else:
            target_dino = "Bungee"
            self.saved_dino_font = "Bungee"
            
        self.font_cb.blockSignals(True)
        self.font_cb.setCurrentFont(QFont(target_dino))
        self.font_cb.blockSignals(False)
        self.preview.dino_font = self.font_cb.currentFont().family()
        self.preview.update()
        self.check_font_changed()

    def handle_character_import(self, path):
        self.custom_character_image = path
        self.char_label.setText(os.path.basename(path))
        self.char_cb.blockSignals(True)
        self.char_cb.setCurrentText("Custom")
        self.char_cb.blockSignals(False)
        self.preview.character_type = "custom"
        self.preview.set_custom_character(path)
        self.check_char_changed()

    def import_character(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Character Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)")
        if file:
            self.handle_character_import(file)

    def update_character_type(self, text):
        char_type = text.lower()
        if char_type == "custom":
            if not getattr(self, "custom_character_image", "") or not os.path.exists(self.custom_character_image):
                self.import_character()
                if not getattr(self, "custom_character_image", ""):
                    self.char_cb.blockSignals(True)
                    self.char_cb.setCurrentText("Dino")
                    self.char_cb.blockSignals(False)
                    self.preview.character_type = "dino"
                    self.preview.update()
                    self.check_char_changed()
                    return
        self.preview.character_type = self.char_cb.currentText().lower()
        self.preview.update()
        self.check_char_changed()

    def check_char_changed(self):
        if not hasattr(self, 'undo_char_btn') or not hasattr(self, 'char_cb'):
            return
        current_type = self.char_cb.currentText()
        current_img = getattr(self, 'custom_character_image', "")
        has_changed = (current_type != self.saved_char_type) or (current_img != self.saved_char_image)
        self.undo_char_btn.setVisible(has_changed)

    def revert_character(self):
        if self.saved_char_image and os.path.exists(self.saved_char_image):
            self.custom_character_image = self.saved_char_image
            self.char_label.setText(os.path.basename(self.custom_character_image))
            self.preview.set_custom_character(self.custom_character_image)
        else:
            self.saved_char_image = ""
            self.custom_character_image = ""
            self.char_label.setText("Default")
            self.preview.set_custom_character("")

        target_type = self.saved_char_type if (self.saved_char_type == "Custom" and self.custom_character_image) else "Dino"
        self.saved_char_type = target_type
        self.char_cb.blockSignals(True)
        self.char_cb.setCurrentText(target_type)
        self.char_cb.blockSignals(False)
        self.preview.character_type = target_type.lower()
        self.preview.update()
        self.check_char_changed()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Bungee-Regular.ttf")
    if getattr(sys, 'frozen', False):
        font_path = os.path.join(sys._MEIPASS, "Bungee-Regular.ttf")
    QFontDatabase.addApplicationFont(font_path)
    
    # Parse Windows screensaver arguments manually
    # Windows passes things like '/c', '/p65535', or '/s'
    mode = 's'
    for arg in sys.argv[1:]:
        arg_lower = arg.lower()
        if arg_lower.startswith('/c') or arg_lower.startswith('-c'):
            mode = 'c'
        elif arg_lower.startswith('/p') or arg_lower.startswith('-p'):
            mode = 'p'
        elif arg_lower.startswith('/s') or arg_lower.startswith('-s'):
            mode = 's'
            
    config_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'Dinoscreener')
    config_path = os.path.join(config_dir, 'config.json')
    
    if mode == 'c':
        dialog = SettingsDialog(config_path)
        dialog.exec()
        sys.exit(0)
    elif mode == 'p':
        # Preview mode inside small settings window. Not supported gracefully in PyQt without heavy win32 embedding.
        sys.exit(0)
        
    # Standard full screen start mode
    default_config = {
        "accent_color": "#8F96BF",
        "show_info": True,
        "strict_exit": False,
        "enable_win_key": False,
        "brightness": 100,
        "clock_style": 1,
        "clock_scales": {"0": 0.45, "1": 0.45, "2": 0.45},
        "use_24hr": False,
        "leading_zero": False,
        "live_weather": False,
        "pixel_shift": False,
        "primary_font": "",
        "dino_font": "Bungee",
        "character_type": "dino",
        "custom_character_image": ""
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                default_config.update(json.load(f))
        except Exception:
            pass
            
    ex = CrispAestheticFlipClock(
        accent_color=default_config["accent_color"], 
        enable_win_key=default_config["enable_win_key"], 
        strict_exit=default_config["strict_exit"],
        show_info=default_config["show_info"],
        brightness=default_config.get("brightness", 100),
        clock_style=default_config.get("clock_style", 1),
        clock_scales=default_config.get("clock_scales", {"0": 0.45, "1": 0.45, "2": 0.45}),
        use_24hr=default_config.get("use_24hr", False),
        leading_zeros=default_config.get("leading_zeros", default_config.get("leading_zero", False)),
        config_path=config_path,
        full_config=default_config,
        ignore_media_keys=default_config.get("ignore_media_keys", False),
        dino_font=default_config.get("dino_font", "Bungee"),
        live_weather=default_config.get("live_weather", False),
        pixel_shift=default_config.get("pixel_shift", False),
        primary_font=default_config.get("primary_font", ""),
        character_type=default_config.get("character_type", "dino"),
        custom_character_image=default_config.get("custom_character_image", "")
    )
    sys.exit(app.exec())

