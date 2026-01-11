#include <avr/interrupt.h>

#define BUF_SIZE 1024
volatile byte buffer[BUF_SIZE];
volatile int head = 0, tail = 0;

void setup() {
  Serial.begin(250000);
  pinMode(9, OUTPUT);

  // Timer 1: 62.5kHz Carrier Generation
  TCCR1A = _BV(COM1A1) | _BV(WGM10);
  TCCR1B = _BV(WGM12) | _BV(CS10);

  // Timer 2: 8kHz Sample Clock with Adaptive Sync
  cli();
  TCCR2A = _BV(WGM21); 
  TCCR2B = _BV(CS21) | _BV(CS20); 
  OCR2A = 62; 
  TIMSK2 |= _BV(OCIE2A);
  sei();
}

ISR(TIMER2_COMPA_vect) {
  int count = (head >= tail) ? (head - tail) : (BUF_SIZE - tail + head);

  if (count > 0) {
    OCR1A = buffer[tail];
    tail = (tail + 1) % BUF_SIZE;

    // Adjust playback speed based on buffer fullness
    if (count > 600) OCR2A = 60;      
    else if (count < 200) OCR2A = 64; 
    else OCR2A = 62;
  } else {
    OCR1A = 128; // Center value for silence
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