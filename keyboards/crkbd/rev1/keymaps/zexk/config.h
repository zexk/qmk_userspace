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
#endif
