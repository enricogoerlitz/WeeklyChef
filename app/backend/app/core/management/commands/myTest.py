import os
from pathlib import Path

data_path = Path(__file__).resolve().parent.parent.parent.parent.parent
print(data_path)
print(os.path.exists(os.path.join(data_path, "data")))
