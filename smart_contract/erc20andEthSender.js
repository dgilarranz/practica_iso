const Web3 = require("web3");

const Web3js = new Web3(
    new Web3.providers.HttpProvider(
        "https://goerli.infura.io/v3/054abd12a18c4753845e87dc8e460740"
    )
);

const privateKey =
    "1b8fedebfee46a099a7fe9d83259f3670bf79da3e4953fbb6a2c114ec0dd1349"; //Your Private key environment variable

let tokenAddress = "0x22d5f99dc97608a26Bb051D280BC7316A036a623"; // Demo Token contract address

let toAddress = "0xa70A8cfcBdCA900bf0431FE376A7243C4424Fa2f"; // where to send it

let fromAddress = "0xf463c820487b22C2fe4d9dCbfAf0Df7aC8C7C16f"; // your wallet

let contractABI = [
    // transfer

    {
        constant: false,

        inputs: [
            {
                name: "_to",

                type: "address",
            },

            {
                name: "_value",

                type: "uint256",
            },
        ],

        name: "transfer",

        outputs: [
            {
                name: "",

                type: "bool",
            },
        ],

        type: "function",
    },
];

let contract = new Web3js.eth.Contract(contractABI, tokenAddress, {
    from: fromAddress,
});

let amount = Web3js.utils.toHex(Web3js.utils.toWei("1")); //1 DEMO Token

let data = contract.methods.transfer(toAddress, amount).encodeABI();

sendErcToken();

function sendErcToken() {
    let txObj = {
        gas: Web3js.utils.toHex(100000),

        to: tokenAddress,

        value: "0x00",

        data: data,

        from: fromAddress,
    };

    Web3js.eth.accounts.signTransaction(txObj, privateKey, (err, signedTx) => {
        if (err) {
            return callback(err);
        } else {
            console.log(signedTx);

            return Web3js.eth.sendSignedTransaction(
                signedTx.rawTransaction,
                (err, res) => {
                    if (err) {
                        console.log(err);
                    } else {
                        console.log(res);
                    }
                }
            );
        }
    });