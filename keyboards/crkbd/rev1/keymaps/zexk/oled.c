#include QMK_KEYBOARD_H
#include "avatar.h"

#ifdef OLED_ENABLE

// ---- avatar tuning ----------------------------------------------------------
#define AVATAR_HAPPY_WPM    18   // >= this -> happy
#define AVATAR_EXCITED_WPM  55   // >= this -> excited (arms up)
#define AVATAR_SLEEP_MS     8000 // idle this long -> sleepy + zzz
#define AVATAR_BLINK_OPEN   3200 // eyes-open stretch between blinks (ms)
#define AVATAR_BLINK_SHUT   140  // blink duration (ms)

// Vertically centred figure in the 32x128 logical canvas (ROTATION_270).
#define AVATAR_TOP ((128 - (HEAD_H + BODY_H)) / 2)

// Blit a 1bpp row-major (MSB-first) PROGMEM sprite at (x0,y0).
static void blit(const uint8_t *sprite, uint8_t w, uint8_t h, uint8_t x0, uint8_t y0) {
    uint8_t bpr = (w + 7) >> 3;
    for (uint8_t y = 0; y < h; y++) {
        for (uint8_t x = 0; x < w; x++) {
            uint8_t byte = pgm_read_byte(&sprite[y * bpr + (x >> 3)]);
            oled_write_pixel(x0 + x, y0 + y, (byte >> (7 - (x & 7))) & 1);
        }
    }
}

// Mood frames: head id picks the expression, cheer raises the arms.
enum avatar_state { A_SLEEP, A_NEUTRAL, A_BLINK, A_HAPPY, A_EXCITED };

static void render_avatar(void) {
    static uint8_t  drawn       = 0xFF;
    static uint32_t last_active = 0;
    static uint32_t blink_at    = 0;
    static bool     eyes_shut   = false;

    uint8_t  wpm = get_current_wpm();
    uint32_t now = timer_read32();
    if (wpm > 0) last_active = now;

    uint8_t state;
    if (timer_elapsed32(last_active) > AVATAR_SLEEP_MS) {
        state = A_SLEEP;
    } else if (wpm >= AVATAR_EXCITED_WPM) {
        state = A_EXCITED;
    } else if (wpm >= AVATAR_HAPPY_WPM) {
        state = A_HAPPY;
    } else {
        if (timer_expired32(now, blink_at)) {
            eyes_shut = !eyes_shut;
            blink_at  = now + (eyes_shut ? AVATAR_BLINK_SHUT : AVATAR_BLINK_OPEN);
        }
        state = eyes_shut ? A_BLINK : A_NEUTRAL;
    }

    if (state == drawn) return;  // only redraw on change
    drawn = state;

    const uint8_t *head;
    const uint8_t *body = avatar_body_idle;
    switch (state) {
        case A_SLEEP:   head = avatar_head_sleep;   break;
        case A_BLINK:   head = avatar_head_blink;   break;
        case A_HAPPY:   head = avatar_head_happy;   break;
        case A_EXCITED: head = avatar_head_excited; body = avatar_body_cheer; break;
        default:        head = avatar_head_neutral; break;
    }

    oled_clear();
    blit(head, AVATAR_W, HEAD_H, 0, AVATAR_TOP);
    blit(body, AVATAR_W, BODY_H, 0, AVATAR_TOP + HEAD_H);
}

// ---- master status ----------------------------------------------------------
static void render_status(void) {
    // Manual 3-digit formatting avoids pulling in sprintf/vfprintf (~1.3KB flash).
    uint8_t wpm = get_current_wpm();
    char buf[5] = {' ',
                   (char)('0' + (wpm / 100) % 10),
                   (char)('0' + (wpm / 10) % 10),
                   (char)('0' + wpm % 10),
                   0};
    oled_write_ln(" wpm", false);
    oled_write_ln(buf, false);

    oled_write_ln(" lyr", false);
    switch (get_highest_layer(layer_state)) {
        case 0:  oled_write_ln(" bse", false); break;
        case 1:  oled_write_ln(" num", false); break;
        case 2:  oled_write_ln(" sym", false); break;
        case 3:  oled_write_ln(" nav", false); break;
        case 4:  oled_write_ln(" sys", false); break;
        default: oled_write_ln(" und", false); break;
    }
}

oled_rotation_t oled_init_user(oled_rotation_t rotation) {
    // Both halves vertical; slave matches master so the avatar stands upright.
    return OLED_ROTATION_270;
}

bool oled_task_user(void) {
    if (is_keyboard_master()) {
        render_status();
    } else {
        render_avatar();
    }
    return false;
}
#endif
