import random

random.seed(10)
def generate_new_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def get_shades_of_color(i):
    color = ["#76c284", "#94d09f", "#b3ddbb", "#d1ead6", "#eff8f1"]
    return color[i]

