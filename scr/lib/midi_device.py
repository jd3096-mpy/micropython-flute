from lib.music_const import *
import time

# MIDI命令常量
MIDI_CMD_NOTE_OFF = 0x80
MIDI_CMD_NOTE_ON = 0x90
MIDI_CMD_CONTROL_CHANGE = 0xB0
MIDI_CMD_PROGRAM_CHANGE = 0xC0
MIDI_CMD_PITCH_BEND = 0xE0
MIDI_CMD_SYSTEM_EXCLUSIVE = 0xF0
MIDI_CMD_END_OF_SYSEX = 0xF7
MIDI_CMD_SYSTEM_RESET = 0xFF

class MIDI_DEVICE:
    def __init__(self, types, devices):
        self.device = devices
        self.type = types
        time.sleep(0.1)  

    def send_cmd(self, buffer):
        if self.type == "uart":
            self.device.write(buffer)
        elif self.type == "ble":
            self.device.notify(b'\x80\x80'+buffer)
            print(b'\x80\x80'+buffer)
        else:
            print('type error!')

    def set_instrument(self, channel, bank):
        cmd_control_change = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x00, bank])
        self.send_cmd(cmd_control_change)

        cmd_program_change = bytearray([MIDI_CMD_PROGRAM_CHANGE | (channel & 0x0f), bank])
        self.send_cmd(cmd_program_change)

    def set_note_on(self, channel, pitch, velocity):
        cmd_note_on = bytearray([MIDI_CMD_NOTE_ON | (channel & 0x0f), pitch, velocity])
        self.send_cmd(cmd_note_on)

    def set_note_off(self, channel, pitch):
        cmd_note_off = bytearray([MIDI_CMD_NOTE_OFF | (channel & 0x0f), pitch, 0x00])
        self.send_cmd(cmd_note_off)

    def set_all_notes_off(self, channel):
        cmd_control_change = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x7b, 0x00])
        self.send_cmd(cmd_control_change)

    def set_pitch_bend(self, channel, value):
        value = int(value * 0x3fff / 1023)
        cmd_pitch_bend = bytearray([MIDI_CMD_PITCH_BEND | (channel & 0x0f),
                                    value & 0x7f, (value >> 7) & 0x7f])
        self.send_cmd(cmd_pitch_bend)

    def set_pitch_bend_range(self, channel, value):
        cmd_control_change = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f),
                                        0x65, 0x00, 0x64, 0x00, 0x06, value & 0x7f])
        self.send_cmd(cmd_control_change)

    def set_master_volume(self, level):
        cmd_system_exclusive = bytearray([MIDI_CMD_SYSTEM_EXCLUSIVE,
                                          0x7f, 0x7f, 0x04, 0x01, 0x00, level & 0x7f, MIDI_CMD_END_OF_SYSEX])
        self.send_cmd(cmd_system_exclusive)

    def set_volume(self, channel, level):
        cmd_control_change = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x07, level])
        self.send_cmd(cmd_control_change)

    def set_reverb(self, channel, program, level, delay_feedback):
        cmd_control_change_1 = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x50, program & 0x07])
        self.send_cmd(cmd_control_change_1)

        cmd_control_change_2 = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x5b, level & 0x7f])
        self.send_cmd(cmd_control_change_2)

        if delay_feedback > 0:
            cmd_system_exclusive = bytearray([MIDI_CMD_SYSTEM_EXCLUSIVE,
                                              0x41, 0x00, 0x42, 0x12, 0x40, 0x01, 0x35, delay_feedback & 0x7f, 0x00, MIDI_CMD_END_OF_SYSEX])
            self.send_cmd(cmd_system_exclusive)

    def set_chorus(self, channel, program, level, feedback, chorus_delay):
        cmd_control_change_1 = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x51, program & 0x07])
        self.send_cmd(cmd_control_change_1)

        cmd_control_change_2 = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x5d, level & 0x7f])
        self.send_cmd(cmd_control_change_2)

        if feedback > 0:
            cmd_system_exclusive_1 = bytearray([MIDI_CMD_SYSTEM_EXCLUSIVE,
                                                0x41, 0x00, 0x42, 0x12, 0x40, 0x01, 0x3b, feedback & 0x7f, 0x00, MIDI_CMD_END_OF_SYSEX])
            self.send_cmd(cmd_system_exclusive_1)

        if chorus_delay > 0:
            cmd_system_exclusive_2 = bytearray([MIDI_CMD_SYSTEM_EXCLUSIVE,
                                                0x41, 0x00, 0x42, 0x12, 0x40, 0x01, 0x3c, chorus_delay & 0x7f, 0x00, MIDI_CMD_END_OF_SYSEX])
            self.send_cmd(cmd_system_exclusive_2)

    def set_pan(self, channel, value):
        cmd_control_change = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x0A, value])
        self.send_cmd(cmd_control_change)

    def set_equalizer(self, channel, low_band, med_low_band, med_high_band, high_band,
                      low_freq, med_low_freq, med_high_freq, high_freq):
        cmd_control_change = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x63, 0x37, 0x62, 0x00, 0x06, low_band & 0x7f])
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x01
        cmd_control_change[6] = med_low_band & 0x7f
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x02
        cmd_control_change[6] = med_high_band & 0x7f
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x03
        cmd_control_change[6] = high_band & 0x7f
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x08
        cmd_control_change[6] = low_freq & 0x7f
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x09
        cmd_control_change[6] = med_low_freq & 0x7f
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x0A
        cmd_control_change[6] = med_high_freq & 0x7f
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x0B
        cmd_control_change[6] = high_freq & 0x7f
        self.send_cmd(cmd_control_change)

    def set_tuning(self, channel, fine, coarse):
        cmd_control_change = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x65, 0x00, 0x64, 0x01, 0x06, fine & 0x7f])
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x02
        cmd_control_change[6] = coarse & 0x7f
        self.send_cmd(cmd_control_change)

    def set_vibrate(self, channel, rate, depth, delay):
        cmd_control_change = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x63, 0x01, 0x62, 0x08, 0x06, rate & 0x7f])
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x09
        cmd_control_change[6] = depth & 0x7f
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x0A
        cmd_control_change[6] = delay & 0x7f
        self.send_cmd(cmd_control_change)

    def set_tvf(self, channel, cutoff, resonance):
        cmd_control_change = bytearray([MIDI_CMD_CONTROL_CHANGE | (channel & 0x0f), 0x63, 0x01, 0x62, 0x20, 0x06, cutoff & 0x7f])
        self.send_cmd(cmd_control_change)

        cmd_control_change[4] = 0x21
        cmd_control_change[6] = resonance & 0x7f
        self.send_cmd(cmd_control_change)
