#include <math.h>

double lift_coefficient(double cl0, double alpha_rad)
{
    double lift_slope = 2.0 * M_PI;
    return cl0 + lift_slope * alpha_rad;
}

double drag_coefficient(
    double cd0,
    double cl,
    double aspect_ratio,
    double oswald_efficiency,
    double mach
)
{
    double induced_drag;
    double wave_drag;
    double cd;

    induced_drag = (cl * cl) / (M_PI * aspect_ratio * oswald_efficiency);
    cd = cd0 + induced_drag;

    if (mach > 0.85) {
        wave_drag = 0.08 * (mach - 0.85) * (mach - 0.85);
        cd = cd + wave_drag;
    }

    return cd;
}

double dynamic_pressure(double rho, double velocity)
{
    return 0.5 * rho * velocity * velocity;
}

double lift_force(double dynamic_pressure_value, double wing_area, double cl)
{
    return dynamic_pressure_value * wing_area * cl;
}

double drag_force(double dynamic_pressure_value, double wing_area, double cd)
{
    return dynamic_pressure_value * wing_area * cd;
}

double speed_of_sound(double temperature)
{
    double gamma = 1.4;
    double gas_constant = 287.05;
    return sqrt(gamma * gas_constant * temperature);
}

double mach_number(double speed_of_sound_value, double velocity)
{
    return velocity / speed_of_sound_value;
}