import pygame
import sys
import time
import threading
from auxiliary_tools.message_manager import MessageManager
from auxiliary_tools.key_listener import KeyListener
from base import Base
from units.stages.play_stage import PlayStage
from units.stages.battle_stage import BattleStage
from units.stages.show_stage import ShowStage
# from units.stages.ui_stage import UIStage
from auxiliary_tools.data_reader import DataReader


class ScreenThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.data_reader = DataReader("./data/setting.xml")
        self.width = int(self.data_reader.get("screen_width"))
        self.height = int(self.data_reader.get("screen_height"))
        self.frame_mode = self.data_reader.get("frame_mode")
        self.size = None
        self.screen = None
        self.clock = None
        self.if_ready = False
        self.update_time_10 = 0
        self.update_time_4 = 0
        self.update_time_1 = 0
        self.update_frame = 0
        self.time001 = 0
        self.time002 = 0
        self.frame = 60
        self.stop = False

        self.stage = None
        self.stage_mode = 0
        # self.ui_stage = None

    def choose_screen(self):
        print("输入数字选择场景：")
        print("输入0--测试场景(高额初始资源，无任务目标，除周围的30只史莱姆外无其他敌人)")
        print("输入1--攻防战(任务目标：摧毁位于右侧的敌方基地，敌方会定期进攻你的基地，进攻强度随时"
              "间增加，保证你的基地不被摧毁。注意：右侧存在一友方哨站，提供前期的防御。")
        print("输入2--展示场景(自己选择何时遭受进攻)")
        print("在游戏过程中，如果你想提前结束，请按下esc键")
        x = int(input())
        if x == 0:
            print("选择：测试场景，祝你好运。")
            time.sleep(2)
            self.stage_mode = 0
        elif x == 1:
            print("选择：攻防战，注意时刻留意右侧来犯的敌人，不要错失最好防守时机，祝你好运。")
            time.sleep(4)
            self.stage_mode = 1
        elif x == 2:
            print("选择：展示场景，祝你好运。")
            time.sleep(2)
            self.stage_mode = 2
        else:
            print("非法输入，默认选择：测试场景，祝你好运。")
            time.sleep(3)
            self.stage_mode = 0

    def run(self):
        self.choose_screen()
        pygame.init()
        self.size = width, height = self.width, self.height
        if self.frame_mode == "full_screen":
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        elif self.frame_mode == "no_frame":
            self.screen = pygame.display.set_mode(self.size, pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE)
        else:
            self.screen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.HWSURFACE)
        if self.stage_mode == 0:
            self.stage = PlayStage(self.screen)
        elif self.stage_mode == 1:
            self.stage = BattleStage(self.screen)
        elif self.stage_mode == 2:
            self.stage = ShowStage(self.screen)
        # self.ui_stage = UIStage(self.screen)
        self.clock = pygame.time.Clock()
        self.if_ready = True

        self.stage.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    MessageManager.send_message("quit", None)
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        MessageManager.send_message("quit", None)
                        break
                    MessageManager.send_message("key_down", (event.key, event.mod))
                elif event.type == pygame.KEYUP:
                    MessageManager.send_message("key_up", (event.key, event.mod))

            if self.stop is False:
                MessageManager.send_message("update_60", None)
                if self.update_time_4 == 4:
                    MessageManager.send_message("update_15", None)
                    self.update_time_4 = 0
                if self.update_time_10 == 10:
                    MessageManager.send_message("update_6", None)
                    self.update_time_10 = 0
            else:
                MessageManager.send_message("stop_update_60", "stop")

            """if self.update_frame >= 60:
                # MessageManager.send_message("update_4", "")
                # print("frame:" + str(60 / (self.frame_time_end - self.frame_time_start)))
                self.frame = int(60 / (self.frame_time_end - self.frame_time_start))
                if self.frame <= 10 or self.frame >= 80:
                    self.frame = 60
                self.stage.set_frame(self.frame)
                self.frame_time_start = self.frame_time_end
                self.frame_time_end = time.time()
                self.update_frame = 0"""
            if self.update_frame >= 10:
                self.time002 = time.time()
                self.update_frame = 0
                if self.time002 - self.time001 != 0:
                    frame = int(10 / (self.time002 - self.time001))
                else:
                    frame = "NaN"
                MessageManager.send_message("frame", frame)
                self.time001 = time.time()
            self.update_time_10 += 1
            self.update_time_4 += 1
            # self.update_time_1 += self.frame / 60
            self.update_frame += 1
            self.clock.tick(60)
            self.update()

    def update(self):
        pygame.display.update(pygame.Rect(0, 0, self.width, self.height))

    def draw(self, draw_list):
        self.screen.blit(draw_list[0], draw_list[1])


class GraphUpdateThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.clock = None
        self.time001 = 0
        self.time002 = 0
        self.if_break = False

    def run(self):
        self.clock = pygame.time.Clock()
        while not self.if_break:
            MessageManager.send_message("graph_update", None)
            self.time002 = time.time()
            if self.time002 - self.time001 != 0:
                frame = int(1 / (self.time002 - self.time001))
            else:
                frame = "NaN"
            MessageManager.send_message("frame", frame)
            self.clock.tick(240)
            self.time001 = time.time()

    def end(self):
        self.if_break = True


class Main(Base):
    def __init__(self):
        super().__init__()
        self.screen_thread = ScreenThread()
        self.screen_thread.start()
        self.key_listener = KeyListener()
        while True:
            if self.screen_thread.if_ready:
                break
            time.sleep(0.1)
        self.message_require("quit", self.quit)
        self.message_require("game_stop", self.game_stop)
        # 游戏启动完毕

    def game_stop(self, data):
        self.screen_thread.stop = not self.screen_thread.stop

    def quit(self, data):
        # self.graph_update.end()
        pygame.quit()
        exit(0)


main = Main()
sys.exit(0)
