"""Small shims so the animation scripts run on Blender 4.x and 5.x (the Blender 5 layered actions have no Action.fcurves)."""


def fcurves(action):
    """Every F-curve of an action, however this Blender stores them."""
    if hasattr(action, "fcurves"):
        return action.fcurves
    return [fc for layer in action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
