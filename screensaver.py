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
    QLineEdit, QCheckBox, QPushButton as NativePushButton, QColorDialog, QFormLayout, QSlider, 
    QFileDialog, QStackedWidget, QFrame, QGridLayout, QComboBox, QFontComboBox, 
    QStackedLayout, QGraphicsOpacityEffect, QGraphicsDropShadowEffect, QProgressBar, QMessageBox, QSizePolicy,
    QStyle, QStyleOption, QStyleOptionButton, QStyleOptionSlider, QScrollArea
)
from PyQt6.QtCore import (
    Qt, QTimer, QTime, QRectF, QDate, QPointF, QByteArray, QThread,
    pyqtSignal, QPropertyAnimation, QEasingCurve, pyqtProperty,
    QParallelAnimationGroup, QSize, QUrl, QVariantAnimation, QRect, QPoint, QEvent, QObject
)
from PyQt6.QtGui import (
    QPainter, QColor, QFont, QPen, QRadialGradient, QLinearGradient, QPainterPath, 
    QFontDatabase, QPixmap, QImage, QIcon, QBrush, QDesktopServices, QShortcut, QKeySequence, QOpenGLContext, QSurfaceFormat, QRegion
)

try:
    from PyQt6.QtOpenGLWidgets import QOpenGLWidget
except ImportError:
    QOpenGLWidget = None


class QPushButton(NativePushButton):
    """Keep native button behavior; smooth QSS outlines at the display's DPR."""
    def paintEvent(self, event):
        option = QStyleOptionButton()
        self.initStyleOption(option)
        dpr = self.devicePixelRatioF()
        key = (self.width(), self.height(), dpr, option.state.value,
               option.features.value, option.palette.cacheKey(), self.styleSheet())
        if getattr(self, '_bevel_key', None) != key:
            scale = dpr * 2.0
            panel = QImage(math.ceil(self.width()*scale), math.ceil(self.height()*scale),
                           QImage.Format.Format_ARGB32_Premultiplied)
            panel.setDevicePixelRatio(scale)
            panel.fill(Qt.GlobalColor.transparent)
            p = QPainter(panel)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            if hasattr(self, '_material_surface'):
                primary, text_action, radius = self._material_surface
                enabled = self.isEnabled()
                hover = bool(option.state & QStyle.StateFlag.State_MouseOver)
                pressed = bool(option.state & QStyle.StateFlag.State_Sunken)
                fill = QColor(MATERIAL['primary']) if primary else QColor(255,255,255,0 if text_action else 14)
                if hover:
                    fill = QColor('#A6B8CC') if primary else QColor(255,255,255,28)
                if pressed:
                    fill = QColor('#7E90A4') if primary else QColor(255,255,255,43)
                if not enabled:
                    fill.setAlpha(20)
                border = QColor(255,255,255,0 if primary or text_action else 61)
                if self.hasFocus() and self.testAttribute(Qt.WidgetAttribute.WA_KeyboardFocusChange):
                    border = QColor('#DCE5EE')
                reset_state = self.property('resetState')
                if reset_state == 1:
                    fill = QColor('#841E26')
                elif text_action and hover:
                    fill = QColor('#FFB4AB')
                p.setPen(QPen(border, 1))
                p.setBrush(fill)
                p.drawRoundedRect(QRectF(self.rect()).adjusted(1,1,-1,-1), radius, radius)
            else:
                self.style().drawControl(QStyle.ControlElement.CE_PushButtonBevel, option, p, self)
            p.end()
            self._bevel_key, self._bevel_image = key, panel
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawImage(QRectF(self.rect()), self._bevel_image)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        if self.objectName() == 'closeIconBtn':
            center = QPointF(self.rect().center()) + QPointF(0.5, 0.5)
            pen = QPen(QColor('#FFFFFF' if self.underMouse() else '#92A4B8'), 1.8)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawLine(center + QPointF(-6, -6), center + QPointF(6, 6))
            painter.drawLine(center + QPointF(6, -6), center + QPointF(-6, 6))
        elif not self.icon().isNull() and self.text():
            label = self.text()
            gap = 7
            width = self.fontMetrics().horizontalAdvance(label)
            size = self.iconSize()
            left = (self.width()-width-gap-size.width())//2
            self.icon().paint(painter, QRect(left,(self.height()-size.height())//2,size.width(),size.height()), Qt.AlignmentFlag.AlignCenter, QIcon.Mode.Normal if self.isEnabled() else QIcon.Mode.Disabled)
            color = option.palette.buttonText().color()
            if self.property('resetState') == 1:
                color = QColor('#FFFFFF')
            elif self.text() in ('Reset Defaults','Resetted!') and self.underMouse():
                color = QColor('#401018')
            painter.setPen(color)
            painter.drawText(QRect(left+size.width()+gap,0,width+1,self.height()),Qt.AlignmentFlag.AlignVCenter,label)
        else:
            self.style().drawControl(QStyle.ControlElement.CE_PushButtonLabel, option, painter, self)
        painter.end()

    def changeEvent(self, event):
        self._bevel_key = None
        super().changeEvent(event)


def clock_gpu_available():
    app=QApplication.instance()
    if QOpenGLWidget is None or app is None or app.platformName()!='windows':return False
    if not hasattr(app,'_clock_gl_available'):
        context=QOpenGLContext()
        app._clock_gl_available=bool(context.create())
    return app._clock_gl_available


class ClockGLSurface(QOpenGLWidget if QOpenGLWidget is not None else QWidget):
    """Accelerate the existing QPainter canvas; settings remain native widgets."""
    def __init__(self,clock):
        super().__init__(clock)
        self.clock=clock
        self.paint_count=0
        self.last_frame_ms=0
        self.engine_name='pending'
        format=QSurfaceFormat()
        format.setAlphaBufferSize(8)
        format.setDepthBufferSize(0)
        format.setStencilBufferSize(8)
        format.setSamples(4)
        # QOpenGLWidget is composited by Qt/DWM; avoid an additional blocking swap wait.
        format.setSwapInterval(0)
        self.setFormat(format)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents,True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setGeometry(clock.rect())
        self.show()
        QTimer.singleShot(500,self.check_context)
    def check_context(self):
        if not self.isValid():
            self.hide()
            self.clock._gpu_surface=None
            self.clock.update()
            self.deleteLater()
    def paintGL(self):
        start=time.perf_counter()
        painter=QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.engine_name=painter.paintEngine().type().name
        # QOpenGLWidget's framebuffer contents outside a clip are undefined.
        # Clear every pixel first; remove rounded corners with an AA shape rather
        # than a stencil clip, whose boundary can leave hard/dirty pixels.
        if self.clock.preview_mode:
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
            painter.fillRect(QRectF(-1, -1, self.width()+2, self.height()+2), Qt.GlobalColor.transparent)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        self.clock.render_clock_canvas(painter,self.width(),self.height(),clip_preview=False)
        if self.clock.preview_mode:
            outside = QPainterPath()
            outside.addRect(QRectF(self.rect()))
            inside = QPainterPath()
            inside.addRoundedRect(QRectF(self.rect()), 12, 12)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationOut)
            painter.fillPath(outside.subtracted(inside), QColor('white'))
        painter.end()
        self.last_frame_ms=(time.perf_counter()-start)*1000
        self.paint_count+=1
        if hasattr(self,'benchmark_samples'):self.benchmark_samples.append(self.last_frame_ms)


class DisplayPositionAnimation(QObject):
    """Elapsed-time drawer easing paced to the actual window's display."""
    finished = pyqtSignal()
    def __init__(self, widget, property_name, parent):
        super().__init__(parent)
        self.widget = widget
        self.property_name = property_name
        self._duration = 260
        self._curve = QEasingCurve(QEasingCurve.Type.OutQuart)
        self._start = QPoint(); self._end = QPoint(); self._running = False
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.timeout.connect(self._tick)
    def setDuration(self, duration):self._duration = duration
    def setEasingCurve(self, curve):self._curve = QEasingCurve(curve)
    def setStartValue(self, point):self._start = int(point) if self.property_name == b'capsuleWidth' else QPoint(point)
    def setEndValue(self, point):self._end = int(point) if self.property_name == b'capsuleWidth' else QPoint(point)
    def endValue(self):return self._end if self.property_name == b'capsuleWidth' else QPoint(self._end)
    def state(self):return QPropertyAnimation.State.Running if self._running else QPropertyAnimation.State.Stopped
    def stop(self):self._timer.stop();self._running = False
    def start(self):
        self.stop();self._running = True;self._started = time.perf_counter();self._frame = 0
        hz = self.widget.screen().refreshRate() if self.widget.screen() else 60
        self._period = 1/max(60,min(360,hz or 60))
        self._tick()
    def _tick(self):
        if not self._running:return
        elapsed = time.perf_counter()-self._started
        progress = min(1,elapsed/(self._duration/1000))
        eased = self._curve.valueForProgress(progress)
        previous = self.widget.geometry()
        if self.property_name == b'capsuleWidth':
            self.widget.set_capsule_width(round(self._start+(self._end-self._start)*eased))
        else:
            self.widget.move(round(self._start.x()+(self._end.x()-self._start.x())*eased),round(self._start.y()+(self._end.y()-self._start.y())*eased))
        parent = self.widget.parentWidget()
        if parent is not None:
            parent.update(previous.united(self.widget.geometry()).adjusted(-2,-2,2,2))
        if progress >= 1:
            self.stop();self.finished.emit();return
        self._frame = max(self._frame+1,int(elapsed/self._period)+1)
        remaining = self._started+self._frame*self._period-time.perf_counter()
        self._timer.start(max(1,round(remaining*1000)))


def save_demo_capture(widget,path):
    """QA-only: QWidget.grab does not reliably include OpenGL child buffers."""
    clock=getattr(widget,'preview',None) or getattr(widget,'clock',None)
    surface=getattr(clock,'_gpu_surface',None) if clock is not None else None
    if surface is None or not surface.isValid():
        widget.grab().save(path);return
    framebuffer=surface.grabFramebuffer()
    if hasattr(widget,'preview'):
        image=widget.grab().toImage()
        painter=QPainter(image)
        point=surface.mapTo(widget,QPoint(0,0))
        target=QRectF(point.x(),point.y(),surface.width(),surface.height())
        painter.fillRect(target,QColor('#121212'))
        painter.drawImage(target,framebuffer)
        painter.end()
    else:
        image=framebuffer.copy()
        image.setDevicePixelRatio(surface.devicePixelRatioF())
        painter=QPainter(image)
        for child in widget.children():
            if isinstance(child,QWidget) and child is not clock and child.isVisible():
                painter.drawPixmap(child.pos(),child.grab())
        painter.end()
    image.save(path)


MATERIAL = {'primary': '#92A4B8', 'on_primary': '#15202B', 'track': '#424A53', 'outline': '#84909D', 'text': '#E5E5E5'}

def action_icon(text, color):
    choices = {'apply': None, 'github':'github-twotone', 'test':'play-twotone',
               'custom':'paint-drop-twotone', 'install':'download-twotone',
               'download':'download-twotone', 'close':'close', 'exit':'close',
               'reset':'backup-restore', 'update':'backup-restore'}
    name = next((icon for word, icon in choices.items() if word in text.lower()), None)
    return QIcon(os.path.join(os.path.dirname(__file__), 'ui-assets', name+'.svg')) if name else QIcon()


def load_ui_font():
    app = QApplication.instance()
    if not hasattr(app, '_sans_flex_id'):
        app._sans_flex_id = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'ui-assets', 'GoogleSansFlex.ttf'))


def polish_controls(root, accent):
    """Shared desktop control treatment; no additional widgets or effects."""
    ink, hover, pressed = get_color_variants(accent)
    for label in root.findChildren(QLabel):
        if label.objectName() == 'versionBadge' or root.__class__.__name__ == 'AboutDialog':
            continue
        text = label.text()
        size = 18 if text == 'Dinoscreener' else 13 if text in ('Appearance', 'Behavior', 'Flip Clock', 'Rotary Clock', 'Dino Runner') else 11
        label.setStyleSheet(label.styleSheet() + f"; font-family: 'Google Sans Flex'; font-size: {size}px; background: transparent;")
    for widget in root.findChildren(QWidget):
        if isinstance(widget, (QSlider, QComboBox, QCheckBox)):
            widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    for slider in root.findChildren(QSlider):
        slider._accent = MATERIAL['primary']
        slider.setStyleSheet(f"""
            QSlider {{ background: transparent; min-height: 26px; }}
            QSlider::groove:horizontal {{ background: rgba(255,255,255,0.14); height: 4px; border-radius: 2px; }}
            QSlider::sub-page:horizontal {{ background: {accent}; border-radius: 2px; }}
            QSlider::handle:horizontal {{ background: #F2F2F2; border: 2px solid {accent}; width: 16px; height: 16px; margin: -6px 0; border-radius: 9px; }}
            QSlider::handle:horizontal:hover, QSlider::handle:horizontal:focus {{ border-color: #FFFFFF; background: #FFFFFF; }}
        """)
    for combo in root.findChildren(QComboBox):
        combo.setMinimumContentsLength(10)
        combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        combo.setStyleSheet(f"""
            QComboBox {{ background: rgba(255,255,255,0.055); color: #E8E8E8; border: 1px solid rgba(255,255,255,0.17); border-radius: 8px; padding: 4px 24px 4px 10px; font: 11px 'Google Sans Flex'; min-height: 22px; }}
            QComboBox:hover {{ background: rgba(255,255,255,0.09); border-color: rgba(255,255,255,0.32); }}
            QComboBox:focus {{ border-color: #E8E8E8; }}
            QComboBox:disabled {{ color: #737373; background: rgba(255,255,255,0.025); border-color: rgba(255,255,255,0.08); }}
            QComboBox::down-arrow:disabled {{ image: none; }}
            QComboBox::drop-down {{ width: 20px; border: none; }}
            QComboBox::down-arrow {{ image: url("{get_or_create_chevron_icon()}"); width: 10px; height: 10px; }}
            QComboBox QAbstractItemView {{ background: #242424; color: #F2F2F2; selection-background-color: {accent}; selection-color: {ink}; border: 1px solid #555555; padding: 6px; }}
        """)
    excluded = set(getattr(getattr(root, 'mode_capsule', None), 'mode_buttons', []))
    for button in root.findChildren(QPushButton):
        if button in excluded or isinstance(button, ColorSwatch):
            continue
        button_accent = MATERIAL['primary']
        ink, hover, pressed = get_color_variants(button_accent)
        primary = button.text() == 'Apply' 
        destructive = 'Reset' in button.text()
        icon = action_icon(button.text(), ink if primary else MATERIAL['primary'])
        if not icon.isNull():
            button.setIcon(icon)
            button.setIconSize(QSize(14,14))
        if button.maximumHeight() >= 28:
            button.setMinimumHeight(28)
        radius = 8
        button._material_surface = (primary, destructive, radius)
        button.setStyleSheet(f"""
            QPushButton {{ background: {button_accent if primary else 'transparent' if destructive else 'rgba(255,255,255,0.055)'}; color: {ink if primary else '#92A4B8'}; border: 1px solid {'transparent' if primary or destructive else 'rgba(255,255,255,0.24)'}; border-radius: {radius}px; font: {'600' if primary else '500'} 11px 'Google Sans Flex'; padding: 5px 10px; }}
            QPushButton:hover {{ background: {hover if primary else 'rgba(255,255,255,0.11)'}; color: {ink if primary else '#FFFFFF'}; border-color: rgba(255,255,255,0.30); }}
            QPushButton:pressed {{ background: {pressed if primary else 'rgba(255,255,255,0.17)'}; }}
            QPushButton:focus {{ border: 1px solid #FFFFFF; }}
            QPushButton:disabled {{ color: #777777; background: rgba(255,255,255,0.025); border-color: rgba(255,255,255,0.06); }}
        """)
        if button.width() <= 40 or button.objectName() == 'closeIconBtn':
            button.setStyleSheet(button.styleSheet() + ' QPushButton { padding: 0px; }')
        if not button.accessibleName():
            button.setAccessibleName(button.text() or button.toolTip())
    for check in root.findChildren(VectorCheckBox):
        check.setStyleSheet("QCheckBox { background: transparent; spacing: 9px; font: 11px 'Google Sans Flex'; min-height: 28px; } QCheckBox::indicator { width: 32px; height: 20px; }")


class StudioSlider(QSlider):
    """Paint at the screen's pixel ratio while preserving Qt input semantics."""
    def paintEvent(self, event):
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        handle = self.style().subControlRect(QStyle.ComplexControl.CC_Slider, option, QStyle.SubControl.SC_SliderHandle, self)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        accent = QColor(getattr(self, '_accent', '#B8B8B8'))
        y = self.height() / 2
        left, right = 9.0, self.width()-9.0
        x = max(left, min(right, handle.center().x()))
        if not self.isEnabled():
            painter.setOpacity(0.38)
        painter.setPen(QPen(QColor(MATERIAL['track']),8,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        painter.drawLine(QPointF(left,y),QPointF(right,y))
        painter.setPen(QPen(accent,8,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        start = right if option.upsideDown else left
        painter.drawLine(QPointF(start,y),QPointF(x,y))
        if self.hasFocus() or self.isSliderDown():
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(146,164,184,40))
            painter.drawEllipse(QPointF(x,y),12,12)
        painter.setPen(QPen(QColor('#19191F'),8,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        painter.drawLine(QPointF(x,y-8),QPointF(x,y+8))
        painter.setPen(QPen(accent,4,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        painter.drawLine(QPointF(x,y-9),QPointF(x,y+9))
        painter.end()


class ColorSwatch(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.color = QColor(color)
        self.setCheckable(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center = QRectF(self.rect()).center()
        ring_radius = min(self.width(), self.height())/2 - 2
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.color)
        painter.drawEllipse(center, 8, 8)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if self.isChecked() or self.hasFocus():
            painter.setPen(QPen(QColor('#F5F5F5'), 1.5))
            painter.drawEllipse(center, ring_radius, ring_radius)
        elif self.underMouse():
            painter.setPen(QPen(QColor(255,255,255,120), 1))
            painter.drawEllipse(center, ring_radius, ring_radius)
        painter.end()


class VectorCheckBox(QCheckBox):
    """Native checkbox semantics with a device-resolution vector indicator."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._accent = QColor("#D0D0D0")

    def hitButton(self, point):
        return self.rect().contains(point)

    def paintEvent(self, event):
        option = QStyleOptionButton()
        self.initStyleOption(option)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, option, self)).adjusted(1, 1, -1, -1)
        label_rect = self.rect().adjusted(int(rect.right()) + 9, 0, 0, 0)
        painter.setFont(self.font())
        painter.setPen(QColor('#E5E5E5') if self.isEnabled() else QColor('#777777'))
        painter.drawText(label_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self.text())
        if not self.isEnabled():
            painter.setOpacity(0.38)
        checked = self.isChecked()
        painter.setPen(QPen(QColor('#C3D0E1' if checked else MATERIAL['outline']), 1.4))
        painter.setBrush(QColor('#C3D0E1' if checked else '#303840'))
        painter.drawRoundedRect(rect, rect.height()/2, rect.height()/2)
        radius = 6.5 if checked else 5.0
        center = QPointF(rect.right()-9 if checked else rect.left()+9, rect.center().y())
        if self.underMouse() or self.hasFocus():
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(146,164,184,45))
            painter.drawEllipse(center,11,11)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(MATERIAL['on_primary'] if checked else '#C6CDD4'))
        painter.drawEllipse(center,radius,radius)
        if self.hasFocus() and self.testAttribute(Qt.WidgetAttribute.WA_KeyboardFocusChange):
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor('#DCE5EE'),1))
            painter.drawRoundedRect(rect.adjusted(2,2,-2,-2),7,7)
        painter.end()


class LockExitSwitch(VectorCheckBox):
    def nextCheckState(self):
        if self.isChecked():
            self.setChecked(False)
            return
        bubble = LockNotice(self)
        if bubble.exec() == QDialog.DialogCode.Accepted:
            self.setChecked(True)
        bubble.deleteLater()


class LockNotice(QDialog):
    message = "IMPORTANT! When the screen saver is active, press Ctrl+Z to exit screensaver. OR You might be stuck forever :(!!"

    def __init__(self, switch):
        super().__init__(switch.window(), Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAccessibleName("Confirm Lock on exit")
        self.setStyleSheet("QDialog { background: transparent; } QLabel { background: transparent; color: #EAF0F5; }")
        self.anchor = switch.mapToGlobal(QPoint(16, switch.height()//2))
        area = switch.screen().availableGeometry()
        self.above = self.anchor.y()-area.top() > 150
        row = QHBoxLayout(self)
        row.setContentsMargins(14, 12 if self.above else 22, 10, 22 if self.above else 12)
        label = QLabel(self.message)
        label.setWordWrap(True)
        label.setFixedWidth(224)
        row.addWidget(label)
        close = QPushButton("×")
        close.setAccessibleName("Acknowledge warning and enable Lock on exit")
        close.setFixedSize(24,24)
        close.clicked.connect(self.accept)
        row.addWidget(close, 0, Qt.AlignmentFlag.AlignTop)
        self.setFixedSize(row.sizeHint())
        x = min(max(area.left(), self.anchor.x()-36), area.right()-self.width()+1)
        y = self.anchor.y()-switch.height()//2-self.height() if self.above else self.anchor.y()+switch.height()//2
        self.tip = max(13,min(self.width()-13,self.anchor.x()-x))
        self.move(x,y)
        self.pulse = QVariantAnimation(self)
        self.pulse.setDuration(600)
        self.pulse.setStartValue(0.0)
        self.pulse.setKeyValueAt(0.45,1.0)
        self.pulse.setEndValue(0.0)
        self.pulse.valueChanged.connect(lambda _: self.update())
        self.pulse.start()

    def paintEvent(self,event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        top = 1 if self.above else 11
        bottom = self.height()-(11 if self.above else 1)
        body = QPainterPath()
        body.addRoundedRect(QRectF(1,top,self.width()-2,bottom-top),5,5)
        side = bottom if self.above else top
        arrow = QPainterPath()
        arrow.moveTo(self.tip-8,side)
        arrow.lineTo(self.tip,side+(9 if self.above else -9))
        arrow.lineTo(self.tip+8,side)
        arrow.closeSubpath()
        p.setBrush(QColor('#222930'))
        p.setPen(QPen(QColor('#92A4B8').lighter(100+round(45*(self.pulse.currentValue() or 0))),2))
        p.drawPath(body.united(arrow))
        p.end()


APP_VERSION = "v6.2"
APP_NAME = "Dinoscreener"
APP_AUTHOR = "Kushal Arvind"
APP_GITHUB_REPO = "kushalarvindo/dinoscreener"
APP_GITHUB_URL = "https://github.com/kushalarvindo/dinoscreener"

SPRITE_B64 = 'iVBORw0KGgoAAAANSUhEUgAABNEAAABECAAAAACKI/xBAAAAAnRSTlMAAHaTzTgAAAoOSURBVHgB7J1bdqS4FkSDu7gPTYSh2AOATw1Pn6kBVA2FieiTrlesq6po8lgt0pj02b06E58HlRhXOCQBBcdxHMdxHOfDMeA7BfcIOI4VwISDKQhvK0O4H9iAobeFZSx8WIK0dqz4ztQRg1XdECNfX/CTGUDmNjJDP6MzuMnKKsQ0Y+Amyxnirurmx1KghAvWXoARAErEPUpAB/KzvK6YcAIl8lD2AtsCbENPS1XGwqMTSnvHhNOYgBV3mKlklKDqPUshMUIzsuzlOXFGW9AQS0C/lv/QMWrahOMoiKZL41HyUCRAdcKyDR0tVRkLD0+oV7Q7yLofm6w6rKbdrmNUL6NOyapMtGcUuixZ2WSHbsl+M97BoUX8TrpyrfGbJJ+saBQ0W9I6jnxF/ZO+4nqo66GQneo325keUjth7bFpX38MO6lbM+ZMaeOYETISzYzN9Wiy7shuyj4dI96JSQXuOMSlWcqkgQ2DSlVdUSIbWbVs2vJ41CvadDs0jTE63Y9NWO26r3x9MU3AzDGk1mQWZu2Bht6VaPzEXrl21gjyZRXNPnKFI8+TJnRKLEED24JNpaqqKBGx/C5oWLSlBR0+Pp4J5yM27YVydp8sX4p+SUGe661TuWE5Y78dtcDSX3u+oqWINjLmRm+wTsBUJWpK06pKaXZpJdbmhoH/LcByq6Rq+LMC+7Dl+OFjvzj2ObRJY/tOa1r/uUvDy9d9QaPz4utMP6ZDysxsPeScf3yly6bOfRbcemtPYESvpAn20GSS0efVKOGc4aNQgojj1ZnzvTEnkxqzOVfGllP3y9qnZ0S3pM2mK5jMwQcpiMb1ZVqdkBANl1aCFbBbdOR6Pvwgtjiu9vkx60jrXNpq15E8ywhz/2tbzGQQwQ4b59Zfe7aipVrSEhCP8mZG1UlzZ20tOgw9Hw6hrzCLZiyObqCkVauZFC0OPL8nqUrk/zHN1gopOfkzngH3fv8SQau20jtMQ09VUSmxQUS1OsZSDAWSwKNFq5SylzA6PhFf+Oo4x3m0pEuYKXb4s5WLAAaT1lwfc3Kr6CDZ6JD6hrUCWVhmjHFrzNk17pxWjdGl/Yi9AuBrBqAbusmvGNNCyWpbhvPU82j1aDMi9Q04p8aLaQtiw7plXZ0A7TwDSojO/GsCiAnE6qAGhg45/eAu7csrunGcEUpEN5NsXYDlUY6Mie67UGPTPiiO1xl0vgLYvXt83glmvkux7ke6WdGzz7mKmiSQM2ufmPEoQUv9d2fu3jEazGqc79JUQjRxghoZT9FoiJnjzvbYtDJGOXOcoxUt4hMybAucE3nloJPOSJh5v6cm8gwFWrnn72aj1txnvR+5RrzoXy8kBOAStWBtw/foGvd1NnyX+h2a+LXQUH2XKAFT0uLpi9byzXg2vrzy9Z6eAZmqIUnHoaJ9PlIofwaAYQMWu6XituAE6vWBgifhla/Xp3ClqjpFESRdt5Z+WCIkQ68vHNBAXysZH3CmuufhInRurCagvLk6QNXpbwMDNvouu+Vn/fLeVo3rA084PzAYiwDtzB1jIB3Jmvuc0YqzQRk6W0d8LhIQ9gPkNhSpEGjr2HKW4XyOuznthx/M+8V/W5+7/vRZ9yARQ4L5a18IIBetJbN18/oGYNjRHwyHt6qiJSj9R25zZ55M7Uiq6u3qglDF2KmBCqqTVqhNO0bQSp+gxRJkV9fi68uP/z8TzgYd3tyw9bQOqBUtpmdd9wwlGoGKGzDstMR7LR1EtENp582d1z5jL3yGrc79y83pSsbBZHquNluXZd5DfteKbbhaLc+Ongp1tUslUUvDve1drSPuSFoE2o/8AIL6rspChrbqZkkb0N5yhNa2E3B95Bm2vN+8m/me3lE9WaGp3LbPPDc/u9VZoJFbZ+uoCvaMhAJEDTS2xOO/Tdzp+Xs6C3mG7fXhnXlR4gnx4rXU7dma/FTl0YS29beOjztTx6NOUF2aVrNEe/bZa4m6+nmuEJUAbnFP15xH+/7fHU/FYG6LG+SmVL5bmnFZ/Ho0J4WP4NK4KMCtS7u0p/Bo9ngnXbfWXnVu/DcNdGf9rRgfeab6sWfR1KXZ1Z0kY7+l3rIToQCImiD2U9y4FepFaHm44jpJjDTGlOmfxVbGHMc92nkEW/PrrRSKJiqjF4CiHaqBNqEuLPxDLsGL/+xcvFavbLph6W89TdHCw5wZCW2zXggfe4Sqcc2oBhYYSAc+EY4zGhM5/teid0osBSaaBC3F/vPAjvpxsdDx5Dp1jjsnI7Y+95hT5z+erpZkzB/dpY2wJS0FPfLH0/wsj/AhJS0FJuTaWOPbHWFbN/9VdCUSwtPW5g81j2aMZULDkbtLE+GSBKOCdGiCURtVTXFpp7KCuEtzl3braVVFQ+g/8n6eQil/X24MmjAIe+oYJNqwK2M8uU5mXc8652rXOY6vdZ6NvdyoiXZ1jBqNcC7o0tKVaw2XlltdGs0VUwsYGTpbxwPO1JXcU7gTGLYfrx0tx6tjsW/PsjHd14p2l+YOzXGPdirBDAwdLe9sAf54IEh86zLA2qQj64SGYp9EM674Dk9Rqy4tY58B2MRqVRZOIr2t44FnymfRzlyJSOHBLg2rOzSnn5vxjI3O1hHXxyVNb8zqt2mNi6OrGzR9egPfH1QLREQgFSDs17Ky/zOoS+O7wVJNfN1axjh108L93G8dH3umelx7gGMTCuLbbfJEQZEYha6KGTbN9l2r+zNn2xkwLnzorNWqsLVP0eaGXMZ74pLWDNXLL0N7+GRnAmdqwgNqE4O7tQkREQmp+zMoudWlATcMaIRN28ErA5nv9pF/6PtEnak/1r8H53lRR6bcfuYe0DrCcZxL3vdk19PHBZQz73u6AT0ODZWGbTAY33Ud0nEcZ3hg64gmZjiO81YiCkK1dXytBauO/wwzsmxBqc3VIhP6DVNw5FhFywDS24/cKeHRCdLfoTiO3zMw58+uYUX/HYD2BLETinY4Z5Bk6+jaFo79DFm3LG4Q+pr6r97I5pH7pRsllgiQUEJ7QsSRCdN2aYfjuEczNDnollPLSKm/7EhQ6pgQ2yUKpx3OaQTZOra2gf7P0M/Q3+ScTJlLX6KgECb49h02lFLudPzVzn0lNQwEURQdrfGuc9anX34AIzk21c/xHjLYCo/JU2W1kLTm/7BeP7kkSZIkZbj0JhHZgDdAg5UeAA6f9f8Ar//eMZqUxs8ggs7BhAEarPQAsPm+hwFus4SnG6Mx3pI0xwEX/syoMMDteO0x17QlCd5m/CbX0STs9m3RDggXBLpKWv5S83eSF787y1Wd5apuCcXDHFu0HL1wPGbhz6lL2WL2VYrtE6NPZW7usXAEy1WZ5epGInCMMLhTBsCQ5erTyhXVlAASQROIjO0FvHBFh+evzparEMvVsp8XMGZ5HuHL3cZGzpu884kxZtN/1HLVynL1uiRJkvQFUg1OaKSaqSkAAAAASUVORK5CYII='
class CrispAestheticFlipClock(QWidget):
    def __init__(self, accent_color="#8F96BF", enable_win_key=False, strict_exit=False, show_info=True, preview_mode=False, brightness=100, clock_style=1, clock_scales=None, use_24hr=False, leading_zeros=None, config_path=None, full_config=None, ignore_media_keys=False, dino_font="Bungee", live_weather=False, pixel_shift=False, primary_font="", character_type="dino", custom_character_image="", show_weather=True, show_battery=True, use_fahrenheit=False, ambient_mode=False, hourly_chime=False, chime_preset="acoustic_bell", chime_volume=45, custom_chime_path="", parent=None, studio_mode=False):
        super().__init__(parent)
        self.studio_mode = studio_mode
        if not preview_mode:
            self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)
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
        self._gpu_surface=ClockGLSurface(self) if clock_gpu_available() else None

    def update(self,*args):
        surface=getattr(self,'_gpu_surface',None)
        if surface is not None:
            surface.update(*args)
            if surface.isValid():return
        super().update(*args)

    def resizeEvent(self,event):
        super().resizeEvent(event)
        surface=getattr(self,'_gpu_surface',None)
        if surface is not None:surface.setGeometry(self.rect())

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
        if not self.preview_mode and not getattr(self, 'studio_mode', False):
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
            self.showFullScreen()
            self.setCursor(Qt.CursorShape.BlankCursor)
            self.setMouseTracking(True)
        elif getattr(self, 'studio_mode', False):
            self.setMouseTracking(True)
        
        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.checkTime)
        self.sync_timer.start(200)

        # High-Refresh Rate & Delta Frame Pacing (Smooth on 165Hz, 144Hz, 120Hz, 60Hz)
        screen = self.screen() or QApplication.primaryScreen()
        hz = screen.refreshRate() if screen else 60.0
        if not hz or hz <= 30.0:
            hz = 60.0
        self.display_hz = hz
        self.target_frame_interval = max(5, int(round(1000.0 / hz)))
        self.last_frame_time = time.perf_counter()

        self.anim_timer = QTimer(self)
        self.anim_timer.setTimerType(Qt.TimerType.PreciseTimer)
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

        # Chime once at the start of each hour in the running screensaver.
        if self.hourly_chime and not self.preview_mode:
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
        if self.clock_style == 0 and not self.animating and not self.show_bg and self.bg_opacity <= 0.0:
            if self.anim_timer.interval() != 1000:
                self.anim_timer.setInterval(1000)
        else:
            # Fractional refresh periods (175Hz = 5.714ms) must not be rounded
            # permanently to 6ms/166Hz. Alternate integer timer waits against a
            # monotonic deadline, and skip missed deadlines instead of bursting.
            period=1/max(30,self.display_hz)
            deadline=getattr(self,'_next_frame_due',now_time)
            if deadline<now_time-period:deadline=now_time
            deadline+=period
            self._next_frame_due=deadline
            interval=max(1,round((deadline-time.perf_counter())*1000))
            if self.anim_timer.interval()!=interval:self.anim_timer.setInterval(interval)
                
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
    def rotary_battery_status(self):
        now=time.monotonic()
        if now<getattr(self,'_battery_check_due',0):return self._battery_display
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
            

        self._battery_display=(bat_text,bat_val,is_charging)
        self._battery_check_due=now+1
        return self._battery_display

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
            key=(int(sz),int(weight))
            if not hasattr(self,'_rotary_fonts'):self._rotary_fonts={}
            if key in self._rotary_fonts:return self._rotary_fonts[key]
            f = QFont()
            families = ["Google Sans", "Product Sans", "Segoe UI", "Arial"]
            f.setFamilies(families)
            f.setPixelSize(int(sz))
            f.setWeight(weight)
            f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
            f.setHintingPreference(QFont.HintingPreference.PreferVerticalHinting)
            self._rotary_fonts[key]=f
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
            bat_text,bat_val,is_charging=self.rotary_battery_status()

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

    def render_clock_canvas(self, painter, w, h, clip_preview=True):
        if self.preview_mode and clip_preview:
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
        surface=getattr(self,'_gpu_surface',None)
        if surface is not None and surface.isValid():return
        w = self.width()
        h = self.height()
        if w <= 0 or h <= 0:
            return
        p_screen = QPainter(self)
        p_screen.setRenderHint(QPainter.RenderHint.Antialiasing)
        p_screen.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        p_screen.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.render_clock_canvas(p_screen, w, h)
        p_screen.end()

    def keyPressEvent(self, event):
        if getattr(self, 'studio_mode', False):
            event.ignore()
            return

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
        if getattr(self, 'studio_mode', False):
            if hasattr(self.parent(), 'handle_canvas_mouse_move'):
                self.parent().handle_canvas_mouse_move(event)
            return
        if self.preview_mode: return
        if self.strict_exit: return
        if self.last_pos is None:
            self.last_pos = event.pos()
            return
        diff = event.pos() - self.last_pos
        if abs(diff.x()) > 5 or abs(diff.y()) > 5:
            self.close()

    def mousePressEvent(self, event):
        if getattr(self, 'studio_mode', False):
            if hasattr(self.parent(), 'handle_canvas_mouse_press'):
                self.parent().handle_canvas_mouse_press(event)
            return
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
        self.setAutoFillBackground(False)
        self.setStyleSheet("QFrame#spatialStage { background: transparent; border: none; }")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        outline = QPainterPath()
        outline.addRoundedRect(QRectF(self.rect()), 20, 20)
        self.setMask(QRegion(outline.toFillPolygon().toPolygon()))
        
    def set_stage_theme(self, clock_style, accent_hex):
        pass
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width()
        h = self.height()
        
        # Deep black true screensaver display
        painter.setBrush(QColor(27, 29, 32))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(QRectF(0, 0, w, h), 20, 20)
        
        # Subtle glass specular border
        border_pen = QPen(QColor(255, 255, 255, 25), 1)
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(QRectF(0.5, 0.5, w - 1, h - 1), 20, 20)


def get_windows_accent_color():
    """Keep the demo's chosen slate accent independent of the Windows theme."""
    return "#92A4B8"


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
        # Explicit pointer-sized HWND signatures for 64-bit builds.
        dwmapi.DwmSetWindowAttribute.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]
        dwmapi.DwmSetWindowAttribute.restype = ctypes.c_long
        dwmapi.DwmExtendFrameIntoClientArea.argtypes = [ctypes.c_void_p, ctypes.POINTER(DWM_MARGINS)]
        dwmapi.DwmExtendFrameIntoClientArea.restype = ctypes.c_long
        
        # 1. Enable Windows 11 Dark Mode Titlebar & Frame (DWMWA_USE_IMMERSIVE_DARK_MODE = 20)
        dark_mode = ctypes.c_int(1)
        dwmapi.DwmSetWindowAttribute(
            hwnd, 20, ctypes.byref(dark_mode), ctypes.sizeof(dark_mode)
        )
        
        # 2. Apply Mica / Acrylic System Backdrop (Windows 11 22H2+ / Build 22621+):
        # DWMWA_SYSTEMBACKDROP_TYPE = 38
        # DWMSBT_MAINWINDOW = 2 (Mica), DWMSBT_TABBEDWINDOW = 4 (Mica Alt), DWMSBT_TRANSIENTWINDOW = 3 (Acrylic)
        applied_backdrop = False
        for backdrop_val in (3, 2, 4):
            backdrop_type = ctypes.c_int(backdrop_val)
            res = dwmapi.DwmSetWindowAttribute(
                hwnd, 38, ctypes.byref(backdrop_type), ctypes.sizeof(backdrop_type)
            )
            if res == 0:
                applied_backdrop = True
                break
                
        # Some compositor customizers acknowledge Acrylic but substitute Mica.
        # Use the window accent blur only in that case, without CPU image effects.
        if applied_backdrop:
            backdrop = ctypes.c_int()
            get_backdrop = dwmapi.DwmGetWindowAttribute
            get_backdrop.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]
            get_backdrop.restype = ctypes.c_long
            if get_backdrop(hwnd, 38, ctypes.byref(backdrop), ctypes.sizeof(backdrop)) == 0 and backdrop.value != 3:
                class AccentPolicy(ctypes.Structure):
                    _fields_ = [('state', ctypes.c_int), ('flags', ctypes.c_int),
                                ('color', ctypes.c_uint), ('animation', ctypes.c_int)]

                class CompositionData(ctypes.Structure):
                    _fields_ = [('attribute', ctypes.c_int), ('data', ctypes.c_void_p),
                                ('size', ctypes.c_size_t)]

                set_composition = getattr(ctypes.windll.user32, 'SetWindowCompositionAttribute', None)
                if set_composition is not None:
                    set_composition.argtypes = [ctypes.c_void_p, ctypes.POINTER(CompositionData)]
                    set_composition.restype = ctypes.c_int
                    policy = AccentPolicy(4, 0, 0x66121212, 0)
                    data = CompositionData(19, ctypes.addressof(policy), ctypes.sizeof(policy))
                    dialog._accent_blur_active = bool(set_composition(hwnd, ctypes.byref(data)))

        # Fallback for Windows 11 21H2 (Build 22000)
        if not applied_backdrop:
            mica_val = ctypes.c_int(1)
            res_mica = dwmapi.DwmSetWindowAttribute(
                hwnd, 1029, ctypes.byref(mica_val), ctypes.sizeof(mica_val)
            )
            if res_mica == 0:
                applied_backdrop = True
                
        # 3. Extend the system backdrop across the client area; no external blur tool needed
        margins = DWM_MARGINS(-1, -1, -1, -1)
        res_frame = dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))
        
        if applied_backdrop and res_frame == 0:
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
    text_color = "#111111" if lum > 140 else "#FFFFFF"
    
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
    temp_path = os.path.join(tempfile.gettempdir(), f"dinoscreener_chk_{clean_col}_v2.png").replace("\\", "/")
    if not os.path.exists(temp_path):
        from PyQt6.QtGui import QImage, QPainter, QPen, QColor, QPainterPath
        from PyQt6.QtCore import Qt, QPointF
        
        img = QImage(72, 72, QImage.Format.Format_ARGB32_Premultiplied)
        img.fill(Qt.GlobalColor.transparent)
        p = QPainter(img)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        pen = QPen(QColor(color_hex))
        pen.setWidthF(8.0)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        p.setPen(pen)
        
        path = QPainterPath()
        path.moveTo(QPointF(14.0, 37.0))
        path.lineTo(QPointF(29.0, 52.0))
        path.lineTo(QPointF(58.0, 19.0))
        p.drawPath(path)
        p.end()
        try:
            img.save(temp_path, "PNG")
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
    accent_hex = "#92A4B8"
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
    accent_hex = "#92A4B8"
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
            ("Rotary Clock", 1),
            ("Dino Runner", 2)
        ]
        self._is_expanded = False
        self._collapsed_width = 152
        self._expanded_width = 376
        self._width = self._collapsed_width
        
        self.setFixedHeight(38)
        self.setFixedWidth(self._collapsed_width)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.setStyleSheet("QFrame#capsuleFrame { background: transparent; border: none; }")
        self.setObjectName("capsuleFrame")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAutoFillBackground(False)
        
        self.stack = QStackedLayout(self)
        self.stack.setContentsMargins(0, 0, 0, 0)
        self.stack.setStackingMode(QStackedLayout.StackingMode.StackOne)
        
        # --- Page 0: Collapsed Pill View ---
        self.collapsed_view = QWidget()
        self.collapsed_view.setStyleSheet('background: transparent;')
        col_layout = QHBoxLayout(self.collapsed_view)
        col_layout.setContentsMargins(18, 0, 18, 0)
        col_layout.setSpacing(0)
        
        # Center title (always 100% centered with symmetrical margins)
        self.lbl_mode_name = QLabel("Flip Clock")
        self.lbl_mode_name.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.lbl_mode_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_mode_name.setStyleSheet("""
            color: #FFFFFF;
            font-size: 11.5px;
            font-weight: 600;
            font-family: 'Google Sans Flex', 'Google Sans Flex', sans-serif;
            background: transparent;
        """)
        
        col_layout.addWidget(self.lbl_mode_name)
        self.stack.addWidget(self.collapsed_view)
        
        # --- Page 1: Expanded 3-Button View ---
        self.expanded_view = QWidget()
        self.expanded_view.setFixedSize(self._expanded_width, 38)
        self.expanded_view.setStyleSheet('background: transparent;')
        exp_layout = QHBoxLayout(self.expanded_view)
        exp_layout.setContentsMargins(7, 4, 7, 4)
        exp_layout.setSpacing(4)
        
        self.mode_buttons = []
        for label, idx in self._modes:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setFixedSize(118, 30)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #A8A8A8;
                    border: 1px solid transparent;
                    border-radius: 14px;
                    font-size: 11.5px;
                    font-weight: 500;
                    outline: none;
                    font-family: 'Google Sans Flex', 'Google Sans Flex', sans-serif;
                }
                QPushButton:hover:!checked {
                    color: #FFFFFF;
                    background: rgba(255, 255, 255, 0.08);
                    border-radius: 14px;
                }
                QPushButton:checked {
                    background: rgba(210,218,228,0.12);
                    color: #92A4B8;
                    font-weight: 600;
                    border: 1px solid rgba(255, 255, 255, 0.18);
                    border-radius: 14px;
                }
            """)
            btn.clicked.connect(lambda checked, i=idx: self.select_mode(i))
            exp_layout.addWidget(btn)
            self.mode_buttons.append(btn)
            
        self.stack.addWidget(self.expanded_view)
        self.stack.setAlignment(self.expanded_view, Qt.AlignmentFlag.AlignCenter)
        self.stack.setCurrentIndex(0)
        
        self.opacity_effect = QGraphicsOpacityEffect(self.expanded_view)
        # Width clipping reveals the native labels without an offscreen opacity layer.
        self.opacity_effect.setOpacity(1.0)
        self.on_mode_changed = None
        self.on_width_changed = None
        self._anim_group = None
        self.set_current_mode(0)

    def paintEvent(self, event):
        super().paintEvent(event)
        if not getattr(self, 'studio_glass', False):
            panel = QPainter(self)
            panel.setRenderHint(QPainter.RenderHint.Antialiasing)
            panel.setPen(QPen(QColor(255,255,255,45),1))
            panel.setBrush(QColor(38,39,42,145 if self.underMouse() else 110))
            panel.drawRoundedRect(QRectF(self.rect()).adjusted(1,1,-1,-1),19,19)
            panel.end()
        if getattr(self, 'studio_glass', False):
            glass = QPainter(self)
            glass.setRenderHint(QPainter.RenderHint.Antialiasing)
            paint_frosted_surface(glass, self, 19)
            glass.end()
        
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
        c_peri = QColor("#92A4B8")
        c_acc = QColor(self.win_accent)
        c_core = QColor("#e0e7ff")
        
        arc_r = r - 1.8
        arc_d = arc_r * 2.0
        
        # Directional Visibility Logic:
        # idx 0 (Flip Clock): ONLY Right indicator
        # idx 1 (Rotary Clock): BOTH Left and Right indicators
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
        if not getattr(self, 'pin_open', False):
            fraction = (w-self._collapsed_width)/(self._expanded_width-self._collapsed_width)
            self.opacity_effect.setOpacity(max(0.0,min(1.0,fraction)))
        if hasattr(self, 'on_width_changed') and callable(self.on_width_changed):
            self.on_width_changed(w)

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
        self.collapse()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if not self._is_expanded:
            self.expand()

    def enterEvent(self, event):
        super().enterEvent(event)
        self.expand()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.collapse()

    def _animate_width(self, expanded):
        if self._anim_group is None:
            self._anim_group = DisplayPositionAnimation(self, b"capsuleWidth", self)
            self._anim_group.finished.connect(self._finish_width)
        self._anim_group.stop()
        self._is_expanded = expanded
        self.stack.setCurrentIndex(1 if expanded else 0)
        self._anim_group.setDuration(240 if expanded else 220)
        self._anim_group.setEasingCurve(QEasingCurve.Type.OutQuart)
        self._anim_group.setStartValue(self.width())
        self._anim_group.setEndValue(self._expanded_width if expanded else self._collapsed_width)
        self._anim_group.start()

    def expand(self):
        if not self._is_expanded:
            self._animate_width(True)

    def collapse(self):
        if not getattr(self, 'pin_open', False) and self._is_expanded:
            self._animate_width(False)

    def _finish_width(self):
        self.stack.setCurrentIndex(1 if self._is_expanded else 0)
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


class PaletteStrip(QWidget):
    colors = ('#F1DAD4','#EFC9CB','#DCB1EE','#F1B5D8','#E89EAE','#F48BAB',
              '#F8BDA2','#F0CA99','#A1E4AD','#A8E1D9','#89BDD8','#7CD7DE',
              '#C6C6F0','#9B8C9F','#D5DCE8')

    def __init__(self):
        super().__init__()
        self.setFixedHeight(22)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bar = QRectF(self.rect()).adjusted(8,8,-8,-8)
        path = QPainterPath()
        path.addRoundedRect(bar,3,3)
        painter.setClipPath(path)
        for index,color in enumerate(self.colors):
            left = round(index*bar.width()/len(self.colors))
            right = round((index+1)*bar.width()/len(self.colors))
            painter.fillRect(QRectF(bar.left()+left,bar.top(),right-left,bar.height()), QColor(color))
        painter.end()


class ResetDismissFilter(QObject):
    def eventFilter(self, watched, event):
        settings = self.parent()
        if event.type() == QEvent.Type.MouseButtonPress and settings.reset_state == 1:
            buttons = [settings.reset_button]
            studio = getattr(settings,'studio',None)
            if studio:
                buttons.append(studio.action_dock.btn_reset)
            point = event.globalPosition().toPoint()
            if not any(b.isVisible() and b.rect().contains(b.mapFromGlobal(point)) for b in buttons):
                settings.set_reset_state(0)
        return False


class AboutDialog(QDialog):
    def __init__(self, parent=None, win_accent="#D0D0D0", auto_check=False):
        super().__init__(parent)
        self.setWindowTitle("About Dinoscreener")
        self.setFixedSize(560, 680)
        self.win_accent = win_accent
        self.contrast_text, self.hover_accent, self.press_accent = get_color_variants(self.win_accent)
        
        # Subpixel ClearType Antialiased Font Hierarchy
        ui_font = QFont(["Google Sans Flex", "Segoe UI Emoji", "Arial", "sans-serif"], 9)
        ui_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
        ui_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.setFont(ui_font)

        # Windows 11 DWM Mica / Glass Blur Backdrop Setup
        self.is_dwm_active = apply_windows_dwm_effects(self)
        QTimer.singleShot(0, lambda: apply_windows_dwm_effects(self))
            
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
        if getattr(sys, 'frozen', False):
            logo_path = os.path.join(sys._MEIPASS, "app_icon.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(os.path.join(os.path.dirname(logo_path), "app_icon_taskbar.png")))
        self.logo_path = logo_path
        
        bg_dialog = "rgba(18, 18, 18, 0.34)" if self.is_dwm_active else "#121212"
        bg_card = "rgba(26, 26, 26, 0.50)" if self.is_dwm_active else "#1A1A1A"
        bg_story = "rgba(0, 0, 0, 0.28)" if self.is_dwm_active else "rgba(0, 0, 0, 0.25)"
        
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_dialog};
            }}
            QLabel {{
                background: transparent;
                color: #FFFFFF;
                font-family: 'Google Sans Flex', 'Google Sans Flex', -apple-system, sans-serif;
            }}
            QFrame {{
                background: transparent;
            }}
            QFrame#aboutCard {{
                background: {bg_card};
                border: 1px solid rgba(255, 255, 255, 0.14);
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
        layout.setContentsMargins(24, 24, 24, 24)
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
        lbl_logo_bg = "rgba(26, 26, 26, 0.50)" if self.is_dwm_active else "#1A1A1A"
        lbl_logo.setStyleSheet("background: transparent; border: none; padding: 0px;")
        if hasattr(self, 'logo_path') and os.path.exists(self.logo_path):
            lbl_logo.setPixmap(get_rounded_pixmap(self.logo_path, size=54, radius=14, dpr=lbl_logo.devicePixelRatioF()))
        logo_row.addWidget(lbl_logo)
        header_box.addLayout(logo_row)
        
        title_row = QHBoxLayout()
        title_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_row.setSpacing(10)
        lbl_title = QLabel(APP_NAME)
        lbl_title.setStyleSheet("background: transparent; font-size: 20px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.3px;")
        title_row.addWidget(lbl_title)
        
        lbl_ver = QLabel(APP_VERSION)
        lbl_ver.setObjectName('versionBadge')
        lbl_ver.setStyleSheet(f"""
            background: #D1D1E5;
            color: #202733;
            border: 1px solid #D1D1E5;
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
        lbl_author.setStyleSheet("font-size: 12px; color: #A8A8A8;")
        header_box.addWidget(lbl_author)
        
        layout.addLayout(header_box)
        
        # 2. Card 1: Authentic Creator Story & Modes with Inset Inner Box
        card_story = QFrame()
        card_story.setObjectName("aboutCard")
        story_layout = QVBoxLayout(card_story)
        story_layout.setContentsMargins(18, 16, 18, 16)
        story_layout.setSpacing(12)
        
        lbl_story_title = QLabel("ABOUT")
        lbl_story_title.setStyleSheet("background: transparent; font-size: 10px; font-weight: 700; color: #858585; letter-spacing: 0.6px;")
        story_layout.addWidget(lbl_story_title)
        
        inner_box = QFrame()
        inner_box.setObjectName("storyInnerBox")
        inner_layout = QVBoxLayout(inner_box)
        inner_layout.setContentsMargins(18, 14, 18, 14)
        inner_layout.setSpacing(0)
        
        story_text = (
            '<p style="margin: 0 0 10px 0; line-height: 1.54;">'
            "✦ Hi, I'm Kushal! 👋 I wanted a screensaver that was simple, neat, and actually fun to look at, so I built <b>Dinoscreener</b>.</p>"
            '<p style="margin: 0 0 10px 0; line-height: 1.54;">'
            "✦ <b>3 cozy styles</b> in one: a playful <b>Jumping Dino</b>, a classic <b>Flip Clock</b>, and a clean <b>Rotary Clock</b> with your weather & battery.</p>"
            '<p style="margin: 0; line-height: 1.54; color: #A8A8A8;">'
            "Hope it makes your desk smile! Ideas are always welcome 😊</p>"
        )
        lbl_story = QLabel(story_text)
        lbl_story.setTextFormat(Qt.TextFormat.RichText)
        lbl_story.setWordWrap(True)
        lbl_story.setStyleSheet("background: transparent; font-size: 11.5px; color: #D2D2D2;")
        inner_layout.addWidget(lbl_story)
        story_layout.addWidget(inner_box)
        
        # Mode Pills Row (Symmetrically centered and evenly spaced)
        pills_row = QHBoxLayout()
        pills_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pills_row.setSpacing(10)
        for icon_text in ["🦕 Chrome Dino", "⏱️ 3D Flip Clock", "⭕ Rotary Clock"]:
            lbl_pill = QLabel(icon_text)
            lbl_pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_pill.setFixedHeight(27)
            lbl_pill.setStyleSheet("""
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                color: #A8A8A8;
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
        lbl_upd_head.setStyleSheet("background: transparent; font-size: 10px; font-weight: 700; color: #858585; letter-spacing: 0.6px;")
        upd_layout.addWidget(lbl_upd_head)
        
        self.lbl_status = QLabel(f"✓ You're on the newest release (<b>{APP_VERSION}</b>).")
        self.lbl_status.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_status.setStyleSheet("background: transparent; font-size: 11.5px; color: #E6E6E6;")
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
        layout.addWidget(PaletteStrip())
        
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
        
        polish_controls(self, MATERIAL['primary'])
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
# INTERACTIVE FULLSCREEN STUDIO MODE (165Hz ZERO-LAG OBSIDIAN GLASS ARCHITECTURE)
# ==============================================================================

class SpatialGrabberBar(QWidget):
    """
    Apple visionOS-style spatial luminous pill grabber:
    Thin, futuristic glowing capsule bar with soft periwinkle ambient bloom.
    Features generous hit areas along screen borders so options reliably show on hover.
    Top: 64x5px horizontal capsule floating 14px from top edge.
    Left & Right: 5x64px vertical capsule floating 14px from screen border.
    """
    def __init__(self, studio, edge='left'):
        super().__init__(studio)
        self.studio = studio
        self.edge = edge  # 'left', 'top', 'right'
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hovered = False
        if self.edge == 'top':
            self.setFixedSize(500, 36)
            self.setToolTip("Display & Atmosphere (Click or hover to toggle)")
        elif self.edge == 'left':
            self.setFixedSize(36, 400)
            self.setToolTip("Mode Settings (Click or hover to toggle)")
        else:
            self.setFixedSize(36, 400)
            self.setToolTip("System & Controls (Click or hover to toggle)")

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hovered = True
        self.update()
        if self.edge == 'left':
            self.studio.set_left_drawer_open(True)
        elif self.edge == 'top':
            self.studio.set_top_drawer_open(True)
        elif self.edge == 'right':
            self.studio.set_right_drawer_open(True)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.edge == 'left':
            self.studio.set_left_drawer_open(not self.studio.left_open)
        elif self.edge == 'top':
            self.studio.set_top_drawer_open(not self.studio.top_open)
        elif self.edge == 'right':
            self.studio.set_right_drawer_open(not self.studio.right_open)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        
        bloom_a = 120 if self.hovered else 50
        core_a = 255 if self.hovered else 175
        
        c_bloom = QColor(146, 164, 184, bloom_a)
        c_core = QColor(255, 255, 255, core_a)
        w, h = float(self.width()), float(self.height())
        p.setPen(Qt.PenStyle.NoPen)
        
        if self.edge == 'top':
            cx = w / 2.0
            cy = 14.0
            pill_rect = QRectF(cx - 32.0, cy - 2.5, 64.0, 5.0)
            glow_rect = QRectF(cx - 34.0, cy - 4.5, 68.0, 9.0)
            p.setBrush(c_bloom)
            p.drawRoundedRect(glow_rect, 4.5, 4.5)
            p.setBrush(c_core)
            p.drawRoundedRect(pill_rect, 2.5, 2.5)
        elif self.edge == 'left':
            cx = 14.0
            cy = h / 2.0
            pill_rect = QRectF(cx - 2.5, cy - 32.0, 5.0, 64.0)
            glow_rect = QRectF(cx - 4.5, cy - 34.0, 9.0, 68.0)
            p.setBrush(c_bloom)
            p.drawRoundedRect(glow_rect, 4.5, 4.5)
            p.setBrush(c_core)
            p.drawRoundedRect(pill_rect, 2.5, 2.5)
        else:
            cx = w - 14.0
            cy = h / 2.0
            pill_rect = QRectF(cx - 2.5, cy - 32.0, 5.0, 64.0)
            glow_rect = QRectF(cx - 4.5, cy - 34.0, 9.0, 68.0)
            p.setBrush(c_bloom)
            p.drawRoundedRect(glow_rect, 4.5, 4.5)
            p.setBrush(c_core)
            p.drawRoundedRect(pill_rect, 2.5, 2.5)
            
        p.end()


def cache_frosted_backdrop(surface, studio, position, neutral=False):
    """Render only the panel region at quarter resolution, then cache a soft image.

    Event-driven only: no screen grabs, pixel loops or blur work in paintEvent.
    """
    started = time.perf_counter()
    scale = 4
    width, height = max(1,surface.width()//scale), max(1,surface.height()//scale)
    image = QImage(width, height, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(QColor('#000000'))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale(1/scale,1/scale)
    painter.translate(-position.x(),-position.y())
    studio.clock.render_clock_canvas(painter,studio.width(),studio.height())
    painter.end()
    # Cascaded smooth resampling is a bounded low-resolution tent filter.
    soft = image.scaled(max(1,width//4),max(1,height//4),Qt.AspectRatioMode.IgnoreAspectRatio,Qt.TransformationMode.SmoothTransformation)
    if neutral:
        soft = soft.convertToFormat(QImage.Format.Format_Grayscale8)
    surface.frosted_backdrop = QPixmap.fromImage(soft.scaled(width,height,Qt.AspectRatioMode.IgnoreAspectRatio,Qt.TransformationMode.SmoothTransformation))
    surface.frosted_origin = QPoint(position)
    surface.frosted_updates = getattr(surface,"frosted_updates",0)+1
    surface.frosted_ms = (time.perf_counter()-started)*1000
    surface.update()


def paint_frosted_surface(painter, surface, radius):
    rect = QRectF(1,1,surface.width()-2,surface.height()-2)
    path = QPainterPath(); path.addRoundedRect(rect,radius,radius)
    painter.save();painter.setClipPath(path)
    painter.fillRect(rect,QColor('#111111'))
    backdrop = getattr(surface,'frosted_backdrop',None)
    if backdrop is not None:
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(rect,backdrop,QRectF(backdrop.rect()))
    painter.fillRect(rect,QColor(24,24,24,170))
    sheen = QLinearGradient(0,0,0,surface.height())
    sheen.setColorAt(0,QColor(255,255,255,15));sheen.setColorAt(1,QColor(255,255,255,3))
    painter.fillRect(rect,sheen);painter.restore()
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(QColor(255,255,255,45),1))
    painter.drawRoundedRect(rect,radius,radius)


class StudioDrawer(QFrame):
    """
    Floating Studio Obsidian Glass Drawer:
    Hosts the REAL, working Settings cards from SettingsDialog.
    Renders with deep obsidian-slate rounded background (QColor(26, 26, 26, 238))
    and a subtle 1px highlight rim border with 26px rounded corners.
    """
    def __init__(self, studio, win_accent, check_icon_path, fixed_w, fixed_h):
        super().__init__(studio)
        self.studio = studio
        self.fixed_w = fixed_w
        self.fixed_h = fixed_h
        self.setFixedSize(fixed_w, fixed_h)
        self.setObjectName("studioDrawer")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.setStyleSheet(f"""
            QFrame#studioDrawer {{
                background: transparent;
                border: none;
            }}
            QFrame#bentoCard {{
                background: transparent;
                border: none;
            }}
            QLabel {{
                background: transparent;
                color: #FFFFFF;
                font-family: 'Google Sans Flex', 'Google Sans Flex', sans-serif;
            }}
            QCheckBox {{
                background: transparent;
                color: #D2D2D2;
                font-family: 'Google Sans Flex', 'Google Sans Flex', sans-serif;
                font-size: 11.5px;
                spacing: 8px;
            }}
            QCheckBox:focus {{ color: #FFFFFF; }}
            QCheckBox::indicator:focus {{ border: 2px solid #FFFFFF; }}
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
                background-color: {win_accent};
                border-color: {win_accent};
                border-radius: 6px;
                image: url("{check_icon_path}");
            }}
            QSlider::groove:horizontal {{
                border: none;
                height: 4px;
                background: rgba(255, 255, 255, 0.12);
                border-radius: 2px;
            }}
            QSlider::sub-page:horizontal {{
                background: {win_accent};
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: #FFFFFF;
                border: 2px solid {win_accent};
                width: 14px;
                margin-top: -5px;
                margin-bottom: -5px;
                border-radius: 7px;
            }}
            QComboBox {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 7px;
                color: #FFFFFF;
                padding: 2px 8px;
                font-size: 11px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #1A1A1A;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                color: #FFFFFF;
                selection-background-color: {win_accent};
            }}
        """)
        
        self.drawer_layout = QVBoxLayout(self)
        self.drawer_layout.setContentsMargins(12, 12, 12, 12)
        self.drawer_layout.setSpacing(0)
        self.card = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        paint_frosted_surface(painter,self,26)
        painter.end()

    def set_card(self, card):
        self.card = card
        self.studio.settings.cards_row.removeWidget(card)
        card.setParent(self)
        card.setAutoFillBackground(False)
        self.drawer_layout.addWidget(card)
        card.show()
        self.fit_content()

    def fit_content(self):
        if self.card is None:
            return
        self.card.layout().activate()
        hint = self.card.layout().minimumSize().expandedTo(self.card.sizeHint())
        self.fixed_w = max(self.fixed_w, hint.width()+24)
        self.fixed_h = max(120, hint.height()+24)
        self.setFixedSize(self.fixed_w, self.fixed_h)



class StudioAboutModal(QFrame):
    """
    In-Canvas Spatial Glass About Modal:
    Zero external Win32 dialogs, 100% stable frameless window activation,
    with 26px rounded corners, deep obsidian glass styling, and smooth fade transitions.
    """
    def __init__(self, studio):
        super().__init__(studio)
        self.studio = studio
        self.setFixedSize(540, 640)
        self.setObjectName("studioAboutModal")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # Subpixel ClearType antialiased font hierarchy
        ui_font = QFont(["Google Sans Flex", "Segoe UI Emoji", "Arial", "sans-serif"], 9)
        ui_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
        ui_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.setFont(ui_font)
        
        self.win_accent = self.studio.win_accent
        self.contrast_text, self.hover_accent, self.press_accent = get_color_variants(self.win_accent)
        
        self.setStyleSheet(f"""
            QFrame#studioAboutModal {{
                background: transparent;
                border: none;
            }}
            QLabel {{
                background: transparent;
                color: #FFFFFF;
                font-family: 'Google Sans Flex', 'Google Sans Flex', -apple-system, sans-serif;
            }}
            QFrame#aboutCard {{
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
            }}
            QFrame#storyInnerBox {{
                background: rgba(0, 0, 0, 0.28);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 12px;
            }}
            QPushButton#accentBtn {{
                background-color: {self.win_accent};
                color: {self.contrast_text};
                border: none;
                border-radius: 12px;
                font-weight: 600;
                font-size: 11.5px;
                padding: 6px 16px;
            }}
            QPushButton#accentBtn:hover {{
                background-color: {self.hover_accent};
            }}
            QPushButton#glassBtn {{
                background-color: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 12px;
                color: #FFFFFF;
                font-size: 11.5px;
                font-weight: 500;
                padding: 6px 16px;
            }}
            QPushButton#glassBtn:hover {{
                background-color: rgba(255, 255, 255, 0.12);
                border-color: rgba(255, 255, 255, 0.25);
            }}
            QPushButton#closeIconBtn {{
                background: transparent;
                border: none;
                color: #A8A8A8;
                font-size: 14px;
                font-weight: bold;
                border-radius: 14px;
            }}
            QPushButton#closeIconBtn:hover {{
                color: #FFFFFF;
                background: rgba(255, 255, 255, 0.10);
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
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(12)
        
        # Header Row
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        
        btn_dummy = QWidget()
        btn_dummy.setFixedSize(28, 28)
        top_bar.addWidget(btn_dummy)
        
        top_bar.addStretch()
        
        header_center = QVBoxLayout()
        header_center.setSpacing(4)
        header_center.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
        if getattr(sys, 'frozen', False):
            logo_path = os.path.join(sys._MEIPASS, "app_icon.png")
        self.logo_path = logo_path
        
        lbl_logo = QLabel()
        lbl_logo.setFixedSize(48, 48)
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setStyleSheet("background: transparent; border: none; padding: 0px;")
        if os.path.exists(logo_path):
            lbl_logo.setPixmap(get_rounded_pixmap(logo_path, size=48, radius=12, dpr=lbl_logo.devicePixelRatioF()))
        logo_box = QHBoxLayout()
        logo_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_box.addWidget(lbl_logo)
        header_center.addLayout(logo_box)
        
        title_row = QHBoxLayout()
        title_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_row.setSpacing(10)
        lbl_title = QLabel(APP_NAME)
        lbl_title.setStyleSheet("background: transparent; font-size: 19px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.3px;")
        title_row.addWidget(lbl_title)
        
        lbl_ver = QLabel(APP_VERSION)
        lbl_ver.setObjectName('versionBadge')
        lbl_ver.setStyleSheet(f"""
            background: #D1D1E5;
            color: #202733;
            border: 1px solid #D1D1E5;
            border-radius: 6px;
            font-size: 10.5px;
            font-weight: 700;
            padding: 2px 7px;
        """)
        title_row.addWidget(lbl_ver)
        header_center.addLayout(title_row)
        
        lbl_author = QLabel("Built by <b>Kushal :)</b> 👋 (@kushalarvindo)")
        lbl_author.setTextFormat(Qt.TextFormat.RichText)
        lbl_author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_author.setStyleSheet("font-size: 11.5px; color: #A8A8A8;")
        header_center.addWidget(lbl_author)
        
        top_bar.addLayout(header_center)
        top_bar.addStretch()
        
        btn_close_top = QPushButton("✕")
        btn_close_top.setObjectName("closeIconBtn")
        btn_close_top.setFixedSize(36, 36)
        btn_close_top.setAccessibleName('Close About')
        btn_close_top.setToolTip('Close About (Esc)')
        btn_close_top.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close_top.clicked.connect(self.studio.hide_about)
        top_bar.addWidget(btn_close_top)
        
        main_layout.addLayout(top_bar)
        
        # 1. Card 1: Story & Modes
        card_story = QFrame()
        card_story.setObjectName("aboutCard")
        story_layout = QVBoxLayout(card_story)
        story_layout.setContentsMargins(16, 12, 16, 12)
        story_layout.setSpacing(10)
        
        lbl_story_title = QLabel("ABOUT")
        lbl_story_title.setStyleSheet("background: transparent; font-size: 10px; font-weight: 700; color: #858585; letter-spacing: 0.6px;")
        story_layout.addWidget(lbl_story_title)
        
        inner_box = QFrame()
        inner_box.setObjectName("storyInnerBox")
        inner_layout = QVBoxLayout(inner_box)
        inner_layout.setContentsMargins(14, 10, 14, 10)
        inner_layout.setSpacing(0)
        
        story_text = (
            '<p style="margin: 0 0 8px 0; line-height: 1.5;">'
            "✦ Hi, I'm Kushal! 👋 I wanted a screensaver that was simple, neat, and actually fun to look at, so I built <b>Dinoscreener</b>.</p>"
            '<p style="margin: 0 0 8px 0; line-height: 1.5;">'
            "✦ <b>3 cozy styles</b> in one: a playful <b>Jumping Dino</b>, a classic <b>Flip Clock</b>, and a clean <b>Rotary Clock</b> with your weather & battery.</p>"
            '<p style="margin: 0; line-height: 1.5; color: #A8A8A8;">'
            "Hope it makes your desk smile! Ideas are always welcome 😊</p>"
        )
        lbl_story = QLabel(story_text)
        lbl_story.setTextFormat(Qt.TextFormat.RichText)
        lbl_story.setWordWrap(True)
        lbl_story.setStyleSheet("background: transparent; font-size: 11px; color: #D2D2D2;")
        inner_layout.addWidget(lbl_story)
        story_layout.addWidget(inner_box)
        
        pills_row = QHBoxLayout()
        pills_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pills_row.setSpacing(8)
        for icon_text in ["🦕 Chrome Dino", "⏱️ 3D Flip Clock", "⭕ Rotary Clock"]:
            lbl_pill = QLabel(icon_text)
            lbl_pill.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_pill.setFixedHeight(24)
            lbl_pill.setStyleSheet("""
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                color: #A8A8A8;
                font-size: 10.5px;
                font-weight: 500;
                padding: 0 10px;
            """)
            pills_row.addWidget(lbl_pill)
        story_layout.addLayout(pills_row)
        main_layout.addWidget(card_story)
        
        # 2. Card 2: Status & Updates
        card_upd = QFrame()
        card_upd.setObjectName("aboutCard")
        upd_layout = QVBoxLayout(card_upd)
        upd_layout.setContentsMargins(16, 12, 16, 12)
        upd_layout.setSpacing(8)
        
        lbl_upd_head = QLabel("UPDATES")
        lbl_upd_head.setStyleSheet("background: transparent; font-size: 10px; font-weight: 700; color: #858585; letter-spacing: 0.6px;")
        upd_layout.addWidget(lbl_upd_head)
        
        self.lbl_status = QLabel(f"✓ You're on the newest release (<b>{APP_VERSION}</b>).")
        self.lbl_status.setTextFormat(Qt.TextFormat.RichText)
        self.lbl_status.setStyleSheet("background: transparent; font-size: 11.5px; color: #E6E6E6;")
        upd_layout.addWidget(self.lbl_status)
        
        self.material_loader = MaterialYouLoader(self.win_accent, self)
        upd_layout.addWidget(self.material_loader)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        upd_layout.addWidget(self.progress_bar)
        
        upd_btn_row = QHBoxLayout()
        upd_btn_row.setSpacing(8)
        
        self.btn_check = QPushButton("Check for Updates")
        self.btn_check.setObjectName("glassBtn")
        self.btn_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_check.clicked.connect(self.check_updates_clicked)
        upd_btn_row.addWidget(self.btn_check, stretch=1)
        
        self.btn_install = QPushButton("Download & Install")
        self.btn_install.setObjectName("accentBtn")
        self.btn_install.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_install.setVisible(False)
        self.btn_install.clicked.connect(self.install_update_clicked)
        upd_btn_row.addWidget(self.btn_install, stretch=1)
        
        upd_layout.addLayout(upd_btn_row)
        main_layout.addWidget(card_upd)
        main_layout.addWidget(PaletteStrip())
        
        # 3. Footer
        footer_row = QHBoxLayout()
        self.btn_github = QPushButton("GitHub")
        self.btn_github.setObjectName("glassBtn")
        self.btn_github.setFixedWidth(90)
        self.btn_github.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(APP_GITHUB_URL)))
        footer_row.addWidget(self.btn_github)
        
        footer_row.addStretch()
        
        btn_close = QPushButton("Close")
        btn_close.setObjectName("glassBtn")
        btn_close.setFixedWidth(90)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(self.studio.hide_about)
        footer_row.addWidget(btn_close)
        main_layout.addLayout(footer_row)
        
        self.latest_download_url = ""
        self.latest_tag = ""

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        paint_frosted_surface(painter,self,26)
        painter.end()

    def show_modal(self):
        sw = self.studio.width()
        sh = self.studio.height()
        self.move((sw - self.width()) // 2, (sh - self.height()) // 2)
        if hasattr(self.studio.settings, 'latest_update_info') and self.studio.settings.latest_update_info:
            latest_tag, body, download_url = self.studio.settings.latest_update_info
            self.on_update_result(True, latest_tag, body, download_url)
        cache_frosted_backdrop(self,self.studio,self.pos())
        self.show()
        self.raise_()
        self.studio.action_dock.raise_()
        self.setFocus()

    def hide_modal(self):
        self.hide()
        if hasattr(self.studio, 'setFocus'):
            self.studio.setFocus()

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
        dlg = AboutDialog(self, win_accent=self.win_accent, auto_check=False)
        dlg.apply_update(downloaded_file)


class StudioInfoButton(QPushButton):
    def __init__(self, studio):
        super().__init__(studio)
        self.studio = studio
        self.setFixedSize(42, 42)
        self.setObjectName("studioInfoBtn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIcon(get_or_create_info_duotone_icon(self.studio.win_accent))
        self.setIconSize(QSize(22, 22))
        self.setToolTip("About, version & updates")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("""
            QPushButton#studioInfoBtn {
                background: transparent;
                border: none;
            }
        """)
        self.clicked.connect(self.studio.toggle_about)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        w, h = float(self.width()), float(self.height())
        bg_col = QColor(40, 40, 40, 245) if self.underMouse() else QColor(26, 26, 26, 238)
        border_col = QColor(255, 255, 255, 60) if self.underMouse() else QColor(255, 255, 255, 26)
        p.setBrush(bg_col)
        p.setPen(QPen(border_col, 1.0))
        p.drawEllipse(QRectF(1.0, 1.0, w - 2.0, h - 2.0))
        p.end()
        super().paintEvent(event)


class StudioActionDock(QFrame):
    def __init__(self, studio):
        super().__init__(studio)
        self.studio = studio
        self.setFixedSize(330, 44)
        self.setObjectName("studioDock")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.setStyleSheet("""
            QFrame#studioDock {
                background: transparent;
                border: none;
            }
            QPushButton {
                font-family: 'Google Sans Flex', 'Google Sans Flex', sans-serif;
            }
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(8)
        
        # 1. Reset Defaults
        self.btn_reset = QPushButton("Reset Defaults")
        self.btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reset.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #A8A8A8;
                border: none;
                border-radius: 12px;
                padding: 4px 8px;
                font-size: 11px;
                font-weight: 500;
            }
            QPushButton:hover {
                color: #F87171;
                background: rgba(239, 68, 68, 0.12);
            }
        """)
        self.btn_reset.clicked.connect(self.studio.reset_defaults_clicked)
        layout.addWidget(self.btn_reset)
        
        # 2. Apply button
        self.btn_apply = QPushButton("Apply")
        self.btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_apply.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.studio.win_accent};
                color: {self.studio.contrast_text};
                border: 1px solid rgba(255, 255, 255, 0.20);
                border-radius: 15px;
                font-weight: 600;
                font-size: 11.5px;
                padding: 5px 18px;
            }}
            QPushButton:hover {{
                background-color: {self.studio.hover_accent};
            }}
        """)
        self.btn_apply.clicked.connect(self.studio.apply_clicked)
        layout.addWidget(self.btn_apply)
        
        # 3. Exit button
        self.btn_exit = QPushButton("Exit")
        self.btn_exit.setToolTip("Return to settings (F11)")
        self.btn_exit.setAccessibleName("Exit fullscreen Studio")
        self.btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                color: #D2D2D2;
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 15px;
                font-weight: 500;
                font-size: 11.5px;
                padding: 5px 14px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.16);
                color: #FFFFFF;
                border-color: rgba(255, 255, 255, 0.28);
            }
        """)
        self.btn_exit.clicked.connect(self.studio.close_studio)
        layout.addWidget(self.btn_exit)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        w, h = float(self.width()), float(self.height())
        paint_frosted_surface(p, self, 22)
        p.end()
        super().paintEvent(event)


class FullscreenStudioMode(QWidget):
    """
    Interactive Fullscreen Studio Mode:
    Live-edit all screensaver settings in fullscreen with the REAL Settings cards,
    minimalist Apple visionOS spatial luminous grabber bars, and 165Hz zero-lag obsidian glass cards.
    """
    def __init__(self, settings_dialog):
        super().__init__()
        self.settings = settings_dialog
        self._closing = False
        self._exit_press = False
        self.win_accent = self.settings.win_accent
        self.contrast_text, self.hover_accent, self.press_accent = get_color_variants(self.win_accent)
        check_icon_path = get_or_create_check_icon(self.contrast_text)
        
        self.setWindowTitle("Dinoscreener Fullscreen Studio")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setObjectName("fullscreenStudioRoot")
        self.setStyleSheet("QWidget#fullscreenStudioRoot { background-color: #000000; }")
        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        
        # 1. Embedded Screensaver Canvas: TRUE FULLSCREEN MODE, Parented, Edge-to-Edge
        self.clock = CrispAestheticFlipClock(
            accent_color=self.settings.config.get("accent_color", self.win_accent),
            enable_win_key=self.settings.win_cb.isChecked(),
            strict_exit=True,
            show_info=self.settings.show_weather_cb.isChecked() or self.settings.show_battery_cb.isChecked(),
            show_weather=self.settings.show_weather_cb.isChecked(),
            show_battery=self.settings.show_battery_cb.isChecked(),
            use_fahrenheit=self.settings.fahrenheit_cb.isChecked(),
            ambient_mode=self.settings.ambient_cb.isChecked(),
            preview_mode=False,
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
            parent=self,
            studio_mode=True
        )
        self.clock.setMouseTracking(True)
        self.clock.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.clock.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.clock.lower()
        
        # 2. Floating HUD Elements
        self.btn_info = StudioInfoButton(self)
        self.action_dock = StudioActionDock(self)
        polish_controls(self.action_dock, self.win_accent)
        
        self.mode_capsule = CollapsibleModeCapsule(win_accent=self.win_accent, parent=self)
        self.mode_capsule.studio_glass = True
        self.mode_capsule.setStyleSheet('QFrame#capsuleFrame { background: transparent; border: none; }')
        self.mode_capsule.set_current_mode(self.clock.clock_style)
        self.mode_capsule.on_mode_changed = self.on_studio_mode_changed
        self.mode_capsule.on_width_changed = self._recenter_mode_capsule
        
        # 3. Real Working Drawers: Hosting the ACTUAL Settings cards
        self.left_drawer = StudioDrawer(self, self.win_accent, check_icon_path, 340, 316)
        self.top_drawer = StudioDrawer(self, self.win_accent, check_icon_path, 350, 270)
        self.right_drawer = StudioDrawer(self, self.win_accent, check_icon_path, 280, 216)
        
        self.left_drawer.set_card(self.settings.card_mode)
        self.top_drawer.set_card(self.settings.card_disp)
        self.right_drawer.set_card(self.settings.card_sys)
        
        # 4. Apple visionOS Spatial Luminous Grabber Bars
        self.left_grabber = SpatialGrabberBar(self, edge='left')
        self.top_grabber = SpatialGrabberBar(self, edge='top')
        self.right_grabber = SpatialGrabberBar(self, edge='right')
        
        # 5. In-Canvas About Modal (Zero window focus deactivation)
        self.about_modal = StudioAboutModal(self)
        self.about_modal.hide()
        polish_controls(self.about_modal, self.win_accent)
        
        # State tracking
        self.left_open = False
        self.top_open = False
        self.right_open = False
        
        # Position animations
        self.anim_left = DisplayPositionAnimation(self.left_drawer, b"pos", self)
        self.anim_left.setDuration(260)
        self.anim_left.setEasingCurve(QEasingCurve.Type.OutQuart)
        
        self.anim_top = DisplayPositionAnimation(self.top_drawer, b"pos", self)
        self.anim_top.setDuration(260)
        self.anim_top.setEasingCurve(QEasingCurve.Type.OutQuart)
        
        self.anim_right = DisplayPositionAnimation(self.right_drawer, b"pos", self)
        self.anim_right.setDuration(260)
        self.anim_right.setEasingCurve(QEasingCurve.Type.OutQuart)

        self.exit_shortcut = QShortcut(QKeySequence("F11"), self)
        self.exit_shortcut.activated.connect(self.close_studio)
        self.apply_feedback_timer = QTimer(self)
        self.apply_feedback_timer.setSingleShot(True)
        self.apply_feedback_timer.timeout.connect(self.restore_apply_button)
        self.backdrop_refresh = QTimer(self)
        self.backdrop_refresh.setSingleShot(True)
        self.backdrop_refresh.timeout.connect(self.refresh_frosted_panels)
        for animation in (self.anim_left,self.anim_top,self.anim_right):
            animation.finished.connect(self.refresh_frosted_panels)
        QApplication.instance().installEventFilter(self)


    def eventFilter(self, watched, event):
        if (isinstance(QApplication.activeModalWidget(), LockNotice) or self._closing or not self.isVisible() or not isinstance(watched, QWidget)
                or not (watched is self or self.isAncestorOf(watched))):
            return super().eventFilter(watched, event)
        kind = event.type()
        if kind not in (QEvent.Type.MouseMove, QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonRelease):
            return super().eventFilter(watched, event)
        point = event.globalPosition().toPoint()
        capsule = self.mode_capsule
        inside_capsule = capsule.rect().contains(capsule.mapFromGlobal(point))
        modal_open = self.about_modal.isVisible()
        if kind == QEvent.Type.MouseButtonPress and self.settings.reset_state == 1:
            reset = self.action_dock.btn_reset
            if not reset.rect().contains(reset.mapFromGlobal(point)):
                self.settings.set_reset_state(0)
        if not modal_open and not getattr(self, "_forwarding_input", False) and (watched is self or watched is self.clock or self.clock.isAncestorOf(watched)):
            receiver = getattr(self, '_drawer_mouse_receiver', None)
            if kind == QEvent.Type.MouseButtonPress:
                receiver = None
                for edge in ('left','top','right'):
                    drawer = getattr(self, edge+'_drawer')
                    if getattr(self, edge+'_open'):
                        child = drawer.childAt(drawer.mapFromGlobal(point))
                        if isinstance(child,(NativePushButton,QCheckBox,QSlider,QComboBox)) and child.isEnabled():
                            receiver = child
                            break
                self._drawer_mouse_receiver = receiver
            if receiver is not None:
                from PyQt6.QtGui import QMouseEvent
                if kind == QEvent.Type.MouseButtonRelease:
                    self._drawer_mouse_receiver = None
                local = QPointF(receiver.mapFromGlobal(point))
                forwarded = QMouseEvent(kind, local, event.globalPosition(), event.button(), event.buttons(), event.modifiers())
                self._forwarding_input = True
                try:
                    QApplication.sendEvent(receiver, forwarded)
                finally:
                    self._forwarding_input = False
                return True
        if kind == QEvent.Type.MouseMove:
            if not modal_open:
                if inside_capsule:
                    capsule.expand()
                elif not capsule.rect().adjusted(-8,-8,8,8).contains(capsule.mapFromGlobal(point)):
                    capsule.collapse()
            return super().eventFilter(watched, event)
        if event.button() != Qt.MouseButton.LeftButton:
            return super().eventFilter(watched, event)
        targets = [self.btn_info]
        if not modal_open:
            targets.extend((self.action_dock.btn_reset, self.action_dock.btn_apply, self.action_dock.btn_exit))
            if capsule.stack.currentIndex() == 1:
                targets.extend(capsule.mode_buttons)
        target = next((button for button in targets if button.isEnabled() and button.isVisible()
                       and button.rect().contains(button.mapFromGlobal(point))
                       and (button not in capsule.mode_buttons or inside_capsule)), None)
        if target is None and inside_capsule and not modal_open:
            target = capsule
        if kind == QEvent.Type.MouseButtonPress:
            self._hud_pressed = target
            if target is not None:
                if isinstance(target, (NativePushButton, QCheckBox)):
                    target.setDown(True)
                return True
        else:
            pressed = getattr(self, '_hud_pressed', None)
            self._hud_pressed = None
            if pressed is not None:
                if isinstance(pressed, (NativePushButton, QCheckBox)):
                    pressed.setDown(False)
                if target is pressed:
                    if pressed is capsule:
                        capsule.expand()
                    else:
                        pressed.click()
                return True
        return super().eventFilter(watched, event)

    def refresh_frosted_panels(self):
        if self._closing:return
        for surface in (self.mode_capsule, self.action_dock):
            cache_frosted_backdrop(surface, self, surface.pos(), neutral=True)
        for opened,drawer,animation in ((self.left_open,self.left_drawer,self.anim_left),(self.top_open,self.top_drawer,self.anim_top),(self.right_open,self.right_drawer,self.anim_right)):
            if opened:
                # A debounced refresh during the slide must sample the final panel
                # location, not its temporary off-screen animation position.
                position = animation.endValue() if animation.state()==QPropertyAnimation.State.Running else drawer.pos()
                cache_frosted_backdrop(drawer,self,position)
        if self.about_modal.isVisible():cache_frosted_backdrop(self.about_modal,self,self.about_modal.pos())

    def _recenter_mode_capsule(self, w=None):
        if w is None:
            w = self.mode_capsule.width()
        sw = self.width()
        sh = self.height()
        bottom = sh - 32
        if (sw + self.mode_capsule._expanded_width)//2 + 8 > self.action_dock.x():
            bottom = self.action_dock.y() - 8
        self.mode_capsule.move((sw - w)//2, bottom - self.mode_capsule.height())
        if hasattr(self, 'backdrop_refresh'):
            self.backdrop_refresh.start(180)

    def on_studio_mode_changed(self, idx):
        self.settings.set_mode(idx)
        self.clock.clock_style = idx
        self.clock.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        sw, sh = self.width(), self.height()
        
        self.clock.setGeometry(0, 0, sw, sh)
        for drawer in (self.left_drawer, self.top_drawer, self.right_drawer):
            drawer.fit_content()
        
        self.btn_info.move(sw - self.btn_info.width() - 32, 32)
        self.btn_info.raise_()
        
        dock_w = self.action_dock.width()
        dock_h = self.action_dock.height()
        self.action_dock.move(sw - dock_w - 32, sh - dock_h - 32)
        self.action_dock.raise_()
        
        cw = self.mode_capsule.width()
        self._recenter_mode_capsule(cw)
        self.mode_capsule.raise_()
        
        self.left_grabber.move(0, (sh - self.left_grabber.height()) // 2)
        self.top_grabber.move((sw - self.top_grabber.width()) // 2, 0)
        self.right_grabber.move(sw - self.right_grabber.width(), (sh - self.right_grabber.height()) // 2)
        self.left_grabber.raise_()
        self.top_grabber.raise_()
        self.right_grabber.raise_()
        
        if hasattr(self, 'about_modal'):
            self.about_modal.move((sw - self.about_modal.width()) // 2, (sh - self.about_modal.height()) // 2)
            if self.about_modal.isVisible():
                self.about_modal.raise_()
        
        if self.left_open:
            self.left_drawer.move(24, (sh - self.left_drawer.height()) // 2)
        else:
            self.left_drawer.move(-self.left_drawer.width() - 20, (sh - self.left_drawer.height()) // 2)
            
        if self.top_open:
            self.top_drawer.move((sw - self.top_drawer.width()) // 2, 24)
        else:
            self.top_drawer.move((sw - self.top_drawer.width()) // 2, -self.top_drawer.height() - 20)
            
        if self.right_open:
            self.right_drawer.move(sw - self.right_drawer.width() - 24, (sh - self.right_drawer.height()) // 2)
        else:
            self.right_drawer.move(sw + 20, (sh - self.right_drawer.height()) // 2)
        self.action_dock.raise_()
        if hasattr(self,"backdrop_refresh"):self.backdrop_refresh.start(80)

    def set_left_drawer_open(self, open_state):
        if self.left_open == open_state:
            return
        if open_state:
            self.set_top_drawer_open(False)
            self.set_right_drawer_open(False)
            
        self.left_open = open_state
        sh = self.height()
        target_pos = QPoint(24, (sh - self.left_drawer.height()) // 2) if open_state else QPoint(-self.left_drawer.width() - 20, (sh - self.left_drawer.height()) // 2)
        
        if open_state:
            cache_frosted_backdrop(self.left_drawer,self,target_pos)
        self.anim_left.stop()
        self.anim_left.setStartValue(self.left_drawer.pos())
        self.anim_left.setEndValue(target_pos)
        self.anim_left.start()
        
        if open_state:
            self.left_drawer.raise_()
            self.action_dock.raise_()

    def set_top_drawer_open(self, open_state):
        if self.top_open == open_state:
            return
        if open_state:
            self.set_left_drawer_open(False)
            self.set_right_drawer_open(False)
            
        self.top_open = open_state
        sw = self.width()
        target_pos = QPoint((sw - self.top_drawer.width()) // 2, 24) if open_state else QPoint((sw - self.top_drawer.width()) // 2, -self.top_drawer.height() - 20)
        
        if open_state:
            cache_frosted_backdrop(self.top_drawer,self,target_pos)
        self.anim_top.stop()
        self.anim_top.setStartValue(self.top_drawer.pos())
        self.anim_top.setEndValue(target_pos)
        self.anim_top.start()
        
        if open_state:
            self.top_drawer.raise_()
            self.action_dock.raise_()

    def set_right_drawer_open(self, open_state):
        if self.right_open == open_state:
            return
        if open_state:
            self.set_left_drawer_open(False)
            self.set_top_drawer_open(False)
            
        self.right_open = open_state
        sw, sh = self.width(), self.height()
        target_pos = QPoint(sw - self.right_drawer.width() - 24, (sh - self.right_drawer.height()) // 2) if open_state else QPoint(sw + 20, (sh - self.right_drawer.height()) // 2)
        
        if open_state:
            cache_frosted_backdrop(self.right_drawer,self,target_pos)
        self.anim_right.stop()
        self.anim_right.setStartValue(self.right_drawer.pos())
        self.anim_right.setEndValue(target_pos)
        self.anim_right.start()
        
        if open_state:
            self.right_drawer.raise_()
            self.action_dock.raise_()

    def handle_canvas_mouse_move(self, event):
        pos = event.pos()
        sw = self.width()
        sh = self.height()
        if pos.x() <= 24:
            self.set_left_drawer_open(True)
        elif pos.y() <= 24:
            self.set_top_drawer_open(True)
        elif pos.x() >= sw - 24:
            self.set_right_drawer_open(True)

    def mouseMoveEvent(self, event):
        self.handle_canvas_mouse_move(event)
        super().mouseMoveEvent(event)

    def handle_canvas_mouse_press(self, event):
        pos = event.pos()
        if hasattr(self, 'about_modal') and self.about_modal.isVisible():
            if not self.about_modal.geometry().contains(pos):
                self.hide_about()
                return
        if self.left_open and not self.left_drawer.geometry().contains(pos):
            self.set_left_drawer_open(False)
        if self.top_open and not self.top_drawer.geometry().contains(pos):
            self.set_top_drawer_open(False)
        if self.right_open and not self.right_drawer.geometry().contains(pos):
            self.set_right_drawer_open(False)

    def mousePressEvent(self, event):
        pos = event.pos()
        if hasattr(self, 'about_modal') and self.about_modal.isVisible():
            if not self.about_modal.geometry().contains(pos):
                if self.btn_info.geometry().contains(pos):
                    super().mousePressEvent(event)
                    return
                self.hide_about()
                event.accept()
                return
        # If click hits floating HUD controls, let children handle it without interruption
        if (self.btn_info.geometry().contains(pos) or 
            self.action_dock.geometry().contains(pos) or 
            self.mode_capsule.geometry().contains(pos)):
            super().mousePressEvent(event)
            return

        if self.left_open and not self.left_drawer.geometry().contains(pos) and not self.left_grabber.geometry().contains(pos):
            self.set_left_drawer_open(False)
        if self.top_open and not self.top_drawer.geometry().contains(pos) and not self.top_grabber.geometry().contains(pos):
            self.set_top_drawer_open(False)
        if self.right_open and not self.right_drawer.geometry().contains(pos) and not self.right_grabber.geometry().contains(pos):
            self.set_right_drawer_open(False)
        super().mousePressEvent(event)

    def toggle_about(self):
        if hasattr(self, 'about_modal') and self.about_modal.isVisible():
            self.hide_about()
        else:
            self.show_about()

    def show_about(self):
        self.set_left_drawer_open(False)
        self.set_top_drawer_open(False)
        self.set_right_drawer_open(False)
        if hasattr(self, 'about_modal'):
            self.about_modal.show_modal()

    def hide_about(self):
        if hasattr(self, 'about_modal') and self.about_modal.isVisible():
            self.about_modal.hide_modal()

    def changeEvent(self, event):
        if event.type() == QEvent.Type.ActivationChange and self.isActiveWindow():
            if hasattr(self, 'clock') and self.clock:
                self.clock.update()
        super().changeEvent(event)

    def apply_clicked(self):
        self.settings.save_config()
        self.action_dock.btn_apply.setText("Saved")
        self.action_dock.btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #10B981;
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 15px;
                font-weight: 600;
                font-size: 11.5px;
                padding: 5px 18px;
            }
        """)
        self.apply_feedback_timer.start(1500)

    def restore_apply_button(self):
        if hasattr(self, 'action_dock'):
            self.action_dock.btn_apply.setText("Apply")
            self.action_dock.btn_apply.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.win_accent};
                    color: {self.contrast_text};
                    border: 1px solid rgba(255, 255, 255, 0.20);
                    border-radius: 15px;
                    font-weight: 600;
                    font-size: 11.5px;
                    padding: 5px 18px;
                }}
                QPushButton:hover {{
                    background-color: {self.hover_accent};
                }}
            """)
            polish_controls(self.action_dock,self.win_accent)

    def reset_defaults_clicked(self):
        self.settings.request_reset()
        self.settings.sync_studio_clock()
        self.mode_capsule.set_current_mode(self.clock.clock_style)

    def close_studio(self):
        if not self._closing:
            self.close()

    def closeEvent(self, event):
        if self._closing:
            event.accept()
            return
        self._closing = True
        QApplication.instance().removeEventFilter(self)
        self.backdrop_refresh.stop()
        self.apply_feedback_timer.stop()
        for animation in (self.anim_left, self.anim_top, self.anim_right):
            animation.stop()
        self.clock.anim_timer.stop()
        self.clock.sync_timer.stop()
        if self.mode_capsule._anim_group is not None:
            self.mode_capsule._anim_group.stop()
        self.setUpdatesEnabled(False)
        self.hide()
        self.settings.restore_cards()
        self.settings.studio = None
        self.settings.show()
        self.settings.raise_()
        self.settings.activateWindow()
        self.settings.btn_fullscreen.setFocus()
        event.accept()

    def keyPressEvent(self, event):
        if hasattr(self, 'about_modal') and self.about_modal.isVisible():
            if event.key() in (Qt.Key.Key_Escape, Qt.Key.Key_Return, Qt.Key.Key_Space):
                self.hide_about()
                event.accept()
                return
        if event.key() == Qt.Key.Key_Space:
            new_val = not self.clock.show_bg
            self.clock.show_bg = new_val
            self.clock.update()
            self.settings.ambient_cb.setChecked(new_val)
            event.accept()
            return
        elif event.key() in (Qt.Key.Key_Escape, Qt.Key.Key_F11):
            if self.left_open or self.top_open or self.right_open:
                self.set_left_drawer_open(False)
                self.set_top_drawer_open(False)
                self.set_right_drawer_open(False)
                event.accept()
                return
            self.close_studio()
            event.accept()
            return
        elif event.key() == Qt.Key.Key_Z and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.close_studio()
            event.accept()
            return
        super().keyPressEvent(event)


class SettingsDialog(QDialog):
    def __init__(self, config_path):
        super().__init__()
        load_ui_font()
        self.setWindowTitle("Dinoscreener Settings")
        self.setFixedSize(680, 760)
        self.setAcceptDrops(True)
        
        # Subpixel ClearType Antialiased Font Hierarchy
        ui_font = QFont(["Google Sans Flex", "Segoe UI Emoji", "Arial", "sans-serif"])
        ui_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
        ui_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
        self.setFont(ui_font)
        
        # Load Application Icon
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
        if getattr(sys, 'frozen', False):
            logo_path = os.path.join(sys._MEIPASS, "app_icon.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(os.path.join(os.path.dirname(logo_path), "app_icon_taskbar.png")))
        self.logo_path = logo_path
        
        # Windows 11 DWM Mica / Glass Blur Backdrop Setup
        self.is_dwm_active = apply_windows_dwm_effects(self)
        QTimer.singleShot(0, lambda: apply_windows_dwm_effects(self))

        self.win_accent = "#D0D0D0"
        self.contrast_text, self.hover_accent, self.press_accent = get_color_variants(self.win_accent)
        check_icon_path = get_or_create_check_icon(self.contrast_text)
        chevron_icon_path = get_or_create_chevron_icon()

        bg_dialog = "rgba(18, 18, 18, 0.34)" if self.is_dwm_active else "#121212"
        bg_card = "rgba(26, 26, 26, 0.50)" if self.is_dwm_active else "#1A1A1A"

        # Spatial Studio Modern Glass Stylesheet (DWM Mica / Glass Blur with clean solid fallback)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg_dialog};
            }}
            QLabel {{
                background: transparent;
                color: #FFFFFF;
                font-family: 'Google Sans Flex', 'Google Sans Flex', -apple-system, sans-serif;
            }}
            QFrame {{
                background: transparent;
            }}
            QFrame#bentoCard {{
                background: {bg_card};
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 14px;
            }}
            QFrame#previewCard {{
                background: #000000;
                border: none;
                border-radius: 12px;
            }}
            /* Fluent Checkbox with Windows Accent Color & Rounded Indicator */
            QCheckBox {{
                color: #D2D2D2;
                font-family: 'Google Sans Flex', 'Google Sans Flex', sans-serif;
                font-size: 11.5px;
                spacing: 8px;
                background: transparent;
            }}
            QCheckBox:focus {{ color: #FFFFFF; }}
            QCheckBox::indicator:focus {{ border: 2px solid #FFFFFF; }}
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
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 9px;
            }}
            /* Comboboxes - Smooth Rounded Pill Style with Visible Chevron Arrow */
            QComboBox, QFontComboBox {{
                background: rgba(255, 255, 255, 0.06);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 12px;
                padding: 4px 10px;
                font-family: 'Google Sans Flex', 'Google Sans Flex', sans-serif;
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
                background: #242424;
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
        self.reset_state = 0
        self.reset_dismiss_filter = ResetDismissFilter(self)
        QApplication.instance().installEventFilter(self.reset_dismiss_filter)
        for switch in self.findChildren(VectorCheckBox):
            switch.toggled.connect(lambda checked: self.set_reset_state(0))
        polish_controls(self, self.win_accent)
        self.setObjectName('settingsRoot')
        self.setStyleSheet(self.styleSheet() + ' QToolTip { background: #292929; color: #F2F2F2; border: 1px solid #606060; padding: 7px; font: 11px "Google Sans Flex"; }')
        self.layout().activate()
        desired = self.size().expandedTo(self.layout().minimumSize())
        screen = self.screen().availableGeometry()
        if desired.height() > screen.height()-80:
            content = QWidget()
            content.setObjectName('settingsContent')
            content.setStyleSheet('QWidget#settingsContent { background: transparent; }')
            content.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            content.setLayout(self.layout())
            content.setMinimumSize(desired)
            self.settings_scroll = QScrollArea(self)
            self.settings_scroll.setWidgetResizable(True)
            self.settings_scroll.setFrameShape(QFrame.Shape.NoFrame)
            self.settings_scroll.setStyleSheet('QScrollArea { background: transparent; border: none; }')
            self.settings_scroll.viewport().setAutoFillBackground(False)
            self.settings_scroll.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
            self.settings_scroll.setWidget(content)
            outer = QVBoxLayout(self)
            outer.setContentsMargins(0,0,0,0)
            outer.addWidget(self.settings_scroll)
            self.setFixedSize(desired.width()+18, max(400,screen.height()-80))
        else:
            self.setFixedSize(desired)
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

    def showEvent(self, event):
        super().showEvent(event)
        if not hasattr(self, 'settings_scroll'):
            self.layout().activate()
            self.setFixedSize(self.size().expandedTo(self.layout().minimumSize()))

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
            "accent_color": get_windows_accent_color(),
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
                    if loaded.get("accent_color") in ["#0078D4", "#8F96BF", "#A5A9DE", "#a5a9de", "#D0D0D0", get_windows_accent_color(), None]:
                        loaded["accent_color"] = get_windows_accent_color()
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
        
        dir_name = os.path.dirname(self.config_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

    def save_settings(self):
        self.save_config()
        self.accept()
        QApplication.quit()

    def closeEvent(self, event):
        if hasattr(self, 'studio') and self.studio:
            try:
                self.studio.close()
            except Exception:
                pass
        QApplication.quit()
        super().closeEvent(event)

    def reject(self):
        if hasattr(self, 'studio') and self.studio:
            try:
                self.studio.close()
            except Exception:
                pass
        QApplication.quit()
        super().reject()

    def restore_cards(self):
        if not hasattr(self, 'cards_row'):return
        owner = self.cards_row.parentWidget()
        owner.setUpdatesEnabled(False)
        try:
            for index,card in enumerate((self.card_mode,self.card_disp,self.card_sys)):
                # Explicitly release scroll ownership before reparenting; layout
                # membership alone does not guarantee a valid on-screen geometry.
                parent = card.parentWidget()
                if parent and isinstance(parent.parentWidget(),QScrollArea):
                    parent.parentWidget().takeWidget()
                self.cards_row.removeWidget(card)
                card.hide();card.setParent(owner)
                self.cards_row.insertWidget(index,card,stretch=1)
                card.show();card.updateGeometry()
            self.cards_row.invalidate()
            owner.layout().invalidate()
            owner.layout().activate()
        finally:
            owner.setUpdatesEnabled(True)
            owner.update()
        self.preview.last_frame_time = time.perf_counter()
        self.preview.checkTime()
        self.preview.anim_timer.start(self.preview.target_frame_interval)
        self.preview.sync_timer.start(200)

    def update_strict_exit(self, state=None):
        self.preview.strict_exit = self.strict_cb.isChecked()
        self.sync_studio_clock()

    def update_ignore_media(self, state=None):
        self.preview.ignore_media_keys = self.ignore_media_cb.isChecked()
        self.sync_studio_clock()

    def update_enable_win_key(self, state=None):
        self.preview.enable_win_key = self.win_cb.isChecked()
        self.sync_studio_clock()

    def _get_active_dialog_parent(self):
        try:
            if hasattr(self, 'studio') and self.studio and self.studio.isVisible():
                return self.studio
        except (RuntimeError, AttributeError):
            self.studio = None
        except Exception:
            pass
        return self

    def sync_studio_clock(self):
        try:
            if hasattr(self, 'studio') and self.studio:
                if not self.studio.isVisible():
                    return
                c = getattr(self.studio, 'clock', None)
                if not c:
                    return
                p = self.preview
                c.clock_style = p.clock_style
                c.clock_scales = dict(p.clock_scales)
                c.leading_zeros = dict(p.leading_zeros)
                c.rotary_accent = p.rotary_accent
                c.show_bg = p.show_bg
                c.brightness = p.brightness
                c.use_24hr = p.use_24hr
                c.show_weather = p.show_weather
                c.show_battery = p.show_battery
                c.use_fahrenheit = p.use_fahrenheit
                c.pixel_shift = p.pixel_shift
                c.strict_exit = getattr(p, 'strict_exit', False)
                c.ignore_media_keys = getattr(p, 'ignore_media_keys', False)
                c.enable_win_key = getattr(p, 'enable_win_key', False)
                c.hourly_chime = p.hourly_chime
                c.chime_preset = getattr(p, 'chime_preset', 'acoustic_bell')
                c.chime_volume = getattr(p, 'chime_volume', 45)
                c.custom_chime_path = getattr(p, 'custom_chime_path', '')
                c.primary_font = getattr(p, 'primary_font', '')
                c.primary_font_family = getattr(p, 'primary_font_family', '')
                c.dino_font = getattr(p, 'dino_font', 'Bungee')
                c.character_type = getattr(p, 'character_type', 'dino')
                c.custom_character_image = getattr(p, 'custom_character_image', '')
                if hasattr(p, 'custom_char_pixmap') and p.custom_char_pixmap and not p.custom_char_pixmap.isNull():
                    # QPixmap sharing avoids reopening the sprite on every slider tick.
                    c.custom_char_pixmap = p.custom_char_pixmap
                elif c.character_type == "custom" and c.custom_character_image and c.custom_char_pixmap.isNull():
                    c.set_custom_character(c.custom_character_image)
                c.anim_timer.setInterval(c.target_frame_interval)
                c.update()
                self.studio.backdrop_refresh.start(80)
        except (RuntimeError, AttributeError):
            self.studio = None
        except Exception:
            pass

    def test_fullscreen(self):
        try:
            self.studio = FullscreenStudioMode(self)
            self.preview.anim_timer.stop()
            self.preview.sync_timer.stop()
            self.hide()
            self.set_reset_state(self.reset_state)
            self.studio.showFullScreen()
            self.studio.raise_()
            self.studio.activateWindow()
            if sys.platform == "win32":
                try:
                    import ctypes
                    ctypes.windll.user32.SetForegroundWindow(int(self.studio.winId()))
                except Exception:
                    pass
        except Exception as e:
            self.show()
            import traceback
            traceback.print_exc()
            print("Error launching fullscreen studio mode:", e)

    def set_reset_state(self, state):
        self.reset_state = state
        buttons = [self.reset_button]
        studio = getattr(self, 'studio', None)
        if studio and hasattr(studio, 'action_dock'):
            buttons.append(studio.action_dock.btn_reset)
        for button in buttons:
            button.setText(('Reset Defaults','Are you Sure?','Resetted!')[state])
            button.setProperty('resetState', state)
            button._bevel_key = None
            button.update()

    def request_reset(self):
        if self.reset_state == 0:
            self.set_reset_state(1)
        elif self.reset_state == 1:
            self.reset_defaults()
            self.set_reset_state(2)

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
        self.set_accent_color(get_windows_accent_color())
        self.set_mode(0)

    def on_preview_scale_scrolled(self, val):
        if hasattr(self, 'scale_slider'):
            self.scale_slider.blockSignals(True)
            self.scale_slider.setValue(val)
            self.scale_slider.blockSignals(False)
            self.lbl_scale_pct.setText(f"{val}%")

    def initUI(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(20, 20, 20, 20)
        root_layout.setSpacing(12)
        
        # 1. TOP HEADER (App Branding with Logo on the left)
        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)
        
        lbl_logo = QLabel()
        lbl_logo.setFixedSize(38, 38)
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setStyleSheet("background: transparent; border: none; padding: 0px;")
        if hasattr(self, 'logo_path') and os.path.exists(self.logo_path):
            lbl_logo.setPixmap(get_rounded_pixmap(self.logo_path, size=38, radius=9, dpr=lbl_logo.devicePixelRatioF()))
        header_row.addWidget(lbl_logo, alignment=Qt.AlignmentFlag.AlignVCenter)
        
        brand_box = QVBoxLayout()
        brand_box.setSpacing(1)
        lbl_app_name = QLabel("Dinoscreener")
        lbl_app_name.setStyleSheet("font-size: 15px; font-weight: 700; color: #FFFFFF; letter-spacing: -0.2px;")
        lbl_app_sub = QLabel("Screensaver Settings :)")
        lbl_app_sub.setStyleSheet("font-size: 11px; color: #A8A8A8;")
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
        self.stage_frame.setFixedSize(576, 331)
        stage_layout = QVBoxLayout(self.stage_frame)
        stage_layout.setContentsMargins(8, 8, 8, 8)
        
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
        self.preview.setFixedSize(560, 315) # Exact 16:9 widescreen ratio
        self.preview_card.setFixedSize(560, 315)
        preview_shape = QPainterPath()
        preview_shape.addRoundedRect(QRectF(0, 0, 560, 315), 12, 12)
        self.preview_card.setMask(QRegion(preview_shape.toFillPolygon().toPolygon()))
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
        self.mode_capsule.pin_open = False
        capsule_slot = QWidget()
        capsule_slot.setFixedSize(self.mode_capsule._expanded_width, 38)
        self.mode_capsule.setParent(capsule_slot)
        self.mode_capsule.on_width_changed = lambda width: self.mode_capsule.move((capsule_slot.width()-width)//2, 0)
        self.mode_capsule.on_width_changed(self.mode_capsule.width())
        self.mode_buttons = self.mode_capsule.mode_buttons
        
        capsule_row.addWidget(capsule_slot)
        capsule_row.addStretch()
        root_layout.addLayout(capsule_row)
        
        # 4. THREE BALANCED SPATIAL BENTO CARDS (Rounded 14px)
        self.cards_row = QHBoxLayout()
        self.cards_row.setSpacing(12)
        self.cards_row.setContentsMargins(0, 0, 0, 0)
        cards_row = self.cards_row
        
        # === CARD 1: Mode Parameters ===
        self.card_mode = QFrame()
        self.card_mode.setObjectName("bentoCard")
        card_mode = self.card_mode
        card_mode_layout = QVBoxLayout(self.card_mode)
        card_mode_layout.setContentsMargins(12, 12, 12, 12)
        card_mode_layout.setSpacing(5)
        
        self.lbl_mode_title = QLabel("Flip Clock")
        self.lbl_mode_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #FFFFFF;")
        card_mode_layout.addWidget(self.lbl_mode_title)
        
        self.pages = QStackedWidget()
        
        # --- Page 0: Flip Clock ---
        page_flip = QWidget()
        flip_layout = QVBoxLayout(page_flip)
        flip_layout.setContentsMargins(0, 2, 0, 0)
        flip_layout.setSpacing(5)
        
        scale_header = QHBoxLayout()
        lbl_scale_title = QLabel("Clock Scale")
        lbl_scale_title.setStyleSheet("color: #E6E6E6; font-size: 11.5px; font-weight: 500;")
        init_scale = int(self.preview.clock_scales.get(str(self.preview.clock_style), 0.45) * 100)
        self.lbl_scale_pct = QLabel(f"{init_scale}%")
        self.lbl_scale_pct.setStyleSheet(f"color: {self.win_accent}; font-size: 12px; font-weight: 600;")
        scale_header.addWidget(lbl_scale_title)
        scale_header.addStretch()
        scale_header.addWidget(self.lbl_scale_pct)
        self.scale_controls = QWidget()
        scale_controls_layout = QVBoxLayout(self.scale_controls)
        scale_controls_layout.setContentsMargins(0,0,0,0)
        scale_controls_layout.setSpacing(5)
        card_mode_layout.addWidget(self.scale_controls)
        self.scale_controls.setVisible(self.preview.clock_style != 1)
        scale_controls_layout.addLayout(scale_header)
        
        scale_box = QHBoxLayout()
        scale_box.setSpacing(6)
        
        undo_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.06);
                color: #A8A8A8;
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
                color: #D2D2D2;
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
        
        self.scale_slider = StudioSlider(Qt.Orientation.Horizontal)
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
        scale_controls_layout.addLayout(scale_box)

        # --- Hourly Bell Chime & Audio Customization ---
        self.chime_group = QWidget()
        chime_policy = self.chime_group.sizePolicy()
        chime_policy.setRetainSizeWhenHidden(True)
        self.chime_group.setSizePolicy(chime_policy)
        chime_layout = QVBoxLayout(self.chime_group)
        chime_layout.setContentsMargins(0, 8, 0, 0)
        chime_layout.setSpacing(4)
        chime_row = QHBoxLayout()
        chime_row.setContentsMargins(0, 4, 0, 0)
        chime_row.setSpacing(6)
        self.hourly_chime_cb = VectorCheckBox("Hourly Chime")
        self.hourly_chime_cb.setChecked(self.config.get("hourly_chime", False))
        self.hourly_chime_cb.setToolTip("Plays a chime every hour on the hour")
        self.hourly_chime_cb.stateChanged.connect(self.on_hourly_chime_changed)
        chime_row.addWidget(self.hourly_chime_cb)
        
        self.btn_test_chime = QPushButton("Test")
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
        chime_layout.addLayout(chime_row)

        sound_box = QHBoxLayout()
        sound_box.setSpacing(5)
        self.sound_caption = lbl_sound = QLabel("Sound:")
        lbl_sound.setFixedWidth(38)
        lbl_sound.setStyleSheet("color: #E6E6E6; font-size: 11px; font-weight: 500;")
        sound_box.addWidget(lbl_sound)

        self.chime_sound_cb = QComboBox()
        self.chime_sound_cb.setMinimumContentsLength(12)
        self.chime_sound_cb.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.chime_sound_cb.setToolTip("Select chime tone or drop custom audio file")
        self.refresh_chime_combobox()
        self.chime_sound_cb.currentIndexChanged.connect(self.on_chime_preset_changed)
        sound_box.addWidget(self.chime_sound_cb, stretch=1)

        self.btn_browse_sound = QPushButton("…")
        self.btn_browse_sound.setFixedSize(22, 22)
        self.btn_browse_sound.setStyleSheet(undo_style)
        self.btn_browse_sound.setToolTip("Browse or drop custom audio (.wav, .mp3, .ogg)")
        self.btn_browse_sound.clicked.connect(self.browse_custom_sound)
        sound_box.addWidget(self.btn_browse_sound)
        chime_layout.addLayout(sound_box)

        vol_box = QHBoxLayout()
        vol_box.setSpacing(6)
        self.vol_caption = lbl_vol = QLabel("Vol:")
        lbl_vol.setFixedWidth(38)
        lbl_vol.setStyleSheet("color: #E6E6E6; font-size: 11px; font-weight: 500;")
        vol_box.addWidget(lbl_vol)

        init_vol = self.config.get("chime_volume", 45)
        self.chime_vol_slider = StudioSlider(Qt.Orientation.Horizontal)
        self.chime_vol_slider.setRange(5, 100)
        self.chime_vol_slider.setValue(init_vol)
        self.chime_vol_slider.setToolTip("Adjust chime playback volume")
        self.chime_vol_slider.valueChanged.connect(self.on_chime_volume_changed)
        vol_box.addWidget(self.chime_vol_slider, stretch=1)

        self.lbl_chime_vol = QLabel(f"{init_vol}%")
        self.lbl_chime_vol.setStyleSheet(f"color: {self.win_accent}; font-size: 11px; font-weight: 600; min-width: 28px;")
        vol_box.addWidget(self.lbl_chime_vol)
        chime_layout.addLayout(vol_box)

        lbl_chime_tip = QLabel("Drop any audio file to use your own chime")
        lbl_chime_tip.setStyleSheet("color: #858585; font-size: 9.5px;")
        chime_layout.addWidget(lbl_chime_tip)
        lbl_chime_tip.setWordWrap(True)

        flip_layout.addStretch()
        self.pages.addWidget(page_flip)
        
        # --- Page 1: Rotary Clock ---
        page_rotary = QWidget()
        rot_layout = QVBoxLayout(page_rotary)
        rot_layout.setContentsMargins(0, 2, 0, 0)
        rot_layout.setSpacing(5)
        
        accent_box = QHBoxLayout()
        accent_box.setSpacing(5)
        lbl_dial = QLabel("Accent:")
        lbl_dial.setStyleSheet("color: #E6E6E6; font-size: 11.5px; font-weight: 500;")
        accent_box.addWidget(lbl_dial)
        
        self.swatch_buttons = []
        raw_presets = [get_windows_accent_color(), "#0078D4", "#60CDFF", "#10B981", "#F59E0B"]
        seen = set()
        preset_colors = []
        for c in raw_presets:
            cu = c.upper()
            if cu not in seen:
                seen.add(cu)
                preset_colors.append(c)
        preset_colors = preset_colors[:5]
        
        for c in preset_colors:
            s_btn = ColorSwatch(c)
            s_btn.setFixedSize(26, 26)
            s_btn.setAccessibleName(f"Accent color {c}")
            s_btn.setToolTip(f"Accent color {c}")
            s_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            s_btn.clicked.connect(lambda checked, col=c: self.set_accent_color(col))
            accent_box.addWidget(s_btn)
            self.swatch_buttons.append((c, s_btn))
            
        btn_custom = QPushButton("Custom...")
        btn_custom.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_custom.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.06);
                color: #D2D2D2;
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
        
        self.show_weather_cb = VectorCheckBox("Show Weather")
        self.show_weather_cb.setChecked(self.config.get("show_weather", self.config.get("show_info", True)))
        self.show_weather_cb.stateChanged.connect(self.update_rotary_telemetry)
        rot_layout.addWidget(self.show_weather_cb)
        
        self.show_battery_cb = VectorCheckBox("Show Battery")
        self.show_battery_cb.setChecked(self.config.get("show_battery", self.config.get("show_info", True)))
        self.show_battery_cb.stateChanged.connect(self.update_rotary_telemetry)
        rot_layout.addWidget(self.show_battery_cb)
        
        self.fahrenheit_cb = VectorCheckBox("Fahrenheit Format (°F)")
        self.fahrenheit_cb.setChecked(self.config.get("use_fahrenheit", self.config.get("live_weather", False)))
        self.fahrenheit_cb.setToolTip("Toggle temperature display between Celsius (°C) and Fahrenheit (°F)")
        self.fahrenheit_cb.stateChanged.connect(self.update_rotary_telemetry)
        self.fahrenheit_cb.hide()
        self.temperature_row = QWidget()
        temperature_layout = QHBoxLayout(self.temperature_row)
        temperature_layout.setContentsMargins(0, 0, 0, 0)
        temperature_layout.addWidget(QLabel("Temperature unit"))
        self.temperature_unit = QComboBox()
        self.temperature_unit.addItems(["°C", "°F"])
        self.temperature_unit.setCurrentIndex(1 if self.fahrenheit_cb.isChecked() else 0)
        self.temperature_unit.currentIndexChanged.connect(lambda index: self.fahrenheit_cb.setChecked(index == 1))
        self.fahrenheit_cb.toggled.connect(lambda checked: self.temperature_unit.setCurrentIndex(int(checked)))
        temperature_layout.addWidget(self.temperature_unit)
        rot_layout.insertWidget(rot_layout.indexOf(self.show_weather_cb)+1, self.temperature_row)
        self.temperature_row.setEnabled(self.show_weather_cb.isChecked())
        self.show_weather_cb.toggled.connect(self.temperature_row.setEnabled)
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
                color: #A8A8A8;
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
        lbl_dino_font.setStyleSheet("color: #E6E6E6; font-size: 11px; font-weight: 500;")
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
        lbl_sprite.setStyleSheet("color: #E6E6E6; font-size: 11px; font-weight: 500;")
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
        lbl_dino_tip.setWordWrap(True)
        lbl_dino_tip.setStyleSheet("color: #858585; font-size: 10px;")
        dino_layout.addWidget(lbl_dino_tip)
        dino_layout.addStretch()
        self.pages.addWidget(page_dino)
        
        card_mode_layout.addWidget(self.pages)
        cards_row.addWidget(card_mode, stretch=1)
        
        # === CARD 2: Display & Atmosphere ===
        self.card_disp = QFrame()
        self.card_disp.setObjectName("bentoCard")
        card_disp = self.card_disp
        card_disp_layout = QVBoxLayout(self.card_disp)
        card_disp_layout.setContentsMargins(12, 12, 12, 12)
        card_disp_layout.setSpacing(5)
        
        lbl_disp_title = QLabel("Appearance")
        lbl_disp_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #FFFFFF;")
        card_disp_layout.addWidget(lbl_disp_title)
        
        # Huge Tactile Brightness Bar
        bright_header = QHBoxLayout()
        lbl_bright_title = QLabel("Brightness")
        lbl_bright_title.setStyleSheet("color: #E6E6E6; font-size: 11.5px; font-weight: 500;")
        self.bright_val_label = QLabel(f"{self.config.get('brightness', 100)}%")
        self.bright_val_label.setStyleSheet(f"color: {self.win_accent}; font-size: 12px; font-weight: 600;")
        bright_header.addWidget(lbl_bright_title)
        bright_header.addStretch()
        bright_header.addWidget(self.bright_val_label)
        card_disp_layout.addLayout(bright_header)
        
        bright_box = QHBoxLayout()
        bright_box.setSpacing(6)
        lbl_sun1 = QLabel("☼")
        lbl_sun1.setStyleSheet("color: #858585; font-size: 13px;")
        lbl_sun2 = QLabel("☀")
        lbl_sun2.setStyleSheet("color: #A8A8A8; font-size: 15px;")
        
        self.bright_slider = StudioSlider(Qt.Orientation.Horizontal)
        self.bright_slider.setRange(10, 100)
        self.bright_slider.setValue(self.config.get("brightness", 100))
        self.bright_slider.valueChanged.connect(self.update_brightness)
        bright_box.addWidget(lbl_sun1)
        bright_box.addWidget(self.bright_slider, stretch=1)
        bright_box.addWidget(lbl_sun2)
        card_disp_layout.addLayout(bright_box)
        
        # Display Toggles
        self.ambient_cb = VectorCheckBox("Ambient Mode (Space)")
        self.ambient_cb.setChecked(self.config.get("ambient_mode", self.preview.show_bg))
        self.ambient_cb.setToolTip("Soft ambient glow behind clock (press Spacebar anytime)")
        self.ambient_cb.stateChanged.connect(self.on_ambient_cb_changed)
        card_disp_layout.addWidget(self.ambient_cb)

        self.pixel_shift_cb = VectorCheckBox("Burn-in protection")
        self.pixel_shift_cb.setChecked(self.config.get("pixel_shift", False))
        self.pixel_shift_cb.setToolTip("Subtle orbital shift so OLED screens don't get burn-in")
        self.pixel_shift_cb.stateChanged.connect(self.update_pixel_shift)
        card_disp_layout.addWidget(self.pixel_shift_cb)

        self.use_24hr_cb = VectorCheckBox("24-Hour Format")
        self.use_24hr_cb.setChecked(self.config.get("use_24hr", False))
        self.use_24hr_cb.stateChanged.connect(self.update_24hr)
        card_mode_layout.insertWidget(1, self.use_24hr_cb)
        
        self.leading_zero_cb = VectorCheckBox("Leading Zeros")
        self.leading_zero_cb.setChecked(self.preview.leading_zeros.get(str(start_style), False))
        self.leading_zero_cb.stateChanged.connect(self.update_leading_zero)
        card_mode_layout.insertWidget(2, self.leading_zero_cb)
        card_disp_layout.addStretch()
        cards_row.addWidget(card_disp, stretch=1)
        
        # === CARD 3: System & Security ===
        self.card_sys = QFrame()
        self.card_sys.setObjectName("bentoCard")
        card_sys = self.card_sys
        card_sys_layout = QVBoxLayout(self.card_sys)
        card_sys_layout.setContentsMargins(12, 12, 12, 12)
        card_sys_layout.setSpacing(5)
        
        lbl_sys_title = QLabel("Behavior")
        lbl_sys_title.setStyleSheet("font-size: 13px; font-weight: 600; color: #FFFFFF;")
        card_sys_layout.addWidget(lbl_sys_title)
        
        self.strict_cb = LockExitSwitch("Lock on exit (Ctrl+Z)")
        self.strict_cb.setToolTip("Require Ctrl+Z to exit the screensaver")
        self.strict_cb.setChecked(self.config.get("strict_exit", False))
        self.strict_cb.setToolTip("Requires pressing Ctrl+Z to dismiss the screensaver")
        self.strict_cb.toggled.connect(self.update_strict_exit)
        card_sys_layout.addWidget(self.strict_cb)
        
        self.ignore_media_cb = VectorCheckBox("Ignore Media Keys")
        self.ignore_media_cb.setChecked(self.config.get("ignore_media_keys", False))
        self.ignore_media_cb.setToolTip("Volume and track keys won't close screensaver")
        self.ignore_media_cb.stateChanged.connect(self.update_ignore_media)
        card_sys_layout.addWidget(self.ignore_media_cb)
        
        self.win_cb = VectorCheckBox("Allow Windows key")
        self.win_cb.setChecked(self.config.get("enable_win_key", False))
        self.win_cb.setToolTip("Use Windows key without waking screensaver")
        self.win_cb.stateChanged.connect(self.update_enable_win_key)
        card_sys_layout.addWidget(self.win_cb)
        card_sys_layout.addWidget(self.chime_group)
        self.chime_group.show()
        self.refresh_chime_enabled()
        card_sys_layout.addStretch()
        cards_row.addWidget(card_sys, stretch=1)
        
        root_layout.addLayout(cards_row)
        
        # 5. FOOTER ACTIONS (Pill Rounded)
        footer_row = QHBoxLayout()
        footer_row.setContentsMargins(0, 0, 0, 0)
        
        self.btn_fullscreen = QPushButton()
        self.btn_fullscreen.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_fullscreen.setIcon(get_or_create_fullscreen_duotone_icon(self.win_accent))
        self.btn_fullscreen.setIconSize(QSize(20, 20))
        self.btn_fullscreen.setFixedSize(116, 34)
        self.btn_fullscreen.setText("Studio")
        self.btn_fullscreen.setAccessibleName("Open fullscreen Studio")
        self.btn_fullscreen.setToolTip("Edit settings in fullscreen Studio")
        self.btn_fullscreen.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
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
                color: #A8A8A8;
                border: none;
                border-radius: 14px;
                padding: 7px 14px;
                font-size: 12px;
                font-family: 'Google Sans Flex', 'Google Sans Flex', sans-serif;
            }
            QPushButton:hover {
                color: #F87171;
            }
        """)
        self.reset_button = btn_reset
        btn_reset.clicked.connect(self.request_reset)
        footer_row.addWidget(btn_reset)
        
        btn_apply = QPushButton("Apply")
        btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_apply.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.win_accent};
                color: {self.contrast_text};
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                padding: 7px 32px;
                font-size: 12px;
                font-weight: 600;
                font-family: 'Google Sans Flex', 'Google Sans Flex', sans-serif;
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
        self.preview.anim_timer.setInterval(self.preview.target_frame_interval)
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
        self.scale_controls.setVisible(idx != 1)
        self.on_preview_scale_scrolled(round(self.preview.clock_scales.get(str(idx), 0.45)*100))
        titles = ["Flip Clock", "Rotary Clock", "Dino Runner"]
        if idx < len(titles):
            self.lbl_mode_title.setText(titles[idx])
        self.update_swatch_highlights()
        if hasattr(self, 'leading_zero_cb'):
            self.leading_zero_cb.blockSignals(True)
            self.leading_zero_cb.setChecked(self.preview.leading_zeros.get(str(idx), False))
            self.leading_zero_cb.blockSignals(False)
        self.sync_studio_clock()
        if hasattr(self, 'studio') and self.studio:
            try:
                if self.studio.isVisible():
                    if hasattr(self.studio, 'mode_capsule') and self.studio.mode_capsule:
                        self.studio.mode_capsule.set_current_mode(idx)
                    if hasattr(self.studio, 'clock') and self.studio.clock:
                        self.studio.clock.clock_style = idx
                        self.studio.clock.update()
            except (RuntimeError, AttributeError):
                self.studio = None
            except Exception:
                pass
        self.update()

    def update_swatch_highlights(self):
        if not hasattr(self, 'swatch_buttons'):
            return
        curr = self.config.get("accent_color", self.win_accent).upper()
        for hex_code, btn in self.swatch_buttons:
            btn.setChecked(hex_code.upper() == curr)
            btn.update()

    def set_accent_color(self, hex_code):
        self.config["accent_color"] = hex_code
        self.preview.set_accent_color(hex_code)
        if hasattr(self, 'stage_frame'):
            self.stage_frame.set_stage_theme(self.preview.clock_style, hex_code)
        self.sync_studio_clock()
        if hasattr(self, 'mode_capsule'):
            self.mode_capsule.update_accent(hex_code)
        if hasattr(self, 'btn_fullscreen'):
            self.btn_fullscreen.setIcon(get_or_create_fullscreen_duotone_icon(hex_code))
        if hasattr(self, 'btn_info'):
            self.btn_info.setIcon(get_or_create_info_duotone_icon(hex_code))
        self.update_swatch_highlights()


    def pick_color(self):
        parent = self._get_active_dialog_parent()
        color = QColorDialog.getColor(QColor(self.config.get("accent_color", self.win_accent)), parent, "Select Accent Color")
        if color.isValid():
            self.set_accent_color(color.name())

    def update_scale(self, val):
        self.lbl_scale_pct.setText(f"{val}%")
        key = str(self.preview.clock_style)
        self.preview.clock_scales[key] = val / 100.0
        self.config["clock_scales"][key] = val / 100.0
        self.preview.update()
        self.sync_studio_clock()

    def step_scale(self, delta):
        if hasattr(self, 'scale_slider'):
            new_val = max(15, min(95, self.scale_slider.value() + delta))
            self.scale_slider.setValue(new_val)

    def on_ambient_cb_changed(self, state=None):
        val = self.ambient_cb.isChecked()
        self.preview.show_bg = val
        self.preview.anim_timer.setInterval(self.preview.target_frame_interval)
        self.config["ambient_mode"] = val
        self.preview.update()
        self.sync_studio_clock()

    def refresh_chime_enabled(self):
        enabled = self.hourly_chime_cb.isChecked()
        for label in (self.sound_caption, self.vol_caption, self.lbl_chime_vol):
            label.setStyleSheet("color: " + ("#E6E6E6" if enabled else "#858585") + "; font-size: 11px;")
        for control in (self.btn_test_chime, self.chime_sound_cb, self.btn_browse_sound,
                        self.chime_vol_slider, self.lbl_chime_vol):
            control.setEnabled(enabled)

    def on_hourly_chime_changed(self, state=None):
        self.refresh_chime_enabled()
        val = self.hourly_chime_cb.isChecked()
        self.preview.hourly_chime = val
        self.config["hourly_chime"] = val
        self.sync_studio_clock()

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
        self.sync_studio_clock()

    def on_chime_volume_changed(self, val):
        self.lbl_chime_vol.setText(f"{val}%")
        self.config["chime_volume"] = val
        self.preview.chime_volume = val
        self.sync_studio_clock()

    def test_chime_sound(self):
        preset = self.chime_sound_cb.currentData() if hasattr(self, 'chime_sound_cb') else "acoustic_bell"
        vol = self.chime_vol_slider.value() if hasattr(self, 'chime_vol_slider') else 45
        c_path = getattr(self, 'custom_chime_path', '')
        play_chime(preset=preset, volume=vol, custom_path=c_path if preset == "custom" else "")

    def browse_custom_sound(self):
        parent = self._get_active_dialog_parent()
        file, _ = QFileDialog.getOpenFileName(parent, "Select Audio File", "", "Audio Files (*.wav *.mp3 *.ogg *.flac)")
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
        self.sync_studio_clock()

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
        self.sync_studio_clock()

    def update_brightness(self, val):
        self.bright_val_label.setText(f"{val}%")
        self.preview.set_brightness(val)
        self.sync_studio_clock()

    def update_24hr(self, state=None):
        self.preview.use_24hr = self.use_24hr_cb.isChecked()
        self.preview.update()
        self.sync_studio_clock()

    def update_rotary_telemetry(self, state=None):
        self.preview.show_weather = self.show_weather_cb.isChecked()
        self.preview.show_battery = self.show_battery_cb.isChecked()
        self.preview.use_fahrenheit = self.fahrenheit_cb.isChecked()
        self.config["show_weather"] = self.show_weather_cb.isChecked()
        self.config["show_battery"] = self.show_battery_cb.isChecked()
        self.config["use_fahrenheit"] = self.fahrenheit_cb.isChecked()
        self.preview.update()
        self.sync_studio_clock()

    def update_pixel_shift(self, state=None):
        val = self.pixel_shift_cb.isChecked()
        self.preview.pixel_shift = val
        self.config["pixel_shift"] = val
        self.preview.update()
        self.sync_studio_clock()

    def refresh_font_combobox(self):
        if not hasattr(self, 'font_cb'):
            return
        self.font_cb.blockSignals(True)
        self.font_cb.clear()
        
        presets = [
            ("Bungee (Default)", "Bungee"),
            ("Google Sans", "Google Sans"),
            ("Segoe UI Variable", "Segoe UI Variable Display"),
            ("Google Sans Flex", "Google Sans Flex"),
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
            self.sync_studio_clock()
        else:
            self.preview.dino_font = str(data)
            self.preview.update()
            self.check_font_changed()
            self.sync_studio_clock()

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
        self.sync_studio_clock()

    def import_primary_font(self):
        parent = self._get_active_dialog_parent()
        file, _ = QFileDialog.getOpenFileName(parent, "Select Font File", "", "Font Files (*.ttf *.otf)")
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
        self.sync_studio_clock()

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
            self.sync_studio_clock()
        else:
            self.preview.character_type = "custom"
            self.preview.set_custom_character(str(data))
            self.preview.update()
            self.check_char_changed()
            self.sync_studio_clock()

    def handle_character_import(self, path):
        if not path or not os.path.exists(path):
            return
        self.custom_character_image = path
        self.preview.character_type = "custom"
        self.preview.set_custom_character(path)
        self.refresh_char_combobox()
        self.preview.update()
        self.check_char_changed()
        self.sync_studio_clock()

    def import_character(self):
        parent = self._get_active_dialog_parent()
        file, _ = QFileDialog.getOpenFileName(parent, "Select Character Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)")
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
        self.sync_studio_clock()

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
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    load_ui_font()
    
    ui_font = QFont(["Google Sans Flex", "Segoe UI Emoji", "Arial", "sans-serif"])
    ui_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias | QFont.StyleStrategy.PreferQuality)
    ui_font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
    app.setFont(ui_font)
    
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.png")
    if getattr(sys, 'frozen', False):
        logo_path = os.path.join(sys._MEIPASS, "app_icon.png")
    if os.path.exists(logo_path):
        app.setWindowIcon(QIcon(os.path.join(os.path.dirname(logo_path), "app_icon_taskbar.png")))
        
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
    
    if '--demo-verify' in sys.argv:
        mode = 'c'
        config_path = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), 'demo-qa-config.json')
    if mode == 'c':
        app.setQuitOnLastWindowClosed(False)
        dialog = SettingsDialog(config_path)
        dialog.show()
        if '--demo-verify' in sys.argv:
            def verify_packaged_demo():
                import traceback
                report = {'passed': False, 'checks': [], 'errors': []}
                sys.excepthook = lambda kind, error, tb: report['errors'].append(str(error))
                output = os.path.dirname(os.path.abspath(sys.executable))
                try:
                    cards = (dialog.card_mode, dialog.card_disp, dialog.card_sys)
                    for mode_index in (0, 1, 2):
                        dialog.set_mode(mode_index)
                        app.processEvents()
                        save_demo_capture(dialog,os.path.join(output, f'packaged-mode-{mode_index}.png'))
                        surface=getattr(dialog.preview,'_gpu_surface',None)
                        if surface is not None and surface.isValid():
                            frame = surface.grabFramebuffer()
                            for x, y in ((0,0),(frame.width()-1,0),(0,frame.height()-1),(frame.width()-1,frame.height()-1)):
                                assert frame.pixelColor(x,y).alpha() == 0, 'Uncleared preview corner'
                            frame.save(os.path.join(output,f'packaged-gpu-mode-{mode_index}.png'))
                            report.setdefault('render_backends',[]).append(surface.engine_name)
                        else:report.setdefault('render_backends',[]).append('Raster fallback')
                        dialog.test_fullscreen()
                        studio = dialog.studio
                        app.processEvents()
                        studio.show_about()
                        app.processEvents()
                        close = studio.about_modal.findChild(QPushButton, 'closeIconBtn')
                        assert close.width() == 36 and close.accessibleName() == 'Close About'
                        save_demo_capture(studio,os.path.join(output, f'packaged-studio-frost-{mode_index}.png'))
                        studio.hide_about()
                        from PyQt6.QtGui import QEnterEvent
                        for edge in ('left','top','right'):
                            grabber = getattr(studio, edge+'_grabber')
                            point = grabber.rect().center()
                            app.sendEvent(grabber,QEnterEvent(QPointF(point),QPointF(point),QPointF(grabber.mapToGlobal(point))))
                            studio.refresh_frosted_panels()
                            drawer = getattr(studio,edge+'_drawer')
                            assert getattr(studio,edge+'_open') and drawer.frosted_backdrop is not None
                            assert drawer.frosted_origin == getattr(studio,'anim_'+edge).endValue()
                            assert drawer.card.parentWidget() is drawer
                            assert drawer.contentsRect().contains(drawer.card.geometry())
                        assert '#92A4B8' in studio.action_dock.btn_apply.styleSheet()
                        from PyQt6.QtGui import QMouseEvent
                        button = studio.action_dock.btn_exit
                        point = button.mapToGlobal(button.rect().center())
                        for event_type in (QEvent.Type.MouseButtonPress,QEvent.Type.MouseButtonRelease):
                            event = QMouseEvent(event_type, QPointF(studio.clock.mapFromGlobal(point)), QPointF(point), Qt.MouseButton.LeftButton, Qt.MouseButton.LeftButton if event_type==QEvent.Type.MouseButtonPress else Qt.MouseButton.NoButton, Qt.KeyboardModifier.NoModifier)
                            app.sendEvent(studio.clock, event)
                        app.processEvents()
                        assert dialog.studio is None
                        assert all(dialog.cards_row.indexOf(card) >= 0 for card in cards)
                        owner = dialog.cards_row.parentWidget()
                        assert all(card.parentWidget() is owner for card in cards)
                        assert all(dialog.cards_row.geometry().contains(card.geometry()) for card in cards)
                        assert all(cards[index].geometry().right() < cards[index+1].geometry().left() for index in (0,1))
                        save_demo_capture(dialog,os.path.join(output,f'packaged-after-studio-{mode_index}.png'))
                        report['checks'].append(f'mode {mode_index}: clean GPU preview corners, larger About close, three hover/frost paths, purple buttons, Studio exit, real cards restored')
                    dialog.save_config()
                    assert not report['errors'], report['errors']
                    report['passed'] = True
                except Exception:
                    report['errors'].append(traceback.format_exc())
                with open(os.path.join(output, 'packaged-qa.json'), 'w', encoding='utf-8') as file:
                    json.dump(report, file, indent=2)
                app.exit(0 if report['passed'] else 1)
            QTimer.singleShot(200, verify_packaged_demo)
        sys.exit(app.exec())
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
            
    if default_config.get('accent_color') == '#D0D0D0':
        default_config['accent_color'] = get_windows_accent_color()
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


