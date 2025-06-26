"""
RDR2 Compendium Navigation Skills

This module contains atomic skills for navigating and searching the compendium in RDR2.
"""

from cradle.config import Config
from cradle.gameio.io_env import IOEnvironment
from cradle.environment import post_skill_wait
from cradle.environment.rdr2.skill_registry import register_skill
from cradle.log import Logger

config = Config()
io_env = IOEnvironment()
logger = Logger()


@register_skill("open_main_menu")
def open_main_menu():
    """
    Open the main game menu by pressing ESC.
    """
    logger.write("Opening main menu with ESC")
    io_env.key_press('esc')
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("navigate_to_progress")
def navigate_to_progress():
    """
    Navigate to and select the PROGRESS menu option.
    """
    logger.write("Navigating to PROGRESS menu")
    # Navigate to PROGRESS option in menu (typically down arrow to navigate)
    io_env.key_press('down')
    io_env.key_press('down')  # May need multiple presses depending on current position
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("select_progress")
def select_progress():
    """
    Select the PROGRESS menu option.
    """
    logger.write("Selecting PROGRESS")
    io_env.key_press('enter')
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("select_compendium")
def select_compendium():
    """
    Select the COMPENDIUM option from the progress menu.
    """
    logger.write("Selecting COMPENDIUM")
    # Navigate to compendium (usually right arrow to move between sections)
    io_env.key_press('right')
    io_env.key_press('enter')
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("select_equipment_category")
def select_equipment_category():
    """
    Select the EQUIPMENT category in the compendium.
    """
    logger.write("Selecting EQUIPMENT category")
    # Navigate to equipment category (usually right arrow)
    io_env.key_press('right')  # Move to EQUIPMENT from default ANIMALS
    io_env.key_press('enter')
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("search_for_camera")
def search_for_camera():
    """
    Search for camera in the equipment grid by navigating through items.
    """
    logger.write("Searching for camera in equipment grid")
    
    # Navigate through the equipment grid to look for camera
    # We'll check several positions since camera could be anywhere in grid
    for i in range(15):  # Check up to 15 positions in the grid
        # Move through the grid systematically
        if i > 0:
            if i % 5 == 0:  # Move to next row every 5 items
                io_env.key_press('down')
            else:
                io_env.key_press('right')
            post_skill_wait(1)  # Short wait between movements
    
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("navigate_equipment_grid")
def navigate_equipment_grid(direction="right"):
    """
    Navigate through the equipment grid using arrow keys.
    
    Parameters:
    - direction: Direction to move ("right", "left", "up", "down")
    """
    logger.write(f"Navigating equipment grid: {direction}")
    
    if direction == "right":
        io_env.key_press('right')
    elif direction == "left":
        io_env.key_press('left')
    elif direction == "up":
        io_env.key_press('up')
    elif direction == "down":
        io_env.key_press('down')
        
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("view_equipment_details")
def view_equipment_details():
    """
    View details of the currently selected equipment item.
    """
    logger.write("Viewing equipment details")
    io_env.key_press('enter')
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("exit_compendium")
def exit_compendium():
    """
    Exit from compendium back to main menu using ESC.
    """
    logger.write("Exiting compendium")
    io_env.key_press('esc')
    post_skill_wait(1)
    io_env.key_press('esc')
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("log_compendium_result")
def log_compendium_result(camera_found=False):
    """
    Log the result of compendium search for camera.
    
    Parameters:
    - camera_found: Boolean indicating if camera was found
    """
    if camera_found:
        result_message = "COMPENDIUM SEARCH RESULT: Camera successfully found in equipment section!"
    else:
        result_message = "COMPENDIUM SEARCH RESULT: Camera not found in equipment section."
        
    logger.write("=" * 60)
    logger.write(result_message)
    logger.write("=" * 60)


__all__ = [
    "open_main_menu",
    "navigate_to_progress", 
    "select_progress",
    "select_compendium",
    "select_equipment_category",
    "search_for_camera",
    "navigate_equipment_grid",
    "view_equipment_details",
    "exit_compendium",
    "log_compendium_result"
] 