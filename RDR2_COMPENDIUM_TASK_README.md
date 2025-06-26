# RDR2 Compendium Search Task

This task enables an AI agent to search for a camera in the RDR2 equipment compendium.

## Task Overview

The agent will:
1. Open the main menu (ESC)
2. Navigate to PROGRESS 
3. Access the COMPENDIUM
4. Select the EQUIPMENT category
5. Systematically search through the equipment grid for a camera
6. Log whether the camera was found or not
7. Exit back to the game

## Task Flow

```
Game → Main Menu → Progress → Compendium → Equipment → Search Grid → Log Result → Return to Game
```

## Skills Created

### Atomic Skills (in `cradle/environment/rdr2/atomic_skills/compendium.py`)

- `open_main_menu()` - Opens the main game menu with ESC
- `navigate_to_progress()` - Navigates to the PROGRESS menu option
- `select_progress()` - Selects the PROGRESS menu option
- `select_compendium()` - Selects the COMPENDIUM from progress menu
- `select_equipment_category()` - Selects EQUIPMENT category in compendium
- `search_for_camera()` - Searches through equipment grid for camera
- `navigate_equipment_grid(direction)` - Navigates grid with arrow keys
- `view_equipment_details()` - Views details of selected equipment
- `exit_compendium()` - Exits compendium back to main menu
- `log_compendium_result(camera_found)` - Logs search results

### Composite Skills (in `cradle/environment/rdr2/composite_skills/compendium_search.py`)

- `search_equipment_compendium()` - Complete workflow for searching compendium
- `search_equipment_grid_for_camera()` - Systematic grid search for camera
- `log_search_result(camera_found)` - Formatted logging of search results
- `navigate_compendium_categories(target_category)` - Navigate to specific category

## Configuration

- **Config File**: `conf/env_config_rdr2_compendium_task.json`
- **Main Skill**: `search_equipment_compendium`
- **Max Steps**: 50
- **Screen Resolution**: 1920x1080

## Usage

Run the task with:

```bash
python runner.py --envConfig ./conf/env_config_rdr2_compendium_task.json
```

## Expected Behavior

1. **Menu Navigation**: Agent opens menu and navigates to compendium
2. **Category Selection**: Selects equipment category
3. **Grid Search**: Systematically searches through equipment grid
4. **Result Logging**: Logs whether camera was found with detailed messages
5. **Cleanup**: Returns to main game

## Success Criteria

- Successfully navigates to equipment compendium
- Searches through equipment grid systematically
- Logs search results clearly
- Returns to game without errors

## Notes

- The task includes simulation logic for finding camera at position (1, 4) in the grid
- Real implementation would use image recognition to identify camera
- All navigation uses keyboard controls (arrow keys, Enter, ESC)
- Logging provides detailed step-by-step information

## Troubleshooting

- If menu navigation fails, check screen resolution settings
- Ensure RDR2 is in focus and not paused
- Verify that compendium is accessible (game progress dependent)
- Check logs for detailed step information

## Related Files

- `cradle/environment/rdr2/atomic_skills/compendium.py`
- `cradle/environment/rdr2/composite_skills/compendium_search.py`
- `conf/env_config_rdr2_compendium_task.json` 