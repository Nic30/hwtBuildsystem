import re


class YosysSynthesisLogParser():
    RE_TABLE_HEADER_LINE = re.compile(r"^=== (.+) ===$")
    RE_INDENT = re.compile(r"^( *)")
    RE_CELLS = re.compile(r"^ *(.+) (\d+)$")

    """
    :ivar text: text of the log from yosys synthesis run
    """

    def __init__(self, text: str, topName: str):
        self.lines = text.split("\r\n")
        self.topName = topName
        self.tables = {}

    def _parseTableColumns(self, line):
        assert line

        indent = self.RE_INDENT.match(line).group(1)
        indent = len(indent)
        if indent == 3:  # first indent
            key, val = line.split(":")
        else:
            m = self.RE_CELLS.match(line)
            key = m.group(1)
            val = m.group(2)

        key = key.strip()
        val = val.strip()

        return indent, key, val

    def parse(self):
        """
        Parse tables which do look like one in code bellow.
        :note: The items with some indents have key as a tuple of parents and self
            e.g. ('Number of cells', 'SB_LUT4')

        .. code-block:: text

            === ExampleTop0 ===

               Number of wires:                 11
               Number of cells:                 14
                 SB_CARRY                        6
                 SB_LUT4                         8
        """

        table_name = None
        table_content = None
        header_separator = False
        actual_parent = []
        for line in self.lines:
            if table_name:
                if not line:
                    if not header_separator:
                        header_separator = True
                        table_content = []
                        continue

                    # end of table
                    assert table_name not in self.tables, table_name
                    self.tables[table_name] = table_content
                    table_name = None
                    table_content = None
                    actual_parent = []

                else:
                    indent, key, val = self._parseTableColumns(line)
                    while actual_parent and actual_parent[-1][0] >= indent:
                        actual_parent.pop()

                    if actual_parent:
                        key = (*(k for _, k in actual_parent), key)
                    actual_parent.append((indent, key))
                    table_content.append((key, val))

            else:
                m = self.RE_TABLE_HEADER_LINE.match(line)
                if m:
                    table_name = m.group(1)

    def getBasicResourceReport(self):
        """
        A small report function which extracts the most important values
        from the tables contained in a report.
        """
        top = { k: v for k, v in self.tables[self.topName]}
        ic40_ffs = [
                'SB_DFF',
                'SB_DFFE',
                'SB_DFFER',
                'SB_DFFES',
                'SB_DFFESR',
                'SB_DFFESS',
                'SB_DFFN',
                'SB_DFFNE',
                'SB_DFFNER',
                'SB_DFFNES',
                'SB_DFFNESR',
                'SB_DFFNESS',
                'SB_DFFNR',
                'SB_DFFNS',
                'SB_DFFNSR',
                'SB_DFFNSS',
                'SB_DFFR',
                'SB_DFFS',
                'SB_DFFSR',
                'SB_DFFSS',
            ]
        ice40_rams = [
            'SB_RAM40_4K',
            'SB_RAM40_4KNR',
            'SB_RAM40_4KNW',
            'SB_RAM40_4KNRNW'
        ]
        return {
            "lut": int(top.get(('Number of cells', 'SB_LUT4'), 0)),
            'ff': sum(int(top.get(('Number of cells', ff), 0)) for ff in ic40_ffs),
            'bram': sum(int(top.get(('Number of cells', ram), 0)) for ram in ice40_rams),
            'uram': 0,  # no URAMS on chip
            'dsp': int(top.get(('Number of cells', 'SB_MAC16'), 0)),
            'latch': 0,  # the latches do syntetize only to LUT
        }

