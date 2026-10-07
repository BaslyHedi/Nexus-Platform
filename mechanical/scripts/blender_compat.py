"""Small shims so the animation scripts run on Blender 4.x and 5.x (the Blender 5 layered actions have no Action.fcurves)."""


def fcurves(action):
    """Every F-curve of an action, however this Blender stores them."""
    if hasattr(action, "fcurves"):
        return action.fcurves
    return [fc for layer in action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]


def mp4(scene):
    """Render to an H.264 MP4: Blender 5 asks for a video media type before 'FFMPEG' is a file format."""
    img = scene.render.image_settings
    if hasattr(img, "media_type"):
        img.media_type = 'VIDEO'
    img.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
