import pygame
from pygame.locals import *
from elements import Button




class SensorGame:
    def __init__(self, custom_serial):
        pygame.init()
        pygame.display.set_caption("Sensor Game")
        self.WIDTH, self.HEIGHT = 640, 480
        self.WHITE = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.my_button = Button((255, 0, 0), 100, 100, 150, 50, 'Download CSV')
        self.my_button.draw(self.screen, (0, 0, 0))
        self.accelerometer_data = [0, 0, 0]
        self.gyroscope_data = [0, 0, 0]
        self.player = Player(self.WIDTH, self.HEIGHT)
        self.custom_serial = custom_serial  # custom_serial is the CustomSerial instanc
        self.font = pygame.font.Font(None, 24)  # Create a font object.
        self.running = True


    def run(self):
        while self.running:
            self.handle_events()
            self.update_game_state()
            self.draw_game_state()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.my_button.is_over(pos):
                    self.custom_serial.download_csv()

            if event.type == pygame.MOUSEMOTION:
                if self.my_button.is_over(pos):
                    self.my_button.color = (255, 0, 0)
                else:
                    self.my_button.color = (0, 255, 0)
        return True

    def update_game_state(self):
        try:
            # Get accelerometer data from custom_serial
            raw_accel_data, ma_accel_data = self.custom_serial.get_data("ACCELEROMETER")
            self.custom_serial.save_data()
            if ma_accel_data is not None and all(element is not None for element in ma_accel_data):
                self.accelerometer_data = ma_accel_data
                self.player.move(self.accelerometer_data[0], -self.accelerometer_data[1])
                self.player.change_size(self.accelerometer_data[2])
            
            # Get gyroscope data from custom_serial
            raw_gyro_data, ma_gyro_data = self.custom_serial.get_data("GYROSCOPE")
            if ma_gyro_data is not None and all(element is not None for element in ma_gyro_data):
                self.gyroscope_data = raw_gyro_data
        except Exception as e:
            print(f"Error occurred while reading data: {e}")
            self.accelerometer_data = [0, 0, 0]
            self.gyroscope_data = [0, 0, 0]


    def draw_game_state(self):
        self.screen.fill(self.WHITE)
        self.my_button.draw(self.screen, (0, 0, 0))
        self.screen.blit(self.player.surf, self.player.rect)

        accel_text = "Accelerometer: x: {:.2f}, y: {:.2f}, z: {:.2f}".format(*self.accelerometer_data)
        gyro_text = "Gyroscope: x: {:.2f}, y: {:.2f}, z: {:.2f}".format(*self.gyroscope_data)
        text_surface_acc = self.font.render(accel_text, True, (0, 0, 0))
        text_surface_gyro = self.font.render(gyro_text, True, (0, 0, 0))

        self.screen.blit(text_surface_acc, (20, 20))
        self.screen.blit(text_surface_gyro, (20, 40))

        pygame.display.flip()



class Player(pygame.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        pygame.draw.circle(self.surf, (0, 0, 255), (25, 25), 25)
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.speed = 5.0
        self.original_surf = self.surf.copy()

    def move(self, x, y):
        self.rect.move_ip(x * self.speed, y * self.speed)

    def change_size(self, z):
        factor = 0.5 + z  # scales the size according to z axis
        self.surf = pygame.transform.rotozoom(self.original_surf, 0, factor)
        self.rect = self.surf.get_rect(center=self.rect.center)

if __name__ == '__main__':
    from custom_serial import CustomSerial
    custom_serial = CustomSerial()
    SensorGame(custom_serial).run()
