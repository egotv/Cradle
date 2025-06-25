from cradle.config import Config
from cradle.gameio.io_env import IOEnvironment
from cradle.environment import post_skill_wait
from cradle.environment.rdr2.skill_registry import register_skill

config = Config()
io_env = IOEnvironment()


@register_skill("contribute_to_camp")
def contribute_to_camp():
    """
    Initiates contribution to camp by pressing 'E' when the "CONTRIBUTE" prompt appears.
    This opens the contribution menu with options for Give Item and Give Money.
    """
    io_env.key_press('e')
    
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("select_give_item")
def select_give_item():
    """
    Ensures the "GIVE ITEM" option is chosen in the contribution menu.
    Implementation notes:
    1. In most cases the cursor starts on "Give Money" or the *previously used* option.
    2. We therefore press the *up-arrow* thrice which guarantees the cursor ends on the
       first entry ("Give Item"), regardless of the initial position, then press *Space*.
    3. This reliably opens the satchel interface instead of the cash-donation screen.
    """

    # Move cursor up thrice – this always lands on the first menu entry
    for _ in range(3):
        io_env.key_press('up')
        post_skill_wait(1)

    # Confirm "Give Item" with Space (as shown in UI)
    io_env.key_press('space')

    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("select_item_to_donate")
def select_item_to_donate():
    """
    Selects an item from the inventory to donate by pressing "enter".
    This highlights the item and shows its details.
    """
    io_env.key_press('enter')
    
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("donate_selected_item")
def donate_selected_item():
    """
    Donates the currently selected item by pressing the DONATE button (Enter).
    This is shown in the bottom right of the donation interface.
    """
    io_env.key_press('space')
    
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("navigate_donation_items_up")
def navigate_donation_items_up():
    """
    Navigate up in the donation item list by pressing the "up" arrow key.
    """
    io_env.key_press('up')


@register_skill("navigate_donation_items_down")
def navigate_donation_items_down():
    """
    Navigate down in the donation item list by pressing the "down" arrow key.
    """
    io_env.key_press('down')


@register_skill("navigate_categories_left")
def navigate_categories_left():
    """
    Navigate left between item categories (the icons at top) by pressing the "left" arrow key.
    Categories include different types of items like valuables, provisions, etc.
    """
    io_env.key_press('left')


@register_skill("navigate_categories_right")
def navigate_categories_right():
    """
    Navigate right between item categories (the icons at top) by pressing the "right" arrow key.
    Categories include different types of items like valuables, provisions, etc.
    """
    io_env.key_press('right')


@register_skill("back_to_donation_menu")
def back_to_donation_menu():
    """
    Go back to the donation menu by pressing the "esc" key (BACK option).
    This returns from item selection to the main donation interface.
    """
    io_env.key_press('esc')
    
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("exit_donation_menu")
def exit_donation_menu():
    """
    Exit the donation menu completely by pressing the "esc" key (LEAVE option).
    """
    io_env.key_press('esc')
    
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("select_platinum_buckle")
def select_platinum_buckle():
    """
    Navigate to and select the Platinum Engraved Buckle in the donation menu.
    Based on the UI, the buckle appears in the valuables category and can be selected directly.
    """
    import time
    
    # The platinum buckle appears to be in the first/default category
    # Navigate to it if not already selected (it may be the first item)
    io_env.key_press('space')  # Select the platinum buckle
    time.sleep(0.5)
    
    # Donate the selected item
    io_env.key_press('space')  # Press DONATE button
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("select_platinum_watch")
def select_platinum_watch():
    """
    Navigate to and select the Platinum Pocket Watch in the donation menu.
    The watch appears to be next to the buckle in the valuables category.
    """
    import time
    
    # Navigate to the platinum pocket watch (should be right next to buckle)
    io_env.key_press('right')  # Move to pocket watch
    time.sleep(0.3)
    
    io_env.key_press('space')  # Select the platinum watch
    time.sleep(0.5)
    
    # Donate the selected item  
    io_env.key_press('space')  # Press DONATE button
    post_skill_wait(config.DEFAULT_POST_ACTION_WAIT_TIME)


@register_skill("move_to_donation_area")
def move_to_donation_area():
    """
    Move towards the donation area in camp using strategic movement.
    The donation box is typically located near the camp's main area.
    """
    from cradle.environment.rdr2.atomic_skills.move import move_forward, turn_left, turn_right
    import time
    
    # Move forward to get closer to camp center
    move_forward(2.0)
    post_skill_wait(1)


@register_skill("turn_to_find_donation_box")
def turn_to_find_donation_box():
    """
    Systematically turn to look for the donation box.
    The donation box should show a "CONTRIBUTE" prompt when approached.
    """
    from cradle.environment.rdr2.atomic_skills.move import turn_left, turn_right
    import time
    
    # Turn right to scan area
    turn_right(90)
    time.sleep(1.5)
    
    # Turn back and go past starting point to scan left side  
    turn_left(180)
    time.sleep(1.5)
    
    # Return to face forward
    turn_right(90)
    post_skill_wait(1)


@register_skill("approach_donation_box")
def approach_donation_box():
    """
    Move closer to the donation box once it's been spotted.
    This should trigger the "CONTRIBUTE" prompt to appear.
    """
    from cradle.environment.rdr2.atomic_skills.move import move_forward
    import time
    
    # Move forward in small increments to approach carefully
    for i in range(4):
        move_forward(0.8)
        time.sleep(0.5)  # Give time for prompts to appear
    
    post_skill_wait(1)


@register_skill("move_around_camp")
def move_around_camp():
    """
    Move around the camp area to search for the donation box.
    Uses a systematic search pattern based on common camp layouts.
    """
    from cradle.environment.rdr2.atomic_skills.move import move_forward, turn_left, turn_right, move_left, move_right
    import time
    
    # Search pattern: move in a widening spiral
    search_moves = [
        ("move_forward", 2.0),
        ("turn_right", 90),
        ("move_forward", 2.5),
        ("turn_right", 90), 
        ("move_forward", 3.0),
        ("turn_right", 90),
        ("move_forward", 2.0),
        ("turn_left", 45),
        ("move_forward", 1.5),
    ]
    
    for move_type, param in search_moves:
        if move_type == "move_forward":
            move_forward(param)
        elif move_type == "turn_right":
            turn_right(param)
        elif move_type == "turn_left":
            turn_left(param)
        elif move_type == "move_left":
            move_left(param)
        elif move_type == "move_right":
            move_right(param)
            
        time.sleep(0.5)  # Brief pause between movements
        
    post_skill_wait(1)


@register_skill("check_for_donation_prompt") 
def check_for_donation_prompt():
    """
    Stand still briefly to check if the "CONTRIBUTE" prompt appears.
    This is a passive skill to give time for the UI to update.
    """
    import time
    time.sleep(1.5)  # Wait to see if prompt appears
    post_skill_wait(1)


__all__ = [
    "contribute_to_camp",
    "select_give_item", 
    "select_item_to_donate",
    "donate_selected_item",
    "navigate_donation_items_up",
    "navigate_donation_items_down", 
    "navigate_categories_left",
    "navigate_categories_right",
    "back_to_donation_menu",
    "exit_donation_menu",
    "select_platinum_buckle",
    "select_platinum_watch",
    "move_to_donation_area",
    "turn_to_find_donation_box", 
    "approach_donation_box",
    "move_around_camp",
    "check_for_donation_prompt"
] 