import pygame as pg
import json

pg.init()

from PyModernRay import *

class CameraControler(CameraRayCasting):
	def __init__(self, pos, distance, fov, ray_num, resolution):
		self.move_vecs = [vec2(math.cos(i/2*math.pi), -math.sin(i/2*math.pi)) for i in range(4)]
		super().__init__(pos, distance, fov, ray_num, resolution)
	
	def rotate(self, angle_x, angle_y):
		self.move_vecs = [rotate_vec2(v, angle_x) for v in self.move_vecs]
		super().rotate(angle_x, angle_y)

	def update(self, event, center):
		pg.mouse.set_visible(False)
		for e in event:
			if e.type == pg.MOUSEMOTION:
				if abs(e.rel[0])>1:
					self.rotate(e.rel[0], 0)
				if abs(e.rel[1])>1:
					self.rotate(0, e.rel[1])
					pg.mouse.set_pos(center)
		keys = pg.key.get_pressed()
		if keys[pg.K_w]:
			self.pos[:2] += self.move_vecs[0]/self.resolution
		if keys[pg.K_a]:
			self.pos[:2] += self.move_vecs[1]/self.resolution
		if keys[pg.K_s]:
			self.pos[:2] += self.move_vecs[2]/self.resolution
		if keys[pg.K_d]:
			self.pos[:2] += self.move_vecs[3]/self.resolution
		if keys[pg.K_SPACE]:
			self.pos[2] += 1/self.resolution
		if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
			self.pos[2] -= 1/self.resolution
		if keys[pg.K_HOME]:
			self.pos = vec3(0,0,0)

class App:
	def __init__(self):
		self.screen = pg.display.set_mode((50*20, 16*20*2))
		self.clock = pg.time.Clock()

		self.global_resolution = 16

		self.assets = [get_model("xyz.png", self.global_resolution),get_model("chr_knight.png", self.global_resolution),get_model("dirt.png", self.global_resolution)]
		#self.assets = [get_model(f"assets/{i}.png", self.global_resolution) for i in range(15)]
		self.assets = np.array(self.assets)

		self.field = np.full((1,1,1), 0)
		# self.field[1][:][:] = 1
		#with open("maps/0.json", "r") as f:
			#self.field = np.array(list(reversed(json.load(f))))

		self.camera = CameraControler(vec3(1.5,1.5,1.5), 100, 90, 50, self.global_resolution)

		self.run = True

	def mainloop(self):
		while self.run:
			self.clock.tick(60)

			events = pg.event.get()
			for e in events:
				if e.type == pg.QUIT:
					self.run = False
			self.camera.update(events, self.screen.get_rect().center)

			self.screen.fill((0, 0, 0))
			self.screen.blit(pg.transform.scale(self.camera.render(self.field, self.assets), self.screen.get_size()), (0,0))
			# self.screen.blit(self.camera.render(self.field, self.assets), (0,0))
			# self.camera.render(self.field, self.assets)
			# multi_ray_cast(self.camera.pos[:2], np.array(self.camera.vecs), self.camera.distance, self.field, self.assets, self.camera.resolution)
			pg.display.update()

			pg.display.set_caption(str(self.clock.get_fps()))

		pg.quit()

if __name__ == '__main__':
	root = App()
	root.mainloop()
