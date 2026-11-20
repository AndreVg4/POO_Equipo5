#include <unity.h>

void test_limites_temperatura()
{
    float temperatura = 5.0;

    TEST_ASSERT_TRUE(
        temperatura >= 2.0 &&
        temperatura <= 8.0
    );
}

void setup()
{
    UNITY_BEGIN();

    RUN_TEST(
        test_limites_temperatura
    );

    UNITY_END();
}

void loop()
{
}