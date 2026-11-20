#include <unity.h>

bool evaluarAlarma(float t)
{
    return (t < 2.0 ||
            t > 8.0);
}

void test_alarma_activada()
{
    TEST_ASSERT_TRUE(
        evaluarAlarma(10)
    );
}

void test_alarma_desactivada()
{
    TEST_ASSERT_FALSE(
        evaluarAlarma(5)
    );
}

void setup()
{
    UNITY_BEGIN();

    RUN_TEST(
        test_alarma_activada
    );

    RUN_TEST(
        test_alarma_desactivada
    );

    UNITY_END();
}

void loop()
{
}