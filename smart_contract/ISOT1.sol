//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract ISOApp is Ownable{
    
    //El string1 sería el hash-Id   String2 sería Hash/Ip
    mapping(bytes32 => bytes32) public hashToPrivateIp;
    mapping(bytes32 => bytes32) public hashToPublicIp;

    
    function updatePrivateIp(bytes32 _idHash, bytes32 _privateIpHash) public onlyOwner{
        hashToPrivateIp[_idHash] = _privateIpHash;
    }

    function updatePublicIp(bytes32 _idHash, bytes32 _publicIpHash) public onlyOwner{
        hashToPublicIp[_idHash] = _publicIpHash;
    }

//    Justo 32 bytes - Usar para tests "0x4554480000000000000000000000000000000000000000000000000000000000"

    function getPrivateIp(bytes32 _idHash) public view returns (bytes32 ) {
        return hashToPrivateIp[_idHash];
    }

    function getPublicIp(bytes32 _idHash) public view returns (bytes32 ) {
        return hashToPublicIp[_idHash];
    }

}