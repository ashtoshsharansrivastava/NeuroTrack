#include "pico/stlib.h"
#include "hardware/adc.h"
#include <stdio.h>

const uint ADC_PIN = 26;
const uint ADC_CHANNEL = 0;
const int READ_DELAY_MS = 1000;
int main (){
    stdio_init_all();
    adc_init();
    adc_gpio_init(ADC_PIN);
    adc_select_input(ADC_CHANNEL);
    while (true) {
        uint16_t result = adc_read();
        printf("EEG reading: %d\n", result);
        sleep_ms(READ_DELAY_MS);
    }
    return 0;
}