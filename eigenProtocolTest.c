#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
// output on USB = PD1 = board pin 1
// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
#define UBBRVAL 51

#include <avr/eeprom.h>


// EEPROM variables
uint8_t EEMEM MIN_TEMP;
uint8_t EEMEM MAX_TEMP;
uint16_t EEMEM NonVolatileInt;
uint8_t EEMEM DEVICE_NAME [10] = "KAAS";


/************************************************************************/
/* Seriële verbinding                                                   */
/************************************************************************/
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

char ser_read() {
	loop_until_bit_is_set(UCSR0A, RXC0);
	return UDR0;
}

void ser_readln(char *line, uint8_t bufsize) {
	uint8_t p=0;
	char c;
	do {
		c=ser_read();
		if (c!='\n') {
			line[p++]=c;
		}
		line[p]='\0';
	} while ((c!='\n') && (p<bufsize-1));
}



/************************************************************************/
/* MAIN                                                                 */
/************************************************************************/
int main(void)
{	
	uart_init();
	_delay_ms(1000);
	
	char command[200];		// buffer for command
	char dataBuffer[10];	// buffer for data
	char stringBuffer[200];	// buffer for sprintf
	
	while (1) {
		ser_readln(command, 200);
		uint8_t ok = 0;
		
		if (!strcmp(command, "handshake")) {
			ser_writeln("pizza");
			ok = 1;
		}
		
		if (!strcmp(command, "ping")) {
			ser_writeln("pong");
			ok = 1;
		}
		
		if (!strcmp(command, "setMinMaxTemp")) {
			eeprom_update_byte(&MIN_TEMP, rand() % 20);
			eeprom_update_byte(&MAX_TEMP, (rand() % 80) + 20);
			//ser_readln(dataBuffer, 200);
			//uint8_t data = (uint8_t)dataBuffer[0];
			//sprintf(stringBuffer, "Saved: %i", data);
			ser_writeln("saved bro");
			ok = 1;
		}
		
		if(!strcmp(command, "getMinMaxTemp")) {
			uint8_t min = eeprom_read_byte(&MIN_TEMP);
			uint8_t max = eeprom_read_byte(&MAX_TEMP);
			sprintf(stringBuffer, "Min: %i, max: %i", min, max);
			ser_writeln(stringBuffer);
			ok = 1;
		}
		
		if (!strcmp(command, "setName")) {
			uint8_t StringOfData[10];
			ser_readln(StringOfData, 10);
			eeprom_update_block((const void*)StringOfData , (void*)DEVICE_NAME, 10);
			ser_writeln("Name is set");
			ok = 1;
		}
		
		if (!strcmp(command, "getName")) {
			uint8_t SRAMstring[10];
			eeprom_read_block((void*)SRAMstring , (const void*)DEVICE_NAME , 10);
			sprintf(stringBuffer, "Get name: %s", (char*)SRAMstring);
			ser_writeln(stringBuffer);
			ok = 1;
		}			
		
		if(ok){
			ser_writeln("OK");
		} else {
			ser_writeln("ERR");
		}
	}
}