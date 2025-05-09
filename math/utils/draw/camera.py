import os
from math import ceil
from typing import List, Optional, Union, cast

from pygame import Surface
from pygame.image import save
from pygame.time import Clock


class Camera:
    """定义三维场景中的摄像头类型"""

    shots: Union[List[int], int]
    remaining_shots: Union[List[int], int]
    window: Optional[Surface]

    def __init__(
        self,
        name: str,
        shots: Optional[Union[List[int], int]] = None,
        dir_: str = "figures",
        comic_strip: int = 0,
    ) -> None:
        """初始化摄像头对象

        Args:
            `name` (`str`): 摄像头名称
            `shots` (Optional[Union[List[int], int]], optional): _description_. Defaults to None.
            dir_ (str, optional): _description_. Defaults to "figures".
            comic_strip (int, optional): _description_. Defaults to 0.
        """
        self.dir = os.path.join(os.getcwd(), dir_)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        self.clock = Clock()
        self.name = name

        if not shots:
            shots = []

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
        """_summary_

        Args:
            window (Surface): _description_
        """
        self.window = window

    def is_shooting(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return not (
            self.shots
            and not self.remaining_shots
            and (self.made_comic_strip or not self.comic_strip)
        )

    def indexes(self) -> List[int]:
        """_summary_

        Returns:
            range: _description_
        """
        if isinstance(self.shots, list):
            return list(range(0, len(self.shots)))

        return list(range(0, self.shots))

    def make_comic_strip(self) -> None:
        """_summary_

        https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python
        """
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
        """_summary_

        Returns:
            bool: _description_
        """
        if isinstance(self.remaining_shots, list):
            return (
                bool(self.remaining_shots)
                and self.total_ticks >= self.remaining_shots[0]
            )
        else:
            return self.get_fps() > 0 and (self.remaining_shots > 0)

    def shoot(self) -> None:
        """_summary_"""
        if isinstance(self.remaining_shots, list):
            idx = cast(List[int], self.shots).index(self.remaining_shots[0])
            self.remaining_shots.pop(0)
        else:
            idx = cast(int, self.shots) - self.remaining_shots
            self.remaining_shots = self.remaining_shots - 1

        image_name = os.path.join(self.dir, self.name + str(idx) + ".png")
        save(self.window, image_name)  # type: ignore

    def tick(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
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
        """_summary_

        Returns:
            float: _description_
        """
        return self.clock.get_fps()


default_camera = Camera("default_camera", [])
