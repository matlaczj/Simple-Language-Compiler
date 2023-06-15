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

if (a > 2)
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
    "baseLineTest": r"""
// Calculate control signal
int signal;
signal = 200;

function int proportional_controller (int k, int error) {
    int signal;
    signal = k * error;
    return signal;
}

int control_signal;
int k;
k = 1;
int error;
error = 10;

control_signal = proportional_controller(k, signal); // get control signal
print control_signal;
// clamp control signal
if (control_signal > 100) {
    control_signal = 100;
}
else {}
if (control_signal < 0) {
    control_signal = 0;
}
else {}

print signal;
print control_signal;

while (control_signal > 90) {
    print control_signal;
    control_signal = control_signal - 1;
}

while (control_signal < 95) {
    print control_signal;
    control_signal = control_signal + 1;
}
""",
    "structTest": r"""
    typedef struct point {
        int x;
        int y;
        float z;
    }
    struct point p;
    p.x = 1;
    p.y = 2;
    p.z = 3.0;

    print p.x * p.y;
    typedef struct mapping {
        int input_domain_idx;
        int output_domain_idx;
    }
    struct mapping m;
    m.input_domain_idx=4;
    m.output_domain_idx=3;
    int sum;
    sum = m.input_domain_idx + m.output_domain_idx;
    print sum;

    """
}

SOURCE_CODE = SOURCE_CODE["structTest"]
