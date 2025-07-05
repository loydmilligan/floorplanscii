import sys
import json

def create_canvas(width, height, fill_char=' '):
    """Initializes a 2D list to act as a drawing canvas."""
    return [[fill_char for _ in range(width)] for _ in range(height)]

def draw_line(canvas, x1, y1, x2, y2, scale_x, scale_y, padding_x, padding_y):
    """Draws a single line on the canvas, merging with existing characters."""
    canvas_height, canvas_width = len(canvas), len(canvas[0])
    x1_c, x2_c = int(x1 * scale_x + padding_x), int(x2 * scale_x + padding_x)
    y1_c, y2_c = int(canvas_height - padding_y - (y1 * scale_y)), int(canvas_height - padding_y - (y2 * scale_y))

    if y1_c == y2_c:
        for x in range(min(x1_c, x2_c), max(x1_c, x2_c) + 1):
            if 0 <= y1_c < canvas_height and 0 <= x < canvas_width:
                if canvas[y1_c][x] in ['|', '+']: canvas[y1_c][x] = '+'
                else: canvas[y1_c][x] = '-'
    elif x1_c == x2_c:
        for y in range(min(y1_c, y2_c), max(y1_c, y2_c) + 1):
            if 0 <= y < canvas_height and 0 <= x1_c < canvas_width:
                if canvas[y][x1_c] in ['-', '+']: canvas[y][x1_c] = '+'
                else: canvas[y][x1_c] = '|'

def place_name(canvas, room, scale_x, scale_y, padding_x, padding_y):
    """Places a room's name in its center."""
    name = room.get('name', '')
    if not name: return
    canvas_height, canvas_width = len(canvas), len(canvas[0])
    inner_width = room['width'] * scale_x - 2
    if inner_width <= 0: return
    display_name = name[:inner_width]
    name_x = int(room['x'] * scale_x + padding_x + 1 + (inner_width - len(display_name)) / 2)
    name_y = int(canvas_height - padding_y - (room['y'] * scale_y) - (room['height'] * scale_y / 2))
    for i, char in enumerate(display_name):
        if 0 <= name_y < canvas_height and 0 <= name_x + i < canvas_width and canvas[name_y][name_x + i] == ' ':
            canvas[name_y][name_x + i] = char

def draw_feature(canvas, feature, scale_x, scale_y, padding_x, padding_y):
    """Draws a feature (door, window, opening) on a wall."""
    canvas_height, canvas_width = len(canvas), len(canvas[0])
    wall, pos = feature['wall'].split('=')
    wall_pos = float(pos)
    
    char_map = {'door': 'D', 'window': 'W', 'opening': 'O'}
    feature_char = char_map.get(feature['type'], '?')

    if wall == 'x':
        x = int(wall_pos * scale_x + padding_x)
        y = int(canvas_height - padding_y - (feature['pos'] * scale_y))
        if 0 <= y < canvas_height and 0 <= x < canvas_width and canvas[y][x] == '|':
            canvas[y][x] = feature_char
    elif wall == 'y':
        x = int(feature['pos'] * scale_x + padding_x)
        y = int(canvas_height - padding_y - (wall_pos * scale_y))
        if 0 <= y < canvas_height and 0 <= x < canvas_width and canvas[y][x] == '-':
            canvas[y][x] = feature_char

def draw_compass(canvas, compass_data, padding_x, padding_y):
    """Draws a simple compass rose."""
    x, y = compass_data['x'] + padding_x, compass_data['y'] + padding_y
    rose = [" N ", "W+E", " S "]
    for i, line in enumerate(rose):
        for j, char in enumerate(line):
            if 0 <= y+i < len(canvas) and 0 <= x+j < len(canvas[0]):
                canvas[y+i][x+j] = char

def draw_axes(canvas, max_x, max_y, scale_x, scale_y, padding_x, padding_y):
    """Draws X and Y axes with numeric labels on the canvas."""
    height, width = len(canvas), len(canvas[0])
    for i in range(height - padding_y):
        if canvas[i][padding_x - 1] == ' ': canvas[i][padding_x - 1] = '.'
    for i in range(padding_x, width):
        if canvas[height - padding_y][i] == ' ': canvas[height - padding_y][i] = '.'
    for y in range(max_y + 1):
        label = str(y)
        y_pos = height - padding_y - (y * scale_y)
        if 0 <= y_pos < height: canvas[y_pos][padding_x - len(label) - 2] = label
    for x in range(max_x + 1):
        label = str(x)
        x_pos = padding_x + (x * scale_x)
        if 0 <= x_pos < width and height - padding_y + 1 < height:
            canvas[height - padding_y + 1][x_pos] = label

def print_canvas(canvas):
    """Prints the canvas to the console."""
    for row in canvas:
        print("".join(row))

if __name__ == '__main__':
    try:
        with open('floorplan.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: floorplan.json not found.", file=sys.stderr)
        sys.exit(1)

    settings = data['settings']
    SCALE_X, SCALE_Y = settings['scale_x'], settings['scale_y']
    PADDING_X, PADDING_Y = settings['padding_x'], settings['padding_y']
    show_axes = settings.get('show_axes', False)
    show_compass = settings.get('show_compass', False) # Read the new setting
    rooms = data['rooms']
    features = data.get('features', {})

    max_x = max(r['x'] + r['width'] for r in rooms)
    max_y = max(r['y'] + r['height'] for r in rooms)
    CANVAS_WIDTH = max_x * SCALE_X + PADDING_X + 15
    CANVAS_HEIGHT = max_y * SCALE_Y + PADDING_Y + 5

    main_canvas = create_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # 1. Draw all walls first
    for room in rooms:
        x, y, w, h = room['x'], room['y'], room['width'], room['height']
        draw_line(main_canvas, x, y, x + w, y, SCALE_X, SCALE_Y, PADDING_X, PADDING_Y)
        draw_line(main_canvas, x, y + h, x + w, y + h, SCALE_X, SCALE_Y, PADDING_X, PADDING_Y)
        draw_line(main_canvas, x, y, x, y + h, SCALE_X, SCALE_Y, PADDING_X, PADDING_Y)
        draw_line(main_canvas, x + w, y, x + w, y + h, SCALE_X, SCALE_Y, PADDING_X, PADDING_Y)

    # 2. Draw features onto the walls
    for feature_type in ['doors', 'windows', 'openings']:
        for feature in features.get(feature_type, []):
            feature['type'] = feature.get('type', feature_type[:-1])
            draw_feature(main_canvas, feature, SCALE_X, SCALE_Y, PADDING_X, PADDING_Y)

    # 3. Draw axes if enabled
    if show_axes:
        draw_axes(main_canvas, max_x, max_y, SCALE_X, SCALE_Y, PADDING_X, PADDING_Y)

    # 4. Place names
    for room in rooms:
        place_name(main_canvas, room, SCALE_X, SCALE_Y, PADDING_X, PADDING_Y)
        
    # 5. Draw compass if enabled
    if show_compass and 'compass' in features:
        draw_compass(main_canvas, features['compass'], PADDING_X, PADDING_Y)

    print("--- Script Output ---")
    print_canvas(main_canvas)
