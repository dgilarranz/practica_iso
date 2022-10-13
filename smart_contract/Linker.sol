//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";


contract Linker is Ownable{
    
    //El string1 sería el hash-Id   String2 sería Hash/Ip
    mapping(string => string) public hashToPrivateIp;
    mapping(string => string) public hashToPublicIp;

    
    function updatePrivateIp(string memory _idHash, string memory _privateIpHash) public onlyOwner{
        hashToPrivateIp[_idHash] = _privateIpHash;
    }

    function updatePublicIp(string memory _idHash, string memory _publicIpHash) public onlyOwner{
        hashToPublicIp[_idHash] = _publicIpHash;
    }

//    Justo 32 bytes - Usar para tests "0x4554480000000000000000000000000000000000000000000000000000000000"

    function getPrivateIp(string memory _idHash) public view returns (string memory) {
        return hashToPrivateIp[_idHash];
    }

    function getPublicIp(string memory _idHash) public view returns (string memory) {
        return hashToPublicIp[_idHash];
    }

    
}