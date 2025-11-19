Tank Battle 2025
Tank Battle 2025 is a 2D game developed using Python and Pygame.

The game now features three modes: Single Player, Two Player, and a unique Bonus survival mode. It also includes multiple background options, interactive sound effects, and simple AI behavior for the enemy tank.

My game was inspired by this video: https://www.youtube.com/watch?v=jO6qQDNa2UY

Added features:
	-Game menu: An interactive main menu to select the game mode and background.
	-Three game modes:
		-Single Player Mode with an AI-controlled enemy tank.
		-Two Player Mode.
		-Bonus Mode:survival mode where you must avoid colliding with the obstacles with progressively increasing speed and frequency.
	-3 types of weapons with different characteristics: cannon, laser and machine gun
	-Background Selection: Choose from multiple backgrounds.
	-Sound Effects: Includes unique firing and hit sound effects for each weapon, and background music

To meet the requirements the folowiing classess were added:
	- Obstacle: manages bombs from the bonus mode.
	- Projectile: base class for all weapons.
	- Bullet, Laser, Shot: subclasses of Projectile class.
	- Healthsystem: manages health of tanks


CONTROLS
Yellow player:
	WASD to move, 1,2,3 to fire cannon laser and machine gun respectively
Green player:
	ARROWS to move, 8, 9, 0 to fire cannon laser and machine gun respectively

How to run:

-To run the game, make sure you have Python and Pygame installed.
-Then put python file containing the game and Assets folder in the same directory.
-Run the game from your terminal.