#include <math.h>

typedef struct {
    double rho;
    double velocity;
    double wing_area;
    double aspect_ratio;
    double cl0;
    double cd0;
    double alpha_rad;
    double oswald_efficiency;
    double mach;
} AeroInput;

typedef struct {
    double cl;
    double cd;
    double dynamic_pressure;
    double lift;
    double drag;
} AeroOutput;

/* Coefficients */
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


/* Forces and pressures */
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

double lift_to_drag_ratio(double lift, double drag)
{
    return lift / drag;
}

double net_force_x(double thrust, double drag)
{
    return thrust - drag;
}

double net_force_y(double lift, double weight)
{
    return lift - weight;
}

double weight_force(double mass)
{
    double gravity = 9.80665;
    return mass * gravity;
}


/* Speed and accelerations */
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

double acceleration_x(double thrust, double drag, double mass)
{
    return net_force_x(thrust, drag) / mass;
}

double acceleration_y(double lift, double weight, double mass)
{
    return net_force_y(lift, weight) / mass;
}

/* Atmosphere */
double temperature_at_altitude(double altitude_meters)
{
    double sea_level_temp = 288.15;
    double lapse_rate = 0.0065;

    return sea_level_temp - lapse_rate * altitude_meters;
}


void calculate_aero_state(AeroInput *inputs, AeroOutput *outputs)
{ 
    outputs->cl = lift_coefficient(
        inputs->cl0,
        inputs->alpha_rad
    );

    outputs->cd = drag_coefficient(
        inputs->cd0,
        outputs->cl,
        inputs->aspect_ratio,
        inputs->oswald_efficiency,
        inputs->mach
    );

    outputs->dynamic_pressure = dynamic_pressure(
        inputs->rho,
        inputs->velocity
    );

    outputs->lift = lift_force(
        outputs->dynamic_pressure,
        inputs->wing_area,
        outputs->cl
    );

    outputs->drag = drag_force(
        outputs->dynamic_pressure,
        inputs->wing_area,
        outputs->cd
    );
}

void calculate_aero_batch(AeroInput *inputs, AeroOutput *outputs, int count)
{
    int i;

    for (i=0; i < count; i++) {
        calculate_aero_state(&inputs[i], &outputs[i]);
    }
}
