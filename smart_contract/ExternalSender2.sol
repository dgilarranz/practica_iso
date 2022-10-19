//SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/IERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol";

contract ExternalSender2 {
    ERC20 _token;
uint256 MAX_INT = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff;


    // token = MyToken's contract address
    constructor(address token) {
        _token = ERC20(token);
    }

    address public contract_address; 

    // Modifier to check token allowance
    modifier checkAllowance(uint amount) {
        require(_token.allowance(msg.sender, address(this)) >= amount, "Allowance Error");
        _;
    }

    // In your case, Account A must to call this function and then deposit an amount of tokens 
    function depositTokens(uint _amount) public checkAllowance(_amount) {
        _token.transferFrom(msg.sender, address(this), _amount);
    }
    
    // to = Account B's address
    function stake(address to, uint amount) public {
        _token.transfer(to, amount);
    }

    function checkSenderBalance() public view returns(uint)
    {
        return _token.balanceOf(msg.sender);
    }

    // Allow you to show how many tokens owns this smart contract
    function getSmartContractBalance() external view returns(uint) {
        return _token.balanceOf(address(this));
    }

    function cAllowance() public view returns (uint)
    {
       return ERC20(0x22d5f99dc97608a26Bb051D280BC7316A036a623).allowance(msg.sender, address(this));
    }



    function approve() public
    //A esta función la llama el user
    {
       _token.approve(address(this), MAX_INT);
    }
    
}