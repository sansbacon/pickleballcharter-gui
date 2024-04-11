from pathlib import Path
import platformdirs

dirs = platformdirs.user_data_dir("pickleballcharter", "truepickle", ensure_exists=True)
user_data_dir = Path(dirs)