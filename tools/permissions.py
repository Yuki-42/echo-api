"""
Tool to convert checkbox permissions to permissions integer.
"""

# Standard Library Imports
from tkinter import BooleanVar, Tk, Variable, ttk
from tkinter.ttk import Frame, Notebook

# Third Party Imports

# Local Imports

# Constants
__all__ = [
    "PermissionsCalculatorWindow"
]


def code_from_list(permissions: list[bool]) -> int:
    """
    Converts a list of boolean permissions to an integer.

    Args:
        permissions (list[bool]): List of boolean permissions.

    Returns:
        int: Integer representation of permissions.
    """
    return int("".join(map(str, map(int, permissions))), 2)


class PermissionsCalculatorWindow:
    """
    Permissions Calculator Window.
    """
    root: Tk
    tab_control: Notebook
    tabs: list[Frame]
    permission_values: list[list[BooleanVar]]
    permission_checkboxes: list[list[ttk.Checkbutton]]
    interface_values: list[Variable]
    interface_boxes: list[ttk.Entry]

    def __init__(self) -> None:
        """
        Initialize the Permissions Calculator Window.
        """
        # Create Tkinter root window
        self.root: Tk = Tk()
        self.root.title = "Disbroad Permissions Tool"

        # Create Tab Control and add tabs
        self.tab_control: Notebook = ttk.Notebook(self.root)
        self.tabs: list[Frame] = [
            ttk.Frame(self.tab_control),
            ttk.Frame(self.tab_control),
            ttk.Frame(self.tab_control)
        ]

        self.tab_control.add(self.tabs[0], text="Guild Permissions")
        self.tab_control.add(self.tabs[1], text="Text Permissions")
        self.tab_control.add(self.tabs[2], text="Voice Permissions")

        self.tab_control.pack(expand=1, fill="both")

        # Add titles for content in tabs
        guild_permissions_tab_label: ttk.Label = ttk.Label(self.tabs[0], text="Guild Permissions")
        guild_permissions_tab_label.grid(column=0, row=0, padx=10, pady=10)

        text_permissions_tab_label: ttk.Label = ttk.Label(self.tabs[1], text="Text Permissions")
        text_permissions_tab_label.grid(column=0, row=0, padx=10, pady=10)

        voice_permissions_tab_label: ttk.Label = ttk.Label(self.tabs[2], text="Voice Permissions")
        voice_permissions_tab_label.grid(column=0, row=0, padx=10, pady=10)

        # Prefill the boolean variables
        self.permission_values: list[list[BooleanVar]] = [
            [BooleanVar(self.tabs[0], False) for _ in range(32)],
            [BooleanVar(self.tabs[1], False) for _ in range(32)],
            [BooleanVar(self.tabs[2], False) for _ in range(32)]
        ]

        self.interface_values: list[Variable] = [
            Variable(self.tabs[0], False),
            Variable(self.tabs[1], False),
            Variable(self.tabs[2], False)
        ]

        # Create the interface boxes for the guild permissions tab
        self.interface_boxes: list[ttk.Entry] = [
            ttk.Entry(self.tabs[0], textvariable=self.interface_values[0]),
            ttk.Entry(self.tabs[1], textvariable=self.interface_values[1]),
            ttk.Entry(self.tabs[2], textvariable=self.interface_values[2])
        ]

        # Add all content for guild permissions tab
        guild_permissions_text: list = [
            "Administrator", "View Audit Logs", "View Insights", "Manage Guild", "Delete Roles",
            "Create Roles", "Manage Roles", "Remove Roles", "Assign Roles", "Delete Channels",
            "Create Channels", "Manage Channels", "Unban Members", "Ban Members", "Kick Members",
            "Manage Members", "Manage Invites", "Delete Emojis", "Create Emojis", "Manage Emojis",
            "Delete Stickers", "Create Stickers", "Manage Stickers", "Delete Webhooks", "Create Webhooks",
            "Manage Webhooks", "Delete Events", "Create Events", "Manage Events", "Send Invites",
            "Not Used", "Not Used"
        ]

        guild_permissions: list[ttk.Checkbutton] = []

        for i, permission in enumerate(guild_permissions_text):
            guild_permissions.append(ttk.Checkbutton(self.tabs[0], text=permission, variable=self.permission_values[0][i], command=self._recalculate_guild_permissions))

        items_in_column_counter: int = 0
        current_row: int = 1
        for i, checkbutton in enumerate(guild_permissions):
            if items_in_column_counter == 8:
                items_in_column_counter = 0
                current_row += 1
            checkbutton.grid(column=items_in_column_counter, row=current_row, padx=3, pady=3, sticky="w")
            items_in_column_counter += 1

        self.permission_checkboxes: list[list[ttk.Checkbutton]] = [guild_permissions]

        # Add all content for text permissions tab
        text_permissions_text: list = [
            "Moderate Private Threads", "Moderate Public Threads", "Moderate Messages", "Moderate Embeds", "Moderate Attachments",
            "Moderate Pins", "Moderate Reactions", "Not Used", "Not Used", "Not Used",
            "Not Used", "Not Used", "Not Used", "Not Used", "Embed Links",
            "Attach Files", "Add Reactions", "Delete Private Threads", "Create Private Threads", "Send TTS Messages",
            "Delete Public Threads", "Create Public Threads", "Use External Animated Stickers", "Use External Stickers", "Use Animated External Emojis",
            "Use External Emojis", "Use Animated Stickers", "Use Stickers", "Use Animated Emojis", "Use Emojis",
            "Delete Messages", "Send Messages"
        ]

        text_permissions: list[ttk.Checkbutton] = []

        for i, permission in enumerate(text_permissions_text):
            text_permissions.append(ttk.Checkbutton(self.tabs[1], text=permission, variable=self.permission_values[1][i], command=self._recalculate_text_permissions))

        items_in_column_counter: int = 0
        current_row: int = 1
        for i, checkbutton in enumerate(text_permissions):
            if items_in_column_counter == 8:
                items_in_column_counter = 0
                current_row += 1
            checkbutton.grid(column=items_in_column_counter, row=current_row, padx=3, pady=3, sticky="w")
            items_in_column_counter += 1

        self.permission_checkboxes.append(text_permissions)

        # Add all content for voice permissions tab
        voice_permissions_text: list = ["Server Deafen Members", "Server Mute Members", "Move Members"]
        voice_permissions_text += ["Not Used" for _ in range(23)]
        voice_permissions_text += ["View Screen Streams", "Stream Camera", "View Cameras", "Use Voice Activity", "Speak", "Listen"]

        voice_permissions: list[ttk.Checkbutton] = []

        for i, permission in enumerate(voice_permissions_text):
            voice_permissions.append(ttk.Checkbutton(self.tabs[2], text=permission, variable=self.permission_values[2][i], command=self._recalculate_voice_permissions))

        items_in_column_counter: int = 0
        current_row: int = 1
        for i, checkbutton in enumerate(voice_permissions):
            if items_in_column_counter == 8:
                items_in_column_counter = 0
                current_row += 1
            checkbutton.grid(column=items_in_column_counter, row=current_row, padx=3, pady=3, sticky="w")
            items_in_column_counter += 1

        self.permission_checkboxes.append(voice_permissions)

        # Draw inputs for all tabs
        for i, entry in enumerate(self.interface_boxes):
            entry.grid(column=0, row=5, padx=10, pady=10)

        # Add select and deselect all buttons for guild permissions
        select_all_guild_permissions_button: ttk.Button = ttk.Button(self.tabs[0], text="Select All", command=self._select_all_guild_permissions)
        select_all_guild_permissions_button.grid(column=0, row=6, padx=10, pady=10)

        deselect_all_guild_permissions_button: ttk.Button = ttk.Button(self.tabs[0], text="Deselect All", command=self._deselect_all_guild_permissions)
        deselect_all_guild_permissions_button.grid(column=1, row=6, padx=10, pady=10)

    def _recalculate_guild_permissions(self) -> None:
        """
        Recalculates the guild permissions.
        """
        permissions: list[bool] = [var.get() for var in self.permission_values[0]]
        self.interface_values[0].set(code_from_list(permissions))

    def _select_all_guild_permissions(self) -> None:
        """
        Selects all guild permissions.
        """
        for var in self.permission_values[0]:
            var.set(True)

        self._recalculate_guild_permissions()

    def _deselect_all_guild_permissions(self) -> None:
        """
        Deselects all guild permissions.
        """
        for var in self.permission_values[0]:
            var.set(False)

        self._recalculate_guild_permissions()

    def _recalculate_text_permissions(self) -> None:
        """
        Recalculates the text permissions.
        """
        permissions: list[bool] = [var.get() for var in self.permission_values[1]]
        self.interface_values[1].set(code_from_list(permissions))

    def _select_all_text_permissions(self) -> None:
        """
        Selects all text permissions.
        """
        for var in self.permission_values[1]:
            var.set(True)

        self._recalculate_text_permissions()

    def _deselect_all_text_permissions(self) -> None:
        """
        Deselects all text permissions.
        """
        for var in self.permission_values[1]:
            var.set(False)

        self._recalculate_text_permissions()

    def _recalculate_voice_permissions(self) -> None:
        """
        Recalculates the voice permissions.
        """
        permissions: list[bool] = [var.get() for var in self.permission_values[2]]
        self.interface_values[2].set(code_from_list(permissions))

    def _select_all_voice_permissions(self) -> None:
        """
        Selects all voice permissions.
        """
        for var in self.permission_values[2]:
            var.set(True)

        self._recalculate_voice_permissions()

    def _deselect_all_voice_permissions(self) -> None:
        """
        Deselects all voice permissions.
        """
        for var in self.permission_values[2]:
            var.set(False)

        self._recalculate_voice_permissions()


if __name__ == "__main__":
    """
    Run tool as a standalone.
    """
    window: PermissionsCalculatorWindow = PermissionsCalculatorWindow()
    window.root.mainloop()
