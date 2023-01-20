import PyInstaller.__main__
from pathlib import Path

app_folder = Path(__file__).parent.parent / "app/"
main_file = Path(__file__).parent / "main.py"
PyInstaller.__main__.run(
    [
        str(main_file.resolve()),
        "--onefile",
        "--onedir",
        "--noconsole",
        "--icon=comfort_tracker.ico",
        "--hidden-import=matplotlib.backends.backend_svg",
        "--icon=comfort_tracker.ico",
        # change dir to the project root
        f"--distpath={str(app_folder.resolve())}",
    ]
)
