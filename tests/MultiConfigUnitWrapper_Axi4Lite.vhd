LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
ENTITY EmptyAxiLite_0 IS
    GENERIC(
        ADDR_WIDTH : INTEGER := 11;
        DATA_WIDTH : INTEGER := 16
    );
    PORT(
        bus_ar_addr : IN STD_LOGIC_VECTOR(10 DOWNTO 0);
        bus_ar_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
        bus_ar_ready : OUT STD_LOGIC;
        bus_ar_valid : IN STD_LOGIC;
        bus_aw_addr : IN STD_LOGIC_VECTOR(10 DOWNTO 0);
        bus_aw_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
        bus_aw_ready : OUT STD_LOGIC;
        bus_aw_valid : IN STD_LOGIC;
        bus_b_ready : IN STD_LOGIC;
        bus_b_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_b_valid : OUT STD_LOGIC;
        bus_r_data : OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
        bus_r_ready : IN STD_LOGIC;
        bus_r_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_r_valid : OUT STD_LOGIC;
        bus_w_data : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
        bus_w_ready : OUT STD_LOGIC;
        bus_w_strb : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_w_valid : IN STD_LOGIC
    );
END ENTITY;

ARCHITECTURE rtl OF EmptyAxiLite_0 IS
BEGIN
    bus_ar_ready <= 'X';
    bus_aw_ready <= 'X';
    bus_b_resp <= "XX";
    bus_b_valid <= 'X';
    bus_r_data <= "XXXXXXXXXXXXXXXX";
    bus_r_resp <= "XX";
    bus_r_valid <= 'X';
    bus_w_ready <= 'X';
    ASSERT ADDR_WIDTH = 11 REPORT "Generated only for this value" SEVERITY failure;
    ASSERT DATA_WIDTH = 16 REPORT "Generated only for this value" SEVERITY failure;
END ARCHITECTURE;
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
ENTITY EmptyAxiLite_1 IS
    GENERIC(
        ADDR_WIDTH : INTEGER := 12;
        DATA_WIDTH : INTEGER := 16
    );
    PORT(
        bus_ar_addr : IN STD_LOGIC_VECTOR(11 DOWNTO 0);
        bus_ar_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
        bus_ar_ready : OUT STD_LOGIC;
        bus_ar_valid : IN STD_LOGIC;
        bus_aw_addr : IN STD_LOGIC_VECTOR(11 DOWNTO 0);
        bus_aw_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
        bus_aw_ready : OUT STD_LOGIC;
        bus_aw_valid : IN STD_LOGIC;
        bus_b_ready : IN STD_LOGIC;
        bus_b_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_b_valid : OUT STD_LOGIC;
        bus_r_data : OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
        bus_r_ready : IN STD_LOGIC;
        bus_r_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_r_valid : OUT STD_LOGIC;
        bus_w_data : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
        bus_w_ready : OUT STD_LOGIC;
        bus_w_strb : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_w_valid : IN STD_LOGIC
    );
END ENTITY;

ARCHITECTURE rtl OF EmptyAxiLite_1 IS
BEGIN
    bus_ar_ready <= 'X';
    bus_aw_ready <= 'X';
    bus_b_resp <= "XX";
    bus_b_valid <= 'X';
    bus_r_data <= "XXXXXXXXXXXXXXXX";
    bus_r_resp <= "XX";
    bus_r_valid <= 'X';
    bus_w_ready <= 'X';
    ASSERT ADDR_WIDTH = 12 REPORT "Generated only for this value" SEVERITY failure;
    ASSERT DATA_WIDTH = 16 REPORT "Generated only for this value" SEVERITY failure;
END ARCHITECTURE;
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
ENTITY EmptyAxiLite_2 IS
    GENERIC(
        ADDR_WIDTH : INTEGER := 13;
        DATA_WIDTH : INTEGER := 16
    );
    PORT(
        bus_ar_addr : IN STD_LOGIC_VECTOR(12 DOWNTO 0);
        bus_ar_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
        bus_ar_ready : OUT STD_LOGIC;
        bus_ar_valid : IN STD_LOGIC;
        bus_aw_addr : IN STD_LOGIC_VECTOR(12 DOWNTO 0);
        bus_aw_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
        bus_aw_ready : OUT STD_LOGIC;
        bus_aw_valid : IN STD_LOGIC;
        bus_b_ready : IN STD_LOGIC;
        bus_b_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_b_valid : OUT STD_LOGIC;
        bus_r_data : OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
        bus_r_ready : IN STD_LOGIC;
        bus_r_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_r_valid : OUT STD_LOGIC;
        bus_w_data : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
        bus_w_ready : OUT STD_LOGIC;
        bus_w_strb : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_w_valid : IN STD_LOGIC
    );
END ENTITY;

ARCHITECTURE rtl OF EmptyAxiLite_2 IS
BEGIN
    bus_ar_ready <= 'X';
    bus_aw_ready <= 'X';
    bus_b_resp <= "XX";
    bus_b_valid <= 'X';
    bus_r_data <= "XXXXXXXXXXXXXXXX";
    bus_r_resp <= "XX";
    bus_r_valid <= 'X';
    bus_w_ready <= 'X';
    ASSERT ADDR_WIDTH = 13 REPORT "Generated only for this value" SEVERITY failure;
    ASSERT DATA_WIDTH = 16 REPORT "Generated only for this value" SEVERITY failure;
END ARCHITECTURE;
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
ENTITY EmptyAxiLite IS
    GENERIC(
        ADDR_WIDTH : INTEGER := 11;
        DATA_WIDTH : INTEGER := 16
    );
    PORT(
        bus_ar_addr : IN STD_LOGIC_VECTOR(ADDR_WIDTH - 1 DOWNTO 0);
        bus_ar_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
        bus_ar_ready : OUT STD_LOGIC;
        bus_ar_valid : IN STD_LOGIC;
        bus_aw_addr : IN STD_LOGIC_VECTOR(ADDR_WIDTH - 1 DOWNTO 0);
        bus_aw_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
        bus_aw_ready : OUT STD_LOGIC;
        bus_aw_valid : IN STD_LOGIC;
        bus_b_ready : IN STD_LOGIC;
        bus_b_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_b_valid : OUT STD_LOGIC;
        bus_r_data : OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
        bus_r_ready : IN STD_LOGIC;
        bus_r_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_r_valid : OUT STD_LOGIC;
        bus_w_data : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
        bus_w_ready : OUT STD_LOGIC;
        bus_w_strb : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
        bus_w_valid : IN STD_LOGIC
    );
END ENTITY;

ARCHITECTURE rtl OF EmptyAxiLite IS
    COMPONENT EmptyAxiLite_0 IS
        GENERIC(
            ADDR_WIDTH : INTEGER := 11;
            DATA_WIDTH : INTEGER := 16
        );
        PORT(
            bus_ar_addr : IN STD_LOGIC_VECTOR(10 DOWNTO 0);
            bus_ar_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
            bus_ar_ready : OUT STD_LOGIC;
            bus_ar_valid : IN STD_LOGIC;
            bus_aw_addr : IN STD_LOGIC_VECTOR(10 DOWNTO 0);
            bus_aw_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
            bus_aw_ready : OUT STD_LOGIC;
            bus_aw_valid : IN STD_LOGIC;
            bus_b_ready : IN STD_LOGIC;
            bus_b_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
            bus_b_valid : OUT STD_LOGIC;
            bus_r_data : OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
            bus_r_ready : IN STD_LOGIC;
            bus_r_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
            bus_r_valid : OUT STD_LOGIC;
            bus_w_data : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
            bus_w_ready : OUT STD_LOGIC;
            bus_w_strb : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
            bus_w_valid : IN STD_LOGIC
        );
    END COMPONENT;
    COMPONENT EmptyAxiLite_1 IS
        GENERIC(
            ADDR_WIDTH : INTEGER := 12;
            DATA_WIDTH : INTEGER := 16
        );
        PORT(
            bus_ar_addr : IN STD_LOGIC_VECTOR(11 DOWNTO 0);
            bus_ar_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
            bus_ar_ready : OUT STD_LOGIC;
            bus_ar_valid : IN STD_LOGIC;
            bus_aw_addr : IN STD_LOGIC_VECTOR(11 DOWNTO 0);
            bus_aw_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
            bus_aw_ready : OUT STD_LOGIC;
            bus_aw_valid : IN STD_LOGIC;
            bus_b_ready : IN STD_LOGIC;
            bus_b_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
            bus_b_valid : OUT STD_LOGIC;
            bus_r_data : OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
            bus_r_ready : IN STD_LOGIC;
            bus_r_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
            bus_r_valid : OUT STD_LOGIC;
            bus_w_data : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
            bus_w_ready : OUT STD_LOGIC;
            bus_w_strb : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
            bus_w_valid : IN STD_LOGIC
        );
    END COMPONENT;
    COMPONENT EmptyAxiLite_2 IS
        GENERIC(
            ADDR_WIDTH : INTEGER := 13;
            DATA_WIDTH : INTEGER := 16
        );
        PORT(
            bus_ar_addr : IN STD_LOGIC_VECTOR(12 DOWNTO 0);
            bus_ar_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
            bus_ar_ready : OUT STD_LOGIC;
            bus_ar_valid : IN STD_LOGIC;
            bus_aw_addr : IN STD_LOGIC_VECTOR(12 DOWNTO 0);
            bus_aw_prot : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
            bus_aw_ready : OUT STD_LOGIC;
            bus_aw_valid : IN STD_LOGIC;
            bus_b_ready : IN STD_LOGIC;
            bus_b_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
            bus_b_valid : OUT STD_LOGIC;
            bus_r_data : OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
            bus_r_ready : IN STD_LOGIC;
            bus_r_resp : OUT STD_LOGIC_VECTOR(1 DOWNTO 0);
            bus_r_valid : OUT STD_LOGIC;
            bus_w_data : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
            bus_w_ready : OUT STD_LOGIC;
            bus_w_strb : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
            bus_w_valid : IN STD_LOGIC
        );
    END COMPONENT;
BEGIN
    implementation_select: IF ADDR_WIDTH = 11 AND DATA_WIDTH = 16 GENERATE
        possible_variants_0_inst: EmptyAxiLite_0 GENERIC MAP(
            ADDR_WIDTH => 11,
            DATA_WIDTH => 16
        ) PORT MAP(
            bus_ar_addr => bus_ar_addr,
            bus_ar_prot => bus_ar_prot,
            bus_ar_ready => bus_ar_ready,
            bus_ar_valid => bus_ar_valid,
            bus_aw_addr => bus_aw_addr,
            bus_aw_prot => bus_aw_prot,
            bus_aw_ready => bus_aw_ready,
            bus_aw_valid => bus_aw_valid,
            bus_b_ready => bus_b_ready,
            bus_b_resp => bus_b_resp,
            bus_b_valid => bus_b_valid,
            bus_r_data => bus_r_data,
            bus_r_ready => bus_r_ready,
            bus_r_resp => bus_r_resp,
            bus_r_valid => bus_r_valid,
            bus_w_data => bus_w_data,
            bus_w_ready => bus_w_ready,
            bus_w_strb => bus_w_strb,
            bus_w_valid => bus_w_valid
        );
    ELSIF ADDR_WIDTH = 12 AND DATA_WIDTH = 16 GENERATE
        possible_variants_1_inst: EmptyAxiLite_1 GENERIC MAP(
            ADDR_WIDTH => 12,
            DATA_WIDTH => 16
        ) PORT MAP(
            bus_ar_addr => bus_ar_addr,
            bus_ar_prot => bus_ar_prot,
            bus_ar_ready => bus_ar_ready,
            bus_ar_valid => bus_ar_valid,
            bus_aw_addr => bus_aw_addr,
            bus_aw_prot => bus_aw_prot,
            bus_aw_ready => bus_aw_ready,
            bus_aw_valid => bus_aw_valid,
            bus_b_ready => bus_b_ready,
            bus_b_resp => bus_b_resp,
            bus_b_valid => bus_b_valid,
            bus_r_data => bus_r_data,
            bus_r_ready => bus_r_ready,
            bus_r_resp => bus_r_resp,
            bus_r_valid => bus_r_valid,
            bus_w_data => bus_w_data,
            bus_w_ready => bus_w_ready,
            bus_w_strb => bus_w_strb,
            bus_w_valid => bus_w_valid
        );
    ELSIF ADDR_WIDTH = 13 AND DATA_WIDTH = 16 GENERATE
        possible_variants_2_inst: EmptyAxiLite_2 GENERIC MAP(
            ADDR_WIDTH => 13,
            DATA_WIDTH => 16
        ) PORT MAP(
            bus_ar_addr => bus_ar_addr,
            bus_ar_prot => bus_ar_prot,
            bus_ar_ready => bus_ar_ready,
            bus_ar_valid => bus_ar_valid,
            bus_aw_addr => bus_aw_addr,
            bus_aw_prot => bus_aw_prot,
            bus_aw_ready => bus_aw_ready,
            bus_aw_valid => bus_aw_valid,
            bus_b_ready => bus_b_ready,
            bus_b_resp => bus_b_resp,
            bus_b_valid => bus_b_valid,
            bus_r_data => bus_r_data,
            bus_r_ready => bus_r_ready,
            bus_r_resp => bus_r_resp,
            bus_r_valid => bus_r_valid,
            bus_w_data => bus_w_data,
            bus_w_ready => bus_w_ready,
            bus_w_strb => bus_w_strb,
            bus_w_valid => bus_w_valid
        );
    ELSE GENERATE
        ASSERT FALSE REPORT "The component was generated for this generic/params combination" SEVERITY failure;
    END GENERATE;
END ARCHITECTURE;
