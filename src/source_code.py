SOURCE_CODE = r"""
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