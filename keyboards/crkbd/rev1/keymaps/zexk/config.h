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

// Persistent defaults: single pressed key lights up (reactive), umbra accent.
// Applied on EEPROM reset (EE_CLR in _SYS, or bootmagic).
// Colour = umbra `iris` accent #b07bbc hue, saturation punched up so the
// per-key LEDs read as vivid plum instead of pale lavender (faithful: sat 88).
#define RGB_MATRIX_DEFAULT_MODE RGB_MATRIX_SOLID_REACTIVE_SIMPLE
#define RGB_MATRIX_DEFAULT_HUE 205
#define RGB_MATRIX_DEFAULT_SAT 200
#define RGB_MATRIX_DEFAULT_VAL 200
#endif
