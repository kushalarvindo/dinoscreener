import sys
import math
import ctypes
import json
import os
import random
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QColorDialog, QFormLayout, QSlider, QFileDialog
from PyQt6.QtCore import Qt, QTimer, QTime, QRectF, QDate, QPointF, QByteArray, QThread, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QRadialGradient, QPainterPath, QFontDatabase, QPixmap, QImage

NEKO_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAFgAAAAvCAYAAABnsg1NAAABGElEQVR4nO2a0QqDMAxFvWP//8sdg7mXMVo1N023c55EJF7CbRpTtw3gp2gvVtHRiuu9zZHzP2i/+OYCSe9nMmiDOlbRi4PNaLR+uZ3RgutoFb04uIqD4Rw4eHaCn7UsY2dW0Huq6cXBZkiwGRJcvYvY61Avjgafc5OtFwev0gf3dtRWrN/O0ouDZ0/TqqDBaVoVmKYl8VGHqjlDi9d2HGxGVZ2hg/OEqnpxsBkSbIYEm6GLCIYuIhm+5EzwJZcEp8pmcLCZ+6zdWyfjHz2RGI0bHYcaPNvB1VHHyfv96H8kjq4cHGzmHnV6Oqtm66L+qP6aadqqswj33Fam+FErrhcHB1c90bi6O7dJ8aNWxGgcHAwAAADbKR6s1dxAUEkf2AAAAABJRU5ErkJggg=='

F1_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAFgAAAAvCAYAAABnsg1NAAAA4UlEQVR4nO3aQQ6DMAxE0Uzvf2ezQN3QBQRn4kT9b90ay4wgRGkNAAAAAABgHmULRES8urCUvvYO/X7e/AnPaXYSqpJc1S8JNlNVEmYlubpfEmymUQl4ekdjcD13/Ww9EmymWevFMK8/V+2XBJvJ9bb93sn487ok2EyudSJOJNiMAZsxYDMGbMaAzRiwGQOu+pK72wPIrp/VWf/6+136JcFmDNiMAVfvRdw9+9INaGz91folwWbsppmRYDMGbMaAzX6+Tnqfyb3nF2Jw/dX7JcGrnovIniWLwfVX7ZcEo23tALdgnCnlRJUrAAAAAElFTkSuQmCC'

TYRE_B64 = 'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAA00lEQVR4nO3awQ6DIBRE0TuT/v8v0xUbEmqrRl6mnI0GXDGBp6A40Fprn/oliQJMCJ1NoloyJoSuJlElGRNCdyWxOhkTQlfrRJU6Y0K8vh3JceR7f7/ePcd+lZ9INxvp3r66oucnopMjvHqumBAmhElftdqkboz9VVYvE8KEMCFMCBPChDAhTAgTwoQwIUwI8y+7KG14y509t5oJYUKY1DnSTn7x7Z3Gp3YaNdmvqrJaxSWifT5SjPrNPkMsQmPDPmdfTLOO/S/KIjp6oEqd4EBMIm+tbGRpkOMc8wAAAABJRU5ErkJggg=='


SPRITE_B64 = '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'
COCKPIT_B64 = '''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'''

class CrispAestheticFlipClock(QWidget):
    def __init__(self, accent_color="#8F96BF", enable_win_key=False, strict_exit=False, show_info=True, preview_mode=False, brightness=100, clock_style=1, clock_scales=None, use_24hr=False, leading_zeros=None, config_path=None, full_config=None, ignore_media_keys=False, dino_font="Bungee", live_weather=False, pixel_shift=False, primary_font="", dino_icon="Dino", custom_dino_path=""):
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
        self.dino_icon = dino_icon
        self.custom_dino_path = custom_dino_path
        
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
            
        def load_b64(b64str):
            pm = QPixmap()
            ba = QByteArray.fromBase64(b64str.encode('utf-8'))
            pm.loadFromData(ba)
            return pm
        
        self.neko_pixmap = load_b64(NEKO_B64)
        self.f1_pixmap = load_b64(F1_B64)
        
        self.tyre_pixmap = load_b64(TYRE_B64)
        self.cockpit_pixmap = load_b64(COCKPIT_B64)
        
        # F1 Mode Variables
        self.f1_player_x = 0.0 # Lane from -1 to 1
        self.f1_obstacles = [] # List of dicts: {'x': lane, 'z': distance (100 to 0)}
        self.f1_speed = 1.0
        self.f1_dead = False
        self.f1_score = 0
        self.f1_road_z = 0.0

        
        self.custom_pixmap = QPixmap()
        if self.custom_dino_path and os.path.exists(self.custom_dino_path):
            self.custom_pixmap.load(self.custom_dino_path)
            self.custom_pixmap = self.custom_pixmap.scaled(44, 47, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)

            
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
            if getattr(self, "dino_icon", "") == "F1 Car":
                self.update_f1_logic()
                self.update()
                return

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
            target_rect = QRectF(dino_x, ground_y - self.dino_y - dino_h, dino_w, dino_h)
            
            if self.dino_icon == "Neko":
                if self.dino_y > 0:
                    src_rect = QRectF(0, 0, 44, 47)
                else:
                    src_rect = QRectF(0, 0, 44, 47) if (self.dino_frame // 5) % 2 == 0 else QRectF(44, 0, 44, 47)
                painter.drawPixmap(target_rect, self.neko_pixmap, src_rect)
            elif self.dino_icon == "F1 Car":
                src_rect = QRectF(0, 0, 296, 76)
                # align right edge of visual car with right edge of 44px collision box
                car_target = QRectF(dino_x - 44, ground_y - self.dino_y - 23, 88, 23)
                painter.drawPixmap(car_target, self.f1_pixmap, src_rect)
            elif self.dino_icon == "Custom Image..." and not self.custom_pixmap.isNull():
                painter.drawPixmap(target_rect.toRect(), self.custom_pixmap)
            else:
                if self.dino_y > 0:
                    dino_rect = QRectF(848, 2, 44, 47) 
                else:
                    if self.dino_frame < 10:
                        dino_rect = QRectF(936, 2, 44, 47) 
                    else:
                        dino_rect = QRectF(980, 2, 44, 47)
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
                
                if self.dino_icon == "F1 Car" and t != 'crow':
                    tw = obs['h'] * 0.688
                    tyre_target = QRectF(obs['x'] + (obs['w'] - tw)/2, ground_y - obs['h'], tw, obs['h'])
                    painter.drawPixmap(tyre_target.toRect(), self.tyre_pixmap)
                else:
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
        if getattr(self, "dino_icon", "") == "F1 Car" and getattr(self, "clock_style", 0) == 2:
            if event.key() == Qt.Key.Key_Left:
                self.f1_player_x = max(-1.0, self.f1_player_x - 1.0)
                return
            elif event.key() == Qt.Key.Key_Right:
                self.f1_player_x = min(1.0, self.f1_player_x + 1.0)
                return
            elif event.key() == Qt.Key.Key_Space:
                if getattr(self, "f1_dead", False):
                    self.f1_dead = False
                    self.f1_score = 0
                    self.f1_obstacles = []
                    self.f1_speed = 1.0
                    self.f1_player_x = 0.0
                return
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

class SettingsDialog(QDialog):
    def __init__(self, config_path):
        super().__init__()
        self.setWindowTitle("Dinoscreener Settings")
        self.setFixedSize(850, 600)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Try to apply Windows 11 Mica & Dark Title Bar
        try:
            hwnd = int(self.winId())
            backdrop_type = ctypes.c_int(2) # DWMSBT_MAINWINDOW (Mica)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 38, ctypes.byref(backdrop_type), ctypes.sizeof(backdrop_type))
            
            dark_mode = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(dark_mode), ctypes.sizeof(dark_mode))
        except Exception:
            pass
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Sleek dark theme with fully transparent dialog background for native Mica
        self.setStyleSheet("""
            QDialog {
                background: transparent;
            }
            QLabel {
                color: #CDD6F4;
                font-family: 'Segoe UI', sans-serif;
                font-weight: bold;
            }
            QCheckBox {
                color: #A6ADC8;
                font-family: 'Segoe UI', sans-serif;
                background: transparent;
            }
            QPushButton {
                background-color: rgba(49, 50, 68, 200);
                color: #CDD6F4;
                border: 1px solid #45475A;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: rgba(69, 71, 90, 200);
            }
            QSlider {
                background: transparent;
            }
            QSlider::groove:horizontal {
                border: 1px solid #45475A;
                height: 4px;
                background: rgba(49, 50, 68, 200);
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #8F96BF;
                width: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }
        """)
        
        self.config_path = config_path
        self.config = self.load_config()
        self.initUI()
        self.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
                self.preview.clock_style = (self.preview.clock_style + (1 if event.key() == Qt.Key.Key_Up else -1)) % 3
                self.preview.update()
                self.update_style_ui()
                return True
        return super().eventFilter(obj, event)
        
    def load_config(self):
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
            "ignore_media_keys": False,
            "dino_font": "Bungee"
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
        self.config["dino_icon"] = getattr(self, 'dino_icon_cb', QComboBox()).currentText() if hasattr(self, 'dino_icon_cb') else self.config.get("dino_icon", "Dino")
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)
        self.accept()
        
    def pick_color(self):
        color = QColorDialog.getColor(QColor(self.config["accent_color"]), self, "Select Accent Color")
        if color.isValid():
            self.config["accent_color"] = color.name()
            self.preview.set_accent_color(color.name())
            
    def update_brightness(self, val):
        self.bright_val_label.setText(f"{val}%")
        self.preview.set_brightness(val)
        
    def update_style_ui(self):
        self.info_cb.setVisible(self.preview.clock_style == 1)
        is_dino = self.preview.clock_style == 2
        self.font_label.setVisible(is_dino)
        self.font_cb.setVisible(is_dino)
        if hasattr(self, 'dino_icon_label'):
            self.dino_icon_label.setVisible(is_dino)
            self.dino_icon_cb.setVisible(is_dino)
        self.primary_font_btn.setVisible(is_dino)
        self.primary_font_label.setVisible(is_dino)
        
        is_rotary = self.preview.clock_style == 1
        self.color_btn.setVisible(is_rotary)
        self.live_weather_cb.setVisible(is_rotary)
        
        # Update leading zero cb state for this style
        self.leading_zero_cb.blockSignals(True)
        self.leading_zero_cb.setChecked(self.preview.leading_zeros.get(str(self.preview.clock_style), False))
        self.leading_zero_cb.blockSignals(False)
        
    def next_style(self):
        self.preview.clock_style = (self.preview.clock_style + 1) % 3
        self.preview.update()
        self.update_style_ui()
        
    def prev_style(self):
        self.preview.clock_style = (self.preview.clock_style - 1) % 3
        self.preview.update()
        self.update_style_ui()
        
    def update_info(self, state=None):
        self.preview.set_show_info(self.info_cb.isChecked())
        
    def update_strict(self, state=None):
        self.preview.strict_exit = self.strict_cb.isChecked()
        
    def update_win(self, state=None):
        self.preview.enable_win_key = self.win_cb.isChecked()
            
    def update_24hr(self, state=None):
        self.preview.use_24hr = self.use_24hr_cb.isChecked()
        self.preview.update()
        
    def update_leading_zero(self, state=None):
        self.preview.leading_zeros[str(self.preview.clock_style)] = self.leading_zero_cb.isChecked()
        self.preview.update()
        
    def update_media_keys(self, state=None):
        self.preview.ignore_media_keys = self.ignore_media_cb.isChecked()
        
    def update_live_weather(self, state=None):
        self.preview.live_weather = self.live_weather_cb.isChecked()
        self.preview.update()
        
    def update_pixel_shift(self, state=None):
        self.preview.pixel_shift = self.pixel_shift_cb.isChecked()
        self.preview.update()
        
    def import_primary_font(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Font File", "", "Font Files (*.ttf *.otf)")
        if file:
            self.primary_font = file
            self.primary_font_label.setText(os.path.basename(file))
            font_id = QFontDatabase.addApplicationFont(file)
            
            # Force refresh QFontComboBox by recreating its model or simply re-setting filters
            from PyQt6.QtWidgets import QFontComboBox
            self.font_cb.setFontFilters(QFontComboBox.FontFilter.AllFonts)
            
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    from PyQt6.QtGui import QFont
                    self.font_cb.setCurrentFont(QFont(families[0]))
                    
            self.preview.primary_font = file
            self.preview.update()
            
    def update_dino_font(self, font):
        self.preview.dino_font = font.family()
        self.preview.update()
        
    def on_dino_icon_changed(self, icon_name):
        if icon_name == "Custom Image...":
            path, _ = QFileDialog.getOpenFileName(self, "Select Custom Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
            if path:
                self.config["custom_dino_path"] = path
                self.preview.custom_dino_path = path
                self.preview.custom_pixmap.load(path)
                self.preview.custom_pixmap = self.preview.custom_pixmap.scaled(44, 47, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            else:
                self.dino_icon_cb.setCurrentText("Dino")
                return
        self.preview.dino_icon = self.dino_icon_cb.currentText()
        self.preview.update()
        
    def reset_defaults(self):
        import os, json
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        # Reload dialog
        self.accept()
        # Note: We rely on the user to re-open settings. Alternatively, we could reset UI elements manually.

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. LIVE PREVIEW
        self.preview = CrispAestheticFlipClock(
            accent_color=self.config["accent_color"],
            enable_win_key=self.config["enable_win_key"],
            strict_exit=self.config["strict_exit"],
            show_info=self.config["show_info"],
            preview_mode=True,
            brightness=self.config["brightness"],
            clock_style=self.config["clock_style"],
            clock_scales=self.config.get("clock_scales", {"0": 0.45, "1": 0.45, "2": 0.45}),
            use_24hr=self.config.get("use_24hr", False),
            leading_zeros=self.config.get("leading_zeros", self.config.get("leading_zero", False)),
            ignore_media_keys=self.config.get("ignore_media_keys", False),
            dino_font=self.config.get("dino_font", "Bungee")
        )
        main_layout.addWidget(self.preview, stretch=1)
        
        # 2. CONTROL BAR (Floating Bottom)
        from PyQt6.QtWidgets import QGridLayout, QFontComboBox, QFrame, QComboBox
        control_bar = QWidget()
        control_bar.setObjectName("controlBar")
        control_bar.setStyleSheet("QWidget#controlBar { background: transparent; border-top: 1px solid #313244; }")
        
        control_layout = QGridLayout()
        control_layout.setContentsMargins(20, 15, 20, 15)
        control_layout.setHorizontalSpacing(15)
        control_layout.setVerticalSpacing(15)
        
        # Row 0: Basic Controls
        bright_label = QLabel("🔆")
        self.bright_slider = QSlider(Qt.Orientation.Horizontal)
        self.bright_slider.setRange(10, 100)
        self.bright_slider.setValue(self.config["brightness"])
        self.bright_slider.setFixedWidth(100)
        self.bright_slider.valueChanged.connect(self.update_brightness)
        
        self.bright_val_label = QLabel(f"{self.config['brightness']}%")
        self.bright_val_label.setFixedWidth(35)
        
        style_prev = QPushButton("◀")
        style_prev.setStyleSheet("padding: 5px 15px; font-size: 14px;")
        style_prev.clicked.connect(self.prev_style)
        
        style_next = QPushButton("▶")
        style_next.setStyleSheet("padding: 5px 15px; font-size: 14px;")
        style_next.clicked.connect(self.next_style)
        
        self.color_btn = QPushButton("🎨")
        self.color_btn.setStyleSheet("padding: 5px 15px; font-size: 14px;")
        self.color_btn.setToolTip("Pick Accent Color")
        self.color_btn.clicked.connect(self.pick_color)
        
        # Row 1: Checkboxes
        self.info_cb = QCheckBox("Weather/Battery")
        self.info_cb.setChecked(self.config["show_info"])
        self.info_cb.stateChanged.connect(self.update_info)
        
        self.strict_cb = QCheckBox("Lock Screen (Ctrl+Z)")
        self.strict_cb.setChecked(self.config["strict_exit"])
        self.strict_cb.stateChanged.connect(self.update_strict)
        
        self.win_cb = QCheckBox("Win Key")
        self.win_cb.setChecked(self.config["enable_win_key"])
        self.win_cb.stateChanged.connect(self.update_win)
        
        self.use_24hr_cb = QCheckBox("24 Hr")
        self.use_24hr_cb.setChecked(self.config.get("use_24hr", False))
        self.use_24hr_cb.stateChanged.connect(self.update_24hr)
        
        self.leading_zero_cb = QCheckBox("Leading Zero (e.g. 09:00)")
        self.leading_zero_cb.setChecked(self.preview.leading_zeros.get(str(self.preview.clock_style), False))
        self.leading_zero_cb.stateChanged.connect(self.update_leading_zero)
        
        self.ignore_media_cb = QCheckBox("Ignore Media Keys")
        self.ignore_media_cb.setChecked(self.config.get("ignore_media_keys", False))
        self.ignore_media_cb.stateChanged.connect(self.update_media_keys)
        
        self.live_weather_cb = QCheckBox("Live Weather")
        self.live_weather_cb.setChecked(self.config.get("live_weather", False))
        self.live_weather_cb.stateChanged.connect(self.update_live_weather)
        
        self.pixel_shift_cb = QCheckBox("OLED Burn-in Protection")
        self.pixel_shift_cb.setChecked(self.config.get("pixel_shift", False))
        self.pixel_shift_cb.stateChanged.connect(self.update_pixel_shift)
        
        # Row 2: Font Config & Actions
        self.font_label = QLabel("Font:")
        self.font_cb = QFontComboBox()
        self.font_cb.setCurrentFont(QFont(self.config.get("dino_font", "Bungee")))
        self.font_cb.currentFontChanged.connect(self.update_dino_font)
        
        reset_btn = QPushButton("Reset Defaults")
        reset_btn.setStyleSheet("color: #FF7777; background: transparent; border: 1px solid #FF7777; padding: 6px 15px; border-radius: 4px;")
        reset_btn.clicked.connect(self.reset_defaults)
        
        save_btn = QPushButton("OK")
        save_btn.setStyleSheet("background-color: #8F96BF; color: #11111B; font-weight: bold; padding: 6px 25px; border-radius: 4px;")
        save_btn.clicked.connect(self.save_config)
        
        # Top Row Assembly
        top_row = QHBoxLayout()
        top_row.addWidget(bright_label)
        top_row.addWidget(self.bright_slider)
        top_row.addWidget(self.bright_val_label)
        top_row.addSpacing(15)
        top_row.addWidget(style_prev)
        top_row.addSpacing(5)
        top_row.addWidget(style_next)
        top_row.addSpacing(15)
        top_row.addWidget(self.color_btn)
        top_row.addStretch()
        
        # Checkbox Grid Assembly
        cb_layout = QGridLayout()
        cb_layout.setHorizontalSpacing(20)
        cb_layout.setVerticalSpacing(10)
        
        cb_layout.addWidget(self.info_cb, 0, 0)
        cb_layout.addWidget(self.strict_cb, 0, 1)
        cb_layout.addWidget(self.win_cb, 0, 2)
        cb_layout.addWidget(self.use_24hr_cb, 0, 3)
        cb_layout.addWidget(self.leading_zero_cb, 1, 0)
        cb_layout.addWidget(self.ignore_media_cb, 1, 1)
        cb_layout.addWidget(self.live_weather_cb, 1, 2)
        cb_layout.addWidget(self.pixel_shift_cb, 1, 3)
        
        # Action Row Assembly
        action_row = QHBoxLayout()
        
        self.primary_font = self.config.get("primary_font", "")
        self.primary_font_btn = QPushButton("Import Font...")
        self.primary_font_btn.setStyleSheet("background: transparent; border: 1px solid #45475A;")
        self.primary_font_btn.clicked.connect(self.import_primary_font)
        self.primary_font_label = QLabel(os.path.basename(self.primary_font) if self.primary_font else "Default")
        self.primary_font_label.setStyleSheet("color: #A6ADC8; font-weight: normal; font-size: 12px;")
        
        action_row.addWidget(self.primary_font_btn)
        action_row.addSpacing(5)
        action_row.addWidget(self.primary_font_label)
        action_row.addSpacing(15)
        action_row.addWidget(self.font_label)
        
        # Style font combobox slightly
        self.font_cb.setStyleSheet("padding: 3px 5px; background: #313244; color: white; border-radius: 3px;")
        action_row.addWidget(self.font_cb)
        
        # Dino Icon
        self.dino_icon_label = QLabel("Icon:")
        self.dino_icon_cb = QComboBox()
        self.dino_icon_cb.addItems(["Dino", "Neko", "F1 Car", "Custom Image..."])
        self.dino_icon_cb.setCurrentText(self.config.get("dino_icon", "Dino"))
        self.dino_icon_cb.currentTextChanged.connect(self.on_dino_icon_changed)
        self.dino_icon_cb.setStyleSheet("padding: 3px 5px; background: #313244; color: white; border-radius: 3px;")
        action_row.addSpacing(15)
        action_row.addWidget(self.dino_icon_label)
        action_row.addWidget(self.dino_icon_cb)
        
        action_row.addStretch()
        action_row.addWidget(reset_btn)
        action_row.addSpacing(10)
        action_row.addWidget(save_btn)
        
        control_layout.addLayout(top_row, 0, 0)
        control_layout.addLayout(cb_layout, 1, 0)
        control_layout.addLayout(action_row, 2, 0)
        
        control_bar.setLayout(control_layout)
        main_layout.addWidget(control_bar)
        
        self.setLayout(main_layout)
        self.update_style_ui()
        
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
        "dino_icon": "Dino",
        "custom_dino_path": ""
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
        dino_icon=default_config.get("dino_icon", "Dino"),
        custom_dino_path=default_config.get("custom_dino_path", "")
    )
    sys.exit(app.exec())


    def update_f1_logic(self):
        if self.f1_dead:
            return
            
        self.f1_score += 1
        self.f1_road_z = (self.f1_road_z + self.f1_speed * 0.1) % 1.0
        
        # Spawn obstacles
        import random
        if not self.f1_obstacles or self.f1_obstacles[-1]['z'] < 80:
            if random.random() < 0.05:
                lane = random.choice([-1.0, 0.0, 1.0])
                self.f1_obstacles.append({'x': lane, 'z': 100.0})
                
        # Move obstacles
        for obs in self.f1_obstacles:
            obs['z'] -= self.f1_speed
            if obs['z'] < 5.0 and obs['z'] > 0:
                # Collision check
                if abs(obs['x'] - self.f1_player_x) < 0.5:
                    self.f1_dead = True
                    
        self.f1_obstacles = [o for o in self.f1_obstacles if o['z'] > 0]
        
        # Accelerate slightly
        if self.f1_speed < 3.0:
            self.f1_speed += 0.0005

    def draw_f1_style(self, painter, w, h):
        # Draw sky/space background
        painter.fillRect(0, 0, int(w), int(h/2), QColor("#050510"))
        # Draw road area
        painter.fillRect(0, int(h/2), int(w), int(h/2), QColor("#000000"))
        
        # Draw stars (simple hash based on w,h)
        painter.setPen(QColor("#FFFFFF"))
        import random
        random.seed(42)
        for i in range(100):
            sx = random.randint(0, int(w))
            sy = random.randint(0, int(h/2))
            painter.drawPoint(sx, sy)
            
        # Draw perspective road lines
        horizon_y = h/2
        center_x = w/2
        
        pen = QPen(QColor("#FFFFFF"))
        pen.setWidth(2)
        painter.setPen(pen)
        
        # Draw grid
        for i in range(-5, 6):
            if i == 0: continue
            x_bottom = center_x + i * 200
            painter.drawLine(int(center_x), int(horizon_y), int(x_bottom), int(h))
            
        # Draw horizontal lines moving forward
        for j in range(1, 10):
            z = j * 10 - (self.f1_road_z * 10)
            if z <= 0: continue
            scale = 100.0 / z
            y = horizon_y + (h/2) / z * 10
            painter.drawLine(0, int(y), int(w), int(y))
            
        # Draw obstacles (tyres)
        for obs in reversed(self.f1_obstacles): # draw furthest first
            if obs['z'] <= 0: continue
            scale = 100.0 / obs['z']
            obs_w = 34 * scale * 2
            obs_h = 50 * scale * 2
            
            # x position based on perspective
            # lane: -1 is left, 0 is center, 1 is right
            # offset from center at bottom of screen is say 300px
            x_offset = obs['x'] * 300 * scale / 10.0
            
            # camera offset based on player steer
            camera_offset = -self.f1_player_x * 300 * scale / 10.0
            
            x_pos = center_x + x_offset + camera_offset - obs_w/2
            y_pos = horizon_y + (h/2) / obs['z'] * 10 - obs_h
            
            painter.drawPixmap(QRectF(x_pos, y_pos, obs_w, obs_h).toRect(), self.tyre_pixmap)
            
        # Draw cockpit overlay at bottom
        cockpit_rect = QRectF(0, h - (w * 600/800), w, w * 600/800)
        # to ensure it anchors to bottom and scales nicely:
        cw = w
        ch = w * (self.cockpit_pixmap.height() / max(1, self.cockpit_pixmap.width()))
        if ch > h:
            ch = h
            cw = h * (self.cockpit_pixmap.width() / max(1, self.cockpit_pixmap.height()))
        painter.drawPixmap(QRectF(w/2 - cw/2, h - ch, cw, ch).toRect(), self.cockpit_pixmap)
        
        # Draw score
        painter.setPen(QColor("#FFFFFF"))
        painter.setFont(QFont(self.primary_font_family, 24, QFont.Weight.Bold))
        painter.drawText(20, 50, f"HI 00000  {int(self.f1_score):05d}")
        
        if self.f1_dead:
            painter.drawText(int(w/2 - 100), int(h/2 - 50), "G A M E   O V E R")
