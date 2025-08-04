from typing import Any
import numpy as np


def aprint(propmpt: str, /, values: dict[str, Any]) -> None:
    print(f"{propmpt}")
    for key, value in values.items():
        print(f"● {key}:")
        print(f"{value}", end="")
        if isinstance(value, (np.ndarray, np.matrix)):
            print(f", shape={value.shape}")
        else:
            print()
