import keyboard

while(true):
	try:
		if keyboard.is_pressed('q'):
			print('You pressed a key')
		else:
			pass
	except:
		break