`ifndef RAL_AMBA_PERIPHERAL_PKG
`define RAL_AMBA_PERIPHERAL_PKG

`ifndef RAL_PRUNE_USER_REG_MODEL
`include "ral_user_reg_model_pkg.sv"
`endif
package ral_amba_peripheral_pkg;
import uvm_pkg::*;

`ifndef RAL_PRUNE_USER_REG_MODEL
import ral_user_reg_model_pkg::*;
`endif
class ral_sys_amba_peripheral extends uvm_reg_block;

`ifndef RAL_PRUNE_USER_REG_MODEL
   rand ral_block_user_reg_model user_reg_model0;
`endif

	function new(string name = "amba_peripheral");
		super.new(name);
	endfunction: new

	function void build();
      this.default_map = create_map("", 0, 4, UVM_LITTLE_ENDIAN, 0);
`ifndef RAL_PRUNE_USER_REG_MODEL
      this.user_reg_model0 = ral_block_user_reg_model::type_id::create("user_reg_model0",,get_full_name());
      this.user_reg_model0.configure(this, "u_user_model_top.u_user_model_amba_reg");
      this.user_reg_model0.build();
      this.default_map.add_submap(this.user_reg_model0.default_map, `UVM_REG_ADDR_WIDTH'hE000);
`endif
	endfunction : build

	`uvm_object_utils(ral_sys_amba_peripheral)
endclass : ral_sys_amba_peripheral


endpackage

`endif
