#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
// output on USB = PD1 = board pin 1
// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
#define UBBRVAL 51


#define HIGH 0x1
#define LOW  0x0

#define TRIGPIN 0	// Pin 8 B0
#define ECHOPIN 1	// Pin 9 B1
#define LICHTPIN 2



// UltrasoneSensor
void timer_init()
{
	//Zet de pre-scaler op 1024
	TCCR1B = (1<<CS12)|(1<<CS10);
}
void write(uint8_t pin, uint8_t val)
{
	if (val == LOW) {
		PORTB &= ~(_BV(pin)); // clear bit
	} else {
		PORTB |= _BV(pin); // set bit
	}
}

uint32_t pulseDuration(void){	
	// Clear trigger
	write(TRIGPIN, LOW);
	_delay_us(2);
	
	// Set trigger for 10 microseconds
	write(TRIGPIN, HIGH);
	TCNT1 = 0;
	_delay_us(10);
	write(TRIGPIN, LOW);
	
	while(1)
	{
		// Check voor echo
		if( PINB & (1 << ECHOPIN) )
		{
			return TCNT1;
		}
		// Timer overflow
		if( TIFR1 & _BV(TOV1) )
		{
			ser_writeln("Overflow");
			TIFR1 |= ~_BV(0);
			return TCNT0;
		}
	}
	
	//uint32_t duration_cm = duration /29 / 2;
}




// Serial
void uart_init()
{
	// set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable transmitter
	UCSR0B = _BV(RXEN0) | _BV(TXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
}

void ser_write(uint8_t data)
{
	// wait for an empty transmit buffer
	// UDRE is set when the transmit buffer is empty
	loop_until_bit_is_set(UCSR0A, UDRE0);
	// send the data
	UDR0 = data;
}

void ser_writeln(const char* line) {
	for (size_t i = 0; i<strlen(line); i++)
	{
		ser_write(line[i]);
	}
	ser_write('\n');
}




int main(void)
{
	uart_init();
	timer_init();
	_delay_ms(1000);
	
	// Ledje
	DDRD |= (1 << LICHTPIN);	// 2 is output
	
	// UltrasoneSensor
	DDRB |= (1 << TRIGPIN);	// 8 is output, trigger
	DDRB &= ~(1 << ECHOPIN);	// 9 is input, echo
	
	char buffer[200];
	
    while(1)
    {
		PORTD ^= (1 << LICHTPIN);
		sprintf(buffer, "Afstand: %i", pulseDuration());
		ser_writeln(buffer);
		_delay_ms(500);
    }
}