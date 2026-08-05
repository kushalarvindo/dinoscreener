import sys
import math
import ctypes
import json
import os
import random
from PyQt6.QtWidgets import QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QColorDialog, QFormLayout, QSlider
from PyQt6.QtCore import Qt, QTimer, QTime, QRectF, QDate, QPointF, QByteArray
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QRadialGradient, QPainterPath, QFontDatabase, QPixmap, QImage

SPRITE_B64 = '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'
class CrispAestheticFliqlo(QWidget):
    def __init__(self, accent_color="#8F96BF", enable_win_key=False, strict_exit=False, show_info=True, preview_mode=False, brightness=100, clock_style=1, clock_scales=None, use_24hr=False, leading_zero=False):
        super().__init__()
        self.last_pos = None
        self.clock_scales = clock_scales if clock_scales else {"0": 0.45, "1": 0.45, "2": 0.45}
        
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
        self.leading_zero = leading_zero
        
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
                gs = self.height() / 300.0
                current_dino_speed = self.dino_speed * gs
                # Physics
                gs = self.height() / 300.0
                self.dino_y += self.dino_vy
                if self.dino_y > 0:
                    self.dino_vy -= 0.6 * gs # gravity
                else:
                    self.dino_y = 0
                    self.dino_vy = 0
                
                # Obstacle Generation
                # Ground scroll
                self.ground_x -= current_dino_speed
                if self.ground_x <= -1200:
                    self.ground_x += 1200

                # Clouds
                if len(self.dino_clouds) < 3:
                    if random.random() < 0.01:
                        self.dino_clouds.append({'x': self.width() + 100, 'y': random.randint(int(self.height()*0.3), int(self.height()*0.6)), 'speed': current_dino_speed * 0.2, 'w': 46 * gs, 'h': 14 * gs})
                for c in self.dino_clouds:
                    c['x'] -= c['speed']
                self.dino_clouds = [c for c in self.dino_clouds if c['x'] > -100]

                if len(self.dino_obstacles) == 0:
                    self.dino_obstacles.append({'x': self.width() + 200, 'w': 25, 'h': 50, 'type': 'large1'})
                else:
                    last_obs = self.dino_obstacles[-1]
                    if self.width() - last_obs['x'] > 400 + random.randint(0, 400):
                        obs_type = random.randint(0, 8)
                        gs = self.height() / 300.0
                        if obs_type in [0, 4]:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 17 * gs, 'h': 35 * gs, 'type': 'small1'})
                        elif obs_type in [1, 5]:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 34 * gs, 'h': 35 * gs, 'type': 'small2'})
                        elif obs_type in [2]:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 51 * gs, 'h': 35 * gs, 'type': 'small3'})
                        elif obs_type in [3]:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 25 * gs, 'h': 50 * gs, 'type': 'large1'})
                        elif obs_type == 6:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 46 * gs, 'h': 40 * gs, 'type': 'crow', 'y_off': 20 * gs})
                        elif obs_type == 7:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 46 * gs, 'h': 40 * gs, 'type': 'crow', 'y_off': 50 * gs})
                        elif obs_type == 8:
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 46 * gs, 'h': 40 * gs, 'type': 'crow', 'y_off': 80 * gs})
                
                for obs in self.dino_obstacles:
                    obs['x'] -= current_dino_speed
                
                self.dino_obstacles = [o for o in self.dino_obstacles if o['x'] > -100]
                
                # Auto-play AI
                gs = self.height() / 300.0
                dino_x = self.width() * 0.2
                dino_w = 40 * gs
                
                next_obs = None
                for obs in self.dino_obstacles:
                    if obs['x'] + obs['w'] > dino_x:
                        next_obs = obs
                        break
                        
                if next_obs:
                    dist = next_obs['x'] - (dino_x + dino_w)
                    if dist < 120 * gs and self.dino_y == 0:
                        self.dino_vy = 12.0 * gs
                                
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
        if self.use_24hr:
            hour_str = f"{hour:02d}" if self.leading_zero else str(hour)
            return hour_str, f"{minute:02d}", ""
        else:
            hour_12 = hour % 12
            if hour_12 == 0: hour_12 = 12
            return str(hour_12), f"{minute:02d}", "PM" if is_pm else "AM"

    # ==========================================
    # DESIGN 1: FLIQLO FLIP CLOCK
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

    def draw_fliqlo_style(self, painter, w, h):
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
        if self.use_24hr:
            hour_str = f"{hour:02d}" if self.leading_zero else str(hour)
        else:
            hour_12 = hour % 12
            if hour_12 == 0: hour_12 = 12
            hour_str = f"{hour_12:02d}"

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
            info_y = offset_y + h * 0.07
            info_h = h * 0.04
            
            # Center dot
            font_info = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
            font_info.setPixelSize(int(h * 0.016))
            font_info.setWeight(QFont.Weight.Medium)
            font_info.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.0)
            painter.setFont(font_info)
            painter.setPen(QColor(120, 125, 130))
            painter.drawText(QRectF(center_x - w*0.01, info_y, w*0.02, info_h), Qt.AlignmentFlag.AlignCenter, "•")
            
            # Weather
            weather_text = "26°C"
            w_icon_size = h * 0.016
            fm = painter.fontMetrics()
            w_text_width = fm.horizontalAdvance(weather_text)
            
            weather_end = center_x - w * 0.015
            weather_text_x = weather_end - w_text_width
            weather_icon_x = weather_text_x - w_icon_size - w * 0.005
            
            painter.save()
            painter.translate(weather_icon_x + w_icon_size/2, info_y + info_h/2)
            painter.setPen(QPen(accent_color, 1.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(QRectF(-w_icon_size*0.4, -w_icon_size*0.4, w_icon_size*0.8, w_icon_size*0.8))
            for i in range(8):
                painter.rotate(45)
                painter.drawLine(int(w_icon_size*0.5), 0, int(w_icon_size*0.8), 0)
            painter.restore()
            
            painter.setPen(QColor(180, 185, 190))
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
                
            bat_start = center_x + w * 0.015
            bat_icon_w = w * 0.02
            bat_icon_h = h * 0.015
            bat_icon_x = bat_start
            bat_text_x = bat_icon_x + bat_icon_w + w * 0.005
            bat_icon_y = info_y + info_h/2 - bat_icon_h/2
            
            painter.setPen(QPen(accent_color, 1.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(QRectF(bat_icon_x, bat_icon_y, bat_icon_w, bat_icon_h), 2, 2)
            painter.drawRect(QRectF(bat_icon_x + bat_icon_w, bat_icon_y + bat_icon_h*0.25, w*0.0015, bat_icon_h*0.5))
            
            if is_charging:
                painter.save()
                painter.translate(bat_icon_x + bat_icon_w/2, bat_icon_y + bat_icon_h/2)
                bolt = QPainterPath()
                bw = bat_icon_w * 0.2
                bh = bat_icon_h * 0.4
                bolt.moveTo(bw*0.3, -bh)
                bolt.lineTo(-bw*0.8, 0)
                bolt.lineTo(0, 0)
                bolt.lineTo(-bw*0.3, bh)
                bolt.lineTo(bw*0.8, 0)
                bolt.lineTo(0, 0)
                bolt.closeSubpath()
                painter.setBrush(accent_color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawPath(bolt)
                painter.restore()
            else:
                fill_w = (bat_icon_w - w*0.002) * (bat_val / 100.0)
                if fill_w > 0:
                    painter.setBrush(accent_color)
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawRect(QRectF(bat_icon_x + w*0.001, bat_icon_y + h*0.002, fill_w, bat_icon_h - h*0.004))
                    
            painter.setPen(QColor(180, 185, 190))
            painter.drawText(QRectF(bat_text_x, info_y, w*0.1, info_h), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, bat_text)

    # ==========================================
    # DESIGN 3: DINO GAME CLOCK
    # ==========================================
    def draw_dino_style(self, painter, w, h):
        now = QTime.currentTime()
        hour = now.hour()
        if self.use_24hr:
            hour_str = f"{hour:02d}" if self.leading_zero else str(hour)
        else:
            hour_12 = hour % 12
            if hour_12 == 0: hour_12 = 12
            hour_str = str(hour_12)
        time_str = f"{hour_str}:{now.minute():02d}"
        
        base_size = int(h * 0.18)
        scaled_size = int(base_size * (self.clock_scales[str(self.clock_style)] / 0.45))
        font_time = QFont(["Bungee", "Arial Black"])
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
        date_y = h * 0.05 + scaled_size * 1.05
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
            self.draw_fliqlo_style(painter, w, h)
        elif self.clock_style == 1:
            self.draw_rotary_style(painter, w, h)
        else:
            self.draw_dino_style(painter, w, h)
            
        # Apply brightness overlay
        if self.brightness < 100:
            overlay_alpha = 255 - int((self.brightness / 100.0) * 255)
            painter.fillRect(self.rect(), QColor(0, 0, 0, overlay_alpha))

    def keyPressEvent(self, event):
        if self.preview_mode: return
        if self.strict_exit and event.key() == Qt.Key.Key_Z and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.close()
            return
            
        if event.key() == Qt.Key.Key_Equal or event.key() == Qt.Key.Key_Plus:
            self.clock_scales[str(self.clock_style)] = min(0.95, self.clock_scales[str(self.clock_style)] + 0.05)
            self.update()
        elif event.key() == Qt.Key.Key_Minus:
            self.clock_scales[str(self.clock_style)] = max(0.15, self.clock_scales[str(self.clock_style)] - 0.05)
            self.update()
        elif event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
            self.clock_style = (self.clock_style + (1 if event.key() == Qt.Key.Key_Up else -1)) % 3 
            self.update()
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
            if not self.strict_exit:
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
        
        # Sleek dark theme with semi-transparent background for Mica to show through
        self.setStyleSheet("""
            QDialog {
                background-color: rgba(17, 17, 27, 160);
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
            "leading_zero": False
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
        self.config["leading_zero"] = self.leading_zero_cb.isChecked()
        
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
        
    def next_style(self):
        self.preview.clock_style = (self.preview.clock_style + 1) % 3
        self.preview.update()
        self.update_style_ui()
        
    def prev_style(self):
        self.preview.clock_style = (self.preview.clock_style - 1) % 3
        self.preview.update()
        self.update_style_ui()
        
    def update_info(self, state):
        self.preview.set_show_info(self.info_cb.isChecked())
            
    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. LIVE PREVIEW
        self.preview = CrispAestheticFliqlo(
            accent_color=self.config["accent_color"],
            enable_win_key=self.config["enable_win_key"],
            strict_exit=self.config["strict_exit"],
            show_info=self.config["show_info"],
            preview_mode=True,
            brightness=self.config["brightness"],
            clock_style=self.config["clock_style"],
            clock_scales=self.config.get("clock_scales", {"0": 0.45, "1": 0.45, "2": 0.45}),
            use_24hr=self.config.get("use_24hr", False),
            leading_zero=self.config.get("leading_zero", False)
        )
        main_layout.addWidget(self.preview, stretch=1)
        
        # 2. CONTROL BAR (Floating Bottom)
        control_bar = QWidget()
        control_bar.setStyleSheet("background: transparent; border-top: 1px solid #313244;")
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(20, 15, 20, 15)
        
        # Controls
        bright_label = QLabel("🔆")
        self.bright_slider = QSlider(Qt.Orientation.Horizontal)
        self.bright_slider.setRange(10, 100)
        self.bright_slider.setValue(self.config["brightness"])
        self.bright_slider.setFixedWidth(100)
        self.bright_slider.valueChanged.connect(self.update_brightness)
        
        self.bright_val_label = QLabel(f"{self.config['brightness']}%")
        self.bright_val_label.setFixedWidth(35)
        
        style_prev = QPushButton("▲")
        style_prev.setFixedSize(30, 30)
        style_prev.clicked.connect(self.prev_style)
        
        style_next = QPushButton("▼")
        style_next.setFixedSize(30, 30)
        style_next.clicked.connect(self.next_style)
        
        color_btn = QPushButton("🎨 Color")
        color_btn.clicked.connect(self.pick_color)
        
        self.info_cb = QCheckBox("Weather/Battery")
        self.info_cb.setChecked(self.config["show_info"])
        self.info_cb.stateChanged.connect(self.update_info)
        
        self.strict_cb = QCheckBox("Lock Screen (Ctrl+Z)")
        self.strict_cb.setChecked(self.config["strict_exit"])
        
        self.win_cb = QCheckBox("Win Key")
        self.win_cb.setChecked(self.config["enable_win_key"])
        
        save_btn = QPushButton("OK")
        save_btn.setStyleSheet("background-color: #8F96BF; color: #11111B; font-weight: bold; padding: 6px 20px;")
        save_btn.clicked.connect(self.save_config)
        
        control_layout.addWidget(bright_label)
        control_layout.addWidget(self.bright_slider)
        control_layout.addWidget(self.bright_val_label)
        control_layout.addSpacing(10)
        control_layout.addWidget(style_prev)
        control_layout.addWidget(style_next)
        control_layout.addSpacing(10)
        control_layout.addWidget(color_btn)
        control_layout.addSpacing(10)
        control_layout.addWidget(self.info_cb)
        control_layout.addSpacing(10)
        control_layout.addWidget(self.strict_cb)
        control_layout.addSpacing(10)
        control_layout.addWidget(self.win_cb)
        
        control_layout.addStretch()
        control_layout.addWidget(save_btn)
        
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
        "leading_zero": False
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                default_config.update(json.load(f))
        except Exception:
            pass
            
    ex = CrispAestheticFliqlo(
        accent_color=default_config["accent_color"], 
        enable_win_key=default_config["enable_win_key"], 
        strict_exit=default_config["strict_exit"],
        show_info=default_config["show_info"],
        brightness=default_config.get("brightness", 100),
        clock_style=default_config.get("clock_style", 1),
        clock_scales=default_config.get("clock_scales", {"0": 0.45, "1": 0.45, "2": 0.45}),
        use_24hr=default_config.get("use_24hr", False),
        leading_zero=default_config.get("leading_zero", False)
    )
    sys.exit(app.exec())

