"""
A-Star Path-finding

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.astar_pathfinding
"""

import arcade
import random
import math

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ENEMY = 0.5
ENEMY_SPEED = 3.0

SPRITE_IMAGE_SIZE = 128
SPRITE_SCALING = 0.25
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "A-Star Path-finding"

MOVEMENT_SPEED = 5

VIEWPORT_MARGIN = 100


class Enemy(arcade.Sprite):
    """
    This class represents the Enemy on our screen.
    """

    def __init__(self, image, scale, position_list):
        super().__init__(image, scale)
        self.arrived = False
        self.position_list = position_list
        self.cur_position = None
        self.speed = ENEMY_SPEED

    def update(self):
        """ Have a sprite follow a path """
        if self.cur_position is None:
            self.cur_position = len(self.position_list) - 1

        if self.arrived:
            print("enemy has arrived")
            return
        # Where are we
        start_x = self.center_x
        start_y = self.center_y

        # Where are we going
        print(f"current pos: {self.cur_position}")
        dest_x = self.position_list[self.cur_position][0]
        dest_y = self.position_list[self.cur_position][1]

        # X and Y diff between the two
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # How fast should we go? If we are close to our destination,
        # lower our speed so we don't overshoot.
        speed = min(self.speed, distance)

        # Calculate vector to travel
        change_x = math.cos(angle) * speed
        change_y = math.sin(angle) * speed

        # Update our location
        self.center_x += change_x
        self.center_y += change_y

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        # If we are there, head to the next point.
        if distance <= self.speed:
            self.cur_position = self.cur_position - 1
            if self.cur_position <= 0:
                self.arrived = True


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Variables that will hold sprite lists
        self.goal_position = None
        self.enemy_start = None
        self.player_list = None
        self.wall_list = None
        self.enemy_list = None

        # Set up the player info
        self.player = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.physics_engine = None

        # --- Related to paths
        # List of points that makes up a path between two points
        self.path = None
        # List of points we checked to see if there is a barrier there
        self.barrier_list = None

        # Used in scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Set the window background color
        self.background_color = arcade.color.AMAZON

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True,
                                           spatial_hash_cell_size=128)
        self.enemy_list = arcade.SpriteList()

        # Set up the player
        resource = ":resources:images/animated_characters/" \
                   "female_person/femalePerson_idle.png"
        self.player = arcade.Sprite(resource, SPRITE_SCALING)
        self.player.center_x = SPRITE_SIZE * 5
        self.player.center_y = SPRITE_SIZE * 1
        self.player_list.append(self.player)

        self.goal_position = (SPRITE_SIZE * 15, SPRITE_SIZE * 4)
        self.enemy_start = (SPRITE_SIZE * -1, SPRITE_SIZE * 0)


        spacing = SPRITE_SIZE * 3
        for column in range(10):
            for row in range(15):
                sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png",
                                       SPRITE_SCALING)

                x = (column + 1) * spacing
                y = (row + 1) * sprite.height

                sprite.center_x = x
                sprite.center_y = y
                not_goal = sprite.center_x != self.goal_position[0] and sprite.center_y != self.goal_position[1]
                not_start = sprite.center_x != self.enemy_start[0] and sprite.center_y != self.enemy_start[1]
                if random.randrange(100) > 30 and not_goal and not_start:
                    self.wall_list.append(sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.wall_list)

        grid_size = SPRITE_SIZE

        playing_field_left_boundary = -SPRITE_SIZE * 2
        playing_field_right_boundary = SPRITE_SIZE * 35
        playing_field_top_boundary = SPRITE_SIZE * 17
        playing_field_bottom_boundary = -SPRITE_SIZE * 2

        # Create the enemy
        enemy = Enemy(":resources:images/animated_characters/robot/robot_idle.png",
                      SPRITE_SCALING_ENEMY, self.path)

        # Add the enemy to the enemy list
        self.enemy_list.append(enemy)

        self.barrier_list = arcade.AStarBarrierList(self.enemy_list[0],
                                                    self.wall_list,
                                                    grid_size,
                                                    playing_field_left_boundary,
                                                    playing_field_right_boundary,
                                                    playing_field_bottom_boundary,
                                                    playing_field_top_boundary)

        assert self.enemy_start not in self.barrier_list.barrier_list
        assert self.goal_position not in self.barrier_list.barrier_list

        self.path = arcade.astar_calculate_path(self.goal_position,
                                                self.enemy_start,
                                                self.barrier_list,
                                                diagonal_movement=False)

        assert self.path is not None

        for enemy in self.enemy_list:
            enemy.center_x = self.enemy_start[0]
            enemy.center_y = self.enemy_start[1]
            print(self.path, "->", self.goal_position)
            if self.path is not None:
                enemy.position_list = self.path

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()

        if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player.change_x = 0
        self.player.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = MOVEMENT_SPEED

        # Update the character
        self.physics_engine.update()

        self.enemy_list.update()

        # --- Manage Scrolling ---

        # Keep track of if we changed the boundary. We don't want to call the
        # set_viewport command if we didn't change the view port.
        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        # Make sure our boundaries are integer values. While the view port does
        # support floating point numbers, for this application we want every pixel
        # in the view port to map directly onto a pixel on the screen. We don't want
        # any rounding errors.
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        # If we changed the boundary values, update the view port to match
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
