import time
from cradle.config import Config
from cradle.log import Logger
from cradle.environment.rdr2.skill_registry import register_skill
from cradle.environment.rdr2.atomic_skills.donate import (
    move_to_donation_area,
    turn_to_find_donation_box,
    approach_donation_box,
    move_around_camp,
    check_for_donation_prompt,
    contribute_to_camp,
    select_give_item,
    select_platinum_buckle,
    select_platinum_watch,
    exit_donation_menu
)

config = Config()
logger = Logger()


@register_skill("donate_platinum_items")
def donate_platinum_items():
    """
    Complete donation workflow for both Platinum Engraved Buckle and Platinum Pocket Watch.
    This includes finding the donation box, navigating the interface, and donating both items.
    """
    logger.write("Starting complete donation workflow for platinum items")
    
    # Phase 1: Find and approach the donation box
    logger.write("Phase 1: Searching for donation box")
    
    # First, move towards the general camp area
    move_to_donation_area()
    
    # Look around for the donation box
    turn_to_find_donation_box()
    
    # Check if we can see the CONTRIBUTE prompt
    check_for_donation_prompt()
    
    # If we don't see it, move around camp to search
    move_around_camp()
    
    # Try to approach what we think is the donation box
    approach_donation_box()
    
    # Check again for the prompt
    check_for_donation_prompt()
    
    # Phase 2: Attempt to open donation interface
    logger.write("Phase 2: Attempting to open donation interface")
    
    try:
        # Try to contribute to camp (this should open the donation menu)
        contribute_to_camp()
        time.sleep(2)  # Wait for menu to appear
        
        # Select "Give Item" option
        select_give_item()
        time.sleep(2)  # Wait for satchel to open
        
        # Phase 3: Donate first item (Platinum Engraved Buckle)
        logger.write("Phase 3: Donating Platinum Engraved Buckle")
        select_platinum_buckle()
        time.sleep(3)  # Wait for donation to complete and menu to close
        
        # Phase 4: Restart for second item (menu closes after each donation)
        logger.write("Phase 4: Reopening donation interface for second item")
        
        # Need to reopen the donation interface since it closes after each donation
        contribute_to_camp()
        time.sleep(2)
        
        select_give_item() 
        time.sleep(2)
        
        # Phase 5: Donate second item (Platinum Pocket Watch)
        logger.write("Phase 5: Donating Platinum Pocket Watch")
        select_platinum_watch()
        time.sleep(3)
        
        logger.write("Donation workflow completed successfully")
        
    except Exception as e:
        logger.write(f"Error during donation workflow: {e}")
        # Try to exit cleanly if something goes wrong
        try:
            exit_donation_menu()
        except:
            pass


@register_skill("approach_and_donate_platinum_items")
def approach_and_donate_platinum_items():
    """
    Navigate to the camp donation center and donate platinum items.
    This includes movement to the donation area and the complete donation process.
    """
    from cradle.environment.rdr2.atomic_skills.move import move_forward, turn
    
    logger.write("Starting approach and donation sequence...")
    
    # Move towards donation center (may need adjustment based on starting position)
    logger.write("Moving towards donation center...")
    
    # Turn towards donation box (adjust angle as needed)
    turn(45)  # Turn right towards camp center
    time.sleep(0.5)
    
    # Move forward to approach donation box
    move_forward(3)  # Move for 3 seconds
    time.sleep(0.5)
    
    # Fine-tune position if needed
    turn(-15)  # Small left adjustment
    move_forward(1)  # Move closer
    
    # Execute donation process
    donate_platinum_items()
    
    logger.write("Approach and donation sequence completed!")


__all__ = [
    "donate_platinum_items",
    "approach_and_donate_platinum_items"
] 