import os
from math import ceil
from typing import List, Union, cast

from pygame import Surface
from pygame.image import save
from pygame.time import Clock


class Camera:
    shots: Union[List[int], int]
    remaining_shots: Union[List[int], int]

    def __init__(
        self,
        name: str,
        shots: Union[List[int], int] = [],
        dir: str = "figures",
        comic_strip: int = 0,
    ) -> None:
        self.dir = os.path.join(os.getcwd(), dir)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.clock = Clock()
        self.name = name

        if isinstance(shots, list):
            shots = sorted(shots)
            self.shots = shots
            self.remaining_shots = shots
        else:
            self.shots = shots
            self.remaining_shots = shots

        self.total_ticks = 0
        self.made_comic_strip = False
        self.comic_strip = comic_strip

    def set_window(self, window: Surface) -> None:
        self.window = window

    def is_shooting(self) -> bool:
        return not (
            self.shots
            and not self.remaining_shots
            and (self.made_comic_strip or not self.comic_strip)
        )

    def indexes(self) -> range:
        if isinstance(self.shots, list):
            return range(0, len(self.shots))
        else:
            return range(0, self.shots)

    def make_comic_strip(self) -> None:
        # https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
        import sys

        from PIL import Image

        image_files = [
            os.path.join(self.dir, self.name + str(idx) + ".png")
            for idx in self.indexes()
        ]

        images = list(map(Image.open, image_files))
        width, height = images[0].size

        total_width = width * self.comic_strip
        max_height = height * int(ceil(len(images) / float(self.comic_strip)))

        new_im = Image.new("RGB", (total_width, max_height))

        for i, im in enumerate(images):
            x_offset = (i % self.comic_strip) * width
            y_offset = (i / self.comic_strip) * height
            print("offsets", (x_offset, y_offset))
            new_im.paste(im, (x_offset, int(y_offset)))

        new_im.save(os.path.join(self.dir, self.name + "_comic_strip.png"))
        self.made_comic_strip = True

    def should_shoot(self) -> bool:
        if isinstance(self.remaining_shots, list):
            return (
                bool(self.remaining_shots)
                and self.total_ticks >= self.remaining_shots[0]
            )
        else:
            return self.get_fps() > 0 and (self.remaining_shots > 0)

    def shoot(self) -> None:
        if isinstance(self.remaining_shots, list):
            idx = cast(List[int], self.shots).index(self.remaining_shots[0])
            self.remaining_shots.pop(0)
        else:
            idx = cast(int, self.shots) - self.remaining_shots
            self.remaining_shots = self.remaining_shots - 1

        image_name = os.path.join(self.dir, self.name + str(idx) + ".png")
        save(self.window, image_name)

    def tick(self) -> int:
        res = self.clock.tick()
        self.total_ticks += res
        if self.should_shoot():
            self.shoot()
        elif (
            self.comic_strip and not self.made_comic_strip and not self.remaining_shots
        ):
            self.make_comic_strip()

        return res

    def get_fps(self) -> float:
        return self.clock.get_fps()


default_camera = Camera("default_camera", [])
