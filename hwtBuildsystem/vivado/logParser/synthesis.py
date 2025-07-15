#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import islice
import re


class VivadoSynthesisLogParser():
    RE_TABLE_HEADER = re.compile(r"^\d+(\.\d+)*\.?\s+(\S+[^\n]*)")
    RE_TABLE_TOP_LINE = re.compile(r"^\+(-*\+)+")
    RE_SECTION_NAME_UNDERLINE = re.compile(r"^-+")

    def __init__(self, text: str):
        self.lines = text.split("\n")
        self.tables = {}

    def _parseTableSize(self, headerLine):
        offset = 1  # 0 is table boundary
        columns = []
        for column in headerLine.split("+")[1:-1]:
            c_width = len(column)
            columns.append((offset, offset + c_width))
            offset += c_width + 1  # +1 for table |

        return columns

    def _parseTableColumns(self, line, columnSizes):
        return [line[x[0]: x[1]].strip() for x in columnSizes]

    def indexByRowNameColumnName(self, table, rowName, columnName):
        c_i = table[0].index(columnName)
        for row in islice(table, 1, None):
            if row[0] == rowName:
                return row[c_i]
        raise KeyError("The row with such a name not found", rowName)

    def parse(self):
        table_name = None
        table_content = None
        table_column_size = None
        for line in self.lines:
            if table_name:
                if not line and table_content:
                    assert table_name not in self.tables, table_name
                    self.tables[table_name] = table_content
                    table_name = None
                    table_content = None
                    table_column_size = None

                else:
                    m_table_top_line = self.RE_TABLE_TOP_LINE.match(line)
                    if m_table_top_line:
                        if table_column_size is None:
                            table_column_size = self._parseTableSize(line)
                        continue

                    if line and table_content is None:
                        m_underline = self.RE_SECTION_NAME_UNDERLINE.match(line)
                        if m_underline:
                            table_content = []
                            continue
                        else:
                            # false detection
                            table_name = None
                    elif line:
                        assert table_column_size, line
                        table_content.append(self._parseTableColumns(line, table_column_size))

            else:
                m = self.RE_TABLE_HEADER.match(line)
                if m:
                    table_name = m.group(2)

    def getBasicResourceReport(self):
        """
        A small report function which extracts the most important values
        from the tables contained in a report.
        """
        i = self.indexByRowNameColumnName
        try:
            Slice_Logic = self.tables["Slice Logic"]
            lut = int(i(Slice_Logic, "Slice LUTs*", "Used"))
            isVersalAndAfter = False
        except KeyError:
            # versal and newer
            Netlist_Logic = self.tables["Netlist Logic"]
            lut = int(i(Netlist_Logic, "CLB LUTs*", "Used"))
            isVersalAndAfter = True
            Slice_Logic = Netlist_Logic

        ff = int(i(Slice_Logic, "Register as Flip Flop", "Used"))
        latch = int(i(Slice_Logic, "Register as Latch", "Used"))
        if isVersalAndAfter:
            BLOCKRAM = self.tables["BLOCKRAM"]
            bram = float(i(BLOCKRAM, "Block RAM Tile", "Used"))
            ARITHMETIC = self.tables["ARITHMETIC"]
            dsp = int(i(ARITHMETIC, "DSP Slices", "Used"))
        else:
            Memory = self.tables["Memory"]
            bram = float(i(Memory, "Block RAM Tile", "Used"))
            DSP = self.tables["DSP"]
            dsp = int(i(DSP, "DSPs", "Used"))

        return {
            "lut": lut,
            "ff": ff,
            "latch": latch,
            'bram': bram,
            'uram': 0,
            'dsp': dsp,
        }


if __name__ == "__main__":
    with open("../examples/tmp/ExampleTop0/ExampleTop0.runs/synth_1/ExampleTop0_utilization_synth.rpt") as f:
        rp = VivadoSynthesisLogParser(f.read())
        rp.parse()
        for table_name, table in rp.tables.items():
            print(table_name)
            for x in table:
                print(x)
