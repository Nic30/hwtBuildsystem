#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import islice
import re


class VivadoSynthesisLogParser():
    RE_TABLE_HEADER = re.compile("^\d+(\.\d+)*\.?\s+(\S+[^\n]*)")
    RE_TABLE_TOP_LINE = re.compile("^\+(-*\+)+")
    RE_SECTION_NAME_UNDERLINE = re.compile("^-+")

    def __init__(self, text):
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
        raise KeyError("The row with such a name not found", columnName)

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
        Slice_Logic = self.tables["Slice Logic"]
        Memory = self.tables["Memory"]
        DSP = self.tables["DSP"]
        i = self.indexByRowNameColumnName

        return {
            "lut": int(i(Slice_Logic, "Slice LUTs*", "Used")),
            "ff": int(i(Slice_Logic, "Register as Flip Flop", "Used")),
            "latch": int(i(Slice_Logic, "Register as Latch", "Used")),
            'bram': float(i(Memory, "Block RAM Tile", "Used")),
            'uram': 0,
            'dsp': int(i(DSP, "DSPs", "Used")),
        }


if __name__ == "__main__":
    with open("../examples/tmp/SimpleUnitAxiStreamTop/SimpleUnitAxiStreamTop.runs/synth_1/SimpleUnitAxiStreamTop_utilization_synth.rpt") as f:
        rp = VivadoSynthesisLogParser(f.read())
        rp.parse()
        for table_name, table in rp.tables.items():
            print(table_name)
            for x in table:
                print(x)
