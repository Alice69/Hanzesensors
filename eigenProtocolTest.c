#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
// output on USB = PD1 = board pin 1
// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
#define UBBRVAL 51

#include <avr/eeprom.h>
#include "AVR_TTC_scheduler.h"


/************************************************************************/
/* EEPROM variables                                                     */
/************************************************************************/
// Settings:
uint8_t EEMEM DEVICE_NAAM [20] = "Naamloos";
uint8_t EEMEM MIN_UITROLSTAND = 2;
uint8_t EEMEM MAX_UITROLSTAND = 8;
uint8_t EEMEM UITROL_TEMPERATUUR = 20;
uint8_t EEMEM OPROL_TEMPERATUUR = 15;
uint8_t EEMEM UITROL_LICHT = 8;
uint8_t EEMEM OPROL_LICHT = 4;
uint8_t EEMEM MODUS = 0;		//0=Automatisch, 1=Handmatig

// Metingen
uint8_t EEMEM TEMPERATUUR;
uint8_t EEMEM LICHT;
uint8_t EEMEM AFSTAND;



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
/* Sensoren Uitlezen                                                    */
/************************************************************************/
void init_adc()
{
	// ref=Vcc, left adjust the result (8 bit resolution),
	// select channel 0 (PC0 = input)
	ADMUX = (1<<REFS0)|(1<<ADLAR);
	// enable the ADC & prescale = 128
	ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
}
uint8_t get_adc_value(uint16_t channel)
{
	ADMUX &= 0xF0;							//Clear the older channel that was read
	ADMUX |= channel;
	ADCSRA |= (1<<ADSC);					// start conversion
	loop_until_bit_is_clear(ADCSRA, ADSC);
	return ADCH;							// 8-bit resolution, left adjusted
}

void meetTemperatuur() {
	uint8_t voltage = (get_adc_value(0) * (5000 / 1024));
	uint8_t temperature = ((voltage * 100) / 1024);
	eeprom_update_byte(&TEMPERATUUR, temperature);
}
void meetLicht() {
	uint8_t lichtsterkte = (get_adc_value(1)*10)/240;
	eeprom_update_byte(&LICHT, lichtsterkte); // Ipv random, sensor uitlezen
}




/************************************************************************/
/* MAIN                                                                 */
/************************************************************************/
int main(void)
{	
	uart_init();
	init_adc();
	SCH_Init_T1();
	_delay_ms(1000);
	
	char command[200];		// buffer for command
	char dataBuffer[10];	// buffer for data
	char stringBuffer[200];	// buffer for sprintf
	
	// Clear EEPROM
	/*for (uint8_t i = 0; i < 512; i++ ) {
		eeprom_update_byte(i, 0);
	}*/
	
	SCH_Add_Task(meetTemperatuur, 0, 4000);
	SCH_Add_Task(meetLicht, 0, 3000);
	SCH_Start();
	
	
	while (1) {
		SCH_Dispatch_Tasks();
		
		ser_readln(command, 200);
		uint8_t ok = 0;
		
		
		/************************************************************************/
		/* Connection:                                                          */
		/************************************************************************/
		if (!strcmp(command, "handshake")) {
			ser_writeln("handshake");
			ok = 1;
		}
		
		if (!strcmp(command, "ping")) {
			ser_writeln("pong");
			ok = 1;
		}
		
		
		/************************************************************************/
		/* Get:                                                                 */
		/************************************************************************/
		// Settings
		if (!strcmp(command, "getNaam")) {
			uint8_t SRAMstring[20];
			eeprom_read_block((void*)SRAMstring , (const void*)DEVICE_NAAM , 20);
			sprintf(stringBuffer, "%s", (char*)SRAMstring);
			ser_writeln(stringBuffer);
			ok = 1;
		}
		
		if(!strcmp(command, "getSettingsTemp")) {
			uint8_t uitrol = eeprom_read_byte(&UITROL_TEMPERATUUR);
			uint8_t oprol = eeprom_read_byte(&OPROL_TEMPERATUUR);
			sprintf(stringBuffer, "%i, %i", uitrol, oprol);
			ser_writeln(stringBuffer);
			ok = 1;
		}

		if(!strcmp(command, "getSettingsLicht")) {
			uint8_t uitrol = eeprom_read_byte(&UITROL_LICHT);
			uint8_t oprol = eeprom_read_byte(&OPROL_LICHT);
			sprintf(stringBuffer, "%i, %i", uitrol, oprol);
			ser_writeln(stringBuffer);
			ok = 1;
		}
		
		if(!strcmp(command, "getUitrolstand")) {
			uint8_t min = eeprom_read_byte(&MIN_UITROLSTAND);
			uint8_t max = eeprom_read_byte(&MAX_UITROLSTAND);
			sprintf(stringBuffer, "%i, %i", min, max);
			ser_writeln(stringBuffer);
			ok = 1;
		}
		
		// Data
		if(!strcmp(command, "getSensorTemp")) {
			uint8_t data = eeprom_read_byte(&TEMPERATUUR);
			sprintf(stringBuffer, "%i", data);
			ser_writeln(stringBuffer);
			ok = 1;
		}
		
		if(!strcmp(command, "getSensorLicht")) {
			uint8_t data = eeprom_read_byte(&LICHT);
			sprintf(stringBuffer, "%i", data);
			ser_writeln(stringBuffer);
			ok = 1;
		}
		
		if(!strcmp(command, "getAfstand")) {
			uint8_t data = 14; // Uitlezen van UltrasonoorSensor
			sprintf(stringBuffer, "%i", data);
			ser_writeln(stringBuffer);
			ok = 1;
		}
		
		if(!strcmp(command, "getModus")) {
			uint8_t data = eeprom_read_byte(&MODUS);
			sprintf(stringBuffer, "%i", data);
			ser_writeln(stringBuffer);
			ok = 1;
		}
		
		
		/************************************************************************/
		/* Set:                                                                 */
		/************************************************************************/
		if (!strcmp(command, "setNaam")) {
			uint8_t StringOfData[20];
			ser_readln(StringOfData, 20);
			eeprom_update_block((const void*)StringOfData , (void*)DEVICE_NAAM, 20);
			//ser_writeln("Name is set"); bevat geen eerste response?
			ok = 1;
		}
		
		if (!strcmp(command, "setTemp")) {		// Moet nog aangepast worden, 2x uitlezen van data(min en max)
			eeprom_update_byte(&OPROL_TEMPERATUUR, rand() % 20);
			eeprom_update_byte(&UITROL_TEMPERATUUR, (rand() % 80) + 20);
			//ser_readln(dataBuffer, 200);
			//uint8_t data = (uint8_t)dataBuffer[0];
			//sprintf(stringBuffer, "Saved: %i", data);
			//ser_writeln("saved bro");
			ok = 1;
		}
		
		if (!strcmp(command, "setLicht")) {		// Moet nog aangepast worden, 2x uitlezen van data(min en max)
			eeprom_update_byte(&OPROL_LICHT, rand() % 20);
			eeprom_update_byte(&UITROL_LICHT, (rand() % 80) + 20);
			//ser_readln(dataBuffer, 200);
			//uint8_t data = (uint8_t)dataBuffer[0];
			//sprintf(stringBuffer, "Saved: %i", data);
			//ser_writeln("saved bro");
			ok = 1;
		}
		
		if (!strcmp(command, "setUitrolstand")) {		// Moet nog aangepast worden, 2x uitlezen van data(min en max)
			eeprom_update_byte(&MIN_UITROLSTAND, rand() % 20);
			eeprom_update_byte(&MAX_UITROLSTAND, (rand() % 80) + 20);
			//ser_readln(dataBuffer, 200);
			//uint8_t data = (uint8_t)dataBuffer[0];
			//sprintf(stringBuffer, "Saved: %i", data);
			//ser_writeln("saved bro");
			ok = 1;
		}
		
		
		/************************************************************************/
		/* Actie:                                                               */
		/************************************************************************/
		if (!strcmp(command, "rolOp")) {
			eeprom_update_byte(&MODUS, 1);
			// Functioncall voor oprollen
			ok = 1;
		}
		if (!strcmp(command, "rolUit")) {
			eeprom_update_byte(&MODUS, 1);
			// Functioncall voor uitrollen
			ok = 1;
		}
		if (!strcmp(command, "setAuto")) {
			eeprom_update_byte(&MODUS, 0);
			ok = 1;
		}

		
		
		/************************************************************************/
		/* OK message:                                                          */
		/************************************************************************/
		if(ok){
			ser_writeln("OK");
		} else {
			ser_writeln("ERR");
		}
	}
}