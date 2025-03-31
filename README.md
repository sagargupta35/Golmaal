# Golmaal

## Data types
1. **Integers**: `10, 20, -10`
2. **Booleans** `true, false`
3. **Strings**: `"golmaal", "is fun"`, `2 + " two"`
4. **Arrays**: `[1, false, "golmaal"] // arrays are immutable`

## Variable Declaration
variables are declared using the `maan_le` keyword <br>
`maan_le a = 10;`<br>
`a = false;` **(re-assignment is allowed only if you have already declared the variable)**<br>
`jaadu b = [1, false, golmaal(a){ye_lo a*2}]`

##  Built-in functions
1. `print(2, 3, false)` // multiple arguements are concatenated with '' as delimiter
2. `len("Golmaal") // 7`
3. `len([1, 2, 3]) // 3` 

## if-else:
>truthy values can be extracted from integers and booleans: <br>
	>> all positive numbers and true yield true <br>
	>> all non-positive numbers and false yield false
	
```
if(3){
	print("fuzz");
} else{
	print("buzz");
}
```

## loop:
```
jaadu a = 10;
while(a){
	print("a");
	a = a-1;
}
```

## Functions:
#### Functions are also expressions in Golmaal.
###### `golmaal` keyword is used to define functions
```
jaadu a = golmaal(a, b){
	ye_lo a + b*2;
}
```
note that ye_lo keyword is optional
<br>
<br>

## Closures:
[What is a Closure?](https://stackoverflow.com/questions/36636/what-is-a-closure)
```
jaadu a = golmaal(a, b){
	ye_lo a + b*2;
}
jaadu b = golmaal(a, b){
	a = a+1;
	a*b(a, 2);
}
print(b(2, a)); // prints 21
```

[Try it on our website](https://golmaal-front-end.onrender.com)