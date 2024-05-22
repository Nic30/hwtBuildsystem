LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
ENTITY ParamEmptyHwModule_0 IS
    GENERIC(
        ADDR_WIDTH : INTEGER := 8;
        DATA_WIDTH : INTEGER := 32
    );
    PORT(
        addr : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
        data : IN STD_LOGIC_VECTOR(31 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF ParamEmptyHwModule_0 IS
BEGIN
    ASSERT ADDR_WIDTH = 8 REPORT "Generated only for this value" SEVERITY failure;
    ASSERT DATA_WIDTH = 32 REPORT "Generated only for this value" SEVERITY failure;
END ARCHITECTURE;
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
ENTITY ParamEmptyHwModule_1 IS
    GENERIC(
        ADDR_WIDTH : INTEGER := 16;
        DATA_WIDTH : INTEGER := 32
    );
    PORT(
        addr : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
        data : IN STD_LOGIC_VECTOR(31 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF ParamEmptyHwModule_1 IS
BEGIN
    ASSERT ADDR_WIDTH = 16 REPORT "Generated only for this value" SEVERITY failure;
    ASSERT DATA_WIDTH = 32 REPORT "Generated only for this value" SEVERITY failure;
END ARCHITECTURE;
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
ENTITY ParamEmptyHwModule_2 IS
    GENERIC(
        ADDR_WIDTH : INTEGER := 32;
        DATA_WIDTH : INTEGER := 32
    );
    PORT(
        addr : IN STD_LOGIC_VECTOR(31 DOWNTO 0);
        data : IN STD_LOGIC_VECTOR(31 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF ParamEmptyHwModule_2 IS
BEGIN
    ASSERT ADDR_WIDTH = 32 REPORT "Generated only for this value" SEVERITY failure;
    ASSERT DATA_WIDTH = 32 REPORT "Generated only for this value" SEVERITY failure;
END ARCHITECTURE;
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
ENTITY ParamEmptyHwModule IS
    GENERIC(
        ADDR_WIDTH : INTEGER := 8;
        DATA_WIDTH : INTEGER := 32
    );
    PORT(
        addr : IN STD_LOGIC_VECTOR(ADDR_WIDTH - 1 DOWNTO 0);
        data : IN STD_LOGIC_VECTOR(31 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF ParamEmptyHwModule IS
    COMPONENT ParamEmptyHwModule_0 IS
        GENERIC(
            ADDR_WIDTH : INTEGER := 8;
            DATA_WIDTH : INTEGER := 32
        );
        PORT(
            addr : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
            data : IN STD_LOGIC_VECTOR(31 DOWNTO 0)
        );
    END COMPONENT;
    COMPONENT ParamEmptyHwModule_1 IS
        GENERIC(
            ADDR_WIDTH : INTEGER := 16;
            DATA_WIDTH : INTEGER := 32
        );
        PORT(
            addr : IN STD_LOGIC_VECTOR(15 DOWNTO 0);
            data : IN STD_LOGIC_VECTOR(31 DOWNTO 0)
        );
    END COMPONENT;
    COMPONENT ParamEmptyHwModule_2 IS
        GENERIC(
            ADDR_WIDTH : INTEGER := 32;
            DATA_WIDTH : INTEGER := 32
        );
        PORT(
            addr : IN STD_LOGIC_VECTOR(31 DOWNTO 0);
            data : IN STD_LOGIC_VECTOR(31 DOWNTO 0)
        );
    END COMPONENT;
BEGIN
    implementation_select: IF ADDR_WIDTH = 8 AND DATA_WIDTH = 32 GENERATE
        possible_variants_0_inst: ParamEmptyHwModule_0 GENERIC MAP(
            ADDR_WIDTH => 8,
            DATA_WIDTH => 32
        ) PORT MAP(
            addr => addr,
            data => data
        );
    ELSIF ADDR_WIDTH = 16 AND DATA_WIDTH = 32 GENERATE
        possible_variants_1_inst: ParamEmptyHwModule_1 GENERIC MAP(
            ADDR_WIDTH => 16,
            DATA_WIDTH => 32
        ) PORT MAP(
            addr => addr,
            data => data
        );
    ELSIF ADDR_WIDTH = 32 AND DATA_WIDTH = 32 GENERATE
        possible_variants_2_inst: ParamEmptyHwModule_2 GENERIC MAP(
            ADDR_WIDTH => 32,
            DATA_WIDTH => 32
        ) PORT MAP(
            addr => addr,
            data => data
        );
    ELSE GENERATE
        ASSERT FALSE REPORT "The component was generated for this generic/params combination" SEVERITY failure;
    END GENERATE;
END ARCHITECTURE;
