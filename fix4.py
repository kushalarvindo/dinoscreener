import re
with open('screensaver.py', 'r') as f:
    code = f.read()

# 1. Update Spacing
old_spacing = '''        painter.setFont(font_date)
        date_y = h * 0.05 + scaled_size * 1.05
        date_rect = QRectF(0, date_y, w, scaled_date * 2)'''
        
new_spacing = '''        painter.setFont(font_date)
        date_y = h * 0.05 + scaled_size * 1.25
        date_rect = QRectF(0, date_y, w, scaled_date * 2)'''
code = code.replace(old_spacing, new_spacing)

if old_spacing not in code:
    print("Warning: old_spacing not found")


# 2. Update Draw Logic
old_draw = '''        if not self.sprite_pixmap.isNull():
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
                if t == 'small1': cactus_rect = QRectF(228, 2, 17, 35)
                elif t == 'small2': cactus_rect = QRectF(228, 2, 34, 35)
                elif t == 'small3': cactus_rect = QRectF(228, 2, 51, 35)
                elif t == 'large1': cactus_rect = QRectF(332, 2, 25, 50)
                elif t == 'large2': cactus_rect = QRectF(332, 2, 50, 50)
                elif t == 'large3': cactus_rect = QRectF(332, 2, 75, 50)
                else: cactus_rect = QRectF(332, 2, 25, 50)
                
                obs_target = QRectF(obs['x'], ground_y - obs['h'], obs['w'], obs['h'])
                painter.drawPixmap(obs_target, self.sprite_pixmap, cactus_rect)'''

new_draw = '''        if not self.sprite_pixmap.isNull():
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
                
                painter.drawPixmap(obs_target, self.sprite_pixmap, obs_rect)'''

if old_draw not in code:
    print("Warning: old_draw not found")
code = code.replace(old_draw, new_draw)

# 3. Remove the line that draws the hardcoded ground line
old_line = '''        ground_y = h * 0.95
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.drawLine(0, int(ground_y), w, int(ground_y))'''
new_line = '''        ground_y = h * 0.95'''
if old_line not in code:
    print("Warning: old_line not found")
code = code.replace(old_line, new_line)

with open('screensaver.py', 'w') as f:
    f.write(code)
