# Arbitrager Joe

An arbitrage bot trading on decentralized exchanges with the use of flashloan, idea from [@cryptofish](https://twitter.com/cryptofishx/status/1491621931866599426) on Twitter.


```
                                                                
                       %,,,%&&&%  &%%%#%//#                     
                     %,***&%%#(#&#/////////                     
                  %*%&.***...  (//////%(                        
                 %*/  ***,..,((/.                               
                (.   /*****/(**,/                               
              ..      ,***/(****/                               
            #               .,*//#                    &,        
          .     .       ,.     ..                %/,//%         
        %  . ...                 .%              ,,,,,,         
       , ..,#(/(     .     .       ..(          /,,,,,,,        
       ,**/////(  ..*.      .     .  .          ,//////*        
      #////////((///*/.     ..     .. .(      *************     
     (//(//(//**//////(.  .#..     /#....    ***/******/*##((   
    (((///**///*////////*/((((#.   /**///(**************(%##    
    ((*//////*/////(///#//(/(((((,((/(((((%&/((****//%%&        
   #(((####(//*/////((/(//*/((((///(((((((((&(/(/  %%##%        
   ((/((##///(/////**//#((((#(((#//((((((((((%/#   %###%        
  /((###((###(#((///*/#####((((((((((((((((((#%    %###%        
 (*******((#(####(*******((((((###(((#(////(*/(    %###%        
 %//(***************/((/#(((((((/((///////////(#   %###%        
 &/(/*((((/(((///*****/(#((((((#/(///////////(((   &###%        
    &((((/////((((((((%##(((((((#//////////(((((   &###%        
     %/((************/####((((((((//////(((((((%   &###%        
      %/(*************(%##########/((((((((((((.   %(/(#        
      /(/****************(##########((((((((((%    %(/(#              
```

## Deployed Addresses
- trader: [0x9C90139BB93BB4b8eeC51ed6B2a25856aD255a8C](https://rinkeby.etherscan.io/address/0x9C90139BB93BB4b8eeC51ed6B2a25856aD255a8C)
- token0: [0x08671a22962e961190Eb2dee3571c78e09d167bd](https://rinkeby.etherscan.io/address/0x08671a22962e961190Eb2dee3571c78e09d167bd)
- token1: [0x03a8FcE0A63AAc36bD37c8be9964293dAAd2aA80](https://rinkeby.etherscan.io/address/0x03a8FcE0A63AAc36bD37c8be9964293dAAd2aA80)

## Usage
```bash
pipenv install & pipenv shell
python trader.py
```

## Features
- Flash loan arbitrage among decentralized exchanges (i.e. you only need gas to make your first trade)
- Logging for all arbitrage trades on concole and telegram

## TODOS
- hardhat + python -> foundry + Rust/Go
- Pairs scanning for arbitrage opportunities
- Memepool monitoring for darkforest plays
- Sizing function for trade size
- Take gas cost into consideration
- Gas auction optimization function (not urgent on avax)
- Change price monitor to listen to block instead
- Develop more sophisticated trading strategies (e.g. triangular arb)
- Optimizing gas usage for Ape.sol
- Unit tests

## Blueprint
```bash
.
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── hardhat
│   ├── README.md
│   ├── contracts
│   │   ├── Ape.sol
│   │   └── testnet
│   │       ├── UniswapV2Factory.sol
│   │       ├── token0.sol
│   │       └── token1.sol
│   ├── hardhat.config.ts
│   ├── package-lock.json
│   ├── package.json
│   ├── scripts
│   │   └── testnet
│   │       ├── 1-deployTokens.ts
│   │       ├── 2-addLiquidity.ts
│   │       └── 3-deployExecutor.ts
│   ├── test
│   │   └── index.ts
│   ├── tsconfig.json
│   └── yarn.lock
├── src
│   ├── abi
│   │   ├── Ape.json
│   │   ├── ERC20.json
│   │   ├── IUniswapV2Factory.json
│   │   ├── IUniswapV2Pair.json
│   │   └── IUniswapV2Router02.json
│   ├── constants.py
│   ├── strategies
│   │   └── naive_arb.py
│   └── utils
│       ├── exchange_setup.py
│       └── logger.py
├── test.py
└── trader.py

10 directories, 29 files
```

## Resoruces
- [On Arbitrage Bot using Flash Swaps](https://docs.google.com/document/d/13sfGbXdJl9gLHDQ-myG3XZgEQUHLQJIEon2qhE9fCvA/edit#heading=h.j3j7vyfbxjer) from @cryptofish
- [Uniswap's documentation](https://docs.uniswap.org/protocol/V2/guides/smart-contract-integration/using-flash-swaps) on flashswap
- A very clear illustration on the usage of swap from [flashswap/uniswap-flash-trade](https://github.com/flashswap/uniswap-flash-trade)
