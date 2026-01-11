#include <avr/interrupt.h>

#define BUF_SIZE 1024
volatile byte buffer[BUF_SIZE];
volatile int head = 0;
volatile int tail = 0;

void setup() {
  Serial.begin(250000); 
  pinMode(9, OUTPUT);

  // Timer 1: 62.5kHz Carrier
  TCCR1A = _BV(COM1A1) | _BV(WGM10);
  TCCR1B = _BV(WGM12) | _BV(CS10);

  // Timer 2: Variable Sample Clock
  cli();
  TCCR2A = _BV(WGM21); // CTC
  TCCR2B = _BV(CS21) | _BV(CS20); // 32 Prescaler
  OCR2A = 62; // Default 8kHz
  TIMSK2 |= _BV(OCIE2A);
  sei();
}

ISR(TIMER2_COMPA_vect) {
  int count = (head >= tail) ? (head - tail) : (BUF_SIZE - tail + head);

  if (count > 0) {
    OCR1A = buffer[tail];
    tail = (tail + 1) % BUF_SIZE;

    // If buffer is getting too full, speed up playback (decrease OCR2A)
    // If buffer is too empty, slow down (increase OCR2A)
    if (count > 600) OCR2A = 60;
    else if (count < 200) OCR2A = 64;
    else OCR2A = 62;
  } else {
    OCR1A = 128; // Silence
  }
}

void loop() {
  while (Serial.available()) {
    int nextHead = (head + 1) % BUF_SIZE;
    if (nextHead != tail) {
      buffer[head] = Serial.read();
      head = nextHead;
    }
  }
}