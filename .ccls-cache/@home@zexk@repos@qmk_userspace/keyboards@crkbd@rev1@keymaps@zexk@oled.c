#include QMK_KEYBOARD_H

#ifdef OLED_ENABLE
static void render_logo(void) {
  static const char PROGMEM logo[] = {
    };
    oled_write_raw_P(logo, false);
}

static void render_status(void) {
    char wpm_str[10];
    sprintf(wpm_str, " %03d", get_current_wpm());
    oled_write_ln(" wpm", false);
    oled_write_ln(wpm_str, false);

    oled_write_ln(" lyr", false);
    switch (get_highest_layer(layer_state)) {
        case 0:
            oled_write_ln(" bse", false);
            break;
        case 1:
            oled_write_ln(" num", false);
            break;
        case 2:
            oled_write_ln(" sym", false);
            break;
        case 3:
            oled_write_ln(" nav", false);
            break;
        case 4:
            oled_write_ln(" sys", false);
            break;
        default:
            oled_write_ln(" und", false);
            break;
        }

  static const char PROGMEM tux[] = {
        0x99, 0x9A, 0xB9, 0xBA
    };
    oled_write_raw(tux, false);
}

oled_rotation_t oled_init_user(oled_rotation_t rotation) {
        if(is_keyboard_master()){
        return OLED_ROTATION_270;
        } else {
        return OLED_ROTATION_0;
        }
}

bool oled_task_user(void) {
    if (is_keyboard_master()) {
        render_status();
    } else {
        render_logo();
    }
    return false;
}
#endif
