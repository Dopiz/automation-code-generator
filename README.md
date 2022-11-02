# Code Generator


## Usage

### ABI Codegen
- ref. https://bscscan.com/address/0x2170ed0880ac9a755fd29b2688956bd959f933f8#code
- ```shell
    $ python command.py -f inputs/eth_abi_example.json -t abi -cp TOKEN -cl ETH -ch BSC
    ```

### API Codegen
- ref. https://petstore.swagger.io/
- ```shell
    $ python command.py -f 'https://petstore.swagger.io/v2/swagger.json' -t api -cp Pet -cl PetStore
    ```

