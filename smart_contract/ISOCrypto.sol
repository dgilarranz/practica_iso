//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./ERC20.sol";

contract ISO is ERC20 {
    constructor(uint256 initialSupply) ERC20("ISOT1", "ISO")
    {
        _mint(msg.sender, initialSupply); 
    }
}