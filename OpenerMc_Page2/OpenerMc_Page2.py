
from __future__ import division

import sys
import math
import random
import time
import base64
import os
from PIL import Image
from collections import deque
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse

TICKS_PER_SEC = 60

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

WALKING_SPEED = 4.3 #5
FLYING_SPEED = 11 #15

GRAVITY = 16.0 #20.0
MAX_JUMP_HEIGHT = 1.1 # About the height of a block.
# To derive the formula for calculating jump speed, first solve
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2

if sys.version_info[0] >= 3:
    xrange = range

def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
    ]


def tex_coord(x, y, n=4):
    """ Return the bounding vertices of the texture square.

    """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.

    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result


TEXTURE_STR = "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"
IMAGE_TEXTURE=base64.b64decode(TEXTURE_STR)
TEXTURE_PATH="\\img\\texture.png"
TEXTURE_FOLDER=APPDATA_PATH+"\\img"
if not os.path.exists(TEXTURE_FOLDER):
    os.makedirs(TEXTURE_FOLDER)
TEXTURE_FILE = open(TEXTURE_PATH, "wb")
TEXTURE_FILE.write(IMAGE_TEXTURE)
TEXTURE_FILE.close()

GRASS = tex_coords((1, 0), (0, 1), (0, 0))  #草方块
SAND = tex_coords((1, 1), (1, 1), (1, 1))   #沙子
BRICK = tex_coords((2, 0), (2, 0), (2, 0))  #砖
STONE = tex_coords((2, 1), (2, 1), (2, 1))  #基岩
STONE_1= tex_coords((3, 0), (3, 0) ,(3, 0)) #石头
BASALT= tex_coords((1, 2), (1, 2) ,(0, 2))  #玄武岩
COMMAND_BLOCK= tex_coords((1, 3), (0, 3) ,(2 ,3))   #命令方块

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]


def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    block_position : tuple of ints of len 3

    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)


def sectorize(position):
    """ Returns a tuple representing the sector for the given `position`.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    sector : tuple of len 3

    """
    x, y, z = normalize(position)
    x, y, z = x // SECTOR_SIZE, y // SECTOR_SIZE, z // SECTOR_SIZE
    return (x, 0, z)


class Model(object):

    def __init__(self):

        # A Batch is a collection of vertex lists for batched rendering.
        self.batch = pyglet.graphics.Batch()

        # A TextureGroup manages an OpenGL texture.
        self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())

        # A mapping from position to the texture of the block at that position.
        # This defines all the blocks that are currently in the world.
        self.world = {}

        # Same mapping as `world` but only contains blocks that are shown.
        self.shown = {}

        # Mapping from position to a pyglet `VertextList` for all shown blocks.
        self._shown = {}

        # Mapping from sector to a list of positions inside that sector.
        self.sectors = {}

        # Simple function queue implementation. The queue is populated with
        # _show_block() and _hide_block() calls
        self.queue = deque()

        self._initialize()

    def _initialize(self):
        """ Initialize the world by placing all the blocks.

        """
        n = 80  # 1/2 width and height of world
        s = 1  # step size
        y = 0  # initial y height
        for x in xrange(-n, n + 1, s):
            for z in xrange(-n, n + 1, s):
                # create a layer stone an grass everywhere.
                self.add_block((x, y - 2, z), GRASS, immediate=False)
                self.add_block((x, y - 3, z), STONE, immediate=False)
                if x in (-n, n) or z in (-n, n):
                    # create outer walls.
                    for dy in xrange(-2, 3):
                        self.add_block((x, y + dy, z), STONE, immediate=False)

        # generate the hills randomly
        o = n - 10
        for _ in xrange(120):
            a = random.randint(-o, o)  # x position of the hill
            b = random.randint(-o, o)  # z position of the hill
            c = -1  # base of the hill
            h = random.randint(1, 6)  # height of the hill
            s = random.randint(4, 8)  # 2 * s is the side length of the hill
            d = 1  # how quickly to taper off the hills
            t = random.choice([GRASS, SAND, BRICK, STONE_1, BASALT])
            for y in xrange(c, c + h):
                for x in xrange(a - s, a + s + 1):
                    for z in xrange(b - s, b + s + 1):
                        if (x - a) ** 2 + (z - b) ** 2 > (s + 1) ** 2:
                            continue
                        if (x - 0) ** 2 + (z - 0) ** 2 < 5 ** 2:
                            continue
                        self.add_block((x, y, z), t, immediate=False)
                s -= d  # decrement side length so hills taper off

    def hit_test(self, position, vector, max_distance=8):
        """ Line of sight search from current position. If a block is
        intersected it is returned, along with the block previously in the line
        of sight. If no block is found, return None, None.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check visibility from.
        vector : tuple of len 3
            The line of sight vector.
        max_distance : int
            How many blocks away to search for a hit.

        """
        m = 8
        x, y, z = position
        dx, dy, dz = vector
        previous = None
        for _ in xrange(max_distance * m):
            key = normalize((x, y, z))
            if key != previous and key in self.world:
                return key, previous
            previous = key
            x, y, z = x + dx / m, y + dy / m, z + dz / m
        return None, None

    def exposed(self, position):
        """ Returns False is given `position` is surrounded on all 6 sides by
        blocks, True otherwise.

        """
        x, y, z = position
        for dx, dy, dz in FACES:
            if (x + dx, y + dy, z + dz) not in self.world:
                return True
        return False

    def add_block(self, position, texture, immediate=True):
        """ Add a block with the given `texture` and `position` to the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to add.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.
        immediate : bool
            Whether or not to draw the block immediately.

        """
        if position in self.world:
            self.remove_block(position, immediate)
        self.world[position] = texture
        self.sectors.setdefault(sectorize(position), []).append(position)
        if immediate:
            if self.exposed(position):
                self.show_block(position)
            self.check_neighbors(position)

    def remove_block(self, position, immediate=True):
        """ Remove the block at the given `position`.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to remove.
        immediate : bool
            Whether or not to immediately remove block from canvas.

        """
        del self.world[position]
        self.sectors[sectorize(position)].remove(position)
        if immediate:
            if position in self.shown:
                self.hide_block(position)
            self.check_neighbors(position)

    def check_neighbors(self, position):
        """ Check all blocks surrounding `position` and ensure their visual
        state is current. This means hiding blocks that are not exposed and
        ensuring that all exposed blocks are shown. Usually used after a block
        is added or removed.

        """
        x, y, z = position
        for dx, dy, dz in FACES:
            key = (x + dx, y + dy, z + dz)
            if key not in self.world:
                continue
            if self.exposed(key):
                if key not in self.shown:
                    self.show_block(key)
            else:
                if key in self.shown:
                    self.hide_block(key)

    def show_block(self, position, immediate=True):
        """ Show the block at the given `position`. This method assumes the
        block has already been added with add_block()

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        immediate : bool
            Whether or not to show the block immediately.

        """
        texture = self.world[position]
        self.shown[position] = texture
        if immediate:
            self._show_block(position, texture)
        else:
            self._enqueue(self._show_block, position, texture)

    def _show_block(self, position, texture):
        """ Private implementation of the `show_block()` method.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to show.
        texture : list of len 3
            The coordinates of the texture squares. Use `tex_coords()` to
            generate.

        """
        x, y, z = position
        vertex_data = cube_vertices(x, y, z, 0.5)
        texture_data = list(texture)
        # create vertex list
        # FIXME Maybe `add_indexed()` should be used instead
        self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
            ('v3f/static', vertex_data),
            ('t2f/static', texture_data))

    def hide_block(self, position, immediate=True):
        """ Hide the block at the given `position`. Hiding does not remove the
        block from the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position of the block to hide.
        immediate : bool
            Whether or not to immediately remove the block from the canvas.

        """
        self.shown.pop(position)
        if immediate:
            self._hide_block(position)
        else:
            self._enqueue(self._hide_block, position)

    def _hide_block(self, position):
        """ Private implementation of the 'hide_block()` method.

        """
        self._shown.pop(position).delete()

    def show_sector(self, sector):
        """ Ensure all blocks in the given sector that should be shown are
        drawn to the canvas.

        """
        for position in self.sectors.get(sector, []):
            if position not in self.shown and self.exposed(position):
                self.show_block(position, False)

    def hide_sector(self, sector):
        """ Ensure all blocks in the given sector that should be hidden are
        removed from the canvas.

        """
        for position in self.sectors.get(sector, []):
            if position in self.shown:
                self.hide_block(position, False)

    def change_sectors(self, before, after):
        """ Move from sector `before` to sector `after`. A sector is a
        contiguous x, y sub-region of world. Sectors are used to speed up
        world rendering.

        """
        before_set = set()
        after_set = set()
        pad = 4
        for dx in xrange(-pad, pad + 1):
            for dy in [0]:  # xrange(-pad, pad + 1):
                for dz in xrange(-pad, pad + 1):
                    if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
                        continue
                    if before:
                        x, y, z = before
                        before_set.add((x + dx, y + dy, z + dz))
                    if after:
                        x, y, z = after
                        after_set.add((x + dx, y + dy, z + dz))
        show = after_set - before_set
        hide = before_set - after_set
        for sector in show:
            self.show_sector(sector)
        for sector in hide:
            self.hide_sector(sector)

    def _enqueue(self, func, *args):
        """ Add `func` to the internal queue.

        """
        self.queue.append((func, args))

    def _dequeue(self):
        """ Pop the top function from the internal queue and call it.

        """
        func, args = self.queue.popleft()
        func(*args)

    def process_queue(self):
        """ Process the entire queue while taking periodic breaks. This allows
        the game loop to run smoothly. The queue contains calls to
        _show_block() and _hide_block() so this method should be called if
        add_block() or remove_block() was called with immediate=False

        """
        start = time.perf_counter()
        while self.queue and time.perf_counter() - start < 1.0 / TICKS_PER_SEC:
            self._dequeue()

    def process_entire_queue(self):
        """ Process the entire queue with no breaks.

        """
        while self.queue:
            self._dequeue()


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        # Whether or not the window exclusively captures the mouse.
        self.exclusive = False

        # When flying gravity has no effect and speed is increased.
        self.flying = False

        # Strafing is moving lateral to the direction you are facing,
        # e.g. moving to the left or right while continuing to face forward.
        #
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise.
        self.strafe = [0, 0]

        # Current (x, y, z) position in the world, specified with floats. Note
        # that, perhaps unlike in math class, the y-axis is the vertical axis.
        self.position = (0, 0, 0)

        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (0, 0)

        # Which sector the player is currently in.
        self.sector = None

        # The crosshairs at the center of the screen.
        self.reticle = None

        # Velocity in the y (upward) direction.
        self.dy = 0

        # A list of blocks the player can place. Hit num keys to cycle.
        self.inventory = [BRICK, GRASS, SAND, STONE_1, BASALT, COMMAND_BLOCK, STONE]

        # The current block the user can place. Hit num keys to cycle.
        self.block = self.inventory[0]

        # Convenience list of num keys.
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]

        # Instance of the model that handles the world.
        self.model = Model()

        # The label that is displayed in the top left of the canvas.
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
            color=(0, 0, 0, 255))

        # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)

    def set_exclusive_mouse(self, exclusive):
        """ If `exclusive` is True, the game will capture the mouse, if False
        the game will ignore the mouse.

        """
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive

    def get_sight_vector(self):
        """ Returns the current line of sight vector indicating the direction
        the player is looking.

        """
        x, y = self.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        """ Returns the current motion vector indicating the velocity of the
        player.

        Returns
        -------
        vector : tuple of len 3
            Tuple containing the velocity in x, y, and z respectively.

        """
        if any(self.strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.strafe[1]:
                    # Moving left or right.
                    dy = 0.0
                    m = 1
                if self.strafe[0] > 0:
                    # Moving backwards.
                    dy *= -1
                # When you are flying up or down, you have less left and right
                # motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)

    def update(self, dt):
        """ This method is scheduled to be called repeatedly by the pyglet
        clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        self.model.process_queue()
        sector = sectorize(self.position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in xrange(m):
            self._update(dt / m)

    def _update(self, dt):
        """ Private implementation of the `update()` method. This is where most
        of the motion logic lives, along with gravity and collision detection.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        # walking
        speed = FLYING_SPEED if self.flying else WALKING_SPEED
        d = dt * speed # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for gravity.
        dx, dy, dz = dx * d, dy * d, dz * d
        # gravity
        if not self.flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            self.dy -= dt * GRAVITY
            self.dy = max(self.dy, -TERMINAL_VELOCITY)
            dy += self.dy * dt
        # collisions
        x, y, z = self.position
        x, y, z = self.collide((x + dx, y + dy, z + dz), PLAYER_HEIGHT)
        self.position = (x, y, z)

    def collide(self, position, height):
        """ Checks to see if the player at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        height : int or float
            The height of the player.

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.

        """
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall grass. If >= .5, you'll fall through the ground.
        pad = 0.25
        p = list(position)
        np = normalize(position)
        for face in FACES:  # check all surrounding blocks
            for i in xrange(3):  # check each dimension independently
                if not face[i]:
                    continue
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in xrange(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in self.model.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.
                        self.dy = 0
                    break
        return tuple(p)

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when a mouse button is pressed. See pyglet docs for button
        amd modifier mappings.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        button : int
            Number representing mouse button that was clicked. 1 = left button,
            4 = right button.
        modifiers : int
            Number representing any modifying keys that were pressed when the
            mouse button was clicked.

        """
        if self.exclusive:
            vector = self.get_sight_vector()
            block, previous = self.model.hit_test(self.position, vector)
            if (button == mouse.RIGHT) or \
                    ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                # ON OSX, control + left click = right click.
                if previous:
                    self.model.add_block(previous, self.block)
            elif button == pyglet.window.mouse.LEFT and block:
                texture = self.model.world[block]
                if texture != STONE:
                    self.model.remove_block(block)
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called when the player moves the mouse.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        dx, dy : float
            The movement of the mouse.

        """
        if self.exclusive:
            m = 0.15
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)

    def on_key_press(self, symbol, modifiers):
        """ Called when the player presses a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if symbol == key.W:
            self.strafe[0] -= 1
        elif symbol == key.S:
            self.strafe[0] += 1
        elif symbol == key.A:
            self.strafe[1] -= 1
        elif symbol == key.D:
            self.strafe[1] += 1
        elif symbol == key.SPACE:
            if self.dy == 0:
                self.dy = JUMP_SPEED
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(False)
        elif symbol == key.TAB:
            self.flying = not self.flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]

    def on_key_release(self, symbol, modifiers):
        """ Called when the player releases a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if symbol == key.W:
            self.strafe[0] += 1
        elif symbol == key.S:
            self.strafe[0] -= 1
        elif symbol == key.A:
            self.strafe[1] += 1
        elif symbol == key.D:
            self.strafe[1] -= 1

    def on_resize(self, width, height):
        """ Called when the window is resized to a new `width` and `height`.

        """
        # label
        self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

    def set_2d(self):
        """ Configure OpenGL to draw in 2d.

        """
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, max(1, width), 0, max(1, height), -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        """ Configure OpenGL to draw in 3d.

        """
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        viewport = self.get_viewport_size()
        glViewport(0, 0, max(1, viewport[0]), max(1, viewport[1]))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
        x, y, z = self.position
        glTranslatef(-x, -y, -z)

    def on_draw(self):
        """ Called by pyglet to draw the canvas.

        """
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.draw_focused_block()
        self.set_2d()
        self.draw_label()
        self.draw_reticle()

    def draw_focused_block(self):
        """ Draw black edges around the block that is currently under the
        crosshairs.

        """
        vector = self.get_sight_vector()
        block = self.model.hit_test(self.position, vector)[0]
        if block:
            x, y, z = block
            vertex_data = cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def draw_label(self):
        """ Draw the label in the top left of the screen.

        """
        x, y, z = self.position
        self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
            pyglet.clock.get_fps(), x, y, z,
            len(self.model._shown), len(self.model.world))
        self.label.draw()

    def draw_reticle(self):
        """ Draw the crosshairs in the center of the screen.

        """
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)


def setup_fog():
    """ Configure the OpenGL fog properties.

    """
    # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
    # post-texturing color."
    glEnable(GL_FOG)
    # Set the fog color.
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
    # Say we have no preference between rendering speed and quality.
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    # Specify the equation used to compute the blending factor.
    glFogi(GL_FOG_MODE, GL_LINEAR)
    # How close and far away fog starts and ends. The closer the start and end,
    # the denser the fog in the fog range.
    glFogf(GL_FOG_START, 20.0)
    glFogf(GL_FOG_END, 60.0)


def setup():
    """ Basic OpenGL configuration.

    """
    # Set the color of "clear", i.e. the sky, in rgba.
    glClearColor(0.5, 0.69, 1.0, 1)
    # Enable culling (not rendering) of back-facing facets -- facets that aren't
    # visible to you.
    glEnable(GL_CULL_FACE)
    # Set the texture minification/magnification function to GL_NEAREST (nearest
    # in Manhattan distance) to the specified texture coordinates. GL_NEAREST
    # "is generally faster than GL_LINEAR, but it can produce textured images
    # with sharper edges because the transition between texture elements is not
    # as smooth."
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    setup_fog()


def main():
    window = Window(width=800, height=600, caption='开了opener-第二关', resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    window.set_exclusive_mouse(True)
    setup()
    pyglet.app.run()


if __name__ == '__main__':
    main()