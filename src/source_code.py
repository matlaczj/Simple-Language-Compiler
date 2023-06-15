SOURCE_CODE = {
    "ifStatement": r"""
float cash;
cash = 100.0;

float tax;
tax = 0.0;

if (cash > 50.0)
{
    tax = 0.1;
}
else
{
    tax = 0.2;
}

float tax_amount;
tax_amount = cash * tax;

cash = cash - tax_amount;
print cash;
""",
    "functionDeclarationAndCall": r"""
int z;
z = 123;
function int add(int a, int b) {
    int z;
    z = a + b;
    return z;
}
int a;
a = 1;
int b;
b = 1;
print add(a, b);
print z;
""",
    "whileLoop": r"""
int cash;
cash = 10;
while (cash > 0)
{
    print cash;
    cash = cash - 1;
}
print cash;
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
        float x;
        float y;
        float z;
    }

    float x;
    float y;
    float z;
    x = 1.0;
    y = 2.0;
    z = 3.0;

    struct point p;
    p.x = x;
    p.y = y;
    p.z = z;

    print p.x;
    print p.y;
    print p.z;
    """
}

SOURCE_CODE = SOURCE_CODE["functionDeclarationAndCall"]
