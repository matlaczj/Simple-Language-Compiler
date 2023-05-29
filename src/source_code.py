SOURCE_CODE = """
int a;
float b;
a = 10;
b = 2.5;
int c;
c = a + 5;
if c > 10 {
    print "Condition is true";
} else {
    print "Condition is false";
}
while b > 0 {
    b = b - 1;
}
function int multiply(int x, int y) {
    int result;
    result = x * y;
    return result;
}
int product;
product = multiply(a, 5);
print "Product: " + product;
read c;
"""
