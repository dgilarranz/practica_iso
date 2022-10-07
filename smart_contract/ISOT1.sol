//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract ISOApp is Ownable{
    //El string1 sería el hash-Id   String2 sería Hash/Ip
    mapping(string => string) public hashToIp;
    user[] public users;
    
    struct user{
        string hashId;
        string hashIp;
    } 

    function updateIp(string memory _idHash, string memory _ipHash) public onlyOwner{
        hashToIp[_idHash] = _ipHash;
    }

    function getIp(string memory _idHash) public view returns (string memory) {
        return hashToIp[_idHash];
    }


}