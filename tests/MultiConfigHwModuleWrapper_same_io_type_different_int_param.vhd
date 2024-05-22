LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
--
--    Simple parametrized module.
--
--    .. hwt-autodoc::
--    
ENTITY SimpleHwModuleWithHwParam_0 IS
    GENERIC(
        DATA_WIDTH : INTEGER := 2
    );
    PORT(
        a : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
        b : OUT STD_LOGIC_VECTOR(1 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF SimpleHwModuleWithHwParam_0 IS
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
ENTITY SimpleHwModuleWithHwParam_1 IS
    GENERIC(
        DATA_WIDTH : INTEGER := 3
    );
    PORT(
        a : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
        b : OUT STD_LOGIC_VECTOR(2 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF SimpleHwModuleWithHwParam_1 IS
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
ENTITY SimpleHwModuleWithHwParam IS
    GENERIC(
        DATA_WIDTH : INTEGER := 2
    );
    PORT(
        a : IN STD_LOGIC_VECTOR(DATA_WIDTH - 1 DOWNTO 0);
        b : OUT STD_LOGIC_VECTOR(DATA_WIDTH - 1 DOWNTO 0)
    );
END ENTITY;

ARCHITECTURE rtl OF SimpleHwModuleWithHwParam IS
    --
    --    Simple parametrized module.
    --
    --    .. hwt-autodoc::
    --    
    COMPONENT SimpleHwModuleWithHwParam_0 IS
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
    COMPONENT SimpleHwModuleWithHwParam_1 IS
        GENERIC(
            DATA_WIDTH : INTEGER := 3
        );
        PORT(
            a : IN STD_LOGIC_VECTOR(2 DOWNTO 0);
            b : OUT STD_LOGIC_VECTOR(2 DOWNTO 0)
        );
    END COMPONENT;
BEGIN
    implementation_select: IF DATA_WIDTH = 2 GENERATE
        possible_variants_0_inst: SimpleHwModuleWithHwParam_0 GENERIC MAP(
            DATA_WIDTH => 2
        ) PORT MAP(
            a => a,
            b => b
        );
    ELSIF DATA_WIDTH = 3 GENERATE
        possible_variants_1_inst: SimpleHwModuleWithHwParam_1 GENERIC MAP(
            DATA_WIDTH => 3
        ) PORT MAP(
            a => a,
            b => b
        );
    ELSE GENERATE
        ASSERT FALSE REPORT "The component was generated for this generic/params combination" SEVERITY failure;
    END GENERATE;
END ARCHITECTURE;
