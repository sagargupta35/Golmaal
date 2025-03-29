# Golmaal

## Data types
1. **Integers**: `10, 20, -10`
2. **Booleans** `true, false`
3. **Strings**: `"golmaal", "is fun"`
4. **Arrays**: `[1, false, "golmaal"]`

## Variable Declaration
`let a = 10;`

`a = false;` **(re-assignment is allowed only if you have already declared the variable)**

`let b = [1, false, fn(a){return a*2}]`

##  Built-in functions
1. `print(2, 3, false)` multiple arguements are printed line by line
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
let a = 10;
while(a){
	print("a");
	a = a-1;
}
```

## Functions:
#### Functions are also expressions in Golmaal.
```
let a = fn(a, b){
	return a + b*2;
}
```
note that return keyword is optional
<br>
<br>

## Closures:
```
let a = fn(a, b){
	return a + b*2;
}
let b = fn(a, b){
	a = a+1;
	a*b(a, 2);
}
print(b(2, a)); // prints 21
```

[Click to know more](https://www.youtube.com/watch?v=dQw4w9WgXcQ)