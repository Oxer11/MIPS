`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2019/05/11 10:51:26
// Design Name: 
// Module Name: Pipeline_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module Pipeline_tb();
    reg clock, reset, sel;
    //wire [31:0] instr, PC;
    wire [7:0] SW;
    wire [6:0] DIGIT;
    Pipeline MUT(clock, reset, 1, 0, 1, SW, DIGIT);
    initial 
    begin
        reset = 1;
        clock = 0;
    end
    initial
        #6 reset = 0;
    always #5 clock = ~clock;
endmodule
