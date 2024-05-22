#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import hashlib
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess

from hwt.serializer.store_manager import SaveToFilesFlat
from hwt.serializer.verilog import VerilogSerializer
from hwt.serializer.vhdl import Vhdl2008Serializer
from hwt.hwModule import HwModule
from hwt.synth import to_rtl
from hwtBuildsystem.common.executor import ToolExecutor
from hwtBuildsystem.common.project import SynthesisToolProject
from hwtBuildsystem.examples.example_HwModule import ExampleTop0
from hwtBuildsystem.fakeTool.recordingExecutor import RecordingExecutor
from hwtBuildsystem.quartus.api.project import QuartusProject
from hwtBuildsystem.quartus.executor import QuartusExecutor
from hwtBuildsystem.quartus.part import IntelPart
from hwtBuildsystem.vivado.api.project import VivadoProject
from hwtBuildsystem.vivado.executor import VivadoExecutor
from hwtBuildsystem.vivado.part import XilinxPart
from hwtBuildsystem.yosys.executor import YosysExecutor
from hwtBuildsystem.yosys.part import LatticePart
from hwt.synthesizer.dummyPlatform import DummyPlatform


def buildHwModule(exe: ToolExecutor, module: HwModule, root:str, part:tuple,
              targetPlatform=DummyPlatform(),
              synthesize:bool=True, implement:bool=True, writeBitstream:bool=True,
              openGui:bool=False) -> SynthesisToolProject:
    """
    Synthetize unit using bitstream synthesis tool like Xilinx Vivado or Intel Quartus

    :param synthesize: if True the synthtesis/mapping compilation stage will be performed
    :param implement: if True the implementation stage of compilation will be performed
    :param writeBitstream: if True the final bitstream will be generated
    :param openGui: if True the GUI of the tool will be opened on task end
    """
    uName = module._getDefaultName()
    p = exe.project(root, uName)
    # generate project
    if p._exists():
        p._remove()

    p.create()
    p.setPart(part)

    # generate files
    if isinstance(exe, (QuartusExecutor, YosysExecutor)) or (isinstance(exe, RecordingExecutor) and
                                                             isinstance(exe.executor, (QuartusExecutor, YosysExecutor))):
        serializer = VerilogSerializer
    else:
        serializer = Vhdl2008Serializer

    store_manager = SaveToFilesFlat(serializer, root=os.path.join(p.path, 'src'))
    to_rtl(module, store_manager=store_manager, target_platform=targetPlatform)
    p.addFiles(store_manager.files)
    p.setTop(module._name)

    if synthesize:
        p.synthAll()

    if implement:
        p.implemAll()

    if writeBitstream:
        p.writeBitstream()

    if openGui:
        exe.openGui()

    return p


SQL_COMMON_BULD_REPORT_COLUMNS = """
    component_name TEXT NOT NULL,
    component_configuration TEXT NOT NULL,
    revision TEXT NOT NULL,
    build_start timestamp,
    build_end timestamp,
    tool_version TEXT NOT NULL,
    machine_name TEXT NOT NULL,
    part TEXT NOT NULL,
    md5_of_inputs TEXT NOT NULL"""
SQL_COMMON_BULD_REPORT_COLUMNS_QUESTIONMARKS = "?, ?, ?, ?, ?, ?, ?, ?, ?"


def calculateSrcChecksum(project: SynthesisToolProject):
    """
    Calculate md5 checksum of all input source files
    """
    src_files = sorted((Path(project.path) / "src").rglob("*"))
    assert src_files
    h = hashlib.md5()
    for fn in src_files:
        h.update(open(fn, "rb").read())
    return h.hexdigest()


def collect_common_build_report_values(component_name: str,
                                       component_configuration: dict,
                                       build_start:datetime.datetime,
                                       project: SynthesisToolProject):
    """
    :return: tuple of table values as defined in :var:`SQL_COMMON_BULD_REPORT_COLUMNS`
    """
    machine_name = socket.gethostname()
    tool_version = "2020.2"
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode()
    now = datetime.datetime.now()
    conf = json.dumps(component_configuration)
    part = str(project.part)
    md5_of_inputs = calculateSrcChecksum(project)

    return (component_name, conf, revision, build_start, now, tool_version, machine_name, part, md5_of_inputs)


def parse_reports(project: SynthesisToolProject):
    report = project.report()
    synth_report = report.parseUtilizationSynth()
    resorces = synth_report.getBasicResourceReport()
    print(resorces)
    print("Bitstream is in file %s" % (report.bitstreamFile))
    return resorces


def store_yosys_report_in_db(db_cursor, build_start:datetime.datetime, project: VivadoProject, component_name: str):
    db_cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS yosys_builds
        ({SQL_COMMON_BULD_REPORT_COLUMNS:s},
         lut int, ff int, latch int, bram DECIMAL(10, 2), uram DECIMAL(10, 2), dsp int)''')

    r = parse_reports(project)
    common = collect_common_build_report_values(component_name, {}, build_start, project)
    db_cursor.execute(f'''
        INSERT INTO yosys_builds
            VALUES({SQL_COMMON_BULD_REPORT_COLUMNS_QUESTIONMARKS:s}, ?, ?, ?, ?, ?, ?)''',
        (*common, r['lut'], r['ff'], r['latch'], r['bram'], r['uram'], r['dsp']),
    )


def store_vivado_report_in_db(db_cursor, build_start:datetime.datetime, project: VivadoProject, component_name: str):
    db_cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS xilinx_vivado_builds
        ({SQL_COMMON_BULD_REPORT_COLUMNS:s},
         lut int, ff int, latch int, bram DECIMAL(10, 2), uram DECIMAL(10, 2), dsp int)''')

    r = parse_reports(project)
    common = collect_common_build_report_values(component_name, {}, build_start, project)
    db_cursor.execute(f'''
        INSERT INTO xilinx_vivado_builds
            VALUES({SQL_COMMON_BULD_REPORT_COLUMNS_QUESTIONMARKS:s}, ?, ?, ?, ?, ?, ?)''',
        (*common, r['lut'], r['ff'], r['latch'], r['bram'], r['uram'], r['dsp']),
    )


def store_quartus_report_in_db(db_cursor, build_start:datetime.datetime, project: QuartusProject, component_name: str):
    db_cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS intel_quartus_builds
        ({SQL_COMMON_BULD_REPORT_COLUMNS:s},
         alm int, lut int, ff int, latch int, bram_bits DECIMAL(10, 2), dsp int)''')
    common = collect_common_build_report_values(component_name, {}, build_start, project)
    r = parse_reports(project)
    db_cursor.execute(f'''
        INSERT INTO intel_quartus_builds
            VALUES({SQL_COMMON_BULD_REPORT_COLUMNS_QUESTIONMARKS:s}, ?, ?, ?, ?, ?, ?)''',
        (*common, r['alm'], r['lut'], r['ff'], r['latch'], r['bram_bits'], r['dsp']),
    )


if __name__ == "__main__":
    """
    :note: An example of usage
    """
    TEST_TRACES = os.path.join(os.path.dirname(__file__), '..', '..', 'tests')
    # from hwtBuildsystem.fakeTool.recordingExecutor import RecordingExecutor
    # from hwtBuildsystem.fakeTool.replayingExecutor import ReplayingExecutor

    def component_constructor():
        return ExampleTop0()

    conn = sqlite3.connect('build_report.db')
    try:
        c = conn.cursor()
        logComunication = True

        # start = datetime.datetime.now()
        # with RecordingExecutor(YosysExecutor(logComunication=logComunication),
        #                       [],
        #                       os.path.join(TEST_TRACES, "ExampleTop0_synth_trace.yosys_ice40.json")
        #                       ) as executor:
        # # with YosysExecutor(logComunication=logComunication) as executor:
        #    m = component_constructor()
        #    # part = IntelPart("Cyclone V", "5CGXFC7C7F23C8")
        #    # part = IntelPart("Arria 10", "10AX048H1F34E1HG")
        #    part = LatticePart('iCE40', 'up5k', 'sg48')
        #    project = buildHwModule(executor, m, "tmp/yosys", part,
        #                  synthesize=True,
        #                  implement=False,
        #                  writeBitstream=False,
        #                  # openGui=True,
        #                  )
        #    name = ".".join([m.__class__.__module__, m.__class__.__qualname__])
        #    store_yosys_report_in_db(c, start, project, name)
        #    conn.commit()

        start = datetime.datetime.now()
        with RecordingExecutor(
            VivadoExecutor(logComunication=logComunication),
            ['tmp/vivado/ExampleTop0/ExampleTop0.xpr',
             'tmp/vivado/ExampleTop0/ExampleTop0.runs/synth_1/ExampleTop0_utilization_synth.rpt'],
             os.path.join(TEST_TRACES, "ExampleTop0_synth_trace.vivado_kintex7.json"),
            removeAllTracedFilesFirst=True) as executor:
        # with ReplayingExecutor(os.path.join(os.path.dirname(__file__), "../../../tests/ExampleTop0_synth_trace.json")) as v:
        # with VivadoExecutor(logComunication=logComunication) as executor:
            m = component_constructor()
            __pb = XilinxPart
            part = XilinxPart(
                    __pb.Family.kintex7,
                    __pb.Size._160t,
                    __pb.Package.ffg676,
                    __pb.Speedgrade._2)
            project = buildHwModule(executor, m, "tmp/vivado", part,
                          synthesize=True,
                          implement=False,
                          writeBitstream=False,
                          # openGui=True,
                          )
            name = ".".join([m.__class__.__module__, m.__class__.__qualname__])
            store_vivado_report_in_db(c, start, project, name)
            conn.commit()

        # start = datetime.datetime.now()
        # with RecordingExecutor(QuartusExecutor(logComunication=logComunication),
        #                       ['tmp/quartus/ExampleTop0/ExampleTop0.map.rpt'],
        #                       os.path.join(TEST_TRACES, "ExampleTop0_synth_trace.quartus_arria10.json"),
        #                       removeAllTracedFilesFirst=True) as executor:
        # #with QuartusExecutor(logComunication=logComunication) as executor:
        #    m = component_constructor()
        #    # part = IntelPart("Cyclone V", "5CGXFC7C7F23C8")
        #    part = IntelPart("Arria 10", "10AX048H1F34E1HG")
        #    project = buildHwModule(executor, m, "tmp/quartus", part,
        #                  synthesize=True,
        #                  implement=False,
        #                  writeBitstream=False,
        #                  # openGui=True,
        #                  )
        #    name = ".".join([m.__class__.__module__, m.__class__.__qualname__])
        #    store_quartus_report_in_db(c, start, project, name)
        #    conn.commit()
        print("All done")
    finally:
        conn.close()
