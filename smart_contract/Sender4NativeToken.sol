pragma solidity ^0.8.0;

contract Sender {

    function send(address payable _addr) payable public {
        require(msg.value >= 0);
        if (msg.value > msg.sender.balance) {revert();}
        _addr.transfer(msg.value);
    }
}