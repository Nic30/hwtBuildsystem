LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
--
--    Simple parametrized module.
--
--    .. hwt-autodoc::
--    
ENTITY SimpleHwModuleWithParam_0 IS
    GENERIC(
        DATA_WIDTH : INTEGER := 2
    );
    PORT(
        a : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
        b : OUT STD_LOGIC_VECTOR(1 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF SimpleHwModuleWithParam_0 IS
BEGIN
    b <= a;
    ASSERT DATA_WIDTH = 2 REPORT "Generated only for this value" SEVERITY failure;
END ARCHITECTURE;
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
--
--    Simple parametrized module.
--
--    .. hwt-autodoc::
--    
ENTITY SimpleHwModuleWithParam_1 IS
    GENERIC(
        DATA_WIDTH : INTEGER := 3
    );
    PORT(
        a : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
        b : OUT STD_LOGIC_VECTOR(2 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF SimpleHwModuleWithParam_1 IS
BEGIN
    b <= a;
    ASSERT DATA_WIDTH = 3 REPORT "Generated only for this value" SEVERITY failure;
END ARCHITECTURE;
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
--
--    Simple parametrized module.
--
--    .. hwt-autodoc::
--    
ENTITY SimpleHwModuleWithParam_2 IS
    GENERIC(
        DATA_WIDTH : INTEGER := 4
    );
    PORT(
        a : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
        b : OUT STD_LOGIC_VECTOR(3 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF SimpleHwModuleWithParam_2 IS
BEGIN
    b <= a;
    ASSERT DATA_WIDTH = 4 REPORT "Generated only for this value" SEVERITY failure;
END ARCHITECTURE;
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
--
--    Simple parametrized module.
--
--    .. hwt-autodoc::
--    
ENTITY SimpleHwModuleWithParam IS
    GENERIC(
        DATA_WIDTH : INTEGER := 2
    );
    PORT(
        a : IN STD_LOGIC_VECTOR(DATA_WIDTH - 1 DOWNTO 0);
        b : OUT STD_LOGIC_VECTOR(DATA_WIDTH - 1 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF SimpleHwModuleWithParam IS
    --
    --    Simple parametrized module.
    --
    --    .. hwt-autodoc::
    --    
    COMPONENT SimpleHwModuleWithParam_0 IS
        GENERIC(
            DATA_WIDTH : INTEGER := 2
        );
        PORT(
            a : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
            b : OUT STD_LOGIC_VECTOR(1 DOWNTO 0)
        );
    END COMPONENT;
    --
    --    Simple parametrized module.
    --
    --    .. hwt-autodoc::
    --    
    COMPONENT SimpleHwModuleWithParam_1 IS
        GENERIC(
            DATA_WIDTH : INTEGER := 3
        );
        PORT(
            a : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
            b : OUT STD_LOGIC_VECTOR(2 DOWNTO 0)
        );
    END COMPONENT;
    --
    --    Simple parametrized module.
    --
    --    .. hwt-autodoc::
    --    
    COMPONENT SimpleHwModuleWithParam_2 IS
        GENERIC(
            DATA_WIDTH : INTEGER := 4
        );
        PORT(
            a : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
            b : OUT STD_LOGIC_VECTOR(3 DOWNTO 0)
        );
    END COMPONENT;
BEGIN
    implementation_select: IF DATA_WIDTH = 2 GENERATE
        possible_variants_0_inst: SimpleHwModuleWithParam_0 GENERIC MAP(
            DATA_WIDTH => 2
        ) PORT MAP(
            a => a,
            b => b
        );
    ELSIF DATA_WIDTH = 3 GENERATE
        possible_variants_1_inst: SimpleHwModuleWithParam_1 GENERIC MAP(
            DATA_WIDTH => 3
        ) PORT MAP(
            a => a,
            b => b
        );
    ELSIF DATA_WIDTH = 4 GENERATE
        possible_variants_2_inst: SimpleHwModuleWithParam_2 GENERIC MAP(
            DATA_WIDTH => 4
        ) PORT MAP(
            a => a,
            b => b
        );
    ELSE GENERATE
        ASSERT FALSE REPORT "The component was generated for this generic/params combination" SEVERITY failure;
    END GENERATE;
END ARCHITECTURE;
