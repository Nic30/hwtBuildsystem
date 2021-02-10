from hwtBuildsystem.vivado.config import VivadoConfig
import os

VIVADO_DEPRECATED_FAMILY = [
    "virtex5",
    "virtex4",
    "virtex6",
    "spartan3e",
    "spartan3a",
    "spartan3adsp",
    "spartan3",
    "spartan6",
]


def listChips():
    root = VivadoConfig.getHome()
    root = os.path.join(root, "data", "parts", "xilinx")
    not_family_dirs = ["common", "compxlib", "constraints",
                          "devint", "estimation", "rtl", "templates",
                          "attributes", ] + VIVADO_DEPRECATED_FAMILY
    not_family_dirs = set(not_family_dirs)
    for familyname in os.listdir(root):
        if familyname in not_family_dirs:
            continue
        bsdl = os.path.join(root, familyname, "public", "bsdl")
        for part_bsd in os.listdir(bsdl):
            if part_bsd in ["FileMap.txt", "ReadMe.txt"] or\
                    "dummy_dap" in part_bsd or \
                    "arm_dap" in part_bsd:
                continue
            f = os.path.join(bsdl, part_bsd)
            assert part_bsd.endswith(".bsd"), part_bsd
            assert part_bsd[0] == "x"
            part_bsd = part_bsd[1:-len(".bsd")]
            undr_i = part_bsd.index("_")
            grade = part_bsd[0]
            family = part_bsd[1:3]
            size = part_bsd[3:undr_i]
            package = part_bsd[undr_i + 1:]

            yield f, (grade, family, size, package)
            # print(grade, family, size, package)


def format_option_list(options):
    for o in sorted(options):
        if o[0].isnumeric():
            print(f"_{o:s} = '{o:s}'")
        else:
            print(f"{o:s} = '{o:s}'")


if __name__ == "__main__":
    grades = set()
    families = set()
    sizes = set()
    packages = set()
    for f, (grade, family, size, package) in listChips():
        if family in {'u2', 'vc', 'vm'}:
            continue
            # print(f, family)
        grades.add(grade)
        families.add(family)
        sizes.add(size)
        packages.add(package)
    format_option_list(packages)
