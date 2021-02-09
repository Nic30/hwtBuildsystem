--Copyright 1986-2015 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2015.2 (lin64) Build 1266856 Fri Jun 26 16:35:25 MDT 2015
--Date        : Wed Apr 27 13:22:30 2016
--Host        : nic30-Precision-M4800 running 64-bit Ubuntu 16.04 LTS
--Command     : generate_target test1.bd
--Design      : test1
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity test1 is
  port (
    portIn : in STD_LOGIC;
    portOut : out STD_LOGIC
  );
  attribute CORE_GENERATION_INFO : string;
  attribute CORE_GENERATION_INFO of test1 : entity is "test1,IP_Integrator,{x_ipProduct=Vivado 2015.2,x_ipVendor=xilinx.com,x_ipLibrary=BlockDiagram,x_ipName=test1,x_ipVersion=1.00.a,x_ipLanguage=VHDL,numBlks=0,numReposBlks=0,numNonXlnxBlks=0,numHierBlks=0,maxHierDepth=0,synth_mode=Global}";
  attribute HW_HANDOFF : string;
  attribute HW_HANDOFF of test1 : entity is "test1.hwdef";
end test1;

architecture STRUCTURE of test1 is
  signal portIn_1 : STD_LOGIC;
begin
  portIn_1 <= portIn;
  portOut <= portIn_1;
end STRUCTURE;
