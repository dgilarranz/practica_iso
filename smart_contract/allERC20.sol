//SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

// Get the latest ETH/USD price from chainlink price feed
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

 contract Funder2 is Ownable{
     //PROTOTIPO DE ENVIO DE CRIPTOS NO NATIVOS - USDC, BTC, ...NO TERMINADO
    function send_ETH(address _cobrador, address _pagador, uint256 _amount) public{    
        IERC20(/*Contrato del Token*/).transferFrom(_pagador, _cobrador, _amount);
        //Transfer(address from, address to, uint256 value)
    }


}