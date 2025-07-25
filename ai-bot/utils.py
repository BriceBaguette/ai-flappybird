def xyxy_to_xywh(box):
    """
    Convert bbox from (x1, y1, x2, y2) to (x, y, w, h)

    Args:
        box (tuple or list): (x1, y1, x2, y2)

    Returns:
        tuple: (x, y, w, h)
    """
    x1, y1, x2, y2 = box
    x = x1
    y = y1
    w = x2 - x1
    h = y2 - y1
    return (x, y, w, h)

def xywh_to_xyxy(box):
    """
    Convert bbox from (x, y, w, h) to (x1, y1, x2, y2)
    """
    x, y, w, h = map(int, box)
    return (x, y, x + w, y + h)
