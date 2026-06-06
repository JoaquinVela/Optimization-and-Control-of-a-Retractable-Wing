import math

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))

def map_value(value, input_min, input_max, output_min, output_max):
    if input_max == input_min:
        return output_min
    
    fraction = (value - input_min) / (input_max - input_min)
    return output_min + fraction * (output_max - output_min)

def deg_to_rad(degrees):
    return degrees * math.pi / 180.0

def draw_centered_text(surface, font, text, color, center):
    rendered = font.render(str(text), True, color)
    rect = rendered.get_rect(center=center)
    surface.blit(rendered, rect)
    return rect

