from loguru import logger
import yaml

# +/- dieser Wert um die Null herum zählt als Null
deadband = 0.025

# Sinn ergeben hier nur Werte bis (1 + deadband)/(1 - deadband), also ungefähr 1, denn bei skaliertem Wert > 1 wird abgeschnitten
max_vel = 1.0

# minimale joystick-bewegung, um einen neuen befehl rauszuschicken
min_change = 0.05
min_change_ax2 = 0.02

class GamepadHandler:

    def __init__(self, cam):

        # reference to camera
        self.cam = cam

        # Joystick Kalibrierung
        self.j_x0 = None
        self.j_y0 = None

        # Joystick aktuelle Position (braucht man immer beide für die move Kommandos)
        # zoom nur der Vollständigkeit halber
        # Werte -1 .. 1
        self.j_x = 0
        self.j_y = 0
        self.j_zoom = 0

        # wahr während button 6 gedrückt
        self.store_preset_active = False

        # presets (erstmal ohne konfig-möglichkeit des pfades)
        self.presets_filename = 'presets.yaml'
        self.presets = {}
        try:
            # jaja, man sollte das nicht mit try-except machen
            with open(self.presets_filename, 'r') as file:
                self.presets = yaml.safe_load(file)

        except FileNotFoundError:
            logger.info(f'could not open preset file {self.presets_filename}, starting with empty presets')


    def axis_0_1_calibrate(self, x, y):
        self.j_x0 = x
        self.j_y0 = y

    def handle_joyaxis_event(self, axis, value):
        # Kalibrierung anwenden
        if axis == 0:
            new_j_x = value - self.j_x0
            # neuen wert nur speichern, wenn die änderung groß genug, oder zurück in die nähe der null
            if abs(new_j_x - self.j_x) > min_change or abs(new_j_x) < deadband:
                self.j_x = new_j_x

        elif axis == 1:
            new_j_y = value - self.j_y0
            if abs(new_j_y - self.j_y) > min_change or abs(new_j_y) < deadband:
                self.j_y = new_j_y

        elif axis == 2:
            if abs(self.j_zoom - value) > min_change_ax2:
                self.j_zoom = value

        if axis in [0, 1]:
            # wenn beide Geschw. in toter Zone, dann stop
            if abs(self.j_x) < deadband and abs(self.j_y) < deadband:
                self.cam.stop()

            else:
                # Geschwindigkeit setzen
                # - nicht die absolute joy-pos verwenden, sondern das was über's deadband hinausgeht
                # - joypos -1..1 skalieren auf Geschwindigkeit -1 .. 1
                if self.j_x < 0:
                    j_x_eff = self.j_x + deadband
                else:
                    j_x_eff = self.j_x - deadband

                if self.j_y < 0:
                    j_y_eff = self.j_y + deadband
                else:
                    j_y_eff = self.j_y - deadband

                cam_vel_x = min(1.0, max(0.0, j_x_eff * max_vel))
                cam_vel_y = min(1.0, max(0.0, j_y_eff * max_vel))
                self.cam.move(cam_vel_x, cam_vel_y)

        elif axis == 2:
            # absoluter zoom, -1..1 auf 0..1 mappen
            self.cam.zoom((self.j_zoom + 1) / 2)

    def handle_button_down_event(self, button):
        if button == 6:
            self.store_preset_active = True

        if button < 6:
            if self.store_preset_active:
                logger.info(f'storing preset {button}')
                x_cam, y_cam, z_cam = self.cam.get_position()

                self.presets[button] = [x_cam, y_cam, z_cam]

                logger.info(f'saving preset file: {self.presets_filename}')
                with open(self.presets_filename, 'w') as file:
                    yaml.dump(self.presets, file)


            else:
                # send preset to camera
                if button in self.presets.keys():
                    logger.info(f'sending preset {button} to camera')
                    x_cam, y_cam, z_cam = self.presets[button]
                    self.cam.absmove_w_zoom(x_cam, y_cam, z_cam)
                else:
                    logger.info(f'no preset stored for button {button}')

    def handle_button_up_event(self, button):
        if button == 6:
            self.store_preset_active = False
