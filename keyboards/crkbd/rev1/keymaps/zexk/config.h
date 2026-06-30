#pragma once

//#define USE_MATRIX_I2C

#define MASTER_RIGHT

#define TAPPING_TERM 200
#define PERMISSIVE_HOLD

// Sync WPM master -> slave so the left-half avatar can react to typing speed.
#define SPLIT_WPM_ENABLE

#ifdef RGB_MATRIX_ENABLE
#define RGB_MATRIX_KEYPRESSES
#define RGB_MATRIX_SLEEP

#define ENABLE_RGB_MATRIX_SOLID_REACTIVE_SIMPLE

// Persistent defaults: single pressed key lights up (reactive), purple hue.
// Applied on EEPROM reset (EE_CLR in _SYS, or bootmagic).
#define RGB_MATRIX_DEFAULT_MODE RGB_MATRIX_SOLID_REACTIVE_SIMPLE
#define RGB_MATRIX_DEFAULT_HUE 191   // ~violet/purple (0-255 wheel)
#define RGB_MATRIX_DEFAULT_SAT 255
#define RGB_MATRIX_DEFAULT_VAL 200
#endif
