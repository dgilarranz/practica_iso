//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Funder {
    address payable[] recipients;
    mapping(address => uint256) public balanceAccount;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function send_ETH(address payable recipient) payable public {
    
    this.invest(msg.value);
    this.fund(recipient);
    }

    function invest(uint256 amount) public{
        //Mover $ de Metamask al Contrato 
        //Tendría que ser internal

        recordTransaction(address(this), amount, false);
        recordTransaction(owner, amount, true);
    }

    function fund(address payable recipient) external {
        //Mover $ de Contrato a Metamask 2

        recordTransaction(address(this), address(this).balance, true);
        recordTransaction(recipient, address(this).balance, false);
        recipient.transfer(address(this).balance);
    }

    function recordTransaction(address recipient, uint256 deposit, bool out) private {
        if (out) {
            balanceAccount[recipient] -= deposit;
        } else {
            balanceAccount[recipient] += deposit;
        }
    }

}
