import tkinter as tk
import threading
import time

def move_sprite(x: int, y: int, sprite: int):

	# Calculos
	sprite_bbox = canvas.bbox(sprite)
	sprite_width = sprite_bbox[2] - sprite_bbox[0]
	sprite_height = sprite_bbox[3] - sprite_bbox[1]

	# Posicion inicial
	posX = 0
	posY = 0

	# Direccion
	dx = 1
	dy = 1

	canvas.move(sprite, posX, posY)

	while True:
		canvas_width = canvas.winfo_width()
		canvas_height = canvas.winfo_height()

		canvas.move(sprite, x * dx, y * dy)
		posX += x * dx
		posY += y * dy

		if (posX >= (canvas_width - sprite_width) or posX < 0):
			dx *= -1

		if (posY >= (canvas_height - sprite_height) or posY < 0):
			dy *= -1

		time.sleep(1 / 60)

if __name__ == '__main__':
	root = tk.Tk()
	root.title('Hilos')

	canvas = tk.Canvas(root, width=800, height=600, borderwidth=0, highlightthickness=0)
	canvas.pack(fill=tk.BOTH, expand=True)

	img_kirby = tk.PhotoImage(file='./kirby.png')
	scaled_kirby = img_kirby.zoom(4, 4)
	sprite_kirby = canvas.create_image(0, 0, anchor=tk.NW, image=scaled_kirby)

	img_thwomp = tk.PhotoImage(file='./thwomp.png')
	scaled_thwomp = img_thwomp.zoom(4, 4)
	sprite_thwomp = canvas.create_image(0, 0, anchor=tk.NW, image=scaled_thwomp)

	# Hilo para mover a kirby
	kirby_thread = threading.Thread(target=move_sprite, args=(6, 4, sprite_kirby))
	kirby_thread.daemon = True # El hilo para cuando el main() se detiene
	kirby_thread.start()

	# Hilo para mover a thwomp
	thwomp_thread = threading.Thread(target=move_sprite, args=(2, 8, sprite_thwomp))
	thwomp_thread.daemon = True # El hilo para cuando el main() se detiene
	thwomp_thread.start()

	root.mainloop()