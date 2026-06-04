#include <math.h>
#include <stdlib.h>

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
    double mass;
    double thrust;
} AeroInput;

typedef struct {
    double cl;
    double cd;
    double dynamic_pressure;
    double lift;
    double drag;
    double weight;
    double net_force_x;
    double net_force_y;
    double acc_x;
    double acc_y;
} AeroOutput;

AeroInput *create_aero_input(void)
{
    AeroInput *input = malloc(sizeof(AeroInput));

    if (input == NULL) {
        return NULL;
    }

    return input;
}

AeroOutput *create_aero_output(void)
{
    AeroOutput *output = malloc(sizeof(AeroOutput));
    
    if (output == NULL) {
        return NULL;
    }

    return output;
}

void initialize_aero_input(
    AeroInput *input,
    double rho,
    double velocity,
    double wing_area,
    double aspect_ratio,
    double cl0,
    double cd0,
    double alpha_rad,
    double oswald_efficiency,
    double mach,
    double mass,
    double thrust
)
{
    if (input == NULL) {
        return;
    }

    input->rho = rho;
    input->velocity = velocity;
    input->wing_area = wing_area;
    input->aspect_ratio = aspect_ratio;
    input->cl0 = cl0;
    input->cd0 = cd0;
    input->alpha_rad = alpha_rad;
    input->oswald_efficiency = oswald_efficiency;
    input->mach = mach;
    input->mass = mass;
    input->thrust = thrust;
}

void initialize_aero_output(AeroOutput *output)
{
    if (output == NULL) {
        return;
    }

    output->cl = 0.0;
    output->cd = 0.0;
    output->dynamic_pressure = 0.0;
    output->lift = 0.0;
    output->drag = 0.0;
    output->weight = 0.0;
    output->net_force_x = 0.0;
    output->net_force_y = 0.0;
    output->acc_x = 0.0;
    output->acc_y = 0.0;
}

void destroy_aero_input(AeroInput *input)
{
    free(input);
}

void destroy_aero_output(AeroOutput *output)
{
    free(output);
}

/* Main pre-req functions */
double dynamic_pressure(double rho, double velocity)
{
    return 0.5 * rho * velocity * velocity;
}


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

double required_lift_coeff(double weight, double rho, double velocity, double wing_area)
{
    double q = dynamic_pressure(rho, velocity);
    return weight / (q * wing_area);
}


/* Geometry */
double required_wing_area(double weight, double rho, double velocity, double cl)
{
    double q = dynamic_pressure(rho, velocity);
    return weight / (q * cl);
}

double wing_area(double span, double chord)
{
    return span * chord;
}

double exposed_wing_area(double full_wing_area, double deployment)
{
    if (deployment < 0.3) {
        deployment = 0.3;
    }

    if (deployment > 1.0) {
        deployment = 1.0;
    }

    return full_wing_area * deployment;
}

double aspect_ratio(double span, double exposed_area)
{
    return (span * span) / exposed_area;
}


/* Forces */
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

double level_flight_drag(
    double weight,
    double rho,
    double velocity, 
    double wing_area,
    double cd0,
    double aspect_ratio,
    double oswald_efficiency,
    double mach
)
{
    double cl = required_lift_coeff(weight, rho, velocity, wing_area);
    double cd = drag_coefficient(cd0, cl, aspect_ratio, oswald_efficiency, mach);
    double q = dynamic_pressure(rho, velocity);

    return q * wing_area * cd;
}

double power_required(double drag, double velocity)
{
    return drag * velocity;
}

double load_factor(double lift, double weight)
{
    return lift / weight;
}


/* Speed and accelerations and rates */
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

double stall_speed(double weight, double rho, double wing_area, double cl_max)
{
    return sqrt((2.0*weight) / (rho * wing_area * cl_max));
}

double rate_of_climb(double thrust, double drag, double velocity, double weight)
{
    return ((thrust -  drag) * velocity) / weight;
}


/* Atmosphere */
double temperature_at_altitude(double altitude_meters)
{
    double sea_level_temp = 288.15;
    double lapse_rate = 0.0065;

    return sea_level_temp - lapse_rate * altitude_meters;
}

double air_density(double pressure, double temperature)
{
    double gas_constant = 287.05;
    return pressure / (gas_constant * temperature);
}

double pressure_at_altitude(double altitude)
{
    double sea_level_pressure = 101325.0;
    double sea_level_temp = 288.15;
    double lapse_rate = 0.0065;
    double gravity = 9.80665;
    double gas_constant = 287.05;

    double temperature = temperature_at_altitude(altitude);

    return sea_level_pressure * pow(
        temperature / sea_level_temp,
        gravity / (gas_constant * lapse_rate));
}

double air_density_at_altitude(double altitude)
{
    double temperature = temperature_at_altitude(altitude);
    double pressure = pressure_at_altitude(altitude);

    return air_density(pressure, temperature);
}

/* Control functions */
double dynamic_trim_alpha(
    double weight,
    double rho,
    double velocity, 
    double wing_area,
    double cl0
)
{
    double q = dynamic_pressure(rho, velocity);
    double required_cl = weight / (q * wing_area);
    double lift_slope = 2.0 * M_PI;

    return (required_cl - cl0) / lift_slope;
}

double clamp(double value, double min, double max)
{
    if (value < min) {
        return min;
    }

    if (value > max) {
        return max;
    }

    return value;
}

double rate_limit(double current_value, double target_value, double max_change)
{
    double error = target_value - current_value;

    if (error > max_change) {
        return current_value + max_change;
    }

    if (error < -max_change) { 
        return current_value - max_change;
    }

    return target_value;
}

/* Performance functions */
int is_level_flight(double lift, double weight, double tolerance)
{
    double percent_diff = fabs(lift - weight) / weight;
    return percent_diff <= tolerance;
}

int is_steady_speed(double thrust, double drag, double tolerance)
{
    double percent_diff = fabs(thrust - drag) / drag;
    return percent_diff <= tolerance;
}

int is_trimmed(double lift, double weight, double thrust, double drag, double tolerance)
{
    return (
        is_level_flight(lift, weight, tolerance)
        && is_steady_speed(thrust, drag, tolerance));
}


/* Boomless functions */
double cutoff_depth(double mach, double temp_gradient)
{
    double mach_excess;
    double base_depth;
    double gradient_factor;

    mach_excess = mach - 1.0;
    base_depth = 25000.0 * mach_excess;

    if (temp_gradient < 0.0) {
        gradient_factor = 1.0;
    } else {
        gradient_factor = 1.5;
    }

    return base_depth * gradient_factor;
}

double cutoff_altitude_agl(double altitude, double mach, double temp_gradient)
{
    if (mach <= 1.0) {
        return 999999.0;
    }

    return altitude - cutoff_depth(mach, temp_gradient);
}

int is_boomless(double altitude, double mach, double temp_gradient, double min_cutoff_altitude_agl)
{
    double cutoff_altitude = cutoff_altitude_agl(altitude, mach, temp_gradient);
    return cutoff_altitude >= min_cutoff_altitude_agl;
}


/* Main calculation functions */
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

    outputs->weight = weight_force(inputs->mass);

    outputs->net_force_x = net_force_x(
        inputs->thrust,
        outputs->drag
    );

    outputs->net_force_y = net_force_y(
        outputs->lift,
        outputs->weight
    );

    outputs->acc_x = outputs->net_force_x / inputs->mass;

    outputs->acc_y = outputs->net_force_y / inputs->mass;
}

void calculate_aero_batch(AeroInput *inputs, AeroOutput *outputs, int count)
{
    int i;

    for (i=0; i < count; i++) {
        calculate_aero_state(&inputs[i], &outputs[i]);
    }
}
