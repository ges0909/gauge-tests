# Echo tests

* This is the setup section called before each scenario.

## Echo should return input as output

tags: successful

* If input is "Hello Syrocon!", then output should be "Hello Syrocon!".
* If input is "", then output should be "".
* If input is "-1", then output should be "-1".
* If input is "1.0", then output should be "1.0".
* If input is "True", then output should be "True".

## Echo should return input as output (table driven scenario)

* If input is input, then output should be output. 

   |input         |output        |
   |--------------|--------------|
   |Hello Syrocon!|Hello Syrocon!|
   |""            |""            |
   |-1            |-1            |
   |1.0           |1.0           |
   |True          |True          |

## Echo should evaluate to false

* If input is "Hello Syrocon!", then output should not be "".

---

* This is the teardown section only called once.
