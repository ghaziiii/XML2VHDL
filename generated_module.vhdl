-- Auto-generated VHDL from XML
-- Generated on 2025-04-01 21:23:37
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity uart_controller is
    generic (
        GENERIC_WIDTH     : integer := 16;  -- generic data width
        GENERIC_DEPTH     : integer := 256;  -- generic ram depth
);
    port (
        CLK_I     : in std_logic;  -- system clock
        RST_I     : in std_logic;  -- system reset, active high
        DATA_I    : out std_logic_vector(7 downto 0);  -- input data
        DATA_O    : out std_logic_vector(7 downto 0);  -- output data
);
end uart_controller;

architecture Behavioral of uart_controller is

    -- Internal signals
    signal S_COUNTER 	: std_logic_vector(31 downto 0) 	:= (others => '0');  -- internal counter signal
    signal S_READY 	: std_logic 	:= '0';  -- internal ready signal

    -- Registers
    signal CONTROL_REG 	: std_logic_vector(7 downto 0);
    -- ENABLE	: bits 7 (default: 0)
    -- MODE	: bits 6-5 (default: 01)

    -- Components
    component FIFO_GENERATOR
        port (
        -- Port declarations
        );
     end component;

begin

    -- Concurrent assignments
    TX_DATA(0) <= CONTROL_REG(0);  -- LSB of tx data
    TX_DATA(7 downto 1) <= (others => '1');  -- MSBs set high

    -- Processes
    P_TX_process : process(CLK_I, RST_I)
     begin
        
    end process;

end Behavioral;