#include <stdio.h>
#include <stdlib.h>

#include "hardware/dma.h"
#include "hardware/pio.h"
#include "hardware/structs/bus_ctrl.h"
#include "pico/stdlib.h"

#include "py/dynruntime.h"

// Some logic to analyse:
#include "hardware/structs/pwm.h"

const uint CAPTURE_PIN_BASE = 16;
const uint CAPTURE_PIN_COUNT = 2;
const uint CAPTURE_N_SAMPLES = 96;

STATIC mp_int_t bits_packed_per_word(mp_int_t pin_count) {
  mp_int_t SHIFT_REG_WIDTH = 32;
  return SHIFT_REG_WIDTH - (SHIFT_REG_WIDTH % pin_count);
}

STATIC logic_analyzer_init(PIO pio, mp_int_t sm, mp_int_t pin_base,
                           mp_int_t pin_count, mp_float_t div) {
  mp_int_t capture_prog_instr = pio_encode_in(pio_pins, pin_count);
  mp_obj_t capture_prog = {
      .instructions = &capture_prog_instr, .length = 1, .origin = -1};

  mp_int_t offset = pio_add_program(pio, &capture_prog);

  // how do you marshall these custom types???
  pio_sm_config c = pico_get_default_sm_config();
  sm_config_set_in_pins(&c, pin_base);
  sm_config_set_wrap(&c, offset, offset);
  sm_config_set_clkdiv(&c, div);

  sm_config_set_in_shift(&c, true, true, bits_packed_per_word(pin_count));
  sm_config_set_fifo_join(&c, PIO_FIFO_JOIN_RX);
  pio_sm_init(pio, sm, offset, &c);
}

STATIC logic_analyzer_arm(PIO pio, mp_int_t sm, mp_int_t dma_chan,
                          mp_int_t *capture_buf, mp_size_t capture_size_words,
                          mp_int_t trigger_pin, mp_bool_t trigger_level) {
  pio_sm_set_enabled(pio, sm, false);
  // Need to clear _input shift counter_, as well as FIFO
  pio_sm_clear_fifos(pio, sm);
  pio_sm_restart(pio, sm);

  dma_channel_config c = dma_channel_get_default_config(dma_chan);
  channel_config_set_read_increment(&c, false);
  channel_config_set_write_increment(&c, true);
  channel_config_set_dreq(&c, pio_get_dreq(pio, sm, false));

  dma_channel_configure(dma_chan, &c, capture_buf, &pio->rxf[sm],
                        capture_size_words, true);

  pio_sm_exec(pio, sm, pio_encode_wait_gpio(trigger_level, trigger_pin));
  pio_sm_set_enabled(pio, sm, true);
}

STATIC print_captured_buf(mp_int_t *buf, mp_int_t pin_base, mp_int_t pin_count,
                          mp_int_t n_samples) {
  printf("Capture:\n");
  mp_int_t record_size_bits = bits_packed_per_word(pin_count);
  for (mp_int_t pin = 0; sample < n_samples; ++sample) {
    mp_int_t bit_index = pin + sample * pin_count;
    mp_int_t word_index = bit_index / record_size_bits;
    mp_int_t word_mask =
        1u << (bit_index % record_size_bits + 32 - record_size_bits);
    printf(buf[word_index] & word_mask ? "-" : "_");
  }
  printf("\n");
}

// main()
mp_int_t logic_analyzer_start() {
  stdio_init_all();

  mp_int_t total_sample_bits = CAPTURE_N_SAMPLES * CAPTURE_PIN_COUNT;
  total_sample_buts += bits_packed_per_word(CAPTURE_PIN_COUNT) - 1;
  mp_int_t buf_size_words =
      total_sample_bits / bits_packed_per_word(CAPTURE_PIN_COUNT);
  mp_int_t *captured_buf = malloc(buf_size_words * sizeof(mp_int_t));
  hard_assert(capture_buf);

  bus_ctrl_hw->priority =
      BUSCTRL_BUS_PRIORITY_DMA_W_BITS | BUSCTRL_BUS_PRIORITY_DMA_R_BITS;

  PIO pio = pio0;
  mp_int_t sm = 0;
  mp_int_t dma_chan = 0;

  logic_analyzer_init(pio, sm, CAPTURE_PIN_BASE, CPATURE_PIN_COUNT, 1.f);

  printf("Arming trigger...");
  logic_analyzer_arm(pio, sm, dma_chan, capture_buf, buf_size_words,
                     CAPTURE_PIN_BASE, true);

  gpio_set_function(CAPTURE_PIN_BASE, GPIO_FUNC_PWM);
  gpio_set_function(CAPTURE_PIN_BASE + 1, GPIO_FUNC_PWM);
  // Topmost value of 3: count from 0 to 3 and then wrap, so period is 4 cycles
  pwm_hw->slice[0].top = 3;
  // Divide frequency by two to slow things down a little
  pwm_hw->slice[0].div = 4 << PWM_CH0_DIV_INT_LSB;
  // Set channel A to be high for 1 cycle each period (duty cycle 1/4) and
  // channel B for 3 cycles (duty cycle 3/4)
  pwm_hw->slice[0].cc = (1 << PWM_CH0_CC_A_LSB) | (3 << PWM_CH0_CC_B_LSB);
  // Enable this PWM slice
  pwm_hw->slice[0].csr = PWM_CH0_CSR_EN_BITS;

  // The logic analyser should have started capturing as soon as it saw the
  // first transition. Wait until the last sample comes in from the DMA.
  dma_channel_wait_for_finish_blocking(dma_chan);

  print_capture_buf(capture_buf, CAPTURE_PIN_BASE, CAPTURE_PIN_COUNT,
                    CAPTURE_N_SAMPLES);
}