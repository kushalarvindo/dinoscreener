import re
with open('screensaver.py', 'r') as f:
    code = f.read()

# Update animation loop
old_obstacle = '''                if len(self.dino_obstacles) == 0:
                    self.dino_obstacles.append({'x': self.width() + 200, 'w': 25, 'h': 50, 'type': 'large1'})
                else:
                    last_obs = self.dino_obstacles[-1]
                    if self.width() - last_obs['x'] > 400 + random.randint(0, 400):
                        obs_type = random.randint(0, 5)
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
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 75, 'h': 50, 'type': 'large3'})'''

new_obstacle = '''                # Ground scroll
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
                            self.dino_obstacles.append({'x': self.width() + 50, 'w': 46, 'h': 40, 'type': 'crow', 'y_off': 80})'''

code = code.replace(old_obstacle, new_obstacle)

old_draw = '''        if not self.sprite_pixmap.isNull():
            # Draw ground line
            painter.setPen(QColor(150, 150, 150))
            painter.drawLine(0, int(ground_y), w, int(ground_y))
            
            # Draw Dino
            dino_w = 44
            dino_h = 47
            if self.dino_y > 0:
                dino_rect = QRectF(1678, 2, 44, 47) # Jumping
            else:
                if (self.dino_frame // 5) % 2 == 0:
                    dino_rect = QRectF(1854, 2, 44, 47) # Run 1
                else:
                    dino_rect = QRectF(1898, 2, 44, 47) # Run 2
                    
            target_rect = QRectF(w * 0.2, ground_y - self.dino_y - dino_h, dino_w, dino_h)
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
            
            # Draw Dino
            dino_w = 44
            dino_h = 47
            if self.dino_y > 0:
                dino_rect = QRectF(1678, 2, 44, 47) # Jumping
            else:
                if (self.dino_frame // 5) % 2 == 0:
                    dino_rect = QRectF(1854, 2, 44, 47) # Run 1
                else:
                    dino_rect = QRectF(1898, 2, 44, 47) # Run 2
                    
            target_rect = QRectF(w * 0.2, ground_y - self.dino_y - dino_h, dino_w, dino_h)
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

code = code.replace(old_draw, new_draw)

# Now, add checkboxes for settings.
settings_old = '''        self.win_cb = QCheckBox("Block Windows Key (experimental)")
        self.win_cb.setChecked(self.config["enable_win_key"])
        self.win_cb.setStyleSheet("color: white; font-family: 'Segoe UI'; font-size: 14px;")
        control_layout.addWidget(self.win_cb)'''

settings_new = '''        self.win_cb = QCheckBox("Block Windows Key (experimental)")
        self.win_cb.setChecked(self.config["enable_win_key"])
        self.win_cb.setStyleSheet("color: white; font-family: 'Segoe UI'; font-size: 14px;")
        control_layout.addWidget(self.win_cb)
        
        self.use_24hr_cb = QCheckBox("Use 24-Hour Format")
        self.use_24hr_cb.setChecked(self.config.get("use_24hr", False))
        self.use_24hr_cb.setStyleSheet("color: white; font-family: 'Segoe UI'; font-size: 14px;")
        self.use_24hr_cb.toggled.connect(self.update_style_ui)
        control_layout.addWidget(self.use_24hr_cb)
        
        self.leading_zero_cb = QCheckBox("Leading Zero (24hr)")
        self.leading_zero_cb.setChecked(self.config.get("leading_zero", False))
        self.leading_zero_cb.setStyleSheet("color: white; font-family: 'Segoe UI'; font-size: 14px;")
        control_layout.addWidget(self.leading_zero_cb)'''

code = code.replace(settings_old, settings_new)

# Update config loading/saving
config_old1 = '''            "clock_style": 1,
            "clock_scale": 0.45'''
config_new1 = '''            "clock_style": 1,
            "clock_scales": {"0": 0.45, "1": 0.45, "2": 0.45},
            "use_24hr": False,
            "leading_zero": False'''
code = code.replace(config_old1, config_new1)

config_old2 = '''        self.config["clock_style"] = self.preview.clock_style
        self.config["clock_scale"] = self.preview.clock_scale'''
config_new2 = '''        self.config["clock_style"] = self.preview.clock_style
        self.config["clock_scales"] = self.preview.clock_scales
        self.config["use_24hr"] = self.use_24hr_cb.isChecked()
        self.config["leading_zero"] = self.leading_zero_cb.isChecked()'''
code = code.replace(config_old2, config_new2)

config_old3 = '''            clock_style=self.config["clock_style"],
            clock_scale=self.config["clock_scale"]'''
config_new3 = '''            clock_style=self.config["clock_style"],
            clock_scales=self.config.get("clock_scales", {"0": 0.45, "1": 0.45, "2": 0.45}),
            use_24hr=self.config.get("use_24hr", False),
            leading_zero=self.config.get("leading_zero", False)'''
code = code.replace(config_old3, config_new3)

config_old4 = '''        "clock_style": 1,
        "clock_scale": 0.45'''
config_new4 = '''        "clock_style": 1,
        "clock_scales": {"0": 0.45, "1": 0.45, "2": 0.45},
        "use_24hr": False,
        "leading_zero": False'''
code = code.replace(config_old4, config_new4)

config_old5 = '''        clock_style=default_config.get("clock_style", 1),
        clock_scale=default_config.get("clock_scale", 0.45)'''
config_new5 = '''        clock_style=default_config.get("clock_style", 1),
        clock_scales=default_config.get("clock_scales", {"0": 0.45, "1": 0.45, "2": 0.45}),
        use_24hr=default_config.get("use_24hr", False),
        leading_zero=default_config.get("leading_zero", False)'''
code = code.replace(config_old5, config_new5)

update_ui_old = '''        is_dino = self.preview.clock_style == 2
        is_rotary = self.preview.clock_style == 0
        if is_dino or is_rotary:
            self.show_info_cb.hide()
        else:
            self.show_info_cb.show()'''
update_ui_new = '''        is_dino = self.preview.clock_style == 2
        is_rotary = self.preview.clock_style == 0
        if is_dino or is_rotary:
            self.show_info_cb.hide()
        else:
            self.show_info_cb.show()
            
        if self.use_24hr_cb.isChecked():
            self.leading_zero_cb.show()
        else:
            self.leading_zero_cb.hide()
            
        self.preview.use_24hr = self.use_24hr_cb.isChecked()
        self.preview.leading_zero = self.leading_zero_cb.isChecked()
        self.preview.update()'''
code = code.replace(update_ui_old, update_ui_new)

with open('screensaver.py', 'w') as f:
    f.write(code)
