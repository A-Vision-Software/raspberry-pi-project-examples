#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"

int main() {
  // Set constants 
  const float reference_resistor_17 =  10000.0f;
  const float reference_resistor_16 = 100000.0f;
  const float reference_voltage = 3.3f;
  const float adc_offset = 0.034; // See manual (https://datasheets.raspberrypi.org/pico/pico-datasheet.pdf Section 4.3)
  const float conversion_factor = reference_voltage / (1 << 12); // ADC resolution is 12 bits
  const size_t samples = 10; // Average over XX samples

  // Select 10K reference resistor by default
  int ref = 17;

  // Enable UART so we can print status output
  stdio_init_all();
  adc_init();

  // Make sure GPIO is high-impedance, no pullups etc
  adc_gpio_init(26); // ADC0
  
  // GPIO16 switch to use 100K reference resitor
  gpio_init(16);
  gpio_set_dir(16, GPIO_OUT);
  gpio_put(16, 1);

  // GPIO17 switch to used 10K refrence resistor
  gpio_init(17);
  gpio_set_dir(17, GPIO_OUT);
  gpio_put(17, 1);

  while (true) {
    // Read multiple samples to average a read value
    float U = 0;
    for (size_t i = 0; i < samples; i++)
    {
      float V = reference_voltage + 1.0f;
      while (V > reference_voltage)
      {
        adc_select_input(0);
        sleep_ms(5);
        uint16_t result = adc_read();
        V = result * conversion_factor;
        V += adc_offset; // Offset by ADC current draw
        if (V <= reference_voltage) {
          U += V;
        }
      }        
    }
    float V = U / samples;
    // V now contains the average of XX samples

    // Based on the read value, switch to the proper reference resistor for the next reading
    float reference_resistor = 0;
    if (V > 2.1f) {
      ref = 16; // select 100K reference resistor
    }
    if (V < 0.4f) {
      ref = 17; // select 10K reference resistor
    }
    if (ref == 16) {
      reference_resistor = reference_resistor_16; // 100kOhm
      gpio_put(16, 0);
      gpio_put(17, 1);
    }
    if (ref == 17) {
      reference_resistor = reference_resistor_17; // 10kOhm
      gpio_put(16, 1);
      gpio_put(17, 0);
    }

    // Now calculate the resistor value from the most recent reading
    float R = (reference_resistor * V) / (reference_voltage - V);
    char unit = ' ';
    if (R > 1000) {
      unit = 'K';
      R = R / 1000.0f;
    }
    if (R > 1000) {
      unit = 'M';
      R = R / 1000.0f;
    }

    // The printf uses the TxD (GPIO0) to output data
    printf("\rVoltage: %8.3f V, Resistor: %7.1f%c ohm", V, R, unit);

    // Keep quiet for 0.5s
    sleep_ms(500);
  }
  return 0;
}
