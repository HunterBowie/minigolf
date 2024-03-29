import os
import random

CURRENT_DIR = os.path.dirname(__file__)


def make_placeholder_names() -> None:
    file_names = os.listdir(CURRENT_DIR)
    for name in file_names:
        if name.endswith(".png"):
            os.rename(os.path.join(CURRENT_DIR, name),
                      os.path.join(CURRENT_DIR, f"placeholder_{random.randint(1, 999999)}.png"))


make_placeholder_names()
file_names = os.listdir(CURRENT_DIR)
i = 0
for name in file_names:
    if name.endswith(".py"):
        continue
    block_id = str(i)
    # if i < 10:
    #     block_id = "0" + str(i)
    os.rename(os.path.join(CURRENT_DIR, name),
              os.path.join(CURRENT_DIR, f"{block_id}.png"))
    i += 1
