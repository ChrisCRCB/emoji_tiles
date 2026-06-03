from typing import cast

import cadquery as cq


def _tile(emoji: str, font_size: float = 50, thickness: float = 1) -> cq.Workplane:
    """Return an emoji on a tile."""
    return cq.Workplane("XY").text(
        txt=emoji,
        fontsize=font_size,
        distance=thickness,
        halign="left",
        valign="bottom",
    )


def _backing(
    emoji_shape: cq.Shape,
    thickness: float = 2,
    padding: float = 2,
    fillet: float = 1,
) -> cq.Workplane:
    """Return backing for a tile."""
    bounding_box = emoji_shape.BoundingBox()
    length = bounding_box.xlen + padding * 2
    width = bounding_box.ylen + padding * 2
    box = cq.Workplane("XY").box(
        length=length, width=width, height=thickness, centered=False
    )
    if fillet > 0:
        box = box.edges(">Z").fillet(fillet)
    return box


def emoji_tile(
    emoji: str,
    font_size: float = 50,
    backing_thickness: float = 2,
    text_thickness: float = 1,
    backing_padding: float = 2,
    backing_fillet: float = 1,
) -> cq.Compound:
    """Generate an emoji tile."""
    content = _tile(
        emoji=emoji,
        font_size=font_size,
        thickness=text_thickness,
    ).translate((backing_padding, backing_padding, backing_thickness))
    emoji_shape = cast(cq.Shape, content.val())
    backing = _backing(
        emoji_shape=emoji_shape,
        fillet=backing_fillet,
        padding=backing_padding,
        thickness=backing_thickness,
    )
    return cq.Compound.makeCompound([emoji_shape, cast(cq.Shape, backing.val())])


if __name__ == "__main__":
    cq.exporters.export(
        emoji_tile("😸"),
        "emoji_tile.step",
    )
