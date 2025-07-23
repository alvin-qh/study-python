import numpy as np


def aprint(propmpt: str, /, values: dict[str, np.ndarray]) -> None:
    print(f"{propmpt}")
    for key, value in values.items():
        print(f"- {key}:")
        print(f"{value}", end="")
        print(f", shape={value.shape}")
