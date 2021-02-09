--Copyright 1986-2015 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2015.2 (lin64) Build 1266856 Fri Jun 26 16:35:25 MDT 2015
--Date        : Wed Apr 27 13:27:17 2016
--Host        : nic30-Precision-M4800 running 64-bit Ubuntu 16.04 LTS
--Command     : generate_target test1_wrapper.bd
--Design      : test1_wrapper
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity test1_wrapper is
  port (
    portIn : in STD_LOGIC;
    portOut : out STD_LOGIC
  );
end test1_wrapper;

architecture STRUCTURE of test1_wrapper is
  component test1 is
  port (
    portIn : in STD_LOGIC;
    portOut : out STD_LOGIC
  );
  end component test1;
begin
test1_i: component test1
     port map (
      portIn => portIn,
      portOut => portOut
    );
end STRUCTURE;
