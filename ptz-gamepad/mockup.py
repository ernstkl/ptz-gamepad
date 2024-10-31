import random

class DummyPtzCam:

    def move(self, x_vel, y_vel):

        print(f'cam move({x_vel}, {y_vel})')

    def stop(self):

        print('cam stop')

    def zoom(self, z):

        print(f'zoom to {z}')


    def get_position(self):

        p = random.random() * 2 - 1
        t = random.random() * 2 - 1
        z = random.random()

        return p, t, z

    def absmove_w_zoom(self, p, t, z):

        print(f'abs move to {p} {t} {z}')


