# app/theme.py
import colorsys

def hex_to_hsl(hex_color: str):
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)   # returns H, L, S
    return h, s, l

def hsl_to_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def generate_shades(hex_color: str, steps: int = 20):
    """Generate 'steps' shades from lightness 100% down to 5%."""
    h, s, _ = hex_to_hsl(hex_color)
    shades = {}
    for i in range(steps):
        lightness = 100 - (i * (95 / (steps - 1)))   # 100% to 5%
        l = lightness / 100.0
        shade_hex = hsl_to_hex(h, s, l)
        percent = 100 - i * 5   # 100, 95, 90, ... 5
        shades[f"{percent}"] = shade_hex
    return shades