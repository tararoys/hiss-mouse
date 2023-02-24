from talon import Module, Context, canvas, ctrl, cron, ui, actions, app, imgui, settings
from talon.types import Point2d


import time


mod = Module()


mod.setting(
    "always_show_crosshairs",
    type=bool,
    default=True,
    desc="Toggles whether the crosshairs are always shown or if the crosshairs are only shown when somebody is actively hissing",
)


always_show_crosshairs = settings.get("user.always_show_crosshairs")

print(always_show_crosshairs)

crosshairs_moving = False

crosshairs_tick_job = None

crosshairs_position = Point2d(ctrl.mouse_pos()[0], ctrl.mouse_pos()[1])

direction = 'east'

hissing = ""


crosshairs_canvas = None


ctx = Context()

ctx.matches = r"""
mode: command
"""


def crosshairs_tick_cb():
    global direction

    if crosshairs_moving:

        if direction == "north":
            ctrl.mouse_move(ctrl.mouse_pos()[0], ctrl.mouse_pos()[1] - 10)
        elif direction == "east":
            ctrl.mouse_move(ctrl.mouse_pos()[0] + 10, ctrl.mouse_pos()[1])
        elif direction == "south":
            ctrl.mouse_move(ctrl.mouse_pos()[0], ctrl.mouse_pos()[1] + 10)
        elif direction == "west":
            ctrl.mouse_move(ctrl.mouse_pos()[0] - 10, ctrl.mouse_pos()[1])



def crosshairs_canvas_draw(canvas):
    global direction    
    
    paint= canvas.paint
    paint.color = "00ff0088"
    paint.stroke_width = 2

    # Draw the north line of the cross hair
    if direction == 'north':
        paint.color = "0000ffff"    
        paint.stroke_width = 6
    canvas.draw_points(canvas.PointMode.LINES,
        [Point2d(ctrl.mouse_pos()[0], 0),
            Point2d(ctrl.mouse_pos()[0], ctrl.mouse_pos()[1])])
    paint.color = "00ff0088"
    paint.stroke_width = 2

    
    # Draw the east line of the cross hair
    if direction == 'east':
        paint.color = "0000ffff"    
        paint.stroke_width = 6
    canvas.draw_points(canvas.PointMode.LINES,
        [Point2d(ctrl.mouse_pos()[0], ctrl.mouse_pos()[1]),
            Point2d(ui.screens()[0].rect.width - 1, ctrl.mouse_pos()[1])])
    paint.color = "00ff0088"
    paint.stroke_width = 2

    # Draw the south line of the cross hair
    if direction == 'south':
        paint.color = "0000ffff"    
        paint.stroke_width = 6
    canvas.draw_points(canvas.PointMode.LINES,
        [Point2d(ctrl.mouse_pos()[0], ui.screens()[0].rect.height - 1),
            Point2d(ctrl.mouse_pos()[0], ctrl.mouse_pos()[1])])
    paint.color = "00ff0088"
    paint.stroke_width = 2

    
    # Draw the west line of the cross hair
    if direction == 'west':
        paint.color = "0000ffff"    
        paint.stroke_width = 6
    canvas.draw_points(canvas.PointMode.LINES,
        [Point2d(ctrl.mouse_pos()[0], ctrl.mouse_pos()[1]),
            Point2d(0, ctrl.mouse_pos()[1])])
    paint.color = "00ff0088"
    paint.stroke_width = 2    


@mod.action_class
class HissSpiralActions:
    def spiral_start():
        """Starts the "spiral" mouse"""

        global crosshairs_canvas
        global crosshairs_position
        global crosshairs_tick_job

        if crosshairs_tick_job:
            cron.cancel(crosshairs_tick_job)
        crosshairs_tick_job = cron.interval("40ms", crosshairs_tick_cb)


        if crosshairs_canvas is None:
            crosshairs_canvas = canvas.Canvas(0, 0, ui.screens()[0].rect.width -1 , ui.screens()[0].rect.height -1)
            crosshairs_position = Point2d(ctrl.mouse_pos()[0], ctrl.mouse_pos()[1])
            crosshairs_canvas.register("draw", crosshairs_canvas_draw)


    def spiral_stop():
        """Stops the "spiral" mouse"""
        global crosshairs_canvas
        global always_show_crosshairs
        cron.cancel(crosshairs_tick_job)
        if not always_show_crosshairs:
            crosshairs_canvas.unregister("draw", crosshairs_canvas_draw)
            crosshairs_canvas.hide()
            crosshairs_canvas = None

    def toggle_always_show_crosshairs():
        """ Toggles whether the crosshairs are always shown. If set to true then the crosshairs are always shown, otherwise the crosshairs are only shown while hissing is going on."""        
        global always_show_crosshairs
        if always_show_crosshairs:
            always_show_crosshairs = not always_show_crosshairs
            actions.user.spiral_stop()
        else:
            always_show_crosshairs = not always_show_crosshairs
            actions.user.spiral_start()

    def crosshairs_move(): 
        """move the crosshairs in a 'fed-ex truck circling the block' clockwise fashioin"""
        global crosshairs_position
        global direction
        global crosshairs_moving 
        global hissing
        crosshairs_moving = True
        hissing = "hissing"


    def crosshairs_stop():
        """stop the crosshairs"""
        global direction
        global crosshairs_moving
        global hissing
        crosshairs_moving = False
        if direction == "north":
            direction = "east"
        elif direction == "east":
            direction = "south"
        elif direction == "south":
            direction = "west"
        elif direction == "west":
            direction = "north"
        hissing = ""

