# FloorplanASCII

FloorplanASCII is a Python script that generates a text-based ASCII art representation of a floorplan from a structured JSON data file. It is designed to create clear, readable, and customizable layouts directly in the terminal, suitable for technical diagrams, smarthome dashboards, or any application where a simple visual representation is needed without a graphical interface.

The script is architected to be data-driven, meaning the entire layout, including room dimensions, features like doors and windows, and display settings, is controlled by the `floorplan.json` file, not the code.

## Features

-   **Data-Driven Layouts:** Define all rooms and their dimensions in a simple JSON file.
-   **Cohesive Wall Merging:** Automatically merges adjacent walls to create a single, connected structure.
-   **Detailed Feature Placement:** Precisely place doors, windows, and openings on specific walls.
-   **Customizable Rendering:** Control the aspect ratio and scale of the output using `scale_x` and `scale_y` settings.
-   **Toggleable UI Elements:** Show or hide a coordinate grid and a compass rose for debugging or cleaner final outputs.

## Usage

To generate a floorplan, you need Python 3 installed. No external libraries are required.

1.  **Save the Files:** Ensure both `floorplanscii.py` (the script) and `floorplan.json` (the data) are in the same directory.
2.  **Configure the Layout:** Edit the `floorplan.json` file to define your rooms, features, and settings.
3.  **Run the Script:** Open a terminal or command prompt, navigate to the directory containing the files, and execute the script:

    ```bash
    python floorplanscii.py
    ```

The script will read the `floorplan.json` file and print the resulting ASCII art floorplan to the console.

## The `floorplan.json` Structure

This file is the heart of the project. It's divided into three main sections: `metadata`, `settings`, and `rooms`.

### `metadata`

An object containing descriptive information about the floorplan.

-   `title`: The main title of the floorplan.
-   `description`: A brief description of the project.
-   `street_address1`, `street_address2`, `city`, `state`, `zipcode`: The physical address associated with the layout.

### `settings`

An object that controls the rendering of the ASCII art.

-   `scale_x`, `scale_y`: Integers that define the aspect ratio. A character in a terminal is taller than it is wide, so a 3:1 or 2:1 ratio is often needed for visually square output.
-   `padding_x`, `padding_y`: Integers that define the margin around the drawing on the canvas.
-   `show_axes`: A boolean (`true` or `false`) to toggle the visibility of the coordinate grid.
-   `show_compass`: A boolean (`true` or `false`) to toggle the visibility of the compass rose.

### `rooms`

An array of objects, where each object represents a single room or space.

-   `name`: The string to be displayed in the center of the room.
-   `x`, `y`: The integer coordinates of the room's bottom-left corner on the grid.
-   `width`, `height`: The integer dimensions of the room in grid units.

### `features`

An object containing arrays of features to be drawn onto the walls of the rooms.

-   **`compass`**: An object defining the position of the compass rose.
    -   `x`, `y`: The grid coordinates for the top-left of the compass.
-   **`doors`**, **`windows`**, **`openings`**: Arrays of feature objects.
    -   `wall`: A string defining the wall the feature lies on. Format is `"x=N"` for a vertical wall or `"y=N"` for a horizontal wall.
    -   `pos`: A float defining the center point of the feature along that wall. This is a `y` coordinate for vertical walls and an `x` coordinate for horizontal walls.
