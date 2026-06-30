#include QMK_KEYBOARD_H

#include "oled.c"
#include "keymap.h"

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [_BASE] = LAYOUT_split_3x6_3(
        //,-----------------------------------------------------.    ,-----------------------------------------------------.
        KC_TAB,  KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,         KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,    KC_BSLS,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
        KC_ESC,  LGUI_T(KC_A), LALT_T(KC_S), LSFT_T(KC_D), LCTL_T(KC_F), KC_G,   KC_H,    RCTL_T(KC_J), RSFT_T(KC_K), LALT_T(KC_L), KC_SCLN, KC_BSPC,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
        KC_LSFT, KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,         KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH, KC_DEL,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
                           KC_LCTL, MO(_SYM), KC_SPC,               KC_ENT,  MO(_NUM), KC_BSPC),

    [_NUM] = LAYOUT_split_3x6_3(
        //,-----------------------------------------------------.    ,-----------------------------------------------------.
        KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,   KC_F6,        KC_F7,   KC_F8,   KC_F9,   KC_F10,  KC_F11,  KC_F12,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
        KC_ESC,  KC_1,    KC_2,    KC_3,    KC_4,    KC_5,         KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    KC_BSPC,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
        KC_LSFT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,     XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
                           KC_LGUI, MO(_NAV), KC_SPC,               KC_ENT,  _______, KC_BSPC),

    [_SYM] = LAYOUT_split_3x6_3(
        //,-----------------------------------------------------.    ,-----------------------------------------------------.
        KC_GRV,  KC_QUOT, KC_LPRN, KC_LBRC, KC_LCBR, KC_MINS,     KC_PLUS, KC_RCBR, KC_RBRC, KC_RPRN, KC_EQUAL, KC_PIPE,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
        KC_LCTL, KC_EXLM, KC_AT,   KC_HASH, KC_DLR,  KC_PERC,     KC_CIRC, KC_AMPR, KC_ASTR, KC_BSLS, KC_GRV,  KC_BSPC,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
        KC_LSFT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC_SLSH,     KC_UNDS, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
                           KC_LGUI, _______, KC_SPC,                KC_ENT,  MO(_NAV), KC_BSPC),

    [_NAV] = LAYOUT_split_3x6_3(
        //,-----------------------------------------------------.    ,-----------------------------------------------------.
        XXXXXXX, XXXXXXX, KC_PGUP, KC_HOME, XXXXXXX, XXXXXXX,     XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
        KC_LCTL, XXXXXXX, KC_PGDN, KC_END,  XXXXXXX, XXXXXXX,     KC_LEFT, KC_DOWN, KC_UP,   KC_RGHT, XXXXXXX, KC_DEL,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
        KC_LSFT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,     XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
                           KC_LGUI, _______, KC_SPC,                MO(_SYS), _______, KC_BSPC),

    [_SYS] = LAYOUT_split_3x6_3(
        //,-----------------------------------------------------.    ,-----------------------------------------------------.
        QK_BOOT, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,     XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
        RM_TOGG, RM_HUEU, RM_SATU, RM_VALU, RM_SPDU, XXXXXXX,     KC_MPRV, KC_VOLD, KC_MPLY, KC_VOLU, KC_MNXT, XXXXXXX,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
        RM_NEXT, RM_HUED, RM_SATD, RM_VALD, RM_SPDD, XXXXXXX,     XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,
        //|--------+--------+--------+--------+--------+--------|    |--------+--------+--------+--------+--------+--------|
                           KC_LGUI, _______, KC_SPC,                KC_ENT,  _______, KC_BSPC)
};
