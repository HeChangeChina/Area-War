from unit_tools.bullet import Bullet
from auxiliary_tools.ballistic import Ballistic


class BulletPre:
    def __init__(self, name, effect, speed=600, last_time=20, direct=True, ballistic=Ballistic(), trajectory_name=None,
                 trajectory_size=None, trajectory_fps=1, trajectory_cycle=2, trajectory_shift=5, hit_effect=None,
                 fps_level=0):
        self.name = name
        self.effect = effect
        self.speed = speed
        self.last_time = last_time
        self.direct = direct
        self.ballistic = ballistic
        self.trajectory_name = trajectory_name
        self.trajectory_size = trajectory_size
        self.trajectory_fps = trajectory_fps
        self.trajectory_cycle = trajectory_cycle
        self.trajectory_shift = trajectory_shift
        self.hit_effect = hit_effect
        self.fps_level = fps_level

    def get_bullet(self):
        return Bullet(self.name, self.effect, self.speed, self.last_time, self.direct, self.ballistic,
                      self.trajectory_name, self.trajectory_size, self.trajectory_fps, self.trajectory_cycle,
                      self.trajectory_shift, self.hit_effect, self.fps_level)
