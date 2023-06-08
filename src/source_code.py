SOURCE_CODE = r"""
int a;
a = 10;

if (a == 10) 
{
    a = 5;
    int w;
    w = a;
}
else
{
    a = 10;
}

while (a > 0)
{
    a = a - 1;
}
"""

SOURCE_CODE1 = r"""
int f;
f = 1;

function int test (int a, int b) {
    int z;
    z = a + b;
    return z;
}
int c;
c = 1;

test(c, c);



int z;
"""