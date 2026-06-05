#include <stdio.h>
#include "aero_core.c"

int main(void)
{
    AeroInput *input = create_aero_input();
    AeroOutput *output = create_aero_output();

    if (input == NULL || output == NULL) {
        printf("Memory allocation failed\n");

        destroy_aero_input(input);
        destroy_aero_output(output);

        return 1;
    }

    initialize_aero_input(
        input,
        1.225,
        145.0,
        20.0,
        5.0,
        0.2,
        0.02,
        0.05,
        0.8,
        0.5,
        1000.0,
        5000.0
    );

    initialize_aero_output(output);

    calculate_aero_state(input, output);

    printf("Heap aero state demo:\n\n");
    printf("CL: %f\n", output->cl);
    printf("CD: %f\n", output->cd);
    printf("Dynamic Pressure: %f\n", output->dynamic_pressure);
    printf("Lift: %f\n", output->lift);
    printf("Drag: %f\n", output->drag);
    printf("Weight: %f\n", output->weight);
    printf("Acc X: %f\n", output->acc_x);
    printf("Acc Y: %f\n", output->acc_y);

    destroy_aero_input(input);
    destroy_aero_output(output);

    return 0;
}