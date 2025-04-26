import sys
import os
from pathlib import Path
project_root = Path(__file__).parent.resolve()
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
from gui.app import ServerControlApp
import config # Import config to potentially use its paths if needed here


def main():
    """Main function to initialize and run the GUI application."""
    print("Starting Server Control GUI...")

    app = ServerControlApp()
    app.mainloop()

    print("GUI application finished.")


if __name__ == "__main__":
    main()