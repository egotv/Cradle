# RDR2 Donation Task

This task enables the agent to walk up to the camp donation center in Red Dead Redemption 2 and donate specific valuable items to help fund the gang's activities.

## Task Description

The agent will:
1. Navigate to the camp donation box
2. Press E to CONTRIBUTE when prompted
3. Select "Give Item" from the contribution menu
4. Donate 1 quantity of **Platinum Engraved Buckle**
5. Repeat the process to donate 1 quantity of **Platinum Pocket Watch**
6. Exit the donation interface

## Prerequisites

- Red Dead Redemption 2 must be running
- Player should be in camp near the donation box
- Player must have the required items in inventory:
  - At least 1 Platinum Engraved Buckle
  - At least 1 Platinum Pocket Watch

## Running the Task

To run this donation task, use the following command:

```bash
python runner.py --envConfig ./conf/env_config_rdr2_donation_task.json
```

## Skills Created

### Atomic Skills (donate.py)
- `contribute_to_camp` - Press E when "CONTRIBUTE" prompt appears
- `select_give_item` - Selects "Give Item" from contribution menu
- `select_item_to_donate` - Selects items for donation
- `donate_selected_item` - Presses DONATE button for selected item
- `navigate_donation_items_up/down` - Navigate within item lists
- `navigate_categories_left/right` - Navigate between item categories
- `back_to_donation_menu` - Returns to donation interface
- `exit_donation_menu` - Exits donation interface completely
- `select_platinum_buckle` - Specifically finds and donates Platinum Engraved Buckle
- `select_platinum_watch` - Specifically finds and donates Platinum Pocket Watch

### Composite Skills (donation.py)
- `donate_platinum_items` - Complete donation workflow for both platinum items
- `approach_and_donate_platinum_items` - Navigate to donation center and execute donation

## Configuration

The task uses the environment configuration file `env_config_rdr2_donation_task.json` which:
- Defines the task description and subtasks
- Specifies which skills are available for the donation task
- Includes movement skills for navigation
- Groups donation-specific skills together

## Controls

The donation skills use standard RDR2 controls as shown in the UI:
- **E** - CONTRIBUTE to camp (when prompt appears)
- **Enter** - Select "Give Item" option and DONATE items
- **Arrow Keys** - Navigate between categories (Left/Right) and items (Up/Down)
- **Esc** - BACK to previous menu or LEAVE donation interface

## Notes

- The agent may need position adjustments based on starting location in camp
- Navigation to the donation box assumes a standard camp layout
- The specific item selection logic may need fine-tuning based on inventory organization
- Donation amounts are fixed at 1 quantity per item as requested

## Troubleshooting

1. **Agent doesn't find donation box**: Ensure player is in camp and near the donation area
2. **Items not found**: Verify the Platinum items are in player inventory
3. **Menu navigation issues**: The navigation sequences may need adjustment based on RDR2 version/settings

## Extending the Task

To add more donation items or modify the behavior:
1. Create new skills in `donate.py` for specific items
2. Update the composite skill `donate_platinum_items` to include new items
3. Modify the task description in the environment config as needed 