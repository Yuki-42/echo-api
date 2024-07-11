"""
Tool to convert checkbox permissions to permissions integer.
"""

from tkinter import Tk, Variable, ttk
from tkinter.ttk import Frame, Notebook


def convert_bit_string(permissions: str) -> int:
    """
    Converts a bit string to an integer.

    Args:
        permissions (str): Bit string of permissions.

    Returns:
        int: Integer representation of permissions.
    """
    return int(permissions, 2)


def convert_boolean_list(permissions: list[bool]) -> int:
    """
    Converts a list of boolean permissions to an integer.

    Args:
        permissions (list[bool]): List of boolean permissions.

    Returns:
        int: Integer representation of permissions.
    """
    return int("".join(map(str, map(int, permissions))), 2)


if __name__ == "__main__":
    """
    Run tool as a standalone.
    """
    # Create Tkinter root window
    root: Tk = Tk()
    root.title = "Disbroad Permissions Tool"

    # Create Tab Control and add tabs
    tab_control: Notebook = ttk.Notebook(root)
    guild_permissions_tab: Frame = ttk.Frame(tab_control)
    text_permissions_tab: Frame = ttk.Frame(tab_control)
    voice_permissions_tab: Frame = ttk.Frame(tab_control)

    tab_control.add(guild_permissions_tab, text="Guild Permissions")
    tab_control.add(text_permissions_tab, text="Text Permissions")
    tab_control.add(voice_permissions_tab, text="Voice Permissions")

    tab_control.pack(expand=1, fill="both")

    # Add titles for content in tabs
    guild_permissions_tab_label: ttk.Label = ttk.Label(guild_permissions_tab, text="Guild Permissions")
    guild_permissions_tab_label.grid(column=0, row=0, padx=10, pady=10)

    text_permissions_tab_label: ttk.Label = ttk.Label(text_permissions_tab, text="Text Permissions")
    text_permissions_tab_label.grid(column=0, row=0, padx=10, pady=10)

    voice_permissions_tab_label: ttk.Label = ttk.Label(voice_permissions_tab, text="Voice Permissions")
    voice_permissions_tab_label.grid(column=0, row=0, padx=10, pady=10)

    # Add all checkboxes for guild permissions
    permissions_text: list = [
        "Administrator", "View Audit Logs", "View Insights", "Manage Guild", "Delete Roles",
        "Create Roles", "Manage Roles", "Remove Roles", "Assign Roles", "Delete Channels",
        "Create Channels", "Manage Channels", "Unban Members", "Ban Members", "Kick Members",
        "Manage Members", "Manage Invites", "Delete Emojis", "Create Emojis", "Manage Emojis",
        "Delete Stickers", "Create Stickers", "Manage Stickers", "Delete Webhooks", "Create Webhooks",
        "Manage Webhooks", "Delete Events", "Create Events", "Manage Events", "Send Invites",
        "Not Used", "Not Used"
    ]
    guild_permissions: list[tuple[Variable, ttk.Checkbutton]] = [(Variable(guild_permissions_tab), ttk.Checkbutton(guild_permissions_tab, text=permission, variable=Variable(guild_permissions_tab))) for permission in permissions_text[:32]]

    items_in_column_counter: int = 0
    current_row: int = 1
    for i, (variable, checkbutton) in enumerate(guild_permissions):
        if items_in_column_counter == 8:
            items_in_column_counter = 0
            current_row += 1
        checkbutton.grid(column=items_in_column_counter, row=current_row, padx=3, pady=3)
        items_in_column_counter += 1

    # Run tkinter main loop
    root.mainloop()
