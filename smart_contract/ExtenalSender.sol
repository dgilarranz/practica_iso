//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Get the latest ETH/USD price from chainlink price feed
import "./Ownable.sol";
import "./IERC20.sol";
import "./ERC20.sol";



contract ExternalSender is Ownable {
    //PROTOTIPO DE ENVIO DE CRIPTOS NO NATIVOS - USDC, BTC, ...NO TERMINADO
    
    address public contract_address; 
    address public tokenAddress;

    function send_ISO(
        address _cobrador,
        address _pagador,
        uint256 _amount
    ) public onlyOwner {
        //function approve(address spender, uint256 amount) external returns (bool);
       
        require (IERC20(tokenAddress).allowance(contract_address, _pagador) >= _amount);
        IERC20(tokenAddress).transferFrom(
            _pagador,
            _cobrador,
            _amount
        );
        //Transfer(address from, address to, uint256 value)
    }


    function setSCAddress(address _contract_address) public onlyOwner
    {
        contract_address = _contract_address; 
    }

    function setTokenAddress(address _tokenAddress) public onlyOwner
    {
        tokenAddress = _tokenAddress; 
    }

    function approve(address _wallet, uint256 _amount) external returns (bool)
    {
        bool check = true;
        if (IERC20(tokenAddress).allowance(contract_address, _wallet) < _amount)
        {
            check = IERC20(tokenAddress).approve(
                contract_address,
                _amount
            );
            
        }
        return check;
    }

}


//Token address 0x22d5f99dc97608a26Bb051D280BC7316A036a623
               // 0x22d5f99dc97608a26Bb051D280BC7316A036a623
