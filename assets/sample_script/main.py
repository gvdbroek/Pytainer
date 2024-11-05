import submodule


def main(**kwargs):
    import os

    in_file = kwargs.get("in")
    assert os.path.exists(in_file)

    lines = None
    with open(in_file, "r") as f:
        lines = f.readLines()

    out_file - kwargs.get("out")
    with open(out_file, "wb") as f:
        f.writelines(lines)
        f.writelines(submodule.sub_method())
