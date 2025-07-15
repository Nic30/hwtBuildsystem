def formatNumberWidthScale(v: int, numFormat="3.1"):
    scale = ""
    highScales = ["K", "M", "G", "T"]
    for s in highScales:
        if v > 1000:
            v /= 1000
            scale = s

    if isinstance(v, int):
        return f"{v}"
    else:
        _format = f"{{v:{numFormat}f}}{{scale:s}}"
        return _format.format(v=v, scale=scale)
        # f"{v:3.1f}{scale:s}"
