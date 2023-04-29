"""
Final Project Game AI
Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.astar_pathfinding
"""
import math

import arcade
import random
import utilities
import turret_placement_ai

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ENEMY = 0.25
TILE_SCALING = 0.5
ENEMY_SPEED = 3.0

BULLET_SPEED = 10
TURRET_RANGE = 100

SPRITE_IMAGE_SIZE = 128
SPRITE_SCALING = 0.25
BULLET_SCALING = 0.75
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)
GRID_PIXEL_SIZE = SPRITE_IMAGE_SIZE * TILE_SCALING

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Final Project: Tower Defense AI"

MOVEMENT_SPEED = 5

VIEWPORT_MARGIN = 100

# Maze must have an ODD number of rows and columns.
# Walls go on EVEN rows/columns.
# Openings go on ODD rows/columns
MAZE_HEIGHT = 21
MAZE_WIDTH = 21

two_halls = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
    [3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 4, 1, 1],
]

windy_maze = [
    [1, 1, 1, 3, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Turret(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.target = None

    def update_target(self, target):
        self.target = target


class Bullet(arcade.Sprite):
    def __init__(self, image, scale, start_pos, angle):
        super().__init__(image, scale)
        self.start_pos = start_pos
        self.center_x = start_pos[0]
        self.center_y = start_pos[1]
        self.angle = math.degrees(angle)
        self.change_x = math.cos(angle) * BULLET_SPEED
        self.change_y = math.sin(angle) * BULLET_SPEED

    def update(self):
        dist_traveled = math.sqrt((self.center_x - self.start_pos[0]) ** 2 + (self.center_y - self.start_pos[1]) ** 2)
        if dist_traveled > TURRET_RANGE:
            self.remove_from_sprite_lists()
        self.center_x += self.change_x
        self.center_y += self.change_y


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
        self.hit_time = 0
        self.health = 10.0
        self.slow_time = 0

    def take_damage(self, damage):
        self.health -= damage
        self.hit_time = 0.10
        self.color = [255, 0, 0]

    def become_slow(self):
        self.slow_time = 1
        self.color = [0, 0, 255]
        self.speed = 0.5 * ENEMY_SPEED

    def update(self):
        """ Have a sprite follow a path """
        if self.cur_position is None:
            self.cur_position = 0

        if self.health <= 0:
            self.remove_from_sprite_lists()

        if self.arrived:
            self.remove_from_sprite_lists()
            return

        # Where are we
        start_x = self.center_x
        start_y = self.center_y

        # Where are we going
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
        self.velocity = [change_x, change_y]

        # Update our location
        self.center_x += change_x
        self.center_y += change_y

        # How far are we?
        distance = math.sqrt((self.center_x - dest_x) ** 2 + (self.center_y - dest_y) ** 2)

        if distance <= self.speed:
            self.cur_position += 1
            if self.cur_position == len(self.position_list):
                self.arrived = True


def find_in_maze(maze, val):
    found = []
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == val:
                found.append([col, row])
    return found


def convert_grid_to_coords(grid):
    return [grid[1] * SPRITE_SIZE + SPRITE_SIZE / 2, grid[0] * SPRITE_SIZE + SPRITE_SIZE / 2]


def check_maze_pos(maze, pos):
    x = pos[0]
    y = pos[1]
    if len(maze) <= y:
        return False
    if y < 0:
        return False
    if len(maze[0]) <= x:
        return False
    if x < 0:
        return False
    return maze[y][x] == 2 or maze[y][x] == 4


def get_neighbors(pos):
    x = pos[0]
    y = pos[1]
    left = [x - 1, y]
    right = [x + 1, y]
    down = [x, y + 1]
    up = [x, y - 1]
    return [left, right, down, up]


def get_paths(maze):
    starts = find_in_maze(maze, 3)
    paths = []
    for start in starts:
        path = []
        pos = start
        node = maze[start[1]][start[0]]
        path.append(start)
        while node != 4:
            neighbors = get_neighbors(pos)
            for neighbor in neighbors:
                if check_maze_pos(maze, neighbor) and neighbor not in path:
                    path.append(neighbor)
                    pos = neighbor
                    node = maze[pos[1]][pos[0]]
                    break
        paths.append([convert_grid_to_coords(x) for x in path])
    return paths


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
        self.enemy_starts = None
        self.player_list = None
        self.tile_map = None
        self.wall_list = None
        self.enemy_list = None
        self.turret_list = None
        self.slow_beams = None
        self.bullet_list = None
        self.slow_bullets = None
        self.maze = None
        self.frame_count = 0

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
        self.paths = None
        # List of points we checked to see if there is a barrier there
        self.barrier_list = None

        # Used in scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Set the window background color
        self.background_color = arcade.color.AMAZON

    def setup_maze(self):
        maze = two_halls
        self.maze = maze
        for row in range(MAZE_HEIGHT):
            for column in range(MAZE_WIDTH):
                if maze[row][column] == 1:
                    wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", SPRITE_SCALING)
                    wall.center_x = row * SPRITE_SIZE + SPRITE_SIZE / 2
                    wall.center_y = column * SPRITE_SIZE + SPRITE_SIZE / 2
                    self.wall_list.append(wall)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True,
                                           spatial_hash_cell_size=128)
        self.enemy_list = arcade.SpriteList()
        self.turret_list = arcade.SpriteList()
        self.slow_beams = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.slow_bullets = arcade.SpriteList()
        self.setup_maze()
        self.paths = get_paths(self.maze)
        self.setup_turrets()
        self.setup_slow_beams()
        self.enemy_starts = find_in_maze(self.maze, 3)
        self.enemy_starts = [convert_grid_to_coords(p) for p in self.enemy_starts]

        # Set up the player
        resource = ":resources:images/animated_characters/" \
                   "female_person/femalePerson_idle.png"
        self.player = arcade.Sprite(resource, SPRITE_SCALING)
        self.player.center_x = SPRITE_SIZE * 5
        self.player.center_y = SPRITE_SIZE * 1
        self.player_list.append(self.player)

        self.goal_position = (SPRITE_SIZE * 15, SPRITE_SIZE * 4)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         self.wall_list)

    def spawn_turret(self, wall):
        resource = ":resources:images/space_shooter/playerShip1_orange.png"
        turret = Turret(resource, SPRITE_SCALING)
        turret.center_x = wall.center_x
        turret.center_y = wall.center_y
        self.turret_list.append(turret)
        self.wall_list.remove(wall)

    def spawn_slow_beam(self, wall):
        resource = ":resources:images/topdown_tanks/tankBody_blue.png"
        turret = Turret(resource, SPRITE_SCALING)
        turret.center_x = wall.center_x
        turret.center_y = wall.center_y
        self.slow_beams.append(turret)
        self.wall_list.remove(wall)

    def setup_turrets(self):
        assert self.wall_list is not None
        for path in self.paths:
            for i in range(2):
                placement_wall = turret_placement_ai.min_total_distance(path, self.wall_list, TURRET_RANGE)
                self.spawn_turret(placement_wall)

    def setup_slow_beams(self):
        assert self.wall_list is not None
        for i in range(2):
            placement_wall = turret_placement_ai.diff_slow(self.paths[0], self.paths[1], self.wall_list, TURRET_RANGE)
            self.spawn_slow_beam(placement_wall)

    def spawn_enemy(self, path, position):
        # Create the enemy
        enemy = Enemy(":resources:images/animated_characters/robot/robot_idle.png",
                      SPRITE_SCALING_ENEMY, path)
        enemy.center_x = position[0]
        enemy.center_y = position[1]

        # Add the enemy to the enemy list
        self.enemy_list.append(enemy)

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
        self.turret_list.draw()
        self.bullet_list.draw()
        self.slow_beams.draw()
        self.slow_bullets.draw()

        for path in self.paths:
            arcade.draw_line_strip(path, arcade.color.BLUE, 2)

    def closest_enemy(self, pos):
        closest_enemy = None
        dist = None
        for enemy in self.enemy_list:
            if closest_enemy is None:
                closest_enemy = enemy
            new_dist = math.sqrt((pos[0] - enemy.center_x) ** 2 + (pos[1] - enemy.center_y) ** 2)
            if dist is None:
                dist = new_dist
            if new_dist < dist:
                dist = new_dist
                closest_enemy = enemy
        return closest_enemy, dist

    def furthest_enemy(self):
        return max(self.enemy_list, key=lambda e: e.cur_position)

    def get_furthest_target_in_range(self, pos):
        target = None
        path_index = None
        enemy_list = sorted(self.enemy_list, key=lambda e: e.cur_position, reverse=True)
        for enemy in enemy_list:
            aim_point = utilities.lead_target(pos, enemy, BULLET_SPEED)
            if aim_point is None:
                continue
            dist = utilities.get_dist(aim_point, pos)

            if dist < TURRET_RANGE:
                return aim_point

    def update_turrets(self, delta_time, slow=False):
        if slow:
            bullets = self.slow_bullets
            turrets = self.slow_beams
        else:
            bullets = self.bullet_list
            turrets = self.turret_list

        for turret in turrets:
            turret.target = self.get_furthest_target_in_range(turret.position)
            if turret.target is None:
                continue
            start_x = turret.center_x
            start_y = turret.center_y

            dest_x = turret.target[0]
            dest_y = turret.target[1]

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            turret.angle = math.degrees(angle) - 90

            if self.frame_count % 60 == 0:
                resource = ":resources:images/space_shooter/laserBlue01.png"
                bullet = Bullet(resource, BULLET_SCALING, (start_x, start_y), angle)
                if not slow:
                    bullet.color = (255, 0, 0)
                bullets.append(bullet)

        for bullet in bullets:
            for enemy in self.enemy_list:
                if arcade.check_for_collision(bullet, enemy):
                    if slow:
                        enemy.become_slow()
                    else:
                        enemy.take_damage(2)
                    bullet.remove_from_sprite_lists()

        bullets.update()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.frame_count += 1
        self.player.change_x = 0
        self.player.change_y = 0

        # Create the enemy
        if self.frame_count % 30 == 0:
            for path, start in zip(self.paths, self.enemy_starts):
                self.spawn_enemy(path, start)

        if self.up_pressed and not self.down_pressed:
            self.player.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = MOVEMENT_SPEED

        for enemy in self.enemy_list:
            enemy.hit_time -= delta_time
            if enemy.hit_time <= 0:
                enemy.color = (255, 255, 255)
            enemy.slow_time -= delta_time
            if enemy.slow_time <= 0:
                enemy.speed = ENEMY_SPEED
                enemy.color = (255, 255, 255)
        # Update the character
        self.physics_engine.update()
        self.enemy_list.update()
        self.update_turrets(delta_time, True)
        self.update_turrets(delta_time)

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
