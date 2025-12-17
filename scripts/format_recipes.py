#!/usr/bin/env python3
"""
Format recipes for KDP with centered titles and page breaks.
Each recipe gets its own page with centered title at top.
"""

import re

def format_recipe_title(recipe_num, recipe_name):
    """Create centered, formatted recipe title."""
    return f"""<div style="page-break-after: always;"></div>

<div style="text-align: center;">

# Recipe {recipe_num:02d}

## {recipe_name}

</div>

"""

def main():
    # Read the KDP file
    with open('Mac-and-Cheese-Cookbook-KDP.md', 'r') as f:
        content = f.read()

    # Split content into before recipes, recipes, and after recipes
    # Find where recipes start
    recipes_start_marker = "## THE RECIPES\n\n---\n\n"
    recipes_start_pos = content.find(recipes_start_marker)

    if recipes_start_pos == -1:
        print("Could not find recipes section!")
        return

    before_recipes = content[:recipes_start_pos + len(recipes_start_marker)]

    # Find where back matter starts (Recipe Notes & Journal)
    back_matter_marker = "## Recipe Notes & Journal"
    back_matter_pos = content.find(back_matter_marker)

    if back_matter_pos == -1:
        # Try alternate marker
        back_matter_marker = "## Batch Cooking & Freezing"
        back_matter_pos = content.find(back_matter_marker, recipes_start_pos)

    if back_matter_pos == -1:
        print("Could not find back matter section!")
        return

    recipes_section = content[recipes_start_pos + len(recipes_start_marker):back_matter_pos]
    after_recipes = content[back_matter_pos:]

    # Split recipes by the pattern ### Recipe XX:
    recipe_pattern = r'### Recipe (\d+): (.+?)\n'
    recipes = re.split(recipe_pattern, recipes_section)

    # First element is empty or content before first recipe
    # Then alternating: number, name, content, number, name, content...

    formatted_recipes = []

    # Process recipes (skip first element which is before first recipe)
    i = 1
    while i < len(recipes):
        if i + 2 > len(recipes):
            break

        recipe_num = recipes[i]
        recipe_name = recipes[i + 1]
        recipe_content = recipes[i + 2] if i + 2 < len(recipes) else ""

        # Clean up the content - remove trailing --- and whitespace
        recipe_content = recipe_content.strip()
        if recipe_content.endswith('---'):
            recipe_content = recipe_content[:-3].strip()

        # Format the recipe
        formatted_recipe = format_recipe_title(int(recipe_num), recipe_name)
        formatted_recipe += recipe_content + "\n\n"

        formatted_recipes.append(formatted_recipe)

        i += 3

    # Combine everything
    new_content = before_recipes + "\n".join(formatted_recipes) + "\n\n<div style=\"page-break-after: always;\"></div>\n\n" + after_recipes

    # Write the new file
    with open('Mac-and-Cheese-Cookbook-KDP.md', 'w') as f:
        f.write(new_content)

    print(f"Successfully formatted {len(formatted_recipes)} recipes!")
    print("Each recipe now has:")
    print("- Centered title at top of page")
    print("- Page break before and after")
    print("- Proper spacing for 8x10 format")

if __name__ == "__main__":
    main()
