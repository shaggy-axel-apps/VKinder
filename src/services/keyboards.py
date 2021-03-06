from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vkinder.settings import BUTTONS


def get_menu_keyboard() -> VkKeyboard:
    keyboard = VkKeyboard(one_time=False, inline=False)
    button_on_line = 0
    for button in BUTTONS:
        if button_on_line == 3:
            keyboard.add_line()
            button_on_line = 0
        keyboard.add_button(button)
        button_on_line += 1
    return keyboard


def get_remove_keyboard(table: str, vk_id: int) -> VkKeyboard:
    kb = VkKeyboard(one_time=False, inline=True)
    kb.add_button(f"Remove from {table}: {vk_id}", color=VkKeyboardColor.NEGATIVE)
    return kb


def get_user_rate_keyboard(vk_id: int) -> VkKeyboard:
    kb = VkKeyboard(one_time=False, inline=True)
    kb.add_button(f"Add to Favorites: {vk_id}", color=VkKeyboardColor.POSITIVE)
    kb.add_button(f"Add to BlackList: {vk_id}", color=VkKeyboardColor.POSITIVE)
    return kb
