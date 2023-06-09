SOURCE_CODE = {
    "ifStatement": r"""
int a;
a = 3;
if (a > 5) 
{
    print 1;
}
else
{
    print 0;
}
""",
    "functionDeclarationAndCall": r"""
function int test (int a, int b) {
    int z;
    z = a + b;
    return z;
}
int a;
a = 1;
int b;
b = 1;
print test(a, b);
""",
    "whileLoop": r"""
int a;
a = 10;
while (a > 0)
{
    print a;
    a = a - 1; 
}
print a;
""",
}
SOURCE_CODE = SOURCE_CODE["whileLoop"]
