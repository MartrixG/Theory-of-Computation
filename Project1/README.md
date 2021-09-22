## 2021 Theory of Computation Project1
<font size=4><center>Name:许天骁 student  ID:21S151066</center></font>

####Development environment
System: Windows10; 16GB RAM; 16-core Processor
Programming language: Python 3.9.7

### Task1
#### Introduction
Write a program to use regular expressions to match IP addresses. It is required to be able to correctly match the legal IP address format.
#### Method
In this experiment, it is assumed that the IP address does not have a leading 0. Means that 192.168.1.01 is unlegal IP address.
IP address has the following characteristics:
1. It consists of four decimal digits separated by ".".
2. Each number cannot be greater than 255 and cannot be less than 0.
   
Based on this premise, we can divide the regular expression into two parts:
1. Represents 256 numbers from 0 to 255, and cannot contain leading 0.
2. Repeat four times, and add "." between each number.

##### Represents the number
Since the leading 0 cannot be included, the representation starts from the number of different digits.
One digit:
- [0-9]
Two digits:
- [1-9][0-9]
Three digits can be divided into two situations:
 1. Greater than 99 and less than 200:
   - 1[0-9][0-9]
 2. Greater than or equal to 200 and less than 256:
   - 2[0-4][0-9]
Based on the above four situations, the regular expression of the number 0-255 can be expressed as follows:
- ([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5])

##### Combine the numbers
It becomes very simple to combine the above numbers with ".":
```
(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))\.
(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))\.
(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))\.
(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))
```

#### Experiment
The test code is as follows:
```python
import re

pattern = re.compile(r'(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))\.'
                     r'(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))\.'
                     r'(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))\.'
                     r'(([0-9])|([1-9][0-9])|(1[0-9][0-9])|(2[0-4][0-9])|(25[0-5]))$')


def ipaddress_check(address):
    match = pattern.match(address)
    if match:
        print('yes')
    else:
        print('no')


if __name__ == '__main__':
    ipaddress_check('255.255.255.255')
    ipaddress_check('192.168.1.1')
    ipaddress_check('192.168.1.0')
    ipaddress_check('192.168.1.01')
    ipaddress_check('192.168.1.256')
    ipaddress_check('192.168.1.2555')
```
The result is shown below:
![](report/ipv4.png)
#### 
### Task2
#### Introduction
Write programs to realize the conversion from regular expressions to non-deterministic finite automata (NFA). The input data is read from the file.
#### Method
First, assume that the regular expression contains only alphanumeric characters and specific special symbols.The special symbols are as follows:"* | ( )".
It is analogous to the program processing of the four arithmetic operations. Regular expressions also contain a few simple operations:Connection, union, closure.Therefore, two stacks are needed, a symbol stack, and a calculated expression stack.The specific calculation process can refer to the code shown.
Because there are only three types of calculations between specific regular expressions: connection, closure, and union. Therefore, in specific experiments, I abstracted regular expressions into three states. And you can use the McMaughton-Yamada-Thompson method for conversion.
After processing, use the McMaughton-Yamada-Thompson algorithm to merge all regular expressions. You can get the corresponding NFA.

#### Experiment
The regular expression is constructed as follows:
- (ab|c)*abb

Using the graphical method completed in the code and the connection of the NFA, the output is as follows:
```
begin=0, end=1, symbol=epsilon
begin=0, end=2, symbol=epsilon
begin=1, end=3, symbol=a
begin=2, end=4, symbol=epsilon
begin=2, end=5, symbol=epsilon
begin=3, end=6, symbol=b
begin=4, end=7, symbol=a
begin=5, end=8, symbol=c
begin=6, end=9, symbol=b
begin=7, end=10, symbol=b
begin=8, end=11, symbol=epsilon
begin=10, end=11, symbol=epsilon
begin=11, end=1, symbol=epsilon
begin=11, end=2, symbol=epsilon
```
![](report/res.png)
It can be seen that the correct NFA can be processed normally.