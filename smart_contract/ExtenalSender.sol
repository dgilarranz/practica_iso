//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Get the latest ETH/USD price from chainlink price feed
import "./Ownable.sol";
import "./IERC20.sol";
import "./ERC20.sol";

 contract ExternalSender is Ownable{
     //PROTOTIPO DE ENVIO DE CRIPTOS NO NATIVOS - USDC, BTC, ...NO TERMINADO
    function send_ISO(address _cobrador, address _pagador, uint256 _amount) public onlyOwner{    
        IERC20(0x22d5f99dc97608a26Bb051D280BC7316A036a623).transferFrom(_pagador, _cobrador, _amount);
        //Transfer(address from, address to, uint256 value)
    }


}