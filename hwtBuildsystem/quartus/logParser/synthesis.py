from hwtBuildsystem.vivado.logParser.synthesis import VivadoSynthesisLogParser
import re


class QuartusSynthesisLogParser(VivadoSynthesisLogParser):
    RE_TABLE_HEADER_LINE = re.compile("^\+(-+)\+$")
    RE_TABLE_NAME_LINE = re.compile("^;\s*([^;]*?)\s*;$")

    def parse(self):
        table_top_seen = False
        table_name = None
        table_content = None
        table_column_size = None
        for line in self.lines:
            if table_name:
                if not line or not (line.startswith(';') or line.startswith('+')):
                    # end of table
                    assert table_name not in self.tables, table_name
                    self.tables[table_name] = table_content
                    table_name = None
                    table_content = None
                    table_column_size = None

                else:
                    m_table_top_line = self.RE_TABLE_TOP_LINE.match(line)
                    if m_table_top_line:
                        if table_column_size is None:
                            # first horizontal line with '+' marking the columns
                            assert m_table_top_line
                            table_column_size = self._parseTableSize(line)
                            table_content = []
                        else:
                            pass
                            # horizontal line in the middle of the table
                        continue

                    assert table_column_size, line
                    table_content.append(self._parseTableColumns(line, table_column_size))

            else:
                if table_top_seen:
                    # now we expect the talbe name
                    table_top_seen = False
                    m = self.RE_TABLE_NAME_LINE.match(line)
                    assert m
                    table_name = m.group(1)
                else:
                    table_top_seen = self.RE_TABLE_HEADER_LINE.match(line)

    def getBasicResourceReport(self):
        """
        A small report function which extracts the most important values
        from the tables contained in a report.
        """
        usage = self.tables["Analysis & Synthesis Resource Usage Summary"]
        i = self.indexByRowNameColumnName

        return {
            "alm": int(i(usage, "Estimate of Logic utilization (ALMs needed)", "Usage")),
            "lut": int(i(usage, "Combinational ALUT usage for logic", "Usage")),
            "ff": int(i(usage, "Dedicated logic registers", "Usage")),
            "latch": 0,
            'bram': 0,
            'uram': 0,
            'dsp': int(i(usage, "Total DSP Blocks", "Usage")),
        }
