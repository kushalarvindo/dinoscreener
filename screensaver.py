import sys
import math
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QTimer, QTime, QRectF, QDate
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QRadialGradient, QPainterPath

class CrispAestheticFliqlo(QWidget):
    def __init__(self):
        super().__init__()
        self.last_pos = None
        self.clock_scale = 0.45 
        
        self.target_time = QTime.currentTime()
        self.old_time = self.target_time
        
        self.animating = False
        self.anim_progress = 0.0
        self.time_elapsed = 0.0 
        
        # States
        self.show_bg = False
        self.bg_opacity = 1.0
        self.clock_style = 1 # 0 = Fliqlo Flip Clock, 1 = Modern Rotary
        
        # --- CUSTOMIZATION ---
        self.rotary_accent = QColor("#8F96BF") 
        
        self.initUI()
        
    def initUI(self):
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
        card_h = int(h * self.clock_scale)
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

        # 5. Right Side Circular Widgets
        dial_radius = h * 0.07
        dial_spacing = h * 0.23
        dial_x = pill_right + w * 0.12
        
        def draw_widget_dial(cy_offset, icon_draw_func, top_text, bottom_text, top_color, bottom_color, track_color, track_progress=None):
            center_y = cy + cy_offset
            
            painter.setPen(QPen(track_color, 2.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            
            # The circle is broken at the top for the icon. Gap from ~70 to 110 degrees.
            painter.drawArc(QRectF(dial_x - dial_radius, center_y - dial_radius, dial_radius*2, dial_radius*2), int(115 * 16), int(310 * 16))
            
            if track_progress is not None:
                painter.setPen(QPen(accent_color, 2.5))
                painter.drawArc(QRectF(dial_x - dial_radius, center_y - dial_radius, dial_radius*2, dial_radius*2), int(115 * 16), int(track_progress * 16))
                
            painter.save()
            painter.translate(dial_x, center_y - dial_radius)
            icon_draw_func()
            painter.restore()
            
            if top_text and bottom_text:
                font_top = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
                font_top.setPixelSize(int(dial_radius * 0.28))
                font_top.setWeight(QFont.Weight.Bold)
                font_top.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.0)
                painter.setFont(font_top)
                painter.setPen(top_color)
                painter.drawText(QRectF(dial_x - dial_radius, center_y - dial_radius*0.25, dial_radius*2, dial_radius*0.4), Qt.AlignmentFlag.AlignCenter, top_text)
                
                font_bot = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
                font_bot.setPixelSize(int(dial_radius * 0.35))
                font_bot.setWeight(QFont.Weight.Bold)
                painter.setFont(font_bot)
                painter.setPen(bottom_color)
                painter.drawText(QRectF(dial_x - dial_radius, center_y + dial_radius*0.15, dial_radius*2, dial_radius*0.4), Qt.AlignmentFlag.AlignCenter, bottom_text)
            elif bottom_text: 
                font_bot = QFont(["Google Sans", "Product Sans", "Segoe UI", "Arial"])
                font_bot.setPixelSize(int(dial_radius * 0.40))
                font_bot.setWeight(QFont.Weight.Bold)
                painter.setFont(font_bot)
                painter.setPen(bottom_color)
                painter.drawText(QRectF(dial_x - dial_radius, center_y - dial_radius*0.2, dial_radius*2, dial_radius*0.4), Qt.AlignmentFlag.AlignCenter, bottom_text)

        # Weather Widget (Top)
        def draw_weather_icon():
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(accent_color)
            painter.drawEllipse(QRectF(-8, -4, 16, 10))
            painter.drawEllipse(QRectF(-12, 0, 10, 6))
            painter.drawEllipse(QRectF(2, 0, 10, 6))
            painter.setPen(QPen(accent_color, 2.0))
            painter.drawLine(-4, 8, -6, 12)
            painter.drawLine(4, 8, 2, 12)
            
        draw_widget_dial(-dial_spacing, draw_weather_icon, "", "26°", accent_color, pure_white, QColor(accent_color.red(), accent_color.green(), accent_color.blue(), 80), track_progress=100)
        
        # Date Widget (Middle)
        def draw_calendar_icon():
            painter.setPen(QPen(accent_color, 1.5))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(QRectF(-9, -5, 18, 14), 2, 2)
            painter.drawLine(-5, -7, -5, -5)
            painter.drawLine(5, -7, 5, -5)
            painter.drawLine(-9, 1, 9, 1)
            painter.setPen(QPen(accent_color, 1.5))
            painter.drawPoint(-4, 5)
            painter.drawPoint(0, 5)
            painter.drawPoint(4, 5)
            
        date_now = QDate.currentDate()
        date_str_top = date_now.toString("ddd").upper()
        date_str_bot = date_now.toString("dd MMM").upper()
        draw_widget_dial(0, draw_calendar_icon, date_str_top, date_str_bot, accent_color, pure_white, QColor(120, 125, 130, 80))
        
        # Heart Rate Widget (Bottom)
        def draw_heart_icon():
            painter.setPen(QPen(accent_color, 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.SquareCap))
            pixels = [
                (-3, -3), (-2, -4), (-1, -4), (0, -3), (1, -4), (2, -4), (3, -3),
                (-4, -2), (4, -2), (-4, -1), (4, -1), (-3, 0), (3, 0),
                (-2, 1), (2, 1), (-1, 2), (1, 2), (0, 3)
            ]
            for px, py in pixels:
                painter.drawPoint(int(px * 1.5), int(py * 1.5))
            
        draw_widget_dial(dial_spacing, draw_heart_icon, "", "--", accent_color, pure_white, QColor(120, 125, 130, 80))

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
        else:
            self.draw_rotary_style(painter, w, h)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Equal or event.key() == Qt.Key.Key_Plus:
            self.clock_scale = min(0.95, self.clock_scale + 0.05)
            self.update()
        elif event.key() == Qt.Key.Key_Minus:
            self.clock_scale = max(0.15, self.clock_scale - 0.05)
            self.update()
        elif event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
            self.clock_style = 1 - self.clock_style 
            self.update()
        elif event.key() in (Qt.Key.Key_Space, Qt.Key.Key_Meta, Qt.Key.Key_Super_L, Qt.Key.Key_Super_R, Qt.Key.Key_F23):
            self.show_bg = not self.show_bg
        else:
            self.close()

    def mouseMoveEvent(self, event):
        if self.last_pos is None:
            self.last_pos = event.pos()
            return
        diff = event.pos() - self.last_pos
        if abs(diff.x()) > 5 or abs(diff.y()) > 5:
            self.close()

    def mousePressEvent(self, event):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CrispAestheticFliqlo()
    sys.exit(app.exec())
