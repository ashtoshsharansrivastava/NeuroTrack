#include "pico/stdlib.h"
#include "hardware/adc.h"
#include <stdio.h>

// --- Constants ---
// The GPIO pin the potentiometer is connected to. GP26 is ADC0.
const uint ADC_PIN = 26;
// The ADC channel for GP26 is 0.
const uint ADC_CHANNEL = 0;
// The delay between readings in milliseconds.
const int READ_DELAY_MS = 100;

int main() {
    // Initialize standard I/O for USB communication. This is a crucial step.
    stdio_init_all();

    // Initialize the ADC hardware
    adc_init();

    // Make sure the GPIO is enabled for ADC input
    adc_gpio_init(ADC_PIN);

    // The infinite loop for reading and sending data
    while (true) {
        // Select the ADC channel to read from
        adc_select_input(ADC_CHANNEL);

        // Read the 12-bit value from the ADC (0-4095)
        uint16_t result = adc_read();

        // Print the value, followed by a newline, to the USB serial port
        printf("%d\n", result);

        // Wait for a short period before the next reading
        sleep_ms(READ_DELAY_MS);
    }

    return 0;
}

