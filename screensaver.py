import sys
import math
import ctypes
import json
import os
import random
import time
import wave
import struct
import subprocess
import tempfile
import zipfile
import shutil
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QCheckBox, QPushButton, QColorDialog, QFormLayout, QSlider, 
    QFileDialog, QStackedWidget, QFrame, QGridLayout, QComboBox, QFontComboBox, 
    QStackedLayout, QGraphicsOpacityEffect, QProgressBar, QMessageBox, QSizePolicy,
    QStyle, QStyleOption
)
from PyQt6.QtCore import (
    Qt, QTimer, QTime, QRectF, QDate, QPointF, QByteArray, QThread,
    pyqtSignal, QPropertyAnimation, QEasingCurve, pyqtProperty,
    QParallelAnimationGroup, QSize, QUrl, QVariantAnimation, QRect, QPoint, QEvent
)
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QPen, QRadialGradient, QLinearGradient, QPainterPath, 
    QFontDatabase, QPixmap, QImage, QIcon, QBrush, QDesktopServices
)

APP_VERSION = "v6.0"
APP_NAME = "Dinoscreener"
APP_AUTHOR = "Kushal Arvind"
APP_GITHUB_REPO = "kushalarvindo/dinoscreener"
APP_GITHUB_URL = "https://github.com/kushalarvindo/dinoscreener"

SPRITE_B64 = 'iVBORw0KGgoAAAANSUhEUgAABNEAAABECAAAAACKI/xBAAAAAnRSTlMAAHaTzTgAAAoOSURBVHgB7J1bdqS4FkSDu7gPTYSh2AOATw1Pn6kBVA2FieiTrlesq6po8lgt0pj02b06E58HlRhXOCQBBcdxHMdxHOfDMeA7BfcIOI4VwISDKQhvK0O4H9iAobeFZSx8WIK0dqz4ztQRg1XdECNfX/CTGUDmNjJDP6MzuMnKKsQ0Y+Amyxnirurmx1KghAvWXoARAErEPUpAB/KzvK6YcAIl8lD2AtsCbENPS1XGwqMTSnvHhNOYgBV3mKlklKDqPUshMUIzsuzlOXFGW9AQS0C/lv/QMWrahOMoiKZL41HyUCRAdcKyDR0tVRkLD0+oV7Q7yLofm6w6rKbdrmNUL6NOyapMtGcUuixZ2WSHbsl+M97BoUX8TrpyrfGbJJ+saBQ0W9I6jnxF/ZO+4nqo66GQneo325keUjth7bFpX38MO6lbM+ZMaeOYETISzYzN9Wiy7shuyj4dI96JSQXuOMSlWcqkgQ2DSlVdUSIbWbVs2vJ41CvadDs0jTE63Y9NWO26r3x9MU3AzDGk1mQWZu2Bht6VaPzEXrl21gjyZRXNPnKFI8+TJnRKLEED24JNpaqqKBGx/C5oWLSlBR0+Pp4J5yM27YVydp8sX4p+SUGe661TuWE5Y78dtcDSX3u+oqWINjLmRm+wTsBUJWpK06pKaXZpJdbmhoH/LcByq6Rq+LMC+7Dl+OFjvzj2ObRJY/tOa1r/uUvDy9d9QaPz4utMP6ZDysxsPeScf3yly6bOfRbcemtPYESvpAn20GSS0efVKOGc4aNQgojj1ZnzvTEnkxqzOVfGllP3y9qnZ0S3pM2mK5jMwQcpiMb1ZVqdkBANl1aCFbBbdOR6Pvwgtjiu9vkx60jrXNpq15E8ywhz/2tbzGQQwQ4b59Zfe7aipVrSEhCP8mZG1UlzZ20tOgw9Hw6hrzCLZiyObqCkVauZFC0OPL8nqUrk/zHN1gopOfkzngH3fv8SQau20jtMQ09VUSmxQUS1OsZSDAWSwKNFq5SylzA6PhFf+Oo4x3m0pEuYKXb4s5WLAAaT1lwfc3Kr6CDZ6JD6hrUCWVhmjHFrzNk17pxWjdGl/Yi9AuBrBqAbusmvGNNCyWpbhvPU82j1aDMi9Q04p8aLaQtiw7plXZ0A7TwDSojO/GsCiAnE6qAGhg45/eAu7csrunGcEUpEN5NsXYDlUY6Mie67UGPTPiiO1xl0vgLYvXt83glmvkux7ke6WdGzz7mKmiSQM2ufmPEoQUv9d2fu3jEazGqc79JUQjRxghoZT9FoiJnjzvbYtDJGOXOcoxUt4hMybAucE3nloJPOSJh5v6cm8gwFWrnn72aj1txnvR+5RrzoXy8kBOAStWBtw/foGvd1NnyX+h2a+LXQUH2XKAFT0uLpi9byzXg2vrzy9Z6eAZmqIUnHoaJ9PlIofwaAYQMWu6XituAE6vWBgifhla/Xp3ClqjpFESRdt5Z+WCIkQ68vHNBAXysZH3CmuufhInRurCagvLk6QNXpbwMDNvouu+Vn/fLeVo3rA084PzAYiwDtzB1jIB3Jmvuc0YqzQRk6W0d8LhIQ9gPkNhSpEGjr2HKW4XyOuznthx/M+8V/W5+7/vRZ9yARQ4L5a18IIBetJbN18/oGYNjRHwyHt6qiJSj9R25zZ55M7Uiq6u3qglDF2KmBCqqTVqhNO0bQSp+gxRJkV9fi68uP/z8TzgYd3tyw9bQOqBUtpmdd9wwlGoGKGzDstMR7LR1EtENp582d1z5jL3yGrc79y83pSsbBZHquNluXZd5DfteKbbhaLc+Ongp1tUslUUvDve1drSPuSFoE2o/8AIL6rspChrbqZkkb0N5yhNa2E3B95Bm2vN+8m/me3lE9WaGp3LbPPDc/u9VZoJFbZ+uoCvaMhAJEDTS2xOO/Tdzp+Xs6C3mG7fXhnXlR4gnx4rXU7dma/FTl0YS29beOjztTx6NOUF2aVrNEe/bZa4m6+nmuEJUAbnFP15xH+/7fHU/FYG6LG+SmVL5bmnFZ/Ho0J4WP4NK4KMCtS7u0p/Bo9ngnXbfWXnVu/DcNdGf9rRgfeab6sWfR1KXZ1Z0kY7+l3rIToQCImiD2U9y4FepFaHm44jpJjDTGlOmfxVbGHMc92nkEW/PrrRSKJiqjF4CiHaqBNqEuLPxDLsGL/+xcvFavbLph6W89TdHCw5wZCW2zXggfe4Sqcc2oBhYYSAc+EY4zGhM5/teid0osBSaaBC3F/vPAjvpxsdDx5Dp1jjsnI7Y+95hT5z+erpZkzB/dpY2wJS0FPfLH0/wsj/AhJS0FJuTaWOPbHWFbN/9VdCUSwtPW5g81j2aMZULDkbtLE+GSBKOCdGiCURtVTXFpp7KCuEtzl3braVVFQ+g/8n6eQil/X24MmjAIe+oYJNqwK2M8uU5mXc8652rXOY6vdZ6NvdyoiXZ1jBqNcC7o0tKVaw2XlltdGs0VUwsYGTpbxwPO1JXcU7gTGLYfrx0tx6tjsW/PsjHd14p2l+YOzXGPdirBDAwdLe9sAf54IEh86zLA2qQj64SGYp9EM674Dk9Rqy4tY58B2MRqVRZOIr2t44FnymfRzlyJSOHBLg2rOzSnn5vxjI3O1hHXxyVNb8zqt2mNi6OrGzR9egPfH1QLREQgFSDs17Ky/zOoS+O7wVJNfN1axjh108L93G8dH3umelx7gGMTCuLbbfJEQZEYha6KGTbN9l2r+zNn2xkwLnzorNWqsLVP0eaGXMZ74pLWDNXLL0N7+GRnAmdqwgNqE4O7tQkREQmp+zMoudWlATcMaIRN28ErA5nv9pF/6PtEnak/1r8H53lRR6bcfuYe0DrCcZxL3vdk19PHBZQz73u6AT0ODZWGbTAY33Ud0nEcZ3hg64gmZjiO81YiCkK1dXytBauO/wwzsmxBqc3VIhP6DVNw5FhFywDS24/cKeHRCdLfoTiO3zMw58+uYUX/HYD2BLETinY4Z5Bk6+jaFo79DFm3LG4Q+pr6r97I5pH7pRsllgiQUEJ7QsSRCdN2aYfjuEczNDnollPLSKm/7EhQ6pgQ2yUKpx3OaQTZOra2gf7P0M/Q3+ScTJlLX6KgECb49h02lFLudPzVzn0lNQwEURQdrfGuc9anX34AIzk21c/xHjLYCo/JU2W1kLTm/7BeP7kkSZIkZbj0JhHZgDdAg5UeAA6f9f8Ar//eMZqUxs8ggs7BhAEarPQAsPm+hwFus4SnG6Mx3pI0xwEX/syoMMDteO0x17QlCd5m/CbX0STs9m3RDggXBLpKWv5S83eSF787y1Wd5apuCcXDHFu0HL1wPGbhz6lL2WL2VYrtE6NPZW7usXAEy1WZ5epGInCMMLhTBsCQ5erTyhXVlAASQROIjO0FvHBFh+evzparEMvVsp8XMGZ5HuHL3cZGzpu884kxZtN/1HLVynL1uiRJkvQFUg1OaKSaqSkAAAAASUVORK5CYII='
class CrispAestheticFlipClock(QWidget):
    def __init__(self, accent_color="#8F96BF", enable_win_key=False, strict_exit=False, show_info=True, preview_mode=False, brightness=100, clock_style=1, clock_scales=None, use_24hr=False, leading_zeros=None, config_path=None, full_config=None, ignore_media_keys=False, dino_font="Bungee", live_weather=False, pixel_shift=False, primary_font="", character_type="dino", custom_character_image="", show_weather=True, show_battery=True, use_fahrenheit=False, ambient_mode=False, hourly_chime=False, chime_preset="acoustic_bell", chime_volume=45, custom_chime_path="", parent=None):
        super().__init__(parent)
        self.last_pos = None
        self.enable_frame_caching = False
        self.cached_frame = None
        self.clock_scales = clock_scales if clock_scales else {"0": 0.45, "1": 0.45, "2": 0.45}
        self.config_path = config_path
        self.full_config = full_config if full_config else {}
        
        self.target_time = QTime.currentTime()
        self.old_time = self.target_time
        
        self.animating = False
        self.anim_progress = 0.0
        self.time_elapsed = 0.0 
        self.scale_callback = None
        self.hourly_chime = hourly_chime
        self.chime_preset = chime_preset
        self.chime_volume = chime_volume
        self.custom_chime_path = custom_chime_path
        self.last_chime_hour = -1
        self.dino_frame_step = 0.0
        
        # States
        self.show_bg = ambient_mode
        self.bg_opacity = 1.0 if ambient_mode else 0.0
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
        self.show_weather = show_weather
        self.show_battery = show_battery
        self.use_fahrenheit = use_fahrenheit
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
        self.primary_font_family = ""
        
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
                        
        self.weather_temp = 24
        self.weather_code = 0  # 0 is clear sky
        self.weather_loaded = False
        
        if getattr(self, "live_weather", False) or (getattr(self, "show_weather", True) and not self.preview_mode):
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

        # High-Refresh Rate & Delta Frame Pacing (Smooth on 165Hz, 144Hz, 120Hz, 60Hz)
        screen = QApplication.primaryScreen()
        hz = screen.refreshRate() if screen else 60.0
        if not hz or hz <= 30.0:
            hz = 60.0
        self.display_hz = hz
        self.target_frame_interval = max(5, int(round(1000.0 / hz)))
        self.last_frame_time = time.perf_counter()

        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.updateAnimation)
        self.anim_timer.start(self.target_frame_interval)


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
            # Restore native high-refresh rate for flip card animation
            if hasattr(self, 'anim_timer') and hasattr(self, 'target_frame_interval'):
                self.anim_timer.setInterval(self.target_frame_interval)

        # Hourly chime (Flip Clock mode, top of the hour :00, non-preview)
        if self.hourly_chime and self.clock_style == 0 and not self.preview_mode:
            if now.minute() == 0 and now.hour() != self.last_chime_hour:
                self.last_chime_hour = now.hour()
                play_chime(
                    preset=getattr(self, 'chime_preset', 'acoustic_bell'),
                    volume=getattr(self, 'chime_volume', 45),
                    custom_path=getattr(self, 'custom_chime_path', '')
                )

    def updateAnimation(self):
        now_time = time.perf_counter()
        if not hasattr(self, 'last_frame_time'):
            self.last_frame_time = now_time
        dt = max(0.001, min(0.05, now_time - self.last_frame_time))
        self.last_frame_time = now_time
        time_factor = dt / 0.0166667

        if self.show_bg and self.bg_opacity < 1.0:
            self.bg_opacity = min(1.0, self.bg_opacity + (0.04 * time_factor))
        elif not self.show_bg and self.bg_opacity > 0.0:
            self.bg_opacity = max(0.0, self.bg_opacity - (0.04 * time_factor))
            
        self.time_elapsed += dt
        
        # Dino Game Loop with Delta-Time Physics (Buttery smooth on 165Hz)
        if self.clock_style == 2:
            self.dino_timer_msec += int(dt * 1000)
            
            if not self.dino_dead:
                # Physics scaled by time factor
                self.dino_y += self.dino_vy * time_factor
                if self.dino_y > 0:
                    self.dino_vy -= 0.6 * time_factor # gravity
                else:
                    self.dino_y = 0
                    self.dino_vy = 0
                
                # Ground scroll scaled by time factor
                self.ground_x -= self.dino_speed * time_factor
                if self.ground_x <= -1200:
                    self.ground_x += 1200

                # Clouds
                if len(self.dino_clouds) < 3:
                    if random.random() < (0.01 * time_factor):
                        self.dino_clouds.append({'x': self.width() + 100, 'y': random.randint(int(self.height()*0.5), int(self.height()*0.75)), 'speed': self.dino_speed * 0.2})
                for c in self.dino_clouds:
                    c['x'] -= c['speed'] * time_factor
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
                    obs['x'] -= self.dino_speed * time_factor
                
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
                                
            self.dino_frame_step += time_factor
            if self.dino_frame_step >= 1.0:
                steps = int(self.dino_frame_step)
                self.dino_frame = (self.dino_frame + steps) % 20
                self.dino_frame_step -= steps
        
        if self.animating:
            self.anim_progress += 0.035 * time_factor
            if self.anim_progress >= 1.0:
                self.anim_progress = 1.0
                self.animating = False
                self.old_time = self.target_time

        # Dynamic Frame Throttle (Power Optimization):
        # When Flip Clock is static (not animating, no ambient glow, and not preview mode),
        # throttle frame timer from 165Hz/60Hz down to 1000ms (1 FPS), dropping CPU usage to < 0.5%
        if not self.preview_mode and self.clock_style == 0 and not self.animating and not self.show_bg and self.bg_opacity <= 0.0:
            if self.anim_timer.interval() != 1000:
                self.anim_timer.setInterval(1000)
        else:
            if hasattr(self, 'target_frame_interval') and self.anim_timer.interval() != self.target_frame_interval:
                self.anim_timer.setInterval(self.target_frame_interval)
                
        self.update()
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
        families = []
        if getattr(self, "primary_font_family", ""):
            families.append(self.primary_font_family)
        families.extend(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
        font.setFamilies(families)
        font.setPixelSize(int(h * 0.65)) 
        font.setWeight(QFont.Weight.Black) 
        font.setStretch(90) 
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
        font.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
        painter.setFont(font)
        
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

        if ampm:
            font_ampm = QFont()
            font_ampm.setFamilies(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
            font_ampm.setPixelSize(int(h * 0.09))
            font_ampm.setWeight(QFont.Weight.Bold)
            font_ampm.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
            font_ampm.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
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

        # Helper for crisp DirectWrite subpixel antialiased text (Original Google Sans / Product Sans aesthetic)
        def make_rotary_font(sz, weight=QFont.Weight.Normal):
            f = QFont()
            families = ["Google Sans", "Product Sans", "Segoe UI", "Arial"]
            f.setFamilies(families)
            f.setPixelSize(int(sz))
            f.setWeight(weight)
            f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
            f.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
            return f

        # --- MINUTE WHEEL ---
        def draw_minute_wheel(radius, val_float, font_size):
            font = make_rotary_font(font_size, QFont.Weight.Medium)
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
                
                # 1. Render number upright with zero painter rotation (DirectWrite Subpixel ClearType)
                if i % 5 == 0 and text_opacity > 0.01:
                    rad = math.radians(angle_deg)
                    tx = cx + radius * math.cos(rad)
                    ty = cy + radius * math.sin(rad)
                    
                    color = QColor(muted_grey)
                    color.setAlpha(int(255 * text_opacity))
                    painter.setPen(color)
                    painter.setFont(font)
                    
                    box_size = w * 0.1
                    text_rect = QRectF(tx - box_size/2, ty - box_size/2, box_size, box_size)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, f"{i:02d}")

                # 2. Rotated Tick Lines
                painter.save()
                painter.translate(cx, cy)
                painter.rotate(angle_deg)
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
            font = make_rotary_font(font_size, QFont.Weight.Medium)
            tick_offset = w * 0.022 
            
            for i in range(60):
                angle_deg = (val_float - i) * 6.0
                norm_angle = (angle_deg + 180) % 360 - 180
                
                opacity = max(0.0, 1.0 - abs(norm_angle) / 75.0) 
                if opacity <= 0.01: continue
                
                # 1. Render number upright with zero painter rotation (DirectWrite Subpixel ClearType)
                if i % 5 == 0:
                    rad = math.radians(angle_deg)
                    tx = cx + radius * math.cos(rad)
                    ty = cy + radius * math.sin(rad)
                    
                    color = QColor(accent_color)
                    color.setAlpha(int(255 * opacity))
                    painter.setPen(color)
                    painter.setFont(font)
                    
                    box_size = w * 0.1
                    text_rect = QRectF(tx - box_size/2, ty - box_size/2, box_size, box_size)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, f"{i:02d}")

                # 2. Rotated Tick Lines
                painter.save()
                painter.translate(cx, cy)
                painter.rotate(angle_deg)
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
        font_min_fixed = make_rotary_font(h * 0.070, QFont.Weight.Bold)
        painter.setFont(font_min_fixed)
        painter.setPen(pure_white)
        min_rect = QRectF(cx + R_min - w*0.05, cy - h*0.05, w*0.1, h*0.1)
        painter.drawText(min_rect, Qt.AlignmentFlag.AlignCenter, f"{now.minute():02d}")

        # 4. Hard-Anchored Left Hour
        font_hr = make_rotary_font(h * 0.28, QFont.Weight.Normal)
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
        font_date_1 = make_rotary_font(h * 0.022, QFont.Weight.Normal)
        font_date_1.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 4.0)
        
        font_date_2 = make_rotary_font(h * 0.038, QFont.Weight.Bold)
        font_date_2.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 3.0)
        
        painter.setFont(font_date_1)
        painter.setPen(accent_color)
        painter.drawText(QRectF(date_x, offset_y - h * 0.10, box_w, h * 0.08), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom, date_str_1)
        
        painter.setFont(font_date_2)
        painter.setPen(pure_white)
        painter.drawText(QRectF(date_x, offset_y - h * 0.01, box_w, h * 0.08), Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, date_str_2)
        
        show_w = getattr(self, 'show_weather', True)
        show_b = getattr(self, 'show_battery', True)
        use_f = getattr(self, 'use_fahrenheit', False)
        
        if self.show_info and (show_w or show_b):
            info_y = offset_y + h * 0.05
            info_h = h * 0.04
            
            font_info = QFont(["Segoe UI Variable Text", "Segoe UI", "Arial"])
            font_info.setPixelSize(int(h * 0.016))
            font_info.setWeight(QFont.Weight.Medium)
            font_info.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.0)
            font_info.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
            painter.setFont(font_info)
            fm = painter.fontMetrics()
            
            # Weather text
            c_temp = getattr(self, 'weather_temp', 24)
            if use_f:
                f_temp = int(c_temp * 9 / 5 + 32)
                weather_text = f"{f_temp}\u00B0F"
            else:
                weather_text = f"{c_temp}\u00B0C"
                
            w_text_width = fm.horizontalAdvance(weather_text)
            emoji_w = w * 0.012
            w_gap = w * 0.004
            weather_total_w = emoji_w + w_gap + w_text_width
            w_icon_size = h * 0.016
            
            # Battery text & status
            bat_text = "100%"
            bat_val = 100
            is_charging = False
            if sys.platform.startswith("win32"):
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
            elif sys.platform.startswith("linux"):
                try:
                    import glob
                    bat_paths = glob.glob("/sys/class/power_supply/BAT*")
                    if bat_paths:
                        cap_file = os.path.join(bat_paths[0], "capacity")
                        status_file = os.path.join(bat_paths[0], "status")
                        if os.path.exists(cap_file):
                            with open(cap_file, "r") as f:
                                bat_val = int(f.read().strip())
                                bat_text = f"{bat_val}%"
                        if os.path.exists(status_file):
                            with open(status_file, "r") as f:
                                is_charging = (f.read().strip().lower() == "charging")
                except Exception:
                    pass
                
            bat_icon_w = w * 0.019
            bat_icon_h = h * 0.015
            b_gap = w * 0.005
            bat_text_w = fm.horizontalAdvance(bat_text)
            battery_total_w = bat_icon_w + b_gap + bat_text_w
            bat_icon_y = info_y + info_h/2 - bat_icon_h/2
            
            # Coordinate layout
            if show_w and show_b:
                weather_icon_x = center_x - w * 0.02 - weather_total_w
                weather_text_x = weather_icon_x + emoji_w + w_gap
                bat_icon_x = center_x + w * 0.02
                bat_text_x = bat_icon_x + bat_icon_w + b_gap
                
                # Center separator dot
                painter.setPen(QColor(120, 125, 130))
                painter.drawText(QRectF(center_x - w*0.01, info_y, w*0.02, info_h), Qt.AlignmentFlag.AlignCenter, "\u2022")
            elif show_w:
                weather_icon_x = center_x - weather_total_w / 2
                weather_text_x = weather_icon_x + emoji_w + w_gap
            elif show_b:
                bat_icon_x = center_x - battery_total_w / 2
                bat_text_x = bat_icon_x + bat_icon_w + b_gap
                
            # Render Weather
            if show_w:
                painter.save()
                painter.translate(weather_icon_x + emoji_w/2, info_y + info_h/2)
                painter.setPen(Qt.PenStyle.NoPen)
                code = getattr(self, 'weather_code', 0) if getattr(self, "live_weather", False) else 0
                if code in [0, 1]:
                    painter.setBrush(QColor(255, 210, 80))
                    painter.drawEllipse(QRectF(-w_icon_size*0.4, -w_icon_size*0.4, w_icon_size*0.8, w_icon_size*0.8))
                elif code in [2, 3, 45, 48]:
                    painter.setBrush(QColor(180, 190, 200))
                    painter.drawEllipse(QRectF(-w_icon_size*0.4, -w_icon_size*0.2, w_icon_size*0.8, w_icon_size*0.5))
                    painter.drawEllipse(QRectF(-w_icon_size*0.2, -w_icon_size*0.4, w_icon_size*0.5, w_icon_size*0.5))
                elif 50 <= code <= 67 or 80 <= code <= 82:
                    painter.setBrush(QColor(100, 150, 255))
                    path = QPainterPath()
                    path.moveTo(0, -w_icon_size*0.4)
                    path.lineTo(-w_icon_size*0.3, w_icon_size*0.1)
                    path.arcTo(QRectF(-w_icon_size*0.3, -w_icon_size*0.2, w_icon_size*0.6, w_icon_size*0.6), 180, 180)
                    path.closeSubpath()
                    painter.drawPath(path)
                elif 70 <= code <= 77 or 85 <= code <= 86:
                    painter.setPen(QPen(QColor(255, 255, 255), 2))
                    painter.drawLine(int(-w_icon_size*0.3), 0, int(w_icon_size*0.3), 0)
                    painter.drawLine(0, int(-w_icon_size*0.3), 0, int(w_icon_size*0.3))
                    painter.drawLine(int(-w_icon_size*0.2), int(-w_icon_size*0.2), int(w_icon_size*0.2), int(w_icon_size*0.2))
                    painter.drawLine(int(-w_icon_size*0.2), int(w_icon_size*0.2), int(w_icon_size*0.2), int(-w_icon_size*0.2))
                elif 95 <= code <= 99:
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
                    painter.setBrush(QColor(255, 210, 80))
                    painter.drawEllipse(QRectF(-w_icon_size*0.4, -w_icon_size*0.4, w_icon_size*0.8, w_icon_size*0.8))
                painter.restore()
                
                painter.setFont(font_info)
                painter.setPen(QColor(230, 235, 240))
                painter.drawText(QRectF(weather_text_x, info_y, w_text_width, info_h), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, weather_text)
                
            # Render Battery
            if show_b:
                painter.setPen(QPen(QColor(255, 255, 255), 1.5))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawRoundedRect(QRectF(bat_icon_x, bat_icon_y, bat_icon_w, bat_icon_h), 2, 2)
                
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(QColor(255, 255, 255))
                painter.drawRoundedRect(QRectF(bat_icon_x + bat_icon_w + 1.5, bat_icon_y + bat_icon_h*0.3, w*0.0015, bat_icon_h*0.4), 1, 1)
                
                fill_margin = 2.5
                fill_w = (bat_icon_w - fill_margin * 2) * (bat_val / 100.0)
                fill_h = bat_icon_h - fill_margin * 2
                if bat_val <= 20:
                    painter.setBrush(QColor(255, 80, 80))
                else:
                    painter.setBrush(QColor(160, 230, 160))
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
                    painter.setBrush(QColor(255, 255, 255))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawPath(bolt)
                    painter.restore()
                    
                painter.setFont(font_info)
                painter.setPen(QColor(230, 235, 240))
                painter.drawText(QRectF(bat_text_x, bat_icon_y, bat_text_w + 5, bat_icon_h), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, bat_text)

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
        font_time.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
        font_time.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
        
        painter.setFont(font_time)
        painter.setPen(QColor(255, 255, 255))
        time_rect = QRectF(0, h * 0.05, w, scaled_size * 1.2)
        painter.drawText(time_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, time_str)
        
        base_date = int(h * 0.025)
        scaled_date = int(base_date * (self.clock_scales[str(self.clock_style)] / 0.45))
        date_str = QDate.currentDate().toString("dddd, d MMMM")
        font_date = QFont(["Segoe UI Variable Text", "Segoe UI", "Arial", "sans-serif"])
        font_date.setPixelSize(scaled_date)
        font_date.setWeight(QFont.Weight.DemiBold)
        font_date.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
        font_date.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
        
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        painter.setFont(font_date)
        painter.setPen(QColor(245, 248, 252))
        date_y = h * 0.05 + scaled_size * 1.30
        date_rect = QRectF(0, date_y, w, scaled_date * 2)
        painter.drawText(date_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, date_str)
        painter.restore()
        
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
            font_dead.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
            font_dead.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
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

    def render_clock_canvas(self, painter, w, h):
        if self.preview_mode:
            clip_path = QPainterPath()
            clip_path.addRoundedRect(QRectF(0, 0, w, h), 12, 12)
            painter.setClipPath(clip_path)

        painter.fillRect(QRectF(0, 0, w, h), QColor(0, 0, 0))
        
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
        
        if self.pixel_shift:
            mult = 0.4 if self.preview_mode else 1.0
            shift_x = int(round(math.sin(self.time_elapsed * 0.04) * (8.0 * mult)))
            shift_y = int(round(math.cos(self.time_elapsed * 0.025) * (6.0 * mult)))
            painter.save()
            painter.translate(shift_x, shift_y)
            if self.clock_style == 0:
                self.draw_flipclock_style(painter, w, h)
            elif self.clock_style == 1:
                self.draw_rotary_style(painter, w, h)
            else:
                self.draw_dino_style(painter, w, h)
            painter.restore()
        else:
            if self.clock_style == 0:
                self.draw_flipclock_style(painter, w, h)
            elif self.clock_style == 1:
                self.draw_rotary_style(painter, w, h)
            else:
                self.draw_dino_style(painter, w, h)
            
        # Apply brightness overlay
        if self.brightness < 100:
            overlay_alpha = 255 - int((self.brightness / 100.0) * 255)
            painter.fillRect(QRectF(0, 0, w, h), QColor(0, 0, 0, overlay_alpha))

    def paintEvent(self, event):
        w = self.width()
        h = self.height()
        if w <= 0 or h <= 0:
            return

        if getattr(self, 'enable_frame_caching', False):
            if not hasattr(self, 'cached_frame') or self.cached_frame is None or self.cached_frame.size() != self.size():
                self.cached_frame = QPixmap(self.size())
            p_buf = QPainter(self.cached_frame)
            p_buf.setRenderHint(QPainter.RenderHint.Antialiasing)
            p_buf.setRenderHint(QPainter.RenderHint.TextAntialiasing)
            p_buf.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            self.render_clock_canvas(p_buf, w, h)
            p_buf.end()
            
            p_screen = QPainter(self)
            p_screen.drawPixmap(0, 0, self.cached_frame)
            p_screen.end()
            
            if self.parent() and hasattr(self.parent(), 'on_clock_frame_rendered'):
                self.parent().on_clock_frame_rendered()
        else:
            p_screen = QPainter(self)
            p_screen.setRenderHint(QPainter.RenderHint.Antialiasing)
            p_screen.setRenderHint(QPainter.RenderHint.TextAntialiasing)
            p_screen.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            self.render_clock_canvas(p_screen, w, h)
            p_screen.end()

    def keyPressEvent(self, event):
        if hasattr(self, 'anim_timer') and hasattr(self, 'target_frame_interval'):
            self.anim_timer.setInterval(self.target_frame_interval)

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
        
    def set_stage_theme(self, clock_style, accent_hex):
        pass
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        
        # Deep black true screensaver display
        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(QRectF(0, 0, w, h), 14, 14)
        
        # Subtle glass specular border
        border_pen = QPen(QColor(255, 255, 255, 25), 1)
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(0.5, 0.5, w - 1, h - 1), 14, 14)


def get_windows_accent_color():
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM")
        val, _ = winreg.QueryValueEx(key, "AccentColor")
        r = val & 0xFF
        g = (val >> 8) & 0xFF
        b = (val >> 16) & 0xFF
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        pass
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Accent")
        val, _ = winreg.QueryValueEx(key, "AccentColorMenu")
        r = val & 0xFF
        g = (val >> 8) & 0xFF
        b = (val >> 16) & 0xFF
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        pass
    return "#0078D4"


if sys.platform == "win32":
    class DWM_MARGINS(ctypes.Structure):
        _fields_ = [
            ("cxLeftWidth", ctypes.c_int),
            ("cxRightWidth", ctypes.c_int),
            ("cyTopHeight", ctypes.c_int),
            ("cyBottomHeight", ctypes.c_int),
        ]


def apply_windows_dwm_effects(dialog):
    """
    Enables Windows 11 DWM dark titlebar, Mica / Acrylic backdrop, and glass frame extension.
    Gracefully falls back on older Windows builds or unsupported platforms without crashing.
    Returns True if DWM backdrop/blur was successfully enabled, False otherwise.
    """
    if sys.platform != "win32":
        return False
        
    try:
        # Pre-set Qt translucency flags so DirectComposition surface is initialized with alpha
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        dialog.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        hwnd = int(dialog.winId())
        if not hwnd:
            dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
            return False
            
        dwmapi = ctypes.windll.dwmapi
        
        # 1. Enable Windows 11 Dark Mode Titlebar & Frame (DWMWA_USE_IMMERSIVE_DARK_MODE = 20)
        dark_mode = ctypes.c_int(1)
        dwmapi.DwmSetWindowAttribute(
            hwnd, 20, ctypes.byref(dark_mode), ctypes.sizeof(dark_mode)
        )
        
        # 2. Apply Mica / Acrylic System Backdrop (Windows 11 22H2+ / Build 22621+):
        # DWMWA_SYSTEMBACKDROP_TYPE = 38
        # DWMSBT_MAINWINDOW = 2 (Mica), DWMSBT_TABBEDWINDOW = 4 (Mica Alt), DWMSBT_TRANSIENTWINDOW = 3 (Acrylic)
        applied_backdrop = False
        for backdrop_val in (2, 4, 3):
            backdrop_type = ctypes.c_int(backdrop_val)
            res = dwmapi.DwmSetWindowAttribute(
                hwnd, 38, ctypes.byref(backdrop_type), ctypes.sizeof(backdrop_type)
            )
            if res == 0:
                applied_backdrop = True
                break
                
        # Fallback for Windows 11 21H2 (Build 22000)
        if not applied_backdrop:
            mica_val = ctypes.c_int(1)
            res_mica = dwmapi.DwmSetWindowAttribute(
                hwnd, 1029, ctypes.byref(mica_val), ctypes.sizeof(mica_val)
            )
            if res_mica == 0:
                applied_backdrop = True
                
        # 3. Extend glass frame into client area for DWM & DWMGlassBlur hookers
        margins = DWM_MARGINS(-1, -1, -1, -1)
        res_frame = dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))
        
        if applied_backdrop or res_frame == 0:
            return True
            
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        return False
    except Exception:
        try:
            dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        except Exception:
            pass
        return False


def get_color_variants(hex_color):
    hex_clean = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    text_color = "#0B0F19" if lum > 140 else "#FFFFFF"
    
    if lum > 140:
        hover_r, hover_g, hover_b = max(0, r - 20), max(0, g - 20), max(0, b - 20)
        press_r, press_g, press_b = max(0, r - 35), max(0, g - 35), max(0, b - 35)
    else:
        hover_r, hover_g, hover_b = min(255, r + 25), min(255, g + 25), min(255, b + 25)
        press_r, press_g, press_b = max(0, r - 25), max(0, g - 25), max(0, b - 25)
        
    hover_hex = f"#{hover_r:02x}{hover_g:02x}{hover_b:02x}"
    press_hex = f"#{press_r:02x}{press_g:02x}{press_b:02x}"
    return text_color, hover_hex, press_hex


def get_or_create_check_icon(color_hex="#FFFFFF"):
    import tempfile
    clean_col = color_hex.replace("#", "")
    temp_path = os.path.join(tempfile.gettempdir(), f"dinoscreener_chk_{clean_col}.svg").replace("\\", "/")
    svg_data = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
<path d="M4.5 12.5l5 5L19.5 6.5" fill="none" stroke="{color_hex}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(svg_data)
    except Exception:
        pass
    return temp_path


def get_or_create_chevron_icon():
    import tempfile
    temp_path = os.path.join(tempfile.gettempdir(), "dinoscreener_chevron.svg").replace("\\", "/")
    svg_data = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
<path d="M6 9.5l6 5.5 6-5.5" fill="none" stroke="#B4C3D7" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(svg_data)
    except Exception:
        pass
    return temp_path


def get_or_create_fullscreen_duotone_icon(accent_hex):
    import tempfile
    clean_col = accent_hex.replace("#", "")
    temp_path = os.path.join(tempfile.gettempdir(), f"dinoscreener_fs_duotone_{clean_col}.svg").replace("\\", "/")
    svg_data = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <path d="M4 9V4h5M20 15v5h-5" fill="none" stroke="{accent_hex}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M15 4h5v5M9 20H4v-5" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="10.5" y="10.5" width="3" height="3" rx="0.8" fill="{accent_hex}"/>
</svg>"""
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(svg_data)
    except Exception:
        pass
    icon = QIcon(temp_path)
    for sz in [20, 24, 32, 40, 48, 64]:
        pix = QPixmap(sz, sz)
        pix.fill(Qt.GlobalColor.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        accent_q = QColor(accent_hex)
        white_q = QColor(255, 255, 255, 240)
        s = sz / 24.0
        pen_acc = QPen(accent_q, 2.2 * s, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        pen_w = QPen(white_q, 2.2 * s, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        p.setPen(pen_acc)
        p.drawLine(QPointF(4 * s, 9 * s), QPointF(4 * s, 4 * s))
        p.drawLine(QPointF(4 * s, 4 * s), QPointF(9 * s, 4 * s))
        p.drawLine(QPointF(20 * s, 15 * s), QPointF(20 * s, 20 * s))
        p.drawLine(QPointF(20 * s, 20 * s), QPointF(15 * s, 20 * s))
        p.setPen(pen_w)
        p.drawLine(QPointF(15 * s, 4 * s), QPointF(20 * s, 4 * s))
        p.drawLine(QPointF(20 * s, 4 * s), QPointF(20 * s, 9 * s))
        p.drawLine(QPointF(9 * s, 20 * s), QPointF(4 * s, 20 * s))
        p.drawLine(QPointF(4 * s, 20 * s), QPointF(4 * s, 15 * s))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(accent_q)
        p.drawRoundedRect(QRectF(10.5 * s, 10.5 * s, 3 * s, 3 * s), 0.8 * s, 0.8 * s)
        p.end()
        icon.addPixmap(pix)
    return icon


def get_or_create_info_duotone_icon(accent_hex):
    import tempfile
    clean_col = accent_hex.replace("#", "")
    temp_path = os.path.join(tempfile.gettempdir(), f"dinoscreener_info_duotone_{clean_col}.svg").replace("\\", "/")
    svg_data = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
  <circle cx="12" cy="12" r="9.5" fill="{accent_hex}" fill-opacity="0.22" stroke="{accent_hex}" stroke-width="1.8"/>
  <circle cx="12" cy="7.8" r="1.3" fill="#FFFFFF"/>
  <line x1="12" y1="11" x2="12" y2="16.5" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/>
</svg>"""
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(svg_data)
    except Exception:
        pass
    icon = QIcon(temp_path)
    for sz in [20, 24, 30, 40, 48, 64]:
        pix = QPixmap(sz, sz)
        pix.fill(Qt.GlobalColor.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        accent_q = QColor(accent_hex)
        accent_glow = QColor(accent_q.red(), accent_q.green(), accent_q.blue(), 55)
        white_q = QColor(255, 255, 255, 245)
        s = sz / 24.0
        p.setPen(QPen(accent_q, 1.8 * s))
        p.setBrush(QBrush(accent_glow))
        p.drawEllipse(QRectF(2.5 * s, 2.5 * s, 19 * s, 19 * s))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(white_q)
        p.drawEllipse(QRectF(10.7 * s, 6.5 * s, 2.6 * s, 2.6 * s))
        p.setPen(QPen(white_q, 1.8 * s, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawLine(QPointF(12 * s, 11 * s), QPointF(12 * s, 16.5 * s))
        p.end()
        icon.addPixmap(pix)
    return icon


def get_rounded_pixmap(src_path, size=38, radius=9, dpr=3.0):
    pix = QPixmap(src_path)
    if pix.isNull():
        return QPixmap()
    target_physical = int(size * dpr)
    scaled = pix.scaled(
        target_physical, 
        target_physical, 
        Qt.AspectRatioMode.KeepAspectRatio, 
        Qt.TransformationMode.SmoothTransformation
    )
    dest = QPixmap(target_physical, target_physical)
    dest.fill(Qt.GlobalColor.transparent)
    p = QPainter(dest)
    p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    path = QPainterPath()
    path.addRoundedRect(QRectF(0, 0, target_physical, target_physical), radius * dpr, radius * dpr)
    p.setClipPath(path)
    ox = (target_physical - scaled.width()) // 2
    oy = (target_physical - scaled.height()) // 2
    p.drawPixmap(ox, oy, scaled)
    p.end()
    dest.setDevicePixelRatio(dpr)
    return dest


class CollapsibleModeCapsule(QFrame):
    def __init__(self, win_accent="#0078D4", parent=None):
        super().__init__(parent)
        self.win_accent = win_accent
        self._current_mode = 0
        self._modes = [
            ("Flip Clock", 0),
            ("Rotary Modern", 1),
            ("Dino Runner", 2)
        ]
        self._is_expanded = False
        self._collapsed_width = 152
        self._expanded_width = 376
        self._width = self._collapsed_width
        
        self.setFixedHeight(38)
        self.setFixedWidth(self._collapsed_width)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.setStyleSheet("""
            QFrame#capsuleFrame {
                background: rgba(23, 27, 38, 0.82);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 19px;
            }
            QFrame#capsuleFrame:hover {
                border: 1px solid rgba(255, 255, 255, 0.22);
                background: rgba(26, 31, 45, 0.88);
            }
        """)
        self.setObjectName("capsuleFrame")
        
        self.stack = QStackedLayout(self)
        self.stack.setContentsMargins(0, 0, 0, 0)
        self.stack.setStackingMode(QStackedLayout.StackingMode.StackOne)
        
        # --- Page 0: Collapsed Pill View ---
        self.collapsed_view = QWidget()
        col_layout = QHBoxLayout(self.collapsed_view)
        col_layout.setContentsMargins(18, 0, 18, 0)
        col_layout.setSpacing(0)
        
        # Center title (always 100% centered with symmetrical margins)
        self.lbl_mode_name = QLabel("Flip Clock")
        self.lbl_mode_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_mode_name.setStyleSheet("""
            color: #FFFFFF;
            font-size: 11.5px;
            font-weight: 600;
            font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
            background: transparent;
        """)
        
        col_layout.addWidget(self.lbl_mode_name)
        self.stack.addWidget(self.collapsed_view)
        
        # --- Page 1: Expanded 3-Button View ---
        self.expanded_view = QWidget()
        exp_layout = QHBoxLayout(self.expanded_view)
        exp_layout.setContentsMargins(3, 3, 3, 3)
        exp_layout.setSpacing(4)
        
        self.mode_buttons = []
        for label, idx in self._modes:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setFixedSize(118, 32)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #94A3B8;
                    border: 1px solid transparent;
                    border-radius: 16px;
                    font-size: 11.5px;
                    font-weight: 500;
                    outline: none;
                    font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
                }
                QPushButton:hover:!checked {
                    color: #FFFFFF;
                    background: rgba(255, 255, 255, 0.08);
                    border-radius: 16px;
                }
                QPushButton:checked {
                    background: #252B3B;
                    color: #FFFFFF;
                    font-weight: 600;
                    border: 1px solid rgba(255, 255, 255, 0.18);
                    border-radius: 16px;
                }
            """)
            btn.clicked.connect(lambda checked, i=idx: self.select_mode(i))
            exp_layout.addWidget(btn)
            self.mode_buttons.append(btn)
            
        self.stack.addWidget(self.expanded_view)
        self.stack.setCurrentIndex(0)
        
        self.opacity_effect = QGraphicsOpacityEffect(self.expanded_view)
        self.expanded_view.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
        
        self.on_mode_changed = None
        self._anim_group = None
        self.set_current_mode(0)

    def enable_frosted_glass(self, studio):
        self.studio_parent = studio
        self.setStyleSheet("""
            QFrame#capsuleFrame {
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 19px;
            }
            QFrame#capsuleFrame:hover {
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.22);
            }
        """)

    def paintEvent(self, event):
        if getattr(self, 'studio_parent', None):
            p_glass = QPainter(self)
            p_glass.setRenderHint(QPainter.RenderHint.Antialiasing)
            w_g, h_g = self.width(), self.height()
            top_left = self.mapTo(self.studio_parent, QPoint(0, 0))
            sample_rect = QRect(top_left.x(), top_left.y(), w_g, h_g)
            canvas_pix = getattr(self.studio_parent.clock, 'cached_frame', None)
            clip_g = QPainterPath()
            clip_g.addRoundedRect(QRectF(0, 0, w_g, h_g), 19, 19)
            p_glass.setClipPath(clip_g)
            if canvas_pix and not canvas_pix.isNull() and canvas_pix.rect().contains(sample_rect):
                sub = canvas_pix.copy(sample_rect)
                dw = max(4, w_g // 10)
                dh = max(4, h_g // 10)
                blurred = sub.scaled(dw, dh, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation).scaled(w_g, h_g, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
                p_glass.drawPixmap(0, 0, blurred)
            else:
                p_glass.fillRect(QRectF(0, 0, w_g, h_g), QColor(10, 14, 23))
            p_glass.fillRect(QRectF(0, 0, w_g, h_g), QColor(18, 21, 31, 192))
            border_pen = QPen(QColor(255, 255, 255, 31), 1.0)
            p_glass.setPen(border_pen)
            p_glass.setBrush(Qt.BrushStyle.NoBrush)
            p_glass.drawRoundedRect(QRectF(0.5, 0.5, w_g - 1.0, h_g - 1.0), 19, 19)
            p_glass.end()

        super().paintEvent(event)
        
        # Do not render edge indicator glows in expanded 3-button view
        if self._is_expanded:
            return
            
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        
        w = float(self.width())
        h = float(self.height())
        r = 19.0
        
        # Strictly clip to the pill's inner rounded boundary (1px inside the 1px border)
        clip_path = QPainterPath()
        clip_path.addRoundedRect(QRectF(1.0, 1.0, w - 2.0, h - 2.0), r - 1.0, r - 1.0)
        p.setClipPath(clip_path)
        
        # Soft periwinkle/accent hues
        c_peri = QColor("#a5b4fc")
        c_acc = QColor(self.win_accent)
        c_core = QColor("#e0e7ff")
        
        arc_r = r - 1.8
        arc_d = arc_r * 2.0
        
        # Directional Visibility Logic:
        # idx 0 (Flip Clock): ONLY Right indicator
        # idx 1 (Rotary Modern): BOTH Left and Right indicators
        # idx 2 (Dino Runner): ONLY Left indicator
        show_left = (self._current_mode in [1, 2])
        show_right = (self._current_mode in [0, 1])
        
        # Vertical gradient fading the top and bottom tips smoothly into transparency
        v_grad_bloom = QLinearGradient(0, 9, 0, 29)
        v_grad_bloom.setColorAt(0.0, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), 0))
        v_grad_bloom.setColorAt(0.2, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), 50))
        v_grad_bloom.setColorAt(0.5, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), 85))
        v_grad_bloom.setColorAt(0.8, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), 50))
        v_grad_bloom.setColorAt(1.0, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), 0))
        
        v_grad_core = QLinearGradient(0, 11, 0, 27)
        v_grad_core.setColorAt(0.0, QColor(c_core.red(), c_core.green(), c_core.blue(), 0))
        v_grad_core.setColorAt(0.3, QColor(c_core.red(), c_core.green(), c_core.blue(), 110))
        v_grad_core.setColorAt(0.5, QColor(c_core.red(), c_core.green(), c_core.blue(), 160))
        v_grad_core.setColorAt(0.7, QColor(c_core.red(), c_core.green(), c_core.blue(), 110))
        v_grad_core.setColorAt(1.0, QColor(c_core.red(), c_core.green(), c_core.blue(), 0))

        if show_left:
            # 1. Subtle radial aura
            grad_l = QRadialGradient(QPointF(1.0, h / 2.0), 12.0)
            grad_l.setColorAt(0.0, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), 45))
            grad_l.setColorAt(0.5, QColor(c_acc.red(), c_acc.green(), c_acc.blue(), 20))
            grad_l.setColorAt(1.0, QColor(c_acc.red(), c_acc.green(), c_acc.blue(), 0))
            p.setBrush(QBrush(grad_l))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(1.0, h / 2.0), 12.0, 12.0)
            
            # 2. Sleek crescent curved arc hugging the inner left border
            arc_rect_l = QRectF(1.8, (h - arc_d) / 2.0, arc_d, arc_d)
            
            # Bloom stroke
            pen_bloom = QPen(v_grad_bloom, 2.2)
            pen_bloom.setCapStyle(Qt.PenCapStyle.RoundCap)
            p.setPen(pen_bloom)
            p.drawArc(arc_rect_l, int(130 * 16), int(100 * 16))
            
            # Core stroke
            pen_core = QPen(v_grad_core, 1.1)
            pen_core.setCapStyle(Qt.PenCapStyle.RoundCap)
            p.setPen(pen_core)
            p.drawArc(arc_rect_l, int(145 * 16), int(70 * 16))
            
        if show_right:
            # 1. Subtle radial aura
            grad_r = QRadialGradient(QPointF(w - 1.0, h / 2.0), 12.0)
            grad_r.setColorAt(0.0, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), 45))
            grad_r.setColorAt(0.5, QColor(c_acc.red(), c_acc.green(), c_acc.blue(), 20))
            grad_r.setColorAt(1.0, QColor(c_acc.red(), c_acc.green(), c_acc.blue(), 0))
            p.setBrush(QBrush(grad_r))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(w - 1.0, h / 2.0), 12.0, 12.0)
            
            # 2. Sleek crescent curved arc hugging the inner right border
            arc_rect_r = QRectF(w - arc_d - 1.8, (h - arc_d) / 2.0, arc_d, arc_d)
            
            # Bloom stroke
            pen_bloom = QPen(v_grad_bloom, 2.2)
            pen_bloom.setCapStyle(Qt.PenCapStyle.RoundCap)
            p.setPen(pen_bloom)
            p.drawArc(arc_rect_r, int(-50 * 16), int(100 * 16))
            
            # Core stroke
            pen_core = QPen(v_grad_core, 1.1)
            pen_core.setCapStyle(Qt.PenCapStyle.RoundCap)
            p.setPen(pen_core)
            p.drawArc(arc_rect_r, int(-35 * 16), int(70 * 16))

        p.end()

    def get_capsule_width(self):
        return self._width

    def set_capsule_width(self, w):
        self._width = w
        self.setFixedWidth(w)

    capsuleWidth = pyqtProperty(int, get_capsule_width, set_capsule_width)

    def set_current_mode(self, idx):
        self._current_mode = idx
        if 0 <= idx < len(self._modes):
            self.lbl_mode_name.setText(self._modes[idx][0])
            
        for i, btn in enumerate(self.mode_buttons):
            btn.blockSignals(True)
            btn.setChecked(i == idx)
            btn.blockSignals(False)
            
        self.update()

    def update_accent(self, accent_hex):
        self.win_accent = accent_hex
        self.update()

    def select_mode(self, idx):
        self.set_current_mode(idx)
        if self.on_mode_changed:
            self.on_mode_changed(idx)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.expand()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.collapse()

    def expand(self):
        if self._is_expanded:
            return
        self._is_expanded = True
        
        if self._anim_group and self._anim_group.state() == QParallelAnimationGroup.State.Running:
            self._anim_group.stop()
            
        self.stack.setCurrentIndex(1)
        
        anim_w = QPropertyAnimation(self, b"capsuleWidth")
        anim_w.setDuration(180)
        anim_w.setStartValue(self.width())
        anim_w.setEndValue(self._expanded_width)
        anim_w.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        anim_op = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim_op.setDuration(180)
        anim_op.setStartValue(0.1)
        anim_op.setEndValue(1.0)
        anim_op.setEasingCurve(QEasingCurve.Type.InQuad)
        
        self._anim_group = QParallelAnimationGroup()
        self._anim_group.addAnimation(anim_w)
        self._anim_group.addAnimation(anim_op)
        self._anim_group.start()

    def collapse(self):
        if not self._is_expanded:
            return
        self._is_expanded = False
        
        if self._anim_group and self._anim_group.state() == QParallelAnimationGroup.State.Running:
            self._anim_group.stop()
            
        anim_w = QPropertyAnimation(self, b"capsuleWidth")
        anim_w.setDuration(160)
        anim_w.setStartValue(self.width())
        anim_w.setEndValue(self._collapsed_width)
        anim_w.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        anim_op = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim_op.setDuration(140)
        anim_op.setStartValue(1.0)
        anim_op.setEndValue(0.0)
        anim_op.setEasingCurve(QEasingCurve.Type.OutQuad)
        
        self._anim_group = QParallelAnimationGroup()
        self._anim_group.addAnimation(anim_w)
        self._anim_group.addAnimation(anim_op)
        self._anim_group.finished.connect(self._on_collapse_finished)
        self._anim_group.start()

    def _on_collapse_finished(self):
        if not self._is_expanded:
            self.stack.setCurrentIndex(0)
            self.opacity_effect.setOpacity(1.0)


# ==========================================
# SOUND LIBRARY & CHIME SYNTHESIZER
# ==========================================
CHIME_PRESETS = [
    ("acoustic_bell", "Acoustic Bell (Gentle)"),
    ("windows_chime", "Windows Modern Chime"),
    ("zen_bowl", "Zen Singing Bowl"),
    ("minimal_ping", "Minimal Watch Ping")
]

def synthesize_preset_wav(preset_key, filename, volume=50):
    sample_rate = 44100
    # Audio perceptual volume taper
    gain = max(0.0, min(1.0, (volume / 100.0) ** 1.3))
    
    if preset_key == "windows_chime":
        duration = 1.3
        num_samples = int(sample_rate * duration)
        frames = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            s1 = 0.0
            if t < 0.45:
                env1 = min(1.0, t / 0.006) * math.exp(-t / 0.16)
                s1 = 0.45 * math.sin(2 * math.pi * 739.99 * t) * env1
            s2 = 0.0
            if t >= 0.08:
                t2 = t - 0.08
                env2 = min(1.0, t2 / 0.006) * math.exp(-t2 / 0.42)
                s2 = (0.55 * math.sin(2 * math.pi * 1108.73 * t2) + 0.15 * math.sin(2 * math.pi * 2217.46 * t2)) * env2
            sample = (s1 + s2) * gain
            sample = max(-0.95, min(0.95, sample))
            frames.extend(struct.pack('<h', int(sample * 32767.0)))
            
    elif preset_key == "zen_bowl":
        duration = 2.0
        num_samples = int(sample_rate * duration)
        frames = bytearray()
        f1, f2, f3 = 329.63, 332.0, 659.25
        for i in range(num_samples):
            t = i / sample_rate
            env = min(1.0, t / 0.015) * math.exp(-t / 0.75)
            sample = (0.45 * math.sin(2 * math.pi * f1 * t) + 0.35 * math.sin(2 * math.pi * f2 * t) + 0.20 * math.sin(2 * math.pi * f3 * t)) * env * gain
            sample = max(-0.95, min(0.95, sample))
            frames.extend(struct.pack('<h', int(sample * 32767.0)))
            
    elif preset_key == "minimal_ping":
        duration = 0.9
        num_samples = int(sample_rate * duration)
        frames = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            s1 = 0.0
            if t < 0.22:
                env1 = min(1.0, t / 0.004) * math.exp(-t / 0.07)
                s1 = 0.5 * math.sin(2 * math.pi * 880.0 * t) * env1
            s2 = 0.0
            if t >= 0.09:
                t2 = t - 0.09
                env2 = min(1.0, t2 / 0.004) * math.exp(-t2 / 0.12)
                s2 = 0.5 * math.sin(2 * math.pi * 1174.66 * t2) * env2
            sample = (s1 + s2) * gain
            sample = max(-0.95, min(0.95, sample))
            frames.extend(struct.pack('<h', int(sample * 32767.0)))
            
    else: # "acoustic_bell" default
        duration = 1.8
        num_samples = int(sample_rate * duration)
        frames = bytearray()
        f1, f2, f3 = 587.33, 880.00, 1174.66
        for i in range(num_samples):
            t = i / sample_rate
            attack = min(1.0, t / 0.008)
            decay = math.exp(-t / 0.55)
            env = attack * decay
            sample = (
                0.55 * math.sin(2.0 * math.pi * f1 * t) +
                0.30 * math.sin(2.0 * math.pi * f2 * t) +
                0.15 * math.sin(2.0 * math.pi * f3 * t)
            ) * env * gain
            sample = max(-0.95, min(0.95, sample))
            frames.extend(struct.pack('<h', int(sample * 32767.0)))

    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(frames)

def scale_custom_wav(src_path, dst_path, volume=50):
    gain = max(0.0, min(1.0, (volume / 100.0) ** 1.3))
    try:
        with wave.open(src_path, 'rb') as src:
            nchannels = src.getnchannels()
            sampwidth = src.getsampwidth()
            framerate = src.getframerate()
            nframes = src.getnframes()
            raw = src.readframes(nframes)
        if sampwidth == 2:
            count = len(raw) // 2
            samples = struct.unpack(f'<{count}h', raw)
            scaled = bytearray()
            for s in samples:
                val = int(s * gain)
                val = max(-32767, min(32767, val))
                scaled.extend(struct.pack('<h', val))
            os.makedirs(os.path.dirname(os.path.abspath(dst_path)), exist_ok=True)
            with wave.open(dst_path, 'wb') as dst:
                dst.setnchannels(nchannels)
                dst.setsampwidth(sampwidth)
                dst.setframerate(framerate)
                dst.writeframes(scaled)
            return dst_path
    except Exception as e:
        print("Could not scale custom wav:", e)
    return src_path

def get_chime_sound_path(preset="acoustic_bell", volume=50, custom_path=""):
    cache_dir = os.path.join(os.path.expanduser("~"), ".dinoscreener")
    os.makedirs(cache_dir, exist_ok=True)
    
    if custom_path and os.path.exists(custom_path):
        scaled_dst = os.path.join(cache_dir, f"custom_vol{volume}.wav")
        if custom_path.lower().endswith(".wav"):
            return scale_custom_wav(custom_path, scaled_dst, volume)
        return custom_path
        
    target_filename = os.path.join(cache_dir, f"chime_{preset}_vol{volume}.wav")
    if not os.path.exists(target_filename) or os.path.getsize(target_filename) < 500:
        synthesize_preset_wav(preset, target_filename, volume)
    return target_filename

def play_chime(preset="acoustic_bell", volume=50, custom_path=""):
    sound_path = get_chime_sound_path(preset=preset, volume=volume, custom_path=custom_path)
    if not os.path.exists(sound_path):
        return
    if sys.platform == "win32":
        try:
            import winsound
            winsound.PlaySound(sound_path, winsound.SND_ASYNC | winsound.SND_FILENAME)
            return
        except Exception:
            pass
    # Linux fallback
    def _play_linux():
        for player in ["paplay", "pw-play", "aplay", "ffplay -nodisp -autoexit"]:
            cmd = player.split() + [sound_path]
            try:
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except FileNotFoundError:
                continue
    threading.Thread(target=_play_linux, daemon=True).start()


# ==========================================
# IN-APP UPDATE CHECKER & DOWNLOAD WORKERS
# ==========================================
def parse_version_tuple(v_str):
    nums = re.findall(r'\d+', str(v_str))
    return tuple(int(n) for n in nums) if nums else (0,)

def is_newer_version(latest, current):
    return parse_version_tuple(latest) > parse_version_tuple(current)

class UpdateCheckerWorker(QThread):
    update_result = pyqtSignal(bool, str, str, str) # has_update, latest_tag, body, download_url
    check_failed = pyqtSignal(str)
    
    def run(self):
        try:
            req = urllib.request.Request(
                f"https://api.github.com/repos/{APP_GITHUB_REPO}/releases/latest",
                headers={"User-Agent": "Dinoscreener-Screensaver"}
            )
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                
            latest_tag = data.get("tag_name", "")
            body = data.get("body", "")
            assets = data.get("assets", [])
            
            download_url = ""
            if sys.platform == "win32":
                for asset in assets:
                    name = asset.get("name", "").lower()
                    if name.endswith("windows.zip") or name.endswith(".zip"):
                        download_url = asset.get("browser_download_url")
                        break
                if not download_url:
                    for asset in assets:
                        name = asset.get("name", "").lower()
                        if name.endswith(".scr") or name.endswith(".exe"):
                            download_url = asset.get("browser_download_url")
                            break
            else:
                for asset in assets:
                    name = asset.get("name", "").lower()
                    if "linux" in name:
                        download_url = asset.get("browser_download_url")
                        break
            if not download_url and data.get("html_url"):
                download_url = data.get("html_url")
                
            has_update = is_newer_version(latest_tag, APP_VERSION)
            self.update_result.emit(has_update, latest_tag, body, download_url)
        except Exception as e:
            self.check_failed.emit(str(e))

class DownloadWorker(QThread):
    progress = pyqtSignal(int, int) # downloaded, total
    finished = pyqtSignal(str) # downloaded file path
    failed = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        
    def run(self):
        try:
            temp_dir = os.path.join(tempfile.gettempdir(), "dinoscreener_update")
            os.makedirs(temp_dir, exist_ok=True)
            filename = self.url.split("/")[-1].split("?")[0]
            if not filename:
                filename = "dinoscreener_update.bin"
            target_path = os.path.join(temp_dir, filename)
            
            req = urllib.request.Request(self.url, headers={"User-Agent": "Dinoscreener-Screensaver"})
            with urllib.request.urlopen(req, timeout=45) as resp:
                total_size = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                chunk_size = 65536
                with open(target_path, "wb") as f:
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        self.progress.emit(downloaded, total_size)
            self.finished.emit(target_path)
        except Exception as e:
            self.failed.emit(str(e))


# ==========================================
# MATERIAL YOU EXPRESSIVE LOADER & ABOUT DIALOG
# ==========================================
class MaterialYouLoader(QWidget):
    """Google Material Design 3 Expressive indeterminate linear loader with fluid sinusoidal dual pulse."""
    def __init__(self, accent_hex="#0078D4", parent=None):
        super().__init__(parent)
        self.accent_hex = accent_hex
        self.setFixedHeight(5)
        self._anim_pos = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(16)  # ~60 fps smooth frame pacing
        self._timer.timeout.connect(self._on_tick)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setVisible(False)

    def set_accent_color(self, hex_code):
        self.accent_hex = hex_code
        self.update()

    def start(self):
        self._anim_pos = 0.0
        self.setVisible(True)
        if not self._timer.isActive():
            self._timer.start()
        self.update()

    def stop(self):
        self._timer.stop()
        self.setVisible(False)

    def _on_tick(self):
        self._anim_pos = (self._anim_pos + 0.018) % 1.0
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        w, h = float(self.width()), float(self.height())
        r = h / 2.0
        
        # Subtle translucent track
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(255, 255, 255, 20))
        p.drawRoundedRect(QRectF(0, 0, w, h), r, r)
        
        # Primary expressive pulse
        t = self._anim_pos
        accent_q = QColor(self.accent_hex)
        s1_head = min(1.0, t * 1.5)
        s1_tail = max(0.0, (t - 0.35) * 1.5)
        x1 = s1_tail * w
        x2 = s1_head * w
        bar1_w = max(16.0, x2 - x1)
        p.setBrush(accent_q)
        p.drawRoundedRect(QRectF(x1, 0, bar1_w, h), r, r)
        
        # Secondary trailing pulse (Material You expressive rhythm)
        if t > 0.35:
            t2 = (t - 0.35) / 0.65
            s2_head = min(1.0, t2 * 1.4)
            s2_tail = max(0.0, (t2 - 0.35) * 1.4)
            x2_1 = s2_tail * w
            x2_2 = s2_head * w
            bar2_w = max(9.0, x2_2 - x2_1)
            accent_soft = QColor(accent_q.red(), accent_q.green(), accent_q.blue(), 180)
            p.setBrush(accent_soft)
            p.drawRoundedRect(QRectF(x2_1, 0, bar2_w, h), r, r)
            
        p.end()


class AboutDialog(QDialog):
    def __init__(self, parent=None, win_accent="#8F96BF", auto_check=False):
        super().__init__(parent)
        self.setWindowTitle("About Dinoscreener")
        self.setFixedSize(560, 680)
        self.win_accent = win_accent
        self.contrast_text, self.hover_accent, self.press_accent = get_color_variants(self.win_accent)
        
        # Subpixel ClearType Antialiased Font Hierarchy
        ui_font = QFont(["Segoe UI Variable Text", "Segoe UI", "Arial", "sans-serif"], 9)
        ui_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
        ui_font.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
        self.setFont(ui_font)

        # Windows 11 DWM Mica / Glass Blur Backdrop Setup
        self.is_dwm_active = apply_windows_dwm_effects(self)
            
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
        if getattr(sys, 'frozen', False):
            logo_path = os.path.join(sys._MEIPASS, "app_icon.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        self.logo_path = logo_path
        
        bg_dialog = "rgba(16, 20, 29, 0.72)" if self.is_dwm_active else "#10141D"
        bg_card = "rgba(23, 27, 38, 0.78)" if self.is_dwm_active else "#171B26"
        bg_story = "rgba(0, 0, 0, 0.28)" if self.is_dwm_active else "rgba(0, 0, 0, 0.25)"
        
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_dialog};
            }}
            QLabel {{
                color: #FFFFFF;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', -apple-system, sans-serif;
            }}
            QFrame#aboutCard {{
                background: {bg_card};
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
            }}
            QFrame#storyInnerBox {{
                background: {bg_story};
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 10px;
            }}
            QPushButton#accentBtn {{
                background-color: {self.win_accent};
                color: {self.contrast_text};
                border: none;
                border-radius: 9px;
                font-weight: 600;
                font-size: 12px;
                padding: 8px 18px;
            }}
            QPushButton#accentBtn:hover {{
                background-color: {self.hover_accent};
            }}
            QPushButton#glassBtn {{
                background-color: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 9px;
                color: #FFFFFF;
                font-size: 12px;
                font-weight: 500;
                padding: 8px 18px;
            }}
            QPushButton#glassBtn:hover {{
                background-color: rgba(255, 255, 255, 0.12);
                border-color: rgba(255, 255, 255, 0.25);
            }}
            QProgressBar {{
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 6px;
                text-align: center;
                color: #FFFFFF;
                font-size: 11px;
                font-weight: 600;
                height: 14px;
            }}
            QProgressBar::chunk {{
                background-color: {self.win_accent};
                border-radius: 5px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 22, 26, 20)
        layout.setSpacing(14)
        
        # 1. Centered Symmetrical Header (Golden Ratio Balance)
        header_box = QVBoxLayout()
        header_box.setSpacing(5)
        header_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_row = QHBoxLayout()
        logo_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo = QLabel()
        lbl_logo.setFixedSize(54, 54)
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo_bg = "rgba(23, 27, 38, 0.78)" if self.is_dwm_active else "#171B26"
        lbl_logo.setStyleSheet(f"""
            background: {lbl_logo_bg};
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 14px;
        """)
        if hasattr(self, 'logo_path') and os.path.exists(self.logo_path):
            lbl_logo.setPixmap(get_rounded_pixmap(self.logo_path, size=54, radius=14, dpr=3.0))
        logo_row.addWidget(lbl_logo)
        header_box.addLayout(logo_row)
        
        title_row = QHBoxLayout()
        title_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_row.setSpacing(8)
        lbl_title = QLabel(APP_NAME)
        lbl_title.setStyleSheet("font-size: 20px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.3px;")
        title_row.addWidget(lbl_title)
        
        lbl_ver = QLabel(APP_VERSION)
        lbl_ver.setStyleSheet(f"""
            background: rgba({QColor(self.win_accent).red()}, {QColor(self.win_accent).green()}, {QColor(self.win_accent).blue()}, 0.18);
            color: {self.win_accent};
            border: 1px solid rgba({QColor(self.win_accent).red()}, {QColor(self.win_accent).green()}, {QColor(self.win_accent).blue()}, 0.38);
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            padding: 2px 7px;
        """)
        title_row.addWidget(lbl_ver)
        header_box.addLayout(title_row)
        
        lbl_author = QLabel("Built by <b>Kushal :)</b> 👋 (@kushalarvindo)")
        lbl_author.setTextFormat(Qt.TextFormat.RichText)
        lbl_author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_author.setStyleSheet("font-size: 12px; color: #94A3B8;")
        header_box.addWidget(lbl_author)
        
        layout.addLayout(header_box)
        
        # 2. Card 1: Authentic Creator Story & Modes with Inset Inner Box
        card_story = QFrame()
        card_story.setObjectName("aboutCard")
        story_layout = QVBoxLayout(card_story)
        story_layout.setContentsMargins(18, 16, 18, 16)
        story_layout.setSpacing(12)
        
        lbl_story_title = QLabel("ABOUT")
        lbl_story_title.setStyleSheet("font-size: 10px; font-weight: 700; color: #64748B; letter-spacing: 0.6px;")
        story_layout.addWidget(lbl_story_title)
        
        inner_box = QFrame()
        inner_box.setObjectName("storyInnerBox")
        inner_layout = QVBoxLayout(inner_box)
        inner_layout.setContentsMargins(18, 14, 18, 14)
        inner_layout.setSpacing(0)
        
        story_text = (
            '<p style="margin: 0 0 10px 0; line-height: 1.54;">'
            "✦ Hi, I'm Kushal! 👋 I wanted a screensaver that was simple, neat, and actually fun to look at—so I built <b>Dinoscreener</b>.</p>"
            '<p style="margin: 0 0 10px 0; line-height: 1.54;">'
            "✦ <b>3 cozy styles</b> in one: a playful <b>Jumping Dino</b>, a classic <b>Flip Clock</b>, and a clean <b>Rotary Dial</b> with your weather & battery.</p>"
            '<p style="margin: 0 0 10px 0; line-height: 1.54;">'
            "✦ Made with love to be <b>super smooth</b>, <b>safe for OLED screens</b>, and complete with gentle <b>hourly bell chimes</b>.</p>"
            '<p style="margin: 0; line-height: 1.54; color: #94A3B8;">'
            "Hope it makes your desk smile! Ideas are always welcome 😊</p>"
        )
        lbl_story = QLabel(story_text)
        lbl_story.setTextFormat(Qt.TextFormat.RichText)
        lbl_story.setWordWrap(True)
        lbl_story.setStyleSheet("font-size: 11.5px; color: #CBD5E1;")
        inner_layout.addWidget(lbl_story)
        story_layout.addWidget(inner_box)
        
        # Mode Pills Row (Symmetrically centered and evenly spaced)
        pills_row = QHBoxLayout()
        pills_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pills_row.setSpacing(10)
        for icon_text in ["🦕 Chrome Dino", "⏱️ 3D Flip Clock", "⭕ Rotary Dial"]:
            lbl_pill = QLabel(icon_text)
            lbl_pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_pill.setFixedHeight(27)
            lbl_pill.setStyleSheet("""
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                color: #94A3B8;
                font-size: 11px;
                font-weight: 500;
                padding: 0 14px;
            """)
            pills_row.addWidget(lbl_pill)
        story_layout.addLayout(pills_row)
        layout.addWidget(card_story)
        
        # 3. Card 2: Updates (Symmetrical Layout with Material You Loader)
        card_upd = QFrame()
        card_upd.setObjectName("aboutCard")
        upd_layout = QVBoxLayout(card_upd)
        upd_layout.setContentsMargins(18, 14, 18, 14)
        upd_layout.setSpacing(10)
        
        lbl_upd_head = QLabel("UPDATES")
        lbl_upd_head.setStyleSheet("font-size: 10px; font-weight: 700; color: #64748B; letter-spacing: 0.6px;")
        upd_layout.addWidget(lbl_upd_head)
        
        self.lbl_status = QLabel(f"✓ You're on the newest release (<b>{APP_VERSION}</b>).")
        self.lbl_status.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_status.setStyleSheet("font-size: 11.5px; color: #E2E8F0;")
        upd_layout.addWidget(self.lbl_status)
        
        self.material_loader = MaterialYouLoader(self.win_accent, self)
        upd_layout.addWidget(self.material_loader)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        upd_layout.addWidget(self.progress_bar)
        
        upd_btn_row = QHBoxLayout()
        upd_btn_row.setSpacing(10)
        
        self.btn_check = QPushButton("Check for Updates")
        self.btn_check.setObjectName("glassBtn")
        self.btn_check.clicked.connect(self.check_updates_clicked)
        upd_btn_row.addWidget(self.btn_check, stretch=1)
        
        self.btn_install = QPushButton("Download & Install")
        self.btn_install.setObjectName("accentBtn")
        self.btn_install.setVisible(False)
        self.btn_install.clicked.connect(self.install_update_clicked)
        upd_btn_row.addWidget(self.btn_install, stretch=1)
        
        upd_layout.addLayout(upd_btn_row)
        layout.addWidget(card_upd)
        
        # 4. Footer Row (Golden Ratio Balance & Outer Symmetry)
        footer_row = QHBoxLayout()
        
        self.btn_github = QPushButton("GitHub")
        self.btn_github.setObjectName("glassBtn")
        self.btn_github.setFixedWidth(100)
        self.btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(APP_GITHUB_URL)))
        footer_row.addWidget(self.btn_github)
        
        footer_row.addStretch()
        
        btn_close = QPushButton("Close")
        btn_close.setObjectName("glassBtn")
        btn_close.setFixedWidth(100)
        btn_close.clicked.connect(self.close)
        footer_row.addWidget(btn_close)
        layout.addLayout(footer_row)
        
        self.latest_download_url = ""
        self.latest_tag = ""
        
        if auto_check:
            self.check_updates_clicked()

    def check_updates_clicked(self):
        self.lbl_status.setText("Checking GitHub for the latest release...")
        self.btn_check.setEnabled(False)
        self.material_loader.start()
        self.worker = UpdateCheckerWorker()
        self.worker.update_result.connect(self.on_update_result)
        self.worker.check_failed.connect(self.on_check_failed)
        self.worker.start()

    def on_update_result(self, has_update, latest_tag, body, download_url):
        self.material_loader.stop()
        self.btn_check.setEnabled(True)
        self.latest_download_url = download_url
        self.latest_tag = latest_tag
        if has_update:
            self.lbl_status.setText(f"🎉 <b>Update {latest_tag} available!</b> Current version is {APP_VERSION}.")
            self.btn_install.setVisible(True)
            self.btn_install.setText(f"Download & Install {latest_tag}")
        else:
            self.lbl_status.setText(f"✓ You are running the newest release (<b>{APP_VERSION}</b>).")
            self.btn_install.setVisible(False)

    def on_check_failed(self, err_msg):
        self.material_loader.stop()
        self.btn_check.setEnabled(True)
        self.lbl_status.setText(f"Could not connect to GitHub API: {err_msg}")

    def install_update_clicked(self):
        if not self.latest_download_url:
            QDesktopServices.openUrl(QUrl(f"{APP_GITHUB_URL}/releases/latest"))
            return
        self.btn_install.setEnabled(False)
        self.btn_check.setEnabled(False)
        self.material_loader.stop()
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.lbl_status.setText(f"Downloading {self.latest_tag} from GitHub...")
        
        self.down_worker = DownloadWorker(self.latest_download_url)
        self.down_worker.progress.connect(self.on_download_progress)
        self.down_worker.finished.connect(self.on_download_finished)
        self.down_worker.failed.connect(self.on_download_failed)
        self.down_worker.start()

    def on_download_progress(self, downloaded, total):
        if total > 0:
            pct = int((downloaded / total) * 100)
            self.progress_bar.setValue(pct)
            mb_down = downloaded / (1024 * 1024)
            mb_tot = total / (1024 * 1024)
            self.lbl_status.setText(f"Downloading {self.latest_tag}: {mb_down:.1f} MB / {mb_tot:.1f} MB ({pct}%)")
        else:
            mb_down = downloaded / (1024 * 1024)
            self.lbl_status.setText(f"Downloading {self.latest_tag}: {mb_down:.1f} MB...")

    def on_download_finished(self, downloaded_file):
        self.progress_bar.setValue(100)
        self.lbl_status.setText("Download complete! Applying update...")
        self.apply_update(downloaded_file)

    def on_download_failed(self, err_msg):
        self.btn_install.setEnabled(True)
        self.btn_check.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.lbl_status.setText(f"Download failed: {err_msg}. Opening GitHub release...")
        QDesktopServices.openUrl(QUrl(f"{APP_GITHUB_URL}/releases/latest"))

    def apply_update(self, downloaded_file):
        target_dir = os.path.dirname(downloaded_file)
        new_bin_path = downloaded_file
        if downloaded_file.endswith(".zip"):
            try:
                with zipfile.ZipFile(downloaded_file, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)
                for f in os.listdir(target_dir):
                    if f.lower().endswith((".exe", ".scr")):
                        new_bin_path = os.path.join(target_dir, f)
                        break
            except Exception as e:
                print("Zip extract error:", e)

        if not getattr(sys, 'frozen', False):
            self.lbl_status.setText(
                f"Update downloaded to:<br><code>{new_bin_path}</code><br>"
                f"Since you are running from Python source, run <code>git pull</code> or execute the binary above."
            )
            return

        current_exe = sys.executable
        if sys.platform == "win32":
            bat_path = os.path.join(tempfile.gettempdir(), "dinoscreener_apply.bat")
            with open(bat_path, "w", encoding="utf-8") as bat:
                bat.write(f"""@echo off
timeout /t 1 /nobreak >nul
:retry
copy /y "{new_bin_path}" "{current_exe}" >nul 2>&1
if errorlevel 1 (
    timeout /t 1 /nobreak >nul
    goto retry
)
start "" "{current_exe}" /c
del "%~f0"
""")
            subprocess.Popen(["cmd.exe", "/c", bat_path], creationflags=0x08000000)
            QApplication.quit()
        else:
            sh_path = os.path.join(tempfile.gettempdir(), "dinoscreener_apply.sh")
            with open(sh_path, "w", encoding="utf-8") as sh:
                sh.write(f"""#!/bin/sh
sleep 1
chmod +x "{new_bin_path}"
cp -f "{new_bin_path}" "{current_exe}"
"{current_exe}" --settings &
rm -- "$0"
""")
            os.chmod(sh_path, 0o755)
            subprocess.Popen(["/bin/sh", sh_path])
            QApplication.quit()

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        p.end()
        super().paintEvent(event)


# ==============================================================================
# INTERACTIVE FULLSCREEN STUDIO MODE & NATIVE FROSTED GLASS ENGINE
# ==============================================================================

class FrostedGlassWidget(QFrame):
    """
    Native, app-rendered dark grey/black frosted glass container without DWM dependency.
    Samples live screensaver canvas region directly behind the widget rect,
    applies smooth downsampled/upscaled Gaussian-like diffusion blur,
    and composites a rich dark slate translucent fill with 1px inner highlight border.
    """
    def __init__(self, studio, radius=16, parent=None):
        super().__init__(parent if parent else studio)
        self.studio = studio
        self.radius = radius
        self.drop_highlight = False
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
    def set_drop_highlight(self, active=True):
        if self.drop_highlight != active:
            self.drop_highlight = active
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return
            
        top_left = self.mapTo(self.studio, QPoint(0, 0))
        sample_rect = QRect(top_left.x(), top_left.y(), w, h)
        
        canvas_pix = getattr(self.studio.clock, 'cached_frame', None)
        clip = QPainterPath()
        clip.addRoundedRect(QRectF(0, 0, w, h), self.radius, self.radius)
        p.setClipPath(clip)
        
        # 1. Native Real-time Frosted Glass Blur
        if canvas_pix and not canvas_pix.isNull() and canvas_pix.rect().contains(sample_rect):
            sub = canvas_pix.copy(sample_rect)
            dw = max(4, w // 10)
            dh = max(4, h // 10)
            blurred = sub.scaled(dw, dh, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation).scaled(w, h, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            p.drawPixmap(0, 0, blurred)
        else:
            p.fillRect(QRectF(0, 0, w, h), QColor(10, 14, 23))
            
        # 2. Rich dark slate translucent fill: rgba(18, 21, 31, 0.75) (alpha ~192)
        p.fillRect(QRectF(0, 0, w, h), QColor(18, 21, 31, 192))
        
        # 3. 1px Inner highlight border / Drop highlight
        if self.drop_highlight:
            accent_col = QColor(self.studio.win_accent)
            pen = QPen(accent_col, 2.0)
            p.setPen(pen)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(QRectF(1.0, 1.0, w - 2.0, h - 2.0), self.radius - 1, self.radius - 1)
        else:
            border_pen = QPen(QColor(255, 255, 255, 31), 1.0)
            p.setPen(border_pen)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(QRectF(0.5, 0.5, w - 1.0, h - 1.0), self.radius, self.radius)
            
        p.end()
        super().paintEvent(event)


# Stylesheet for controls inside Fullscreen Studio frosted panels
STUDIO_CONTROL_STYLESHEET = """
    QLabel {
        color: #FFFFFF;
        font-family: 'Segoe UI Variable Text', 'Segoe UI', -apple-system, sans-serif;
        background: transparent;
    }
    QCheckBox {
        color: #CBD5E1;
        font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
        font-size: 11.5px;
        spacing: 8px;
        background: transparent;
    }
    QCheckBox:hover {
        color: #FFFFFF;
    }
    QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 5px;
        background: rgba(255, 255, 255, 0.05);
    }
    QCheckBox::indicator:hover {
        border-color: rgba(255, 255, 255, 0.45);
        background: rgba(255, 255, 255, 0.09);
    }
    QSlider {
        min-height: 22px;
        background: transparent;
    }
    QSlider::groove:horizontal {
        height: 5px;
        background: rgba(255, 255, 255, 0.12);
        border-radius: 2px;
    }
    QComboBox {
        background: rgba(255, 255, 255, 0.08);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 3px 8px;
        font-size: 11px;
        min-height: 20px;
        font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
    }
    QComboBox:hover {
        background: rgba(255, 255, 255, 0.14);
        border-color: rgba(255, 255, 255, 0.30);
    }
    QComboBox QAbstractItemView {
        background: #181C26;
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 8px;
        padding: 4px;
        outline: none;
    }
"""



# ==============================================================================
# STUDIO FLOATING PANELS & DRAWERS
# ==============================================================================

class StudioInfoButton(FrostedGlassWidget):
    def __init__(self, studio):
        super().__init__(studio, radius=19)
        self.setFixedSize(38, 38)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("About, version & updates (ⓘ)")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.btn = QPushButton()
        self.btn.setIcon(get_or_create_info_duotone_icon(self.studio.win_accent))
        self.btn.setIconSize(QSize(20, 20))
        self.btn.setFixedSize(38, 38)
        self.btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn.setStyleSheet("background: transparent; border: none; outline: none;")
        self.btn.clicked.connect(self.studio.open_about)
        layout.addWidget(self.btn)


class StudioActionDock(FrostedGlassWidget):
    def __init__(self, studio):
        super().__init__(studio, radius=19)
        self.setFixedHeight(38)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 3, 8, 3)
        layout.setSpacing(6)
        
        # 1. Reset Defaults Button
        self.btn_reset = QPushButton("Reset Defaults")
        self.btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reset.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94A3B8;
                border: none;
                border-radius: 12px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 500;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                color: #F87171;
            }
        """)
        self.btn_reset.clicked.connect(self.studio.reset_defaults_clicked)
        layout.addWidget(self.btn_reset)
        
        # 2. Apply Button (glowing accent pill with "✓ Saved" feedback)
        self.btn_apply = QPushButton("Apply")
        self.btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_apply.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.studio.win_accent};
                color: {self.studio.contrast_text};
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 14px;
                font-weight: 600;
                font-size: 11.5px;
                padding: 5px 16px;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{
                background-color: {self.studio.hover_accent};
            }}
        """)
        self.btn_apply.clicked.connect(self.studio.apply_clicked)
        layout.addWidget(self.btn_apply)
        
        # 3. Exit Badge Button
        self.btn_exit = QPushButton("✕")
        self.btn_exit.setFixedSize(26, 26)
        self.btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_exit.setToolTip("Exit Fullscreen Studio (Esc)")
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                color: #E2E8F0;
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 13px;
                font-size: 11px;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.25);
                border-color: rgba(239, 68, 68, 0.45);
                color: #EF4444;
            }
        """)
        self.btn_exit.clicked.connect(self.studio.close_studio)
        layout.addWidget(self.btn_exit)


class StudioTopDrawer(FrostedGlassWidget):
    """
    Top-center Display & Atmosphere drawer: slides down from top edge.
    """
    def __init__(self, studio):
        super().__init__(studio, radius=16)
        self.setFixedSize(470, 145)
        self.setStyleSheet(STUDIO_CONTROL_STYLESHEET)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # Header Row
        header = QHBoxLayout()
        lbl_title = QLabel("Display & Atmosphere")
        lbl_title.setStyleSheet("font-size: 12.5px; font-weight: 700; color: #FFFFFF;")
        self.lbl_bright = QLabel(f"{self.studio.settings.bright_slider.value()}%")
        self.lbl_bright.setStyleSheet(f"color: {self.studio.win_accent}; font-weight: 600; font-size: 11.5px;")
        header.addWidget(lbl_title)
        header.addStretch()
        header.addWidget(self.lbl_bright)
        layout.addLayout(header)
        
        # Brightness Slider Row
        bright_box = QHBoxLayout()
        bright_box.setSpacing(8)
        lbl_sun1 = QLabel("☼")
        lbl_sun1.setStyleSheet("color: #64748B; font-size: 13px;")
        lbl_sun2 = QLabel("☀")
        lbl_sun2.setStyleSheet("color: #94A3B8; font-size: 15px;")
        
        self.bright_slider = QSlider(Qt.Orientation.Horizontal)
        self.bright_slider.setRange(10, 100)
        self.bright_slider.setValue(self.studio.settings.bright_slider.value())
        self.bright_slider.valueChanged.connect(self.on_bright_changed)
        bright_box.addWidget(lbl_sun1)
        bright_box.addWidget(self.bright_slider, stretch=1)
        bright_box.addWidget(lbl_sun2)
        layout.addLayout(bright_box)
        
        # Checkboxes Grid
        cb_grid = QGridLayout()
        cb_grid.setHorizontalSpacing(14)
        cb_grid.setVerticalSpacing(5)
        
        self.cb_ambient = QCheckBox("Ambient Mode (Space)")
        self.cb_ambient.setChecked(self.studio.settings.ambient_cb.isChecked())
        self.cb_ambient.toggled.connect(self.on_ambient_toggled)
        cb_grid.addWidget(self.cb_ambient, 0, 0)
        
        self.cb_oled = QCheckBox("OLED Protection")
        self.cb_oled.setChecked(self.studio.settings.pixel_shift_cb.isChecked())
        self.cb_oled.toggled.connect(self.on_oled_toggled)
        cb_grid.addWidget(self.cb_oled, 0, 1)
        
        self.cb_24hr = QCheckBox("24-Hour Format")
        self.cb_24hr.setChecked(self.studio.settings.use_24hr_cb.isChecked())
        self.cb_24hr.toggled.connect(self.on_24hr_toggled)
        cb_grid.addWidget(self.cb_24hr, 1, 0)
        
        layout.addLayout(cb_grid)

    def on_bright_changed(self, val):
        self.lbl_bright.setText(f"{val}%")
        self.studio.clock.brightness = val
        self.studio.clock.update()
        self.studio.settings.bright_slider.setValue(val)

    def on_ambient_toggled(self, checked):
        self.studio.clock.show_bg = checked
        self.studio.clock.update()
        self.studio.settings.ambient_cb.setChecked(checked)

    def on_oled_toggled(self, checked):
        self.studio.clock.pixel_shift = checked
        self.studio.clock.update()
        self.studio.settings.pixel_shift_cb.setChecked(checked)

    def on_24hr_toggled(self, checked):
        self.studio.clock.use_24hr = checked
        self.studio.clock.update()
        self.studio.settings.use_24hr_cb.setChecked(checked)


class StudioRightDrawer(FrostedGlassWidget):
    """
    Right-center System & Controls drawer: slides in from right edge.
    """
    def __init__(self, studio):
        super().__init__(studio, radius=16)
        self.setFixedSize(250, 155)
        self.setStyleSheet(STUDIO_CONTROL_STYLESHEET)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        lbl_title = QLabel("System & Controls")
        lbl_title.setStyleSheet("font-size: 12.5px; font-weight: 700; color: #FFFFFF;")
        layout.addWidget(lbl_title)
        
        self.cb_strict = QCheckBox("Lock on Exit (Win+L)")
        self.cb_strict.setChecked(self.studio.settings.strict_cb.isChecked())
        self.cb_strict.toggled.connect(self.on_strict_toggled)
        layout.addWidget(self.cb_strict)
        
        self.cb_media = QCheckBox("Ignore Media Keys")
        self.cb_media.setChecked(self.studio.settings.ignore_media_cb.isChecked())
        self.cb_media.toggled.connect(self.on_media_toggled)
        layout.addWidget(self.cb_media)
        
        self.cb_win = QCheckBox("Enable Windows Key")
        self.cb_win.setChecked(self.studio.settings.win_cb.isChecked())
        self.cb_win.toggled.connect(self.on_win_toggled)
        layout.addWidget(self.cb_win)
        layout.addStretch()

    def on_strict_toggled(self, checked):
        self.studio.settings.strict_cb.setChecked(checked)

    def on_media_toggled(self, checked):
        self.studio.clock.ignore_media_keys = checked
        self.studio.settings.ignore_media_cb.setChecked(checked)

    def on_win_toggled(self, checked):
        self.studio.clock.enable_win_key = checked
        self.studio.settings.win_cb.setChecked(checked)


class StudioLeftDrawer(FrostedGlassWidget):
    """
    Left-center Mode-Specific Settings drawer: slides in from left edge.
    Dynamically switches pages between Flip Clock, Rotary Modern, and Dino Runner.
    """
    def __init__(self, studio):
        super().__init__(studio, radius=16)
        self.setFixedSize(310, 390)
        self.setStyleSheet(STUDIO_CONTROL_STYLESHEET)
        
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(16, 12, 16, 12)
        root_layout.setSpacing(10)
        
        # Header Row with Mode Badge
        header = QHBoxLayout()
        lbl_title = QLabel("Mode Settings")
        lbl_title.setStyleSheet("font-size: 13px; font-weight: 700; color: #FFFFFF;")
        self.lbl_badge = QLabel("Flip Clock")
        self.lbl_badge.setStyleSheet(f"""
            font-size: 11px; font-weight: 600; 
            color: {self.studio.win_accent}; 
            background: rgba(255, 255, 255, 0.06); 
            border: 1px solid rgba(255, 255, 255, 0.12); 
            border-radius: 6px; padding: 2px 8px;
        """)
        header.addWidget(lbl_title)
        header.addStretch()
        header.addWidget(self.lbl_badge)
        root_layout.addLayout(header)
        
        # Universal Scale Slider
        scale_box = QHBoxLayout()
        scale_box.setSpacing(6)
        lbl_sc = QLabel("Scale:")
        lbl_sc.setStyleSheet("font-size: 11px; font-weight: 500; color: #E2E8F0;")
        scale_box.addWidget(lbl_sc)
        
        btn_step_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.18);
            }
        """
        self.btn_scale_minus = QPushButton("−")
        self.btn_scale_minus.setFixedSize(22, 22)
        self.btn_scale_minus.setStyleSheet(btn_step_style)
        self.btn_scale_minus.clicked.connect(lambda: self.step_scale(-5))
        scale_box.addWidget(self.btn_scale_minus)
        
        curr_mode = self.studio.clock.clock_style
        init_scale = int(self.studio.clock.clock_scales.get(str(curr_mode), 0.45) * 100)
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(15, 95)
        self.scale_slider.setValue(init_scale)
        self.scale_slider.valueChanged.connect(self.on_scale_changed)
        scale_box.addWidget(self.scale_slider, stretch=1)
        
        self.btn_scale_plus = QPushButton("+")
        self.btn_scale_plus.setFixedSize(22, 22)
        self.btn_scale_plus.setStyleSheet(btn_step_style)
        self.btn_scale_plus.clicked.connect(lambda: self.step_scale(5))
        scale_box.addWidget(self.btn_scale_plus)
        
        self.lbl_scale_val = QLabel(f"{init_scale}%")
        self.lbl_scale_val.setStyleSheet("color: #94A3B8; font-size: 11px; min-width: 28px;")
        scale_box.addWidget(self.lbl_scale_val)
        root_layout.addLayout(scale_box)
        
        # Mode Stacked Pages
        self.pages = QStackedLayout()
        
        # --- PAGE 0: FLIP CLOCK ---
        page_flip = QWidget()
        flip_layout = QVBoxLayout(page_flip)
        flip_layout.setContentsMargins(0, 4, 0, 0)
        flip_layout.setSpacing(8)
        
        # Hourly Chime Row
        chime_row = QHBoxLayout()
        self.cb_chime = QCheckBox("Hourly Chime")
        self.cb_chime.setChecked(self.studio.settings.hourly_chime_cb.isChecked())
        self.cb_chime.toggled.connect(self.on_chime_toggled)
        chime_row.addWidget(self.cb_chime)
        
        self.btn_test_chime = QPushButton("🔔 Test")
        self.btn_test_chime.setFixedSize(54, 22)
        self.btn_test_chime.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                color: #FFFFFF;
                font-size: 11px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.18);
            }
        """)
        self.btn_test_chime.clicked.connect(self.studio.settings.test_chime_sound)
        chime_row.addWidget(self.btn_test_chime)
        chime_row.addStretch()
        flip_layout.addLayout(chime_row)
        
        # Sound Presets Dropdown
        snd_row = QHBoxLayout()
        lbl_snd = QLabel("Sound:")
        lbl_snd.setStyleSheet("font-size: 11px; color: #E2E8F0;")
        snd_row.addWidget(lbl_snd)
        
        self.chime_sound_cb = QComboBox()
        self.refresh_chime_combobox()
        self.chime_sound_cb.currentIndexChanged.connect(self.on_chime_preset_changed)
        snd_row.addWidget(self.chime_sound_cb, stretch=1)
        
        self.btn_browse_sound = QPushButton("📂")
        self.btn_browse_sound.setFixedSize(22, 22)
        self.btn_browse_sound.setStyleSheet(btn_step_style)
        self.btn_browse_sound.setToolTip("Browse audio file (.wav, .mp3, .ogg)")
        self.btn_browse_sound.clicked.connect(self.studio.browse_custom_sound)
        snd_row.addWidget(self.btn_browse_sound)
        flip_layout.addLayout(snd_row)
        
        # Volume Row
        vol_row = QHBoxLayout()
        lbl_vol = QLabel("Vol:")
        lbl_vol.setStyleSheet("font-size: 11px; color: #E2E8F0;")
        vol_row.addWidget(lbl_vol)
        
        init_vol = self.studio.settings.chime_vol_slider.value() if hasattr(self.studio.settings, 'chime_vol_slider') else 45
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(5, 100)
        self.vol_slider.setValue(init_vol)
        self.vol_slider.valueChanged.connect(self.on_volume_changed)
        vol_row.addWidget(self.vol_slider, stretch=1)
        
        self.lbl_vol = QLabel(f"{init_vol}%")
        self.lbl_vol.setStyleSheet("color: #94A3B8; font-size: 11px; min-width: 28px;")
        vol_row.addWidget(self.lbl_vol)
        flip_layout.addLayout(vol_row)
        
        # Leading Zeros
        self.cb_lz_flip = QCheckBox("Leading Zeros (09 vs 9)")
        self.cb_lz_flip.setChecked(self.studio.clock.leading_zeros.get("0", False))
        self.cb_lz_flip.toggled.connect(lambda c: self.on_lz_toggled(0, c))
        flip_layout.addWidget(self.cb_lz_flip)
        flip_layout.addStretch()
        self.pages.addWidget(page_flip)
        
        # --- PAGE 1: ROTARY MODERN ---
        page_rotary = QWidget()
        rotary_layout = QVBoxLayout(page_rotary)
        rotary_layout.setContentsMargins(0, 4, 0, 0)
        rotary_layout.setSpacing(8)
        
        # Weather & Fahrenheit
        w_row = QHBoxLayout()
        self.cb_weather = QCheckBox("Live Weather")
        self.cb_weather.setChecked(self.studio.settings.show_weather_cb.isChecked())
        self.cb_weather.toggled.connect(self.on_weather_toggled)
        w_row.addWidget(self.cb_weather)
        
        self.cb_fahr = QCheckBox("°F")
        self.cb_fahr.setChecked(self.studio.settings.fahrenheit_cb.isChecked())
        self.cb_fahr.toggled.connect(self.on_fahr_toggled)
        w_row.addWidget(self.cb_fahr)
        w_row.addStretch()
        rotary_layout.addLayout(w_row)
        
        # Battery Indicator
        self.cb_battery = QCheckBox("Battery Level")
        self.cb_battery.setChecked(self.studio.settings.show_battery_cb.isChecked())
        self.cb_battery.toggled.connect(self.on_battery_toggled)
        rotary_layout.addWidget(self.cb_battery)
        
        # Leading Zeros
        self.cb_lz_rotary = QCheckBox("Leading Zeros (09 vs 9)")
        self.cb_lz_rotary.setChecked(self.studio.clock.leading_zeros.get("1", False))
        self.cb_lz_rotary.toggled.connect(lambda c: self.on_lz_toggled(1, c))
        rotary_layout.addWidget(self.cb_lz_rotary)
        rotary_layout.addStretch()
        self.pages.addWidget(page_rotary)
        
        # --- PAGE 2: DINO RUNNER ---
        page_dino = QWidget()
        dino_layout = QVBoxLayout(page_dino)
        dino_layout.setContentsMargins(0, 4, 0, 0)
        dino_layout.setSpacing(8)
        
        # Dino Font
        f_row = QHBoxLayout()
        lbl_df = QLabel("Font:")
        lbl_df.setStyleSheet("font-size: 11px; color: #E2E8F0;")
        f_row.addWidget(lbl_df)
        
        self.font_cb = QComboBox()
        self.refresh_font_combobox()
        self.font_cb.currentIndexChanged.connect(self.on_font_changed)
        f_row.addWidget(self.font_cb, stretch=1)
        
        self.btn_undo_font = QPushButton("↺")
        self.btn_undo_font.setFixedSize(22, 22)
        self.btn_undo_font.setStyleSheet(btn_step_style)
        self.btn_undo_font.setToolTip("Revert font to default")
        self.btn_undo_font.clicked.connect(self.revert_font)
        f_row.addWidget(self.btn_undo_font)
        dino_layout.addLayout(f_row)
        
        # Dino Sprite
        s_row = QHBoxLayout()
        lbl_ds = QLabel("Sprite:")
        lbl_ds.setStyleSheet("font-size: 11px; color: #E2E8F0;")
        s_row.addWidget(lbl_ds)
        
        self.char_cb = QComboBox()
        self.refresh_char_combobox()
        self.char_cb.currentIndexChanged.connect(self.on_char_changed)
        s_row.addWidget(self.char_cb, stretch=1)
        
        self.btn_undo_char = QPushButton("↺")
        self.btn_undo_char.setFixedSize(22, 22)
        self.btn_undo_char.setStyleSheet(btn_step_style)
        self.btn_undo_char.setToolTip("Revert sprite to default Dino")
        self.btn_undo_char.clicked.connect(self.revert_character)
        s_row.addWidget(self.btn_undo_char)
        dino_layout.addLayout(s_row)
        
        # Drop Zone Indicator
        self.drop_box = QFrame()
        self.drop_box.setStyleSheet("""
            QFrame {
                border: 1px dashed rgba(255, 255, 255, 0.20);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.03);
            }
        """)
        drop_layout = QVBoxLayout(self.drop_box)
        drop_layout.setContentsMargins(8, 8, 8, 8)
        lbl_drop = QLabel("Drop audio (.wav/.mp3) or sprite image anytime")
        lbl_drop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_drop.setStyleSheet("color: #94A3B8; font-size: 10px; background: transparent;")
        drop_layout.addWidget(lbl_drop)
        dino_layout.addWidget(self.drop_box)
        
        dino_layout.addStretch()
        self.pages.addWidget(page_dino)
        
        root_layout.addLayout(self.pages)
        self.set_mode(curr_mode)

    def set_mode(self, idx):
        self.pages.setCurrentIndex(idx)
        titles = ["Flip Clock", "Rotary Modern", "Dino Runner"]
        self.lbl_badge.setText(titles[idx])
        scale_val = int(self.studio.clock.clock_scales.get(str(idx), 0.45) * 100)
        self.scale_slider.blockSignals(True)
        self.scale_slider.setValue(scale_val)
        self.scale_slider.blockSignals(False)
        self.lbl_scale_val.setText(f"{scale_val}%")

    def step_scale(self, delta):
        self.scale_slider.setValue(max(15, min(95, self.scale_slider.value() + delta)))

    def on_scale_changed(self, val):
        self.lbl_scale_val.setText(f"{val}%")
        mode_key = str(self.studio.clock.clock_style)
        self.studio.clock.clock_scales[mode_key] = val / 100.0
        self.studio.clock.update()
        self.studio.settings.scale_slider.blockSignals(True)
        self.studio.settings.scale_slider.setValue(val)
        self.studio.settings.scale_slider.blockSignals(False)

    def on_chime_toggled(self, checked):
        self.studio.clock.hourly_chime = checked
        self.studio.settings.hourly_chime_cb.setChecked(checked)

    def on_volume_changed(self, val):
        self.lbl_vol.setText(f"{val}%")
        self.studio.clock.chime_volume = val
        if hasattr(self.studio.settings, 'chime_vol_slider'):
            self.studio.settings.chime_vol_slider.setValue(val)

    def on_weather_toggled(self, checked):
        self.studio.clock.show_weather = checked
        self.studio.clock.update()
        self.studio.settings.show_weather_cb.setChecked(checked)

    def on_fahr_toggled(self, checked):
        self.studio.clock.use_fahrenheit = checked
        self.studio.clock.update()
        self.studio.settings.fahrenheit_cb.setChecked(checked)

    def on_battery_toggled(self, checked):
        self.studio.clock.show_battery = checked
        self.studio.clock.update()
        self.studio.settings.show_battery_cb.setChecked(checked)

    def on_lz_toggled(self, style_idx, checked):
        self.studio.clock.leading_zeros[str(style_idx)] = checked
        self.studio.clock.update()
        self.studio.settings.leading_zero_cb.setChecked(checked)

    def refresh_chime_combobox(self):
        self.chime_sound_cb.blockSignals(True)
        self.chime_sound_cb.clear()
        self.chime_sound_cb.addItem("Acoustic Bell", "acoustic_bell")
        self.chime_sound_cb.addItem("Soft Marimba", "soft_marimba")
        self.chime_sound_cb.addItem("Grandfather Clock", "grandfather_clock")
        self.chime_sound_cb.addItem("Zen Singing Bowl", "zen_bowl")
        custom_path = getattr(self.studio.clock, 'custom_chime_path', "")
        if custom_path and os.path.exists(custom_path):
            self.chime_sound_cb.addItem(f"Custom: {os.path.basename(custom_path)}", "custom")
            self.chime_sound_cb.setCurrentIndex(4)
        else:
            preset = getattr(self.studio.clock, 'chime_preset', 'acoustic_bell')
            idx = self.chime_sound_cb.findData(preset)
            if idx >= 0:
                self.chime_sound_cb.setCurrentIndex(idx)
        self.chime_sound_cb.blockSignals(False)

    def on_chime_preset_changed(self, idx):
        preset = self.chime_sound_cb.currentData()
        if preset != "custom":
            self.studio.clock.chime_preset = preset
            self.studio.settings.refresh_chime_combobox()

    def refresh_font_combobox(self):
        self.font_cb.blockSignals(True)
        self.font_cb.clear()
        self.font_cb.addItem("Bungee (Default)", "Bungee")
        self.font_cb.addItem("Press Start 2P", "Press Start 2P")
        self.font_cb.addItem("Silkscreen", "Silkscreen")
        self.font_cb.addItem("VT323", "VT323")
        prim = getattr(self.studio.clock, 'primary_font', "")
        if prim and os.path.exists(prim):
            self.font_cb.addItem(f"Custom: {os.path.basename(prim)}", "custom_imported")
            self.font_cb.setCurrentIndex(self.font_cb.count() - 1)
        else:
            d_font = getattr(self.studio.clock, 'dino_font', "Bungee")
            idx = self.font_cb.findData(d_font)
            if idx >= 0:
                self.font_cb.setCurrentIndex(idx)
        self.font_cb.blockSignals(False)

    def on_font_changed(self, idx):
        data = self.font_cb.currentData()
        if data != "custom_imported":
            self.studio.clock.dino_font = data
            self.studio.clock.primary_font = ""
            self.studio.clock.update()
            self.studio.settings.refresh_font_combobox()

    def revert_font(self):
        self.studio.settings.revert_font()
        self.refresh_font_combobox()
        self.studio.clock.dino_font = "Bungee"
        self.studio.clock.primary_font = ""
        self.studio.clock.update()

    def refresh_char_combobox(self):
        self.char_cb.blockSignals(True)
        self.char_cb.clear()
        self.char_cb.addItem("Default Dino (T-Rex)", "dino")
        cust_img = getattr(self.studio.clock, 'custom_character_image', "")
        if cust_img and os.path.exists(cust_img):
            self.char_cb.addItem(f"Custom: {os.path.basename(cust_img)}", "custom")
            self.char_cb.setCurrentIndex(1)
        else:
            self.char_cb.setCurrentIndex(0)
        self.char_cb.blockSignals(False)

    def on_char_changed(self, idx):
        data = self.char_cb.currentData()
        if data == "dino":
            self.studio.clock.character_type = "dino"
            self.studio.clock.custom_character_image = ""
            self.studio.clock.update()
            self.studio.settings.revert_character()

    def revert_character(self):
        self.studio.settings.revert_character()
        self.refresh_char_combobox()
        self.studio.clock.character_type = "dino"
        self.studio.clock.custom_character_image = ""
        self.studio.clock.update()



# ==============================================================================
# FULLSCREEN STUDIO WINDOW
# ==============================================================================

class FullscreenStudioMode(QWidget):
    """
    Interactive Fullscreen Studio Mode: Live-edit all screensaver settings in fullscreen
    with native frosted glass floating HUD elements, hidden edge-glow drawers,
    audio drag-and-drop, and real-time synchronization with the Settings window.
    """
    def __init__(self, settings_dialog):
        super().__init__()
        self.settings = settings_dialog
        self.win_accent = self.settings.win_accent
        self.contrast_text, self.hover_accent, self.press_accent = get_color_variants(self.win_accent)
        
        self.setWindowTitle("Dinoscreener Fullscreen Studio")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        
        # 1. Embedded Screensaver Canvas with Frame Caching
        self.clock = CrispAestheticFlipClock(
            accent_color=self.settings.config.get("accent_color", self.win_accent),
            enable_win_key=self.settings.win_cb.isChecked(),
            strict_exit=True,
            show_info=self.settings.show_weather_cb.isChecked() or self.settings.show_battery_cb.isChecked(),
            show_weather=self.settings.show_weather_cb.isChecked(),
            show_battery=self.settings.show_battery_cb.isChecked(),
            use_fahrenheit=self.settings.fahrenheit_cb.isChecked(),
            ambient_mode=self.settings.ambient_cb.isChecked(),
            preview_mode=True,
            brightness=self.settings.bright_slider.value(),
            clock_style=self.settings.preview.clock_style,
            clock_scales=dict(self.settings.preview.clock_scales),
            use_24hr=self.settings.use_24hr_cb.isChecked(),
            leading_zeros=dict(self.settings.preview.leading_zeros),
            ignore_media_keys=self.settings.ignore_media_cb.isChecked(),
            dino_font=getattr(self.settings.preview, 'dino_font', "Bungee"),
            primary_font=getattr(self.settings, 'primary_font', ""),
            character_type=getattr(self.settings.preview, 'character_type', "dino"),
            custom_character_image=getattr(self.settings, 'custom_character_image', ""),
            live_weather=self.settings.show_weather_cb.isChecked(),
            pixel_shift=self.settings.pixel_shift_cb.isChecked(),
            hourly_chime=self.settings.hourly_chime_cb.isChecked(),
            chime_preset=self.settings.chime_sound_cb.currentData() if hasattr(self.settings, 'chime_sound_cb') else "acoustic_bell",
            chime_volume=self.settings.chime_vol_slider.value() if hasattr(self.settings, 'chime_vol_slider') else 45,
            custom_chime_path=getattr(self.settings, "custom_chime_path", ""),
            )
        self.clock.enable_frame_caching = True
        self.clock.setMouseTracking(True)
        self.clock.installEventFilter(self)
        
        # 2. Always-Visible Floating HUD Elements
        self.btn_info = StudioInfoButton(self)
        self.action_dock = StudioActionDock(self)
        
        self.mode_capsule = CollapsibleModeCapsule(win_accent=self.win_accent, parent=self)
        self.mode_capsule.enable_frosted_glass(self)
        self.mode_capsule.set_current_mode(self.clock.clock_style)
        self.mode_capsule.on_mode_changed = self.on_mode_switched
        self.mode_capsule.installEventFilter(self)
        
        # 3. Hidden Edge-Triggered Floating Drawers
        self.left_drawer = StudioLeftDrawer(self)
        self.top_drawer = StudioTopDrawer(self)
        self.right_drawer = StudioRightDrawer(self)
        
        # Drawer State Tracking
        self.left_open = False
        self.top_open = False
        self.right_open = False
        
        self.left_open_ratio = 0.0
        self.top_open_ratio = 0.0
        self.right_open_ratio = 0.0
        
        self.left_pos = -320
        self.top_pos = -160
        self.right_pos = 9999
        
        # Animations
        self.anim_left = QVariantAnimation(self)
        self.anim_left.setDuration(220)
        self.anim_left.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim_left.valueChanged.connect(self.on_anim_left)
        
        self.anim_top = QVariantAnimation(self)
        self.anim_top.setDuration(220)
        self.anim_top.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim_top.valueChanged.connect(self.on_anim_top)
        
        self.anim_right = QVariantAnimation(self)
        self.anim_right.setDuration(220)
        self.anim_right.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim_right.valueChanged.connect(self.on_anim_right)
        
        # Install Event Filters for stable mouse tracking
        self.install_child_event_filters(self.left_drawer)
        self.install_child_event_filters(self.top_drawer)
        self.install_child_event_filters(self.right_drawer)
        self.install_child_event_filters(self.action_dock)
        self.install_child_event_filters(self.btn_info)

    def install_child_event_filters(self, widget):
        widget.installEventFilter(self)
        for child in widget.findChildren(QWidget):
            child.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.mode_capsule and event.type() == QEvent.Type.Resize:
            sw, sh = self.width(), self.height()
            cw = self.mode_capsule.width()
            self.mode_capsule.move((sw - cw) // 2, sh - self.mode_capsule.height() - 36)
        elif event.type() == QEvent.Type.MouseMove:
            # Map mouse position to studio window coordinate space
            global_pos = event.globalPosition().toPoint()
            local_pos = self.mapFromGlobal(global_pos)
            self.check_drawer_hover(local_pos)
        return super().eventFilter(obj, event)

    def on_clock_frame_rendered(self):
        # Repaint open drawers to refresh live blurred reflections
        if self.left_open_ratio > 0.05:
            self.left_drawer.update()
        if self.top_open_ratio > 0.05:
            self.top_drawer.update()
        if self.right_open_ratio > 0.05:
            self.right_drawer.update()
        self.btn_info.update()
        self.action_dock.update()
        self.mode_capsule.update()
        self.update() # For edge glow breathing

    def resizeEvent(self, event):
        super().resizeEvent(event)
        sw, sh = self.width(), self.height()
        self.clock.setGeometry(0, 0, sw, sh)
        
        # Top-Right Info Button: 24px margin
        self.btn_info.move(sw - self.btn_info.width() - 24, 24)
        self.btn_info.raise_()
        
        # Bottom-Right Action Dock: 24px margin
        self.action_dock.move(sw - self.action_dock.width() - 24, sh - self.action_dock.height() - 24)
        self.action_dock.raise_()
        
        # Bottom-Center Mode Switcher: 36px from bottom
        cw = self.mode_capsule.width()
        self.mode_capsule.move((sw - cw) // 2, sh - self.mode_capsule.height() - 36)
        self.mode_capsule.raise_()
        
        # Left Drawer: Centered vertically
        dh_l = self.left_drawer.height()
        target_y_l = (sh - dh_l) // 2
        self.left_pos = 24 if self.left_open else -self.left_drawer.width() - 10
        self.left_drawer.move(self.left_pos, target_y_l)
        self.left_drawer.raise_()
        
        # Top Drawer: Centered horizontally
        dw_t = self.top_drawer.width()
        target_x_t = (sw - dw_t) // 2
        self.top_pos = 24 if self.top_open else -self.top_drawer.height() - 10
        self.top_drawer.move(target_x_t, self.top_pos)
        self.top_drawer.raise_()
        
        # Right Drawer: Centered vertically
        dh_r = self.right_drawer.height()
        target_y_r = (sh - dh_r) // 2
        self.right_pos = sw - self.right_drawer.width() - 24 if self.right_open else sw + 10
        self.right_drawer.move(self.right_pos, target_y_r)
        self.right_drawer.raise_()

    # --- Drawer Animation Handlers ---
    def set_left_drawer_open(self, open_state):
        if self.left_open == open_state: return
        self.left_open = open_state
        self.anim_left.stop()
        start_x = self.left_drawer.x()
        end_x = 24 if open_state else -self.left_drawer.width() - 10
        self.anim_left.setStartValue(start_x)
        self.anim_left.setEndValue(end_x)
        self.anim_left.start()

    def on_anim_left(self, val):
        self.left_pos = val
        sh = self.height()
        target_y = (sh - self.left_drawer.height()) // 2
        self.left_drawer.move(val, target_y)
        w = self.left_drawer.width()
        # open_ratio from 0.0 (closed) to 1.0 (open)
        self.left_open_ratio = max(0.0, min(1.0, (val + w + 10) / (24 + w + 10)))
        self.left_drawer.update()
        self.update()

    def set_top_drawer_open(self, open_state):
        if self.top_open == open_state: return
        self.top_open = open_state
        self.anim_top.stop()
        start_y = self.top_drawer.y()
        end_y = 24 if open_state else -self.top_drawer.height() - 10
        self.anim_top.setStartValue(start_y)
        self.anim_top.setEndValue(end_y)
        self.anim_top.start()

    def on_anim_top(self, val):
        self.top_pos = val
        sw = self.width()
        target_x = (sw - self.top_drawer.width()) // 2
        self.top_drawer.move(target_x, val)
        h = self.top_drawer.height()
        self.top_open_ratio = max(0.0, min(1.0, (val + h + 10) / (24 + h + 10)))
        self.top_drawer.update()
        self.update()

    def set_right_drawer_open(self, open_state):
        if self.right_open == open_state: return
        self.right_open = open_state
        self.anim_right.stop()
        sw = self.width()
        start_x = self.right_drawer.x()
        end_x = sw - self.right_drawer.width() - 24 if open_state else sw + 10
        self.anim_right.setStartValue(start_x)
        self.anim_right.setEndValue(end_x)
        self.anim_right.start()

    def on_anim_right(self, val):
        self.right_pos = val
        sh = self.height()
        target_y = (sh - self.right_drawer.height()) // 2
        self.right_drawer.move(val, target_y)
        sw = self.width()
        target_open_x = sw - self.right_drawer.width() - 24
        closed_x = sw + 10
        self.right_open_ratio = max(0.0, min(1.0, (closed_x - val) / (closed_x - target_open_x)))
        self.right_drawer.update()
        self.update()

    # --- Mouse Tracking & Hysteresis ---
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.check_drawer_hover(event.pos())

    def check_drawer_hover(self, pos):
        mx, my = pos.x(), pos.y()
        sw, sh = self.width(), self.height()
        
        # 1. Left Drawer (Trigger <= 28px; Stay open in drawer rect + 25px)
        if not self.left_open:
            if mx <= 28 and (sh * 0.15 <= my <= sh * 0.85):
                self.set_left_drawer_open(True)
        else:
            safety_rect = self.left_drawer.geometry().adjusted(-28, -25, 25, 25)
            if not safety_rect.contains(pos):
                self.set_left_drawer_open(False)
                
        # 2. Top Drawer (Trigger <= 28px; Stay open in drawer rect + 25px)
        if not self.top_open:
            if my <= 28 and (sw * 0.20 <= mx <= sw * 0.80):
                self.set_top_drawer_open(True)
        else:
            safety_rect = self.top_drawer.geometry().adjusted(-25, -28, 25, 25)
            if not safety_rect.contains(pos):
                self.set_top_drawer_open(False)
                
        # 3. Right Drawer (Trigger >= sw - 28px; Avoid top-right and bottom-right buttons)
        if not self.right_open:
            if mx >= sw - 28 and (75 <= my <= sh - 75):
                self.set_right_drawer_open(True)
        else:
            safety_rect = self.right_drawer.geometry().adjusted(-25, -25, 28, 25)
            if not safety_rect.contains(pos):
                self.set_right_drawer_open(False)

    # --- Ambient Edge Glows with Breathing Pulse ---
    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        sw = float(self.width())
        sh = float(self.height())
        if sw <= 0 or sh <= 0: return
        
        t = getattr(self.clock, 'time_elapsed', 0.0)
        pulse = 0.80 + 0.20 * math.sin(t * 2.8)
        c_peri = QColor("#a5b4fc")
        
        # 1. Left Edge Ambient Glow
        left_alpha = int(60 * pulse * (1.0 - self.left_open_ratio))
        if left_alpha > 2:
            glow_h = 130.0
            glow_w = 16.0
            cy = sh / 2.0
            grad_l = QRadialGradient(QPointF(0, cy), glow_h / 2.0)
            grad_l.setColorAt(0.0, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), left_alpha))
            grad_l.setColorAt(0.5, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), int(left_alpha * 0.4)))
            grad_l.setColorAt(1.0, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), 0))
            p.setBrush(QBrush(grad_l))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(0, cy), glow_w * 2.0, glow_h / 2.0)
            
        # 2. Top Edge Ambient Glow
        top_alpha = int(60 * pulse * (1.0 - self.top_open_ratio))
        if top_alpha > 2:
            glow_w = 150.0
            glow_h = 16.0
            cx = sw / 2.0
            grad_t = QRadialGradient(QPointF(cx, 0), glow_w / 2.0)
            grad_t.setColorAt(0.0, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), top_alpha))
            grad_t.setColorAt(0.5, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), int(top_alpha * 0.4)))
            grad_t.setColorAt(1.0, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), 0))
            p.setBrush(QBrush(grad_t))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(cx, 0), glow_w / 2.0, glow_h * 2.0)
            
        # 3. Right Edge Ambient Glow
        right_alpha = int(60 * pulse * (1.0 - self.right_open_ratio))
        if right_alpha > 2:
            glow_h = 130.0
            glow_w = 16.0
            cy = sh / 2.0
            grad_r = QRadialGradient(QPointF(sw, cy), glow_h / 2.0)
            grad_r.setColorAt(0.0, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), right_alpha))
            grad_r.setColorAt(0.5, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), int(right_alpha * 0.4)))
            grad_r.setColorAt(1.0, QColor(c_peri.red(), c_peri.green(), c_peri.blue(), 0))
            p.setBrush(QBrush(grad_r))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(sw, cy), glow_w * 2.0, glow_h / 2.0)

    # --- Audio Drag and Drop ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for u in event.mimeData().urls():
                ext = os.path.splitext(u.toLocalFile())[1].lower()
                if ext in ['.wav', '.mp3', '.ogg', '.flac']:
                    event.acceptProposedAction()
                    self.set_left_drawer_open(True)
                    self.left_drawer.set_drop_highlight(True)
                    return
        event.ignore()

    def dragLeaveEvent(self, event):
        self.left_drawer.set_drop_highlight(False)

    def dropEvent(self, event):
        self.left_drawer.set_drop_highlight(False)
        if event.mimeData().hasUrls():
            for u in event.mimeData().urls():
                path = u.toLocalFile()
                ext = os.path.splitext(path)[1].lower()
                if ext in ['.wav', '.mp3', '.ogg', '.flac']:
                    self.handle_audio_file(path)
                    event.acceptProposedAction()
                    return

    def handle_audio_file(self, path):
        if not os.path.exists(path): return
        self.clock.custom_chime_path = path
        self.settings.custom_chime_path = path
        self.left_drawer.refresh_chime_combobox()
        self.settings.refresh_chime_combobox()
        self.settings.test_chime_sound()

    def browse_custom_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Hourly Chime Audio", "",
            "Audio Files (*.wav *.mp3 *.ogg *.flac)"
        )
        if file_path:
            self.handle_audio_file(file_path)

    # --- Mode Switcher Interaction ---
    def on_mode_switched(self, idx):
        self.clock.clock_style = idx
        self.clock.update()
        self.left_drawer.set_mode(idx)
        self.settings.set_mode(idx)

    # --- Action Dock Callbacks ---
    def apply_clicked(self):
        # Save in-memory configurations to disk
        self.settings.save_config()
        self.action_dock.btn_apply.setText("✓ Saved")
        self.action_dock.btn_apply.setStyleSheet(f"""
            QPushButton {{
                background-color: #10B981;
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.20);
                border-radius: 14px;
                font-weight: 600;
                font-size: 11.5px;
                padding: 5px 16px;
            }}
        """)
        QTimer.singleShot(1500, self.restore_apply_button)

    def restore_apply_button(self):
        if hasattr(self, 'action_dock'):
            self.action_dock.btn_apply.setText("Apply")
            self.action_dock.btn_apply.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.win_accent};
                    color: {self.contrast_text};
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    border-radius: 14px;
                    font-weight: 600;
                    font-size: 11.5px;
                    padding: 5px 16px;
                }}
                QPushButton:hover {{
                    background-color: {self.hover_accent};
                }}
            """)

    def reset_defaults_clicked(self):
        self.settings.reset_defaults()
        # Re-sync in-memory state
        self.clock.clock_scales = dict(self.settings.preview.clock_scales)
        self.clock.leading_zeros = dict(self.settings.preview.leading_zeros)
        self.clock.brightness = 100
        self.clock.use_24hr = False
        self.clock.show_bg = False
        self.clock.pixel_shift = False
        self.clock.hourly_chime = False
        self.clock.clock_style = 0
        self.clock.update()
        
        # Re-sync controls
        self.mode_capsule.set_current_mode(0)
        self.left_drawer.set_mode(0)
        self.top_drawer.bright_slider.setValue(100)
        self.top_drawer.cb_ambient.setChecked(False)
        self.top_drawer.cb_oled.setChecked(False)
        self.top_drawer.cb_24hr.setChecked(False)
        self.right_drawer.cb_strict.setChecked(False)
        self.right_drawer.cb_media.setChecked(False)
        self.right_drawer.cb_win.setChecked(False)

    def open_about(self):
        dlg = AboutDialog(self, win_accent=self.win_accent, auto_check=False)
        dlg.exec()

    def close_studio(self):
        self.close()
        if hasattr(self, 'settings') and self.settings:
            self.settings.raise_()
            self.settings.activateWindow()

    # --- Keyboard Controls ---
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            # Space toggles ambient mode live
            new_val = not self.clock.show_bg
            self.clock.show_bg = new_val
            self.clock.update()
            self.top_drawer.cb_ambient.setChecked(new_val)
            self.settings.ambient_cb.setChecked(new_val)
            event.accept()
            return
        elif event.key() in (Qt.Key.Key_Escape, Qt.Key.Key_F11):
            self.close_studio()
            event.accept()
            return
        elif event.key() == Qt.Key.Key_Z and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.close_studio()
            event.accept()
            return
        elif Qt.Key.Key_A <= event.key() <= Qt.Key.Key_Z or Qt.Key.Key_0 <= event.key() <= Qt.Key.Key_9:
            # Standard exit on keyboard press
            self.close_studio()
            event.accept()
            return
        super().keyPressEvent(event)


class SettingsDialog(QDialog):
    def __init__(self, config_path):
        super().__init__()
        self.setWindowTitle("Dinoscreener Settings")
        self.setFixedSize(680, 760)
        self.setAcceptDrops(True)
        
        # Subpixel ClearType Antialiased Font Hierarchy
        ui_font = QFont(["Segoe UI Variable Text", "Segoe UI", "Arial", "sans-serif"])
        ui_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
        ui_font.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
        self.setFont(ui_font)
        
        # Load Application Icon
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
        if getattr(sys, 'frozen', False):
            logo_path = os.path.join(sys._MEIPASS, "app_icon.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        self.logo_path = logo_path
        
        # Windows 11 DWM Mica / Glass Blur Backdrop Setup
        self.is_dwm_active = apply_windows_dwm_effects(self)

        self.win_accent = get_windows_accent_color()
        self.contrast_text, self.hover_accent, self.press_accent = get_color_variants(self.win_accent)
        check_icon_path = get_or_create_check_icon(self.contrast_text)
        chevron_icon_path = get_or_create_chevron_icon()

        bg_dialog = "rgba(16, 20, 29, 0.72)" if self.is_dwm_active else "#10141D"
        bg_card = "rgba(23, 27, 38, 0.78)" if self.is_dwm_active else "#171B26"

        # Spatial Studio Modern Glass Stylesheet (DWM Mica / Glass Blur with clean solid fallback)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_dialog};
            }}
            QLabel {{
                color: #FFFFFF;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', -apple-system, sans-serif;
            }}
            QFrame#bentoCard {{
                background: {bg_card};
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
            }}
            QFrame#previewCard {{
                background: #000000;
                border: none;
                border-radius: 12px;
            }}
            /* Fluent Checkbox with Windows Accent Color & Rounded Indicator */
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
                width: 17px;
                height: 17px;
                border: 1px solid rgba(255, 255, 255, 0.22);
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.05);
            }}
            QCheckBox::indicator:hover {{
                border-color: rgba(255, 255, 255, 0.45);
                background: rgba(255, 255, 255, 0.09);
            }}
            QCheckBox::indicator:checked {{
                background-color: {self.win_accent};
                border-color: {self.win_accent};
                border-radius: 6px;
                image: url("{check_icon_path}");
            }}
            /* Tactile Modern Slider with Windows Accent */
            QSlider {{
                min-height: 24px;
                background: transparent;
            }}
            QSlider::groove:horizontal {{
                height: 6px;
                background: rgba(255, 255, 255, 0.12);
                border-radius: 3px;
            }}
            QSlider::sub-page:horizontal {{
                background: {self.win_accent};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: #FFFFFF;
                border: 2px solid {self.win_accent};
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}
            QSlider::handle:horizontal:hover {{
                background: #FFFFFF;
                border: 2px solid #FFFFFF;
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }}
            /* Comboboxes - Smooth Rounded Pill Style with Visible Chevron Arrow */
            QComboBox, QFontComboBox {{
                background: rgba(255, 255, 255, 0.06);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 12px;
                padding: 4px 10px;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
                font-size: 11px;
                min-height: 20px;
            }}
            QComboBox:hover, QFontComboBox:hover {{
                background: rgba(255, 255, 255, 0.10);
                border-color: rgba(255, 255, 255, 0.28);
            }}
            QComboBox::drop-down, QFontComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 22px;
                border: none;
            }}
            QComboBox::down-arrow, QFontComboBox::down-arrow {{
                image: url("{chevron_icon_path}");
                width: 10px;
                height: 10px;
            }}
            QComboBox QAbstractItemView, QFontComboBox QAbstractItemView {{
                background: #181C26;
                color: #FFFFFF;
                selection-background-color: {self.win_accent};
                selection-color: {self.contrast_text};
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 10px;
                padding: 4px;
            }}
        """)
        
        self.config_path = config_path
        self.config = self.load_config()
        self.custom_chime_path = self.config.get("custom_chime_path", "")
        
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
            
        self.latest_update_info = None
        self.initUI()
        self.installEventFilter(self)
        self.check_font_changed()
        self.check_char_changed()
        
        # Start background update check
        self.bg_update_worker = UpdateCheckerWorker()
        self.bg_update_worker.update_result.connect(self.on_bg_update_checked)
        self.bg_update_worker.start()
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for u in event.mimeData().urls():
                ext = os.path.splitext(u.toLocalFile())[1].lower()
                if ext in ['.ttf', '.otf', '.png', '.jpg', '.jpeg', '.bmp', '.webp', '.wav', '.mp3', '.ogg', '.flac']:
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
                elif ext in ['.wav', '.mp3', '.ogg', '.flac']:
                    self.handle_sound_import(path)
                    self.set_mode(0)
                    event.acceptProposedAction()
                    return

    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Space:
                if hasattr(self, 'ambient_cb'):
                    self.ambient_cb.setChecked(not self.ambient_cb.isChecked())
                    return True
            elif event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
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

    def get_default_config(self):
        return {
            "accent_color": self.win_accent,
            "show_info": True,
            "show_weather": True,
            "show_battery": True,
            "use_fahrenheit": False,
            "ambient_mode": False,
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
            "hourly_chime": False,
            "chime_preset": "acoustic_bell",
            "chime_volume": 45,
            "custom_chime_path": "",
            "primary_font": "",
            "ignore_media_keys": False,
            "dino_font": "Bungee",
            "character_type": "dino",
            "custom_character_image": ""
        }

    def load_config(self):
        default_config = self.get_default_config()
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    loaded = json.load(f)
                    if loaded.get("accent_color") in ["#0078D4", "#8F96BF", None]:
                        loaded["accent_color"] = self.win_accent
                    if "show_weather" not in loaded and "show_info" in loaded:
                        loaded["show_weather"] = loaded["show_info"]
                    if "show_battery" not in loaded and "show_info" in loaded:
                        loaded["show_battery"] = loaded["show_info"]
                    if "use_fahrenheit" not in loaded and "live_weather" in loaded:
                        loaded["use_fahrenheit"] = loaded["live_weather"]
                    default_config.update(loaded)
            except Exception:
                pass
        return default_config

    def save_config(self):
        self.config["show_weather"] = self.show_weather_cb.isChecked()
        self.config["show_battery"] = self.show_battery_cb.isChecked()
        self.config["use_fahrenheit"] = self.fahrenheit_cb.isChecked()
        self.config["show_info"] = self.show_weather_cb.isChecked() or self.show_battery_cb.isChecked()
        self.config["ambient_mode"] = self.ambient_cb.isChecked()
        self.config["strict_exit"] = self.strict_cb.isChecked()
        self.config["enable_win_key"] = self.win_cb.isChecked()
        self.config["brightness"] = self.bright_slider.value()
        self.config["clock_style"] = self.preview.clock_style
        self.config["clock_scales"] = self.preview.clock_scales
        self.config["use_24hr"] = self.use_24hr_cb.isChecked()
        self.config["leading_zeros"] = self.preview.leading_zeros
        self.config["pixel_shift"] = self.pixel_shift_cb.isChecked()
        self.config["hourly_chime"] = self.hourly_chime_cb.isChecked()
        self.config["chime_preset"] = self.chime_sound_cb.currentData() if hasattr(self, 'chime_sound_cb') else "acoustic_bell"
        self.config["chime_volume"] = self.chime_vol_slider.value() if hasattr(self, 'chime_vol_slider') else 45
        self.config["custom_chime_path"] = getattr(self, "custom_chime_path", "")
        self.config["primary_font"] = getattr(self, 'primary_font', "")
        self.config["ignore_media_keys"] = self.ignore_media_cb.isChecked()
        self.config["dino_font"] = getattr(self.preview, 'dino_font', "Bungee")
        self.config["character_type"] = getattr(self.preview, 'character_type', "dino")
        self.config["custom_character_image"] = getattr(self, 'custom_character_image', "")
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def save_settings(self):
        self.save_config()
        self.accept()

    def test_fullscreen(self):
        try:
            self.studio = FullscreenStudioMode(self)
            self.studio.showFullScreen()
        except Exception as e:
            print("Error launching fullscreen studio mode:", e)

    def reset_defaults(self):
        # Reset UI controls and in-memory stage preview to factory defaults.
        # CRITICAL: self.config_path on disk is NOT modified until the user explicitly clicks 'Apply'!
        self.config = self.get_default_config()
        self.preview.clock_scales = dict(self.config["clock_scales"])
        self.preview.leading_zeros = dict(self.config["leading_zeros"])
        self.scale_slider.setValue(int(self.preview.clock_scales.get("0", 0.45) * 100))
        self.bright_slider.setValue(100)
        self.use_24hr_cb.setChecked(False)
        self.leading_zero_cb.setChecked(False)
        self.ambient_cb.setChecked(False)
        self.strict_cb.setChecked(False)
        self.ignore_media_cb.setChecked(False)
        self.win_cb.setChecked(False)
        self.pixel_shift_cb.setChecked(False)
        self.hourly_chime_cb.setChecked(False)
        self.custom_chime_path = ""
        if hasattr(self, 'chime_vol_slider'):
            self.chime_vol_slider.setValue(45)
        self.refresh_chime_combobox()
        self.show_weather_cb.setChecked(True)
        self.show_battery_cb.setChecked(True)
        self.fahrenheit_cb.setChecked(False)
        self.revert_font()
        self.revert_character()
        self.set_accent_color(self.win_accent)
        self.set_mode(0)

    def on_preview_scale_scrolled(self, val):
        if hasattr(self, 'scale_slider'):
            self.scale_slider.blockSignals(True)
            self.scale_slider.setValue(val)
            self.scale_slider.blockSignals(False)
            self.lbl_scale_pct.setText(f"{val}%")

    def initUI(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(18, 12, 18, 12)
        root_layout.setSpacing(8)
        
        # 1. TOP HEADER (App Branding with Logo on the left)
        header_row = QHBoxLayout()
        header_row.setContentsMargins(2, 0, 2, 0)
        header_row.setSpacing(10)
        
        lbl_logo = QLabel()
        lbl_logo.setFixedSize(38, 38)
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setStyleSheet("""
            QLabel {
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.16);
                border-radius: 9px;
            }
        """)
        if hasattr(self, 'logo_path') and os.path.exists(self.logo_path):
            lbl_logo.setPixmap(get_rounded_pixmap(self.logo_path, size=38, radius=9, dpr=3.0))
        header_row.addWidget(lbl_logo, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        brand_box = QVBoxLayout()
        brand_box.setSpacing(1)
        lbl_app_name = QLabel("Dinoscreener")
        lbl_app_name.setStyleSheet("font-size: 15px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.2px;")
        lbl_app_sub = QLabel("ScreenSaver Settings :)")
        lbl_app_sub.setStyleSheet("font-size: 11px; color: #94A3B8;")
        brand_box.addWidget(lbl_app_name)
        brand_box.addWidget(lbl_app_sub)
        header_row.addLayout(brand_box)
        header_row.addStretch()

        self.btn_update_badge = QPushButton("✨ Update Available")
        self.btn_update_badge.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.win_accent};
                color: {self.contrast_text};
                border: none;
                border-radius: 12px;
                font-weight: 600;
                font-size: 11px;
                padding: 4px 11px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_accent};
            }}
        """)
        self.btn_update_badge.setVisible(False)
        self.btn_update_badge.clicked.connect(lambda: self.open_about_dialog(auto_check=False))
        header_row.addWidget(self.btn_update_badge, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.btn_info = QPushButton()
        self.btn_info.setObjectName("btnInfo")
        self.btn_info.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_info.setIcon(get_or_create_info_duotone_icon(self.win_accent))
        self.btn_info.setIconSize(QSize(20, 20))
        self.btn_info.setFixedSize(30, 30)
        self.btn_info.setToolTip("About, version & updates")
        self.btn_info.setStyleSheet("""
            QPushButton#btnInfo {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 15px;
                outline: none;
            }
            QPushButton#btnInfo:hover {
                background: rgba(255, 255, 255, 0.14);
                border-color: rgba(255, 255, 255, 0.28);
            }
            QPushButton#btnInfo:pressed {
                background: rgba(255, 255, 255, 0.06);
            }
        """)
        self.btn_info.clicked.connect(lambda: self.open_about_dialog(auto_check=False))
        header_row.addWidget(self.btn_info, alignment=Qt.AlignmentFlag.AlignVCenter)

        root_layout.addLayout(header_row)
        
        # 2. 16:9 WIDESCREEN PREVIEW STAGE (Authentic Monitor Aspect Ratio)
        self.stage_frame = SpatialStageFrame()
        self.stage_frame.setFixedSize(644, 364)
        stage_layout = QVBoxLayout(self.stage_frame)
        stage_layout.setContentsMargins(2, 2, 2, 2)
        
        self.preview_card = QFrame()
        self.preview_card.setObjectName("previewCard")
        preview_layout = QVBoxLayout(self.preview_card)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        start_style = self.config.get("clock_style", 0)
        self.preview = CrispAestheticFlipClock(
            accent_color=self.config.get("accent_color", self.win_accent),
            enable_win_key=self.config.get("enable_win_key", False),
            strict_exit=self.config.get("strict_exit", False),
            show_info=self.config.get("show_info", True),
            show_weather=self.config.get("show_weather", True),
            show_battery=self.config.get("show_battery", True),
            use_fahrenheit=self.config.get("use_fahrenheit", False),
            ambient_mode=self.config.get("ambient_mode", False),
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
            custom_character_image=self.config.get("custom_character_image", ""),
            pixel_shift=self.config.get("pixel_shift", False),
            hourly_chime=self.config.get("hourly_chime", False)
        )
        self.preview.setFixedSize(640, 360) # Exact 16:9 widescreen ratio
        self.preview.scale_callback = self.on_preview_scale_scrolled
        preview_layout.addWidget(self.preview)
        stage_layout.addWidget(self.preview_card)
        root_layout.addWidget(self.stage_frame, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # 3. FLOATING COLLAPSIBLE CAPSULE (Minimized Pill that Expands on Hover)
        capsule_row = QHBoxLayout()
        capsule_row.setContentsMargins(0, 6, 0, 6)
        capsule_row.addStretch()
        
        self.mode_capsule = CollapsibleModeCapsule(win_accent=self.win_accent)
        self.mode_capsule.on_mode_changed = self.set_mode
        self.mode_buttons = self.mode_capsule.mode_buttons
        
        capsule_row.addWidget(self.mode_capsule)
        capsule_row.addStretch()
        root_layout.addLayout(capsule_row)
        
        # 4. THREE BALANCED SPATIAL BENTO CARDS (Rounded 14px)
        cards_row = QHBoxLayout()
        cards_row.setSpacing(10)
        cards_row.setContentsMargins(0, 0, 0, 0)
        
        # === CARD 1: Mode Parameters ===
        card_mode = QFrame()
        card_mode.setObjectName("bentoCard")
        card_mode_layout = QVBoxLayout(card_mode)
        card_mode_layout.setContentsMargins(12, 11, 12, 11)
        card_mode_layout.setSpacing(8)
        
        self.lbl_mode_title = QLabel("Flip Clock")
        self.lbl_mode_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #FFFFFF;")
        card_mode_layout.addWidget(self.lbl_mode_title)
        
        self.pages = QStackedWidget()
        
        # --- Page 0: Flip Clock ---
        page_flip = QWidget()
        flip_layout = QVBoxLayout(page_flip)
        flip_layout.setContentsMargins(0, 2, 0, 0)
        flip_layout.setSpacing(8)
        
        scale_header = QHBoxLayout()
        lbl_scale_title = QLabel("Clock Scale")
        lbl_scale_title.setStyleSheet("color: #E2E8F0; font-size: 11.5px; font-weight: 500;")
        init_scale = int(self.preview.clock_scales.get("0", 0.45) * 100)
        self.lbl_scale_pct = QLabel(f"{init_scale}%")
        self.lbl_scale_pct.setStyleSheet(f"color: {self.win_accent}; font-size: 12px; font-weight: 600;")
        scale_header.addWidget(lbl_scale_title)
        scale_header.addStretch()
        scale_header.addWidget(self.lbl_scale_pct)
        flip_layout.addLayout(scale_header)
        
        scale_box = QHBoxLayout()
        scale_box.setSpacing(6)
        
        undo_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.06);
                color: #94A3B8;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 11px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.14);
                color: #FFFFFF;
                border-color: rgba(255, 255, 255, 0.25);
            }
        """
        btn_step_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.06);
                color: #CBD5E1;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 12px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
                color: #FFFFFF;
                border-color: rgba(255, 255, 255, 0.25);
            }
        """
        self.btn_scale_minus = QPushButton("−")
        self.btn_scale_minus.setFixedSize(24, 24)
        self.btn_scale_minus.setStyleSheet(btn_step_style)
        self.btn_scale_minus.clicked.connect(lambda: self.step_scale(-5))
        scale_box.addWidget(self.btn_scale_minus)
        
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(15, 95)
        self.scale_slider.setValue(init_scale)
        self.scale_slider.valueChanged.connect(self.update_scale)
        self.scale_slider.setToolTip("Scroll mouse on preview or press + / − anytime to adjust scale")
        scale_box.addWidget(self.scale_slider, stretch=1)
        
        self.btn_scale_plus = QPushButton("+")
        self.btn_scale_plus.setFixedSize(24, 24)
        self.btn_scale_plus.setStyleSheet(btn_step_style)
        self.btn_scale_plus.clicked.connect(lambda: self.step_scale(5))
        scale_box.addWidget(self.btn_scale_plus)
        flip_layout.addLayout(scale_box)

        # --- Hourly Bell Chime & Audio Customization ---
        chime_row = QHBoxLayout()
        chime_row.setContentsMargins(0, 4, 0, 0)
        chime_row.setSpacing(6)
        self.hourly_chime_cb = QCheckBox("Hourly Chime")
        self.hourly_chime_cb.setChecked(self.config.get("hourly_chime", False))
        self.hourly_chime_cb.setToolTip("Plays a chime every hour on the hour")
        self.hourly_chime_cb.stateChanged.connect(self.on_hourly_chime_changed)
        chime_row.addWidget(self.hourly_chime_cb)
        
        self.btn_test_chime = QPushButton("🔔 Test")
        self.btn_test_chime.setToolTip("Preview chime at current volume")
        self.btn_test_chime.setFixedWidth(56)
        self.btn_test_chime.setFixedHeight(22)
        self.btn_test_chime.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                color: #FFFFFF;
                font-size: 11px;
                font-weight: 600;
                padding: 0px 4px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.16);
                border-color: rgba(255, 255, 255, 0.30);
            }
        """)
        self.btn_test_chime.clicked.connect(self.test_chime_sound)
        chime_row.addWidget(self.btn_test_chime)
        chime_row.addStretch()
        flip_layout.addLayout(chime_row)

        sound_box = QHBoxLayout()
        sound_box.setSpacing(5)
        lbl_sound = QLabel("Sound:")
        lbl_sound.setFixedWidth(38)
        lbl_sound.setStyleSheet("color: #E2E8F0; font-size: 11px; font-weight: 500;")
        sound_box.addWidget(lbl_sound)

        self.chime_sound_cb = QComboBox()
        self.chime_sound_cb.setToolTip("Select chime tone or drop custom audio file")
        self.refresh_chime_combobox()
        self.chime_sound_cb.currentIndexChanged.connect(self.on_chime_preset_changed)
        sound_box.addWidget(self.chime_sound_cb, stretch=1)

        self.btn_browse_sound = QPushButton("📂")
        self.btn_browse_sound.setFixedSize(22, 22)
        self.btn_browse_sound.setStyleSheet(undo_style)
        self.btn_browse_sound.setToolTip("Browse or drop custom audio (.wav, .mp3, .ogg)")
        self.btn_browse_sound.clicked.connect(self.browse_custom_sound)
        sound_box.addWidget(self.btn_browse_sound)
        flip_layout.addLayout(sound_box)

        vol_box = QHBoxLayout()
        vol_box.setSpacing(6)
        lbl_vol = QLabel("Vol:")
        lbl_vol.setFixedWidth(38)
        lbl_vol.setStyleSheet("color: #E2E8F0; font-size: 11px; font-weight: 500;")
        vol_box.addWidget(lbl_vol)

        init_vol = self.config.get("chime_volume", 45)
        self.chime_vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.chime_vol_slider.setRange(5, 100)
        self.chime_vol_slider.setValue(init_vol)
        self.chime_vol_slider.setToolTip("Adjust chime playback volume")
        self.chime_vol_slider.valueChanged.connect(self.on_chime_volume_changed)
        vol_box.addWidget(self.chime_vol_slider, stretch=1)

        self.lbl_chime_vol = QLabel(f"{init_vol}%")
        self.lbl_chime_vol.setStyleSheet(f"color: {self.win_accent}; font-size: 11px; font-weight: 600; min-width: 28px;")
        vol_box.addWidget(self.lbl_chime_vol)
        flip_layout.addLayout(vol_box)

        lbl_chime_tip = QLabel("Drop any audio file to use your own chime")
        lbl_chime_tip.setStyleSheet("color: #64748B; font-size: 9.5px;")
        flip_layout.addWidget(lbl_chime_tip)

        flip_layout.addStretch()
        self.pages.addWidget(page_flip)
        
        # --- Page 1: Rotary Modern ---
        page_rotary = QWidget()
        rot_layout = QVBoxLayout(page_rotary)
        rot_layout.setContentsMargins(0, 2, 0, 0)
        rot_layout.setSpacing(8)
        
        accent_box = QHBoxLayout()
        accent_box.setSpacing(5)
        lbl_dial = QLabel("Accent:")
        lbl_dial.setStyleSheet("color: #E2E8F0; font-size: 11.5px; font-weight: 500;")
        accent_box.addWidget(lbl_dial)
        
        self.swatch_buttons = []
        raw_presets = [self.win_accent, "#0078D4", "#60CDFF", "#10B981", "#F59E0B"]
        seen = set()
        preset_colors = []
        for c in raw_presets:
            cu = c.upper()
            if cu not in seen:
                seen.add(cu)
                preset_colors.append(c)
        preset_colors = preset_colors[:5]
        
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
                border-radius: 10px;
                padding: 2px 7px;
                font-size: 10.5px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.14);
                color: #FFFFFF;
                border-color: rgba(255, 255, 255, 0.25);
            }
        """)
        btn_custom.clicked.connect(self.pick_color)
        accent_box.addWidget(btn_custom)
        accent_box.addStretch()
        rot_layout.addLayout(accent_box)
        
        self.show_weather_cb = QCheckBox("Show Weather")
        self.show_weather_cb.setChecked(self.config.get("show_weather", self.config.get("show_info", True)))
        self.show_weather_cb.stateChanged.connect(self.update_rotary_telemetry)
        rot_layout.addWidget(self.show_weather_cb)
        
        self.show_battery_cb = QCheckBox("Show Battery")
        self.show_battery_cb.setChecked(self.config.get("show_battery", self.config.get("show_info", True)))
        self.show_battery_cb.stateChanged.connect(self.update_rotary_telemetry)
        rot_layout.addWidget(self.show_battery_cb)
        
        self.fahrenheit_cb = QCheckBox("Fahrenheit Format (°F)")
        self.fahrenheit_cb.setChecked(self.config.get("use_fahrenheit", self.config.get("live_weather", False)))
        self.fahrenheit_cb.setToolTip("Toggle temperature display between Celsius (°C) and Fahrenheit (°F)")
        self.fahrenheit_cb.stateChanged.connect(self.update_rotary_telemetry)
        rot_layout.addWidget(self.fahrenheit_cb)
        rot_layout.addStretch()
        self.pages.addWidget(page_rotary)
        
        # --- Page 2: Dino Runner ---
        page_dino = QWidget()
        dino_layout = QVBoxLayout(page_dino)
        dino_layout.setContentsMargins(0, 2, 0, 0)
        dino_layout.setSpacing(7)
        
        undo_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.06);
                color: #94A3B8;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 11px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.16);
                color: #FFFFFF;
                border-color: rgba(255, 255, 255, 0.25);
            }
        """
        
        # 1. Unified Font Dropdown (Curated list + Import Font option)
        font_box = QHBoxLayout()
        font_box.setSpacing(6)
        lbl_dino_font = QLabel("Font:")
        lbl_dino_font.setFixedWidth(40)
        lbl_dino_font.setStyleSheet("color: #E2E8F0; font-size: 11px; font-weight: 500;")
        font_box.addWidget(lbl_dino_font)
        
        self.primary_font = self.config.get("primary_font", "")
        self.font_cb = QComboBox()
        self.refresh_font_combobox()
        self.font_cb.currentIndexChanged.connect(self.on_font_combobox_changed)
        font_box.addWidget(self.font_cb, stretch=1)
        
        self.undo_font_btn = QPushButton("↺")
        self.undo_font_btn.setFixedSize(22, 22)
        self.undo_font_btn.setStyleSheet(undo_style)
        self.undo_font_btn.setToolTip("Revert font to saved settings")
        self.undo_font_btn.clicked.connect(self.revert_font)
        self.undo_font_btn.hide()
        font_box.addWidget(self.undo_font_btn)
        dino_layout.addLayout(font_box)
        
        # 2. Unified Sprite Dropdown (Dino default + Custom sprite + Import option)
        char_box = QHBoxLayout()
        char_box.setSpacing(6)
        lbl_sprite = QLabel("Sprite:")
        lbl_sprite.setFixedWidth(40)
        lbl_sprite.setStyleSheet("color: #E2E8F0; font-size: 11px; font-weight: 500;")
        char_box.addWidget(lbl_sprite)
        
        self.custom_character_image = self.config.get("custom_character_image", "")
        self.char_cb = QComboBox()
        self.refresh_char_combobox()
        self.char_cb.currentIndexChanged.connect(self.on_char_combobox_changed)
        char_box.addWidget(self.char_cb, stretch=1)
        
        self.undo_char_btn = QPushButton("↺")
        self.undo_char_btn.setFixedSize(22, 22)
        self.undo_char_btn.setStyleSheet(undo_style)
        self.undo_char_btn.setToolTip("Revert character to default Dino")
        self.undo_char_btn.clicked.connect(self.revert_character)
        self.undo_char_btn.hide()
        char_box.addWidget(self.undo_char_btn)
        dino_layout.addLayout(char_box)
        
        lbl_dino_tip = QLabel("Drop font or sprite image to customize")
        lbl_dino_tip.setStyleSheet("color: #64748B; font-size: 10px;")
        dino_layout.addWidget(lbl_dino_tip)
        dino_layout.addStretch()
        self.pages.addWidget(page_dino)
        
        card_mode_layout.addWidget(self.pages)
        cards_row.addWidget(card_mode, stretch=1)
        
        # === CARD 2: Display & Atmosphere ===
        card_disp = QFrame()
        card_disp.setObjectName("bentoCard")
        card_disp_layout = QVBoxLayout(card_disp)
        card_disp_layout.setContentsMargins(12, 11, 12, 11)
        card_disp_layout.setSpacing(8)
        
        lbl_disp_title = QLabel("Display")
        lbl_disp_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #FFFFFF;")
        card_disp_layout.addWidget(lbl_disp_title)
        
        # Huge Tactile Brightness Bar
        bright_header = QHBoxLayout()
        lbl_bright_title = QLabel("Brightness")
        lbl_bright_title.setStyleSheet("color: #E2E8F0; font-size: 11.5px; font-weight: 500;")
        self.bright_val_label = QLabel(f"{self.config.get('brightness', 100)}%")
        self.bright_val_label.setStyleSheet(f"color: {self.win_accent}; font-size: 12px; font-weight: 600;")
        bright_header.addWidget(lbl_bright_title)
        bright_header.addStretch()
        bright_header.addWidget(self.bright_val_label)
        card_disp_layout.addLayout(bright_header)
        
        bright_box = QHBoxLayout()
        bright_box.setSpacing(6)
        lbl_sun1 = QLabel("☼")
        lbl_sun1.setStyleSheet("color: #64748B; font-size: 13px;")
        lbl_sun2 = QLabel("☀")
        lbl_sun2.setStyleSheet("color: #94A3B8; font-size: 15px;")
        
        self.bright_slider = QSlider(Qt.Orientation.Horizontal)
        self.bright_slider.setRange(10, 100)
        self.bright_slider.setValue(self.config.get("brightness", 100))
        self.bright_slider.valueChanged.connect(self.update_brightness)
        bright_box.addWidget(lbl_sun1)
        bright_box.addWidget(self.bright_slider, stretch=1)
        bright_box.addWidget(lbl_sun2)
        card_disp_layout.addLayout(bright_box)
        
        # Display Toggles
        self.ambient_cb = QCheckBox("Ambient Mode (Space)")
        self.ambient_cb.setChecked(self.config.get("ambient_mode", self.preview.show_bg))
        self.ambient_cb.setToolTip("Soft ambient glow behind clock (press Spacebar anytime)")
        self.ambient_cb.stateChanged.connect(self.on_ambient_cb_changed)
        card_disp_layout.addWidget(self.ambient_cb)

        self.pixel_shift_cb = QCheckBox("OLED Burn-in Protection")
        self.pixel_shift_cb.setChecked(self.config.get("pixel_shift", False))
        self.pixel_shift_cb.setToolTip("Subtle orbital shift so OLED screens don't get burn-in")
        self.pixel_shift_cb.stateChanged.connect(self.update_pixel_shift)
        card_disp_layout.addWidget(self.pixel_shift_cb)

        self.use_24hr_cb = QCheckBox("24-Hour Format")
        self.use_24hr_cb.setChecked(self.config.get("use_24hr", False))
        self.use_24hr_cb.stateChanged.connect(self.update_24hr)
        card_disp_layout.addWidget(self.use_24hr_cb)
        
        self.leading_zero_cb = QCheckBox("Leading Zeros")
        self.leading_zero_cb.setChecked(self.preview.leading_zeros.get(str(start_style), False))
        self.leading_zero_cb.stateChanged.connect(self.update_leading_zero)
        card_disp_layout.addWidget(self.leading_zero_cb)
        card_disp_layout.addStretch()
        cards_row.addWidget(card_disp, stretch=1)
        
        # === CARD 3: System & Security ===
        card_sys = QFrame()
        card_sys.setObjectName("bentoCard")
        card_sys_layout = QVBoxLayout(card_sys)
        card_sys_layout.setContentsMargins(12, 11, 12, 11)
        card_sys_layout.setSpacing(8)
        
        lbl_sys_title = QLabel("System")
        lbl_sys_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #FFFFFF;")
        card_sys_layout.addWidget(lbl_sys_title)
        
        self.strict_cb = QCheckBox("Lock on Exit (Ctrl+Z)")
        self.strict_cb.setChecked(self.config.get("strict_exit", False))
        self.strict_cb.setToolTip("Requires pressing Ctrl+Z to dismiss the screensaver")
        self.strict_cb.stateChanged.connect(lambda s: setattr(self.preview, 'strict_exit', self.strict_cb.isChecked()))
        card_sys_layout.addWidget(self.strict_cb)
        
        self.ignore_media_cb = QCheckBox("Ignore Media Keys")
        self.ignore_media_cb.setChecked(self.config.get("ignore_media_keys", False))
        self.ignore_media_cb.setToolTip("Volume and track keys won't close screensaver")
        self.ignore_media_cb.stateChanged.connect(lambda s: setattr(self.preview, 'ignore_media_keys', self.ignore_media_cb.isChecked()))
        card_sys_layout.addWidget(self.ignore_media_cb)
        
        self.win_cb = QCheckBox("Enable Windows Key")
        self.win_cb.setChecked(self.config.get("enable_win_key", False))
        self.win_cb.setToolTip("Use Windows key without waking screensaver")
        self.win_cb.stateChanged.connect(lambda s: setattr(self.preview, 'enable_win_key', self.win_cb.isChecked()))
        card_sys_layout.addWidget(self.win_cb)
        card_sys_layout.addStretch()
        cards_row.addWidget(card_sys, stretch=1)
        
        root_layout.addLayout(cards_row)
        
        # 5. FOOTER ACTIONS (Pill Rounded)
        footer_row = QHBoxLayout()
        footer_row.setContentsMargins(4, 2, 4, 0)
        
        self.btn_fullscreen = QPushButton()
        self.btn_fullscreen.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_fullscreen.setIcon(get_or_create_fullscreen_duotone_icon(self.win_accent))
        self.btn_fullscreen.setIconSize(QSize(20, 20))
        self.btn_fullscreen.setFixedSize(36, 32)
        self.btn_fullscreen.setToolTip("Fullscreen Preview")
        self.btn_fullscreen.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 16px;
                outline: none;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.12);
                border-color: rgba(255, 255, 255, 0.28);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.04);
            }
        """)
        self.btn_fullscreen.clicked.connect(self.test_fullscreen)
        footer_row.addWidget(self.btn_fullscreen)
        footer_row.addStretch()
        
        btn_reset = QPushButton("Reset Defaults")
        btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reset.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94A3B8;
                border: none;
                border-radius: 14px;
                padding: 7px 14px;
                font-size: 12px;
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
        btn_apply.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.win_accent};
                color: {self.contrast_text};
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 16px;
                padding: 7px 32px;
                font-size: 12px;
                font-weight: 600;
                font-family: 'Segoe UI Variable Text', 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{
                background-color: {self.hover_accent};
            }}
            QPushButton:pressed {{
                background-color: {self.press_accent};
            }}
        """)
        btn_apply.clicked.connect(self.save_settings)
        footer_row.addWidget(btn_apply)
        root_layout.addLayout(footer_row)
        
        self.set_mode(start_style)

    def set_mode(self, idx):
        self.preview.clock_style = idx
        self.preview.update()
        if hasattr(self, 'stage_frame'):
            self.stage_frame.set_stage_theme(idx, self.config.get("accent_color", self.win_accent))
        if hasattr(self, 'mode_capsule'):
            self.mode_capsule.set_current_mode(idx)
        else:
            for i, btn in enumerate(self.mode_buttons):
                btn.blockSignals(True)
                btn.setChecked(i == idx)
                btn.blockSignals(False)
        self.pages.setCurrentIndex(idx)
        titles = ["Flip Clock", "Rotary Modern", "Dino Runner"]
        if idx < len(titles):
            self.lbl_mode_title.setText(titles[idx])
        self.update_swatch_highlights()
        if hasattr(self, 'leading_zero_cb'):
            self.leading_zero_cb.blockSignals(True)
            self.leading_zero_cb.setChecked(self.preview.leading_zeros.get(str(idx), False))
            self.leading_zero_cb.blockSignals(False)
        self.repaint()

    def update_swatch_highlights(self):
        if not hasattr(self, 'swatch_buttons'):
            return
        curr = self.config.get("accent_color", self.win_accent).upper()
        for hex_code, btn in self.swatch_buttons:
            if hex_code.upper() == curr:
                btn.setStyleSheet(f"background-color: {hex_code}; border: 2px solid #FFFFFF; border-radius: 10px;")
            else:
                btn.setStyleSheet(f"background-color: {hex_code}; border: 1px solid rgba(255, 255, 255, 0.25); border-radius: 10px;")

    def set_accent_color(self, hex_code):
        self.config["accent_color"] = hex_code
        self.preview.set_accent_color(hex_code)
        if hasattr(self, 'stage_frame'):
            self.stage_frame.set_stage_theme(self.preview.clock_style, hex_code)
        if hasattr(self, 'mode_capsule'):
            self.mode_capsule.update_accent(hex_code)
        if hasattr(self, 'btn_fullscreen'):
            self.btn_fullscreen.setIcon(get_or_create_fullscreen_duotone_icon(hex_code))
        if hasattr(self, 'btn_info'):
            self.btn_info.setIcon(get_or_create_info_duotone_icon(hex_code))
        self.update_swatch_highlights()


    def pick_color(self):
        color = QColorDialog.getColor(QColor(self.config.get("accent_color", self.win_accent)), self, "Select Accent Color")
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

    def on_ambient_cb_changed(self, state=None):
        val = self.ambient_cb.isChecked()
        self.preview.show_bg = val
        self.config["ambient_mode"] = val
        self.preview.update()

    def on_hourly_chime_changed(self, state=None):
        val = self.hourly_chime_cb.isChecked()
        self.preview.hourly_chime = val
        self.config["hourly_chime"] = val

    def refresh_chime_combobox(self):
        if not hasattr(self, 'chime_sound_cb'):
            return
        self.chime_sound_cb.blockSignals(True)
        self.chime_sound_cb.clear()
        current_preset = self.config.get("chime_preset", "acoustic_bell")
        selected_idx = 0
        for idx, (key, label) in enumerate(CHIME_PRESETS):
            self.chime_sound_cb.addItem(label, key)
            if key == current_preset and not getattr(self, 'custom_chime_path', ''):
                selected_idx = idx
        if getattr(self, 'custom_chime_path', '') and os.path.exists(self.custom_chime_path):
            base_name = os.path.splitext(os.path.basename(self.custom_chime_path))[0]
            display_name = f"Custom ({base_name[:12]})"
            self.chime_sound_cb.addItem(display_name, "custom")
            if current_preset == "custom":
                selected_idx = self.chime_sound_cb.count() - 1
        self.chime_sound_cb.setCurrentIndex(selected_idx)
        self.chime_sound_cb.blockSignals(False)

    def on_chime_preset_changed(self, idx):
        key = self.chime_sound_cb.currentData()
        if key == "custom":
            self.config["chime_preset"] = "custom"
            self.preview.chime_preset = "custom"
        else:
            self.config["chime_preset"] = key
            self.preview.chime_preset = key

    def on_chime_volume_changed(self, val):
        self.lbl_chime_vol.setText(f"{val}%")
        self.config["chime_volume"] = val
        self.preview.chime_volume = val

    def test_chime_sound(self):
        preset = self.chime_sound_cb.currentData() if hasattr(self, 'chime_sound_cb') else "acoustic_bell"
        vol = self.chime_vol_slider.value() if hasattr(self, 'chime_vol_slider') else 45
        c_path = getattr(self, 'custom_chime_path', '')
        play_chime(preset=preset, volume=vol, custom_path=c_path if preset == "custom" else "")

    def browse_custom_sound(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav *.mp3 *.ogg *.flac)")
        if file:
            self.handle_sound_import(file)

    def handle_sound_import(self, path):
        if not path or not os.path.exists(path):
            return
        self.custom_chime_path = path
        self.config["custom_chime_path"] = path
        self.config["chime_preset"] = "custom"
        self.preview.custom_chime_path = path
        self.preview.chime_preset = "custom"
        self.refresh_chime_combobox()
        self.test_chime_sound()

    def on_bg_update_checked(self, has_update, latest_tag, body, download_url):
        if has_update and hasattr(self, 'btn_update_badge'):
            self.btn_update_badge.setText(f"✨ Update {latest_tag}")
            self.btn_update_badge.setVisible(True)
            self.latest_update_info = (latest_tag, body, download_url)

    def open_about_dialog(self, auto_check=False):
        dlg = AboutDialog(self, win_accent=self.win_accent, auto_check=auto_check)
        if hasattr(self, 'latest_update_info') and self.latest_update_info:
            latest_tag, body, download_url = self.latest_update_info
            dlg.on_update_result(True, latest_tag, body, download_url)
        dlg.exec()

    def update_leading_zero(self, state=None):
        val = self.leading_zero_cb.isChecked()
        self.preview.leading_zeros[str(self.preview.clock_style)] = val
        self.preview.update()

    def update_brightness(self, val):
        self.bright_val_label.setText(f"{val}%")
        self.preview.set_brightness(val)

    def update_24hr(self, state=None):
        self.preview.use_24hr = self.use_24hr_cb.isChecked()
        self.preview.update()

    def update_rotary_telemetry(self, state=None):
        self.preview.show_weather = self.show_weather_cb.isChecked()
        self.preview.show_battery = self.show_battery_cb.isChecked()
        self.preview.use_fahrenheit = self.fahrenheit_cb.isChecked()
        self.config["show_weather"] = self.show_weather_cb.isChecked()
        self.config["show_battery"] = self.show_battery_cb.isChecked()
        self.config["use_fahrenheit"] = self.fahrenheit_cb.isChecked()
        self.preview.update()

    def update_pixel_shift(self, state=None):
        val = self.pixel_shift_cb.isChecked()
        self.preview.pixel_shift = val
        self.config["pixel_shift"] = val
        self.preview.update()

    def refresh_font_combobox(self):
        if not hasattr(self, 'font_cb'):
            return
        self.font_cb.blockSignals(True)
        self.font_cb.clear()
        
        presets = [
            ("Bungee (Default)", "Bungee"),
            ("Google Sans", "Google Sans"),
            ("Segoe UI Variable", "Segoe UI Variable Display"),
            ("Segoe UI", "Segoe UI"),
            ("Arial Black", "Arial Black"),
            ("Consolas", "Consolas"),
        ]
        for label, family in presets:
            self.font_cb.addItem(label, family)
            
        if getattr(self, 'primary_font', '') and os.path.exists(self.primary_font):
            custom_fam = getattr(self.preview, "primary_font_family", "")
            if not custom_fam or custom_fam == "Google Sans":
                font_id = QFontDatabase.addApplicationFont(self.primary_font)
                if font_id != -1:
                    fams = QFontDatabase.applicationFontFamilies(font_id)
                    if fams:
                        custom_fam = fams[0]
                        self.preview.primary_font_family = custom_fam
            if not custom_fam:
                custom_fam = os.path.splitext(os.path.basename(self.primary_font))[0]
            self.font_cb.addItem(f"Custom: {custom_fam}", self.primary_font)
            
        self.font_cb.addItem("📁 Import Font (.ttf / .otf)...", "__IMPORT__")
        
        current_dino = getattr(self.preview, "dino_font", "Bungee")
        target_idx = 0
        if self.primary_font and os.path.exists(self.primary_font) and (current_dino == getattr(self.preview, "primary_font_family", "") or current_dino == self.primary_font):
            target_idx = self.font_cb.count() - 2
        else:
            for i in range(self.font_cb.count()):
                if self.font_cb.itemData(i) == current_dino:
                    target_idx = i
                    break
                    
        self.font_cb.setCurrentIndex(max(0, target_idx))
        self.font_cb.blockSignals(False)
        self.check_font_changed()

    def on_font_combobox_changed(self, idx):
        if idx < 0:
            return
        data = self.font_cb.itemData(idx)
        if data == "__IMPORT__":
            self.import_primary_font()
        elif str(data).lower().endswith((".ttf", ".otf")) or (getattr(self, 'primary_font', '') and data == self.primary_font):
            custom_fam = getattr(self.preview, "primary_font_family", "")
            if not custom_fam:
                custom_fam = os.path.splitext(os.path.basename(self.primary_font))[0]
            self.preview.dino_font = custom_fam
            self.preview.primary_font = self.primary_font
            self.preview.update()
            self.check_font_changed()
        else:
            self.preview.dino_font = str(data)
            self.preview.update()
            self.check_font_changed()

    def handle_font_import(self, path):
        if not path or not os.path.exists(path):
            return
        self.primary_font = path
        font_id = QFontDatabase.addApplicationFont(path)
        family = ""
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                family = families[0]
        if not family:
            family = os.path.splitext(os.path.basename(path))[0]
        self.preview.primary_font = path
        self.preview.primary_font_family = family
        self.preview.dino_font = family
        self.refresh_font_combobox()
        self.preview.update()
        self.check_font_changed()

    def import_primary_font(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Font File", "", "Font Files (*.ttf *.otf)")
        if file:
            self.handle_font_import(file)
        else:
            self.refresh_font_combobox()

    def check_font_changed(self):
        if not hasattr(self, 'undo_font_btn') or not hasattr(self, 'saved_dino_font'):
            return
        current_primary = getattr(self, 'primary_font', "")
        current_dino = getattr(self.preview, 'dino_font', "Bungee")
        has_changed = (current_primary != self.saved_primary_font) or (current_dino != self.saved_dino_font)
        self.undo_font_btn.setVisible(has_changed)

    def revert_font(self):
        if self.saved_primary_font and os.path.exists(self.saved_primary_font):
            self.primary_font = self.saved_primary_font
            font_id = QFontDatabase.addApplicationFont(self.primary_font)
            family = ""
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    family = families[0]
            self.preview.primary_font = self.primary_font
            self.preview.primary_font_family = family
            self.preview.dino_font = self.saved_dino_font if self.saved_dino_font else family
        else:
            self.primary_font = ""
            self.preview.primary_font = ""
            self.preview.primary_font_family = "Google Sans"
            self.preview.dino_font = self.saved_dino_font if self.saved_dino_font else "Bungee"
            
        self.refresh_font_combobox()
        self.preview.update()
        self.check_font_changed()

    def refresh_char_combobox(self):
        if not hasattr(self, 'char_cb'):
            return
        self.char_cb.blockSignals(True)
        self.char_cb.clear()
        
        self.char_cb.addItem("Dino (Default)", "dino")
        
        if getattr(self, 'custom_character_image', '') and os.path.exists(self.custom_character_image):
            img_name = os.path.basename(self.custom_character_image)
            self.char_cb.addItem(f"Custom: {img_name}", self.custom_character_image)
            
        self.char_cb.addItem("📁 Import Sprite Image...", "__IMPORT__")
        
        curr_type = getattr(self.preview, "character_type", "dino").lower()
        if curr_type == "custom" and getattr(self, 'custom_character_image', '') and os.path.exists(self.custom_character_image):
            self.char_cb.setCurrentIndex(1)
        else:
            self.char_cb.setCurrentIndex(0)
            
        self.char_cb.blockSignals(False)
        self.check_char_changed()

    def on_char_combobox_changed(self, idx):
        if idx < 0:
            return
        data = self.char_cb.itemData(idx)
        if data == "__IMPORT__":
            self.import_character()
        elif data == "dino":
            self.preview.character_type = "dino"
            self.preview.update()
            self.check_char_changed()
        else:
            self.preview.character_type = "custom"
            self.preview.set_custom_character(str(data))
            self.preview.update()
            self.check_char_changed()

    def handle_character_import(self, path):
        if not path or not os.path.exists(path):
            return
        self.custom_character_image = path
        self.preview.character_type = "custom"
        self.preview.set_custom_character(path)
        self.refresh_char_combobox()
        self.preview.update()
        self.check_char_changed()

    def import_character(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Character Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)")
        if file:
            self.handle_character_import(file)
        else:
            self.refresh_char_combobox()

    def check_char_changed(self):
        if not hasattr(self, 'undo_char_btn') or not hasattr(self, 'char_cb'):
            return
        curr_type = getattr(self.preview, 'character_type', 'dino').capitalize()
        curr_img = getattr(self, 'custom_character_image', "")
        has_changed = (curr_type != self.saved_char_type) or (curr_img != self.saved_char_image)
        self.undo_char_btn.setVisible(has_changed)

    def revert_character(self):
        if self.saved_char_image and os.path.exists(self.saved_char_image):
            self.custom_character_image = self.saved_char_image
            self.preview.set_custom_character(self.custom_character_image)
        else:
            self.saved_char_image = ""
            self.custom_character_image = ""
            self.preview.set_custom_character("")

        target_type = self.saved_char_type if (self.saved_char_type == "Custom" and getattr(self, 'custom_character_image', '')) else "Dino"
        self.saved_char_type = target_type
        self.preview.character_type = target_type.lower()
        self.refresh_char_combobox()
        self.preview.update()
        self.check_char_changed()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, p, self)
        p.end()
        super().paintEvent(event)


if __name__ == '__main__':
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    
    ui_font = QFont(["Segoe UI Variable Text", "Segoe UI", "Arial", "sans-serif"])
    ui_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
    ui_font.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
    app.setFont(ui_font)
    
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
    if getattr(sys, 'frozen', False):
        logo_path = os.path.join(sys._MEIPASS, "app_icon.png")
    if os.path.exists(logo_path):
        app.setWindowIcon(QIcon(logo_path))
        
    font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Bungee-Regular.ttf")
    if getattr(sys, 'frozen', False):
        font_path = os.path.join(sys._MEIPASS, "Bungee-Regular.ttf")
    QFontDatabase.addApplicationFont(font_path)
    
    # Parse CLI arguments for Windows & Linux
    # Windows passes: '/c', '/p65535', or '/s'
    # Linux / standard CLI passes: '--settings', '--config', '-c', '--fullscreen', '-s'
    # If no arguments are passed on Linux desktop, default to Settings Dialog ('c')
    # If Windows screensaver idle invokes with '/s', run fullscreen ('s')
    mode = 'c' if (sys.platform.startswith("linux") and len(sys.argv) == 1) else 's'
    for arg in sys.argv[1:]:
        arg_lower = arg.lower()
        if arg_lower in ('/c', '-c', '--c', '--config', '--settings', '-settings', 'config', 'settings'):
            mode = 'c'
        elif arg_lower.startswith('/c') or arg_lower.startswith('-c'):
            mode = 'c'
        elif arg_lower.startswith('/p') or arg_lower.startswith('-p'):
            mode = 'p'
        elif arg_lower in ('/s', '-s', '--s', '--fullscreen', '-fullscreen', 'fullscreen'):
            mode = 's'
        elif arg_lower.startswith('/s') or arg_lower.startswith('-s'):
            mode = 's'
            
    if sys.platform.startswith("linux"):
        config_dir = os.path.join(os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config')), 'dinoscreener')
    else:
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
        "show_weather": True,
        "show_battery": True,
        "use_fahrenheit": False,
        "ambient_mode": False,
        "strict_exit": False,
        "enable_win_key": False,
        "brightness": 100,
        "clock_style": 1,
        "clock_scales": {"0": 0.45, "1": 0.45, "2": 0.45},
        "use_24hr": False,
        "leading_zero": False,
        "live_weather": False,
        "pixel_shift": False,
        "hourly_chime": False,
        "chime_preset": "acoustic_bell",
        "chime_volume": 45,
        "custom_chime_path": "",
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
        show_weather=default_config.get("show_weather", default_config.get("show_info", True)),
        show_battery=default_config.get("show_battery", default_config.get("show_info", True)),
        use_fahrenheit=default_config.get("use_fahrenheit", default_config.get("live_weather", False)),
        ambient_mode=default_config.get("ambient_mode", False),
        brightness=default_config.get("brightness", 100),
        clock_style=default_config.get("clock_style", 1),
        clock_scales=default_config.get("clock_scales", {"0": 0.45, "1": 0.45, "2": 0.45}),
        use_24hr=default_config.get("use_24hr", False),
        leading_zeros=default_config.get("leading_zeros", default_config.get("leading_zero", False)),
        config_path=config_path,
        full_config=default_config,
        ignore_media_keys=default_config.get("ignore_media_keys", False),
        dino_font=default_config.get("dino_font", "Bungee"),
        live_weather=default_config.get("show_weather", True),
        pixel_shift=default_config.get("pixel_shift", False),
        hourly_chime=default_config.get("hourly_chime", False),
        chime_preset=default_config.get("chime_preset", "acoustic_bell"),
        chime_volume=default_config.get("chime_volume", 45),
        custom_chime_path=default_config.get("custom_chime_path", ""),
        primary_font=default_config.get("primary_font", ""),
        character_type=default_config.get("character_type", "dino"),
        custom_character_image=default_config.get("custom_character_image", "")
    )
    sys.exit(app.exec())

