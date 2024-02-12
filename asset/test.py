import time

# Constants
WIDTH = 384
HEIGHT = 216
SCREEN_CENTER_X = WIDTH // 2
SCREEN_CENTER_Y = HEIGHT // 2
RADIUS = 50
LIGHT = [30, 30, 50]

# Functions
def draw_circle(screen, color, center, radius):
    for y in range(center[1] - radius, center[1] + radius):
        for x in range(center[0] - radius, center[0] + radius):
            if (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2:
                screen.plot(x, y, color)

def normalize(vector):
    length = (vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2) ** 0.5
    return [vector[0] / length, vector[1] / length, vector[2] / length]

# Main loop
while True:
    start_time = time.time()

    # Clear screen
    screen.clear()

    # Draw spheres
    draw_circle(screen, color=Color.RED, center=[200, 200], radius=150)
    draw_circle(screen, color=Color.RED, center=[200, 800], radius=600)
    draw_circle(screen, color=Color.RED, center=[280, 290], radius=100)

    # Update screen
    screen.refresh()

    # Calculate frame rate
    frame_time = time.time() - start_time
    frame_rate = 1 / frame_time
    print("FPS:", frame_rate)

    # Delay for stable frame rate
    if frame_time < 0.033:
        time.sleep(0.033 - frame_time)
