#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
#include <string.h>
#include <stdio.h>
// output on USB = PD1 = board pin 1
// datasheet p.190; F_OSC = 16 MHz & baud rate = 19.200
#define UBBRVAL 51

#include <avr/eeprom.h>
#include "AVR_TTC_scheduler.h"
#include "Ultrasoon.h"

/************************************************************************/
/* EEPROM variables                                                     */
/************************************************************************/
// Settings:
uint8_t EEMEM DEVICE_NAAM [20];
uint8_t EEMEM MIN_UITROLSTAND;
uint8_t EEMEM MAX_UITROLSTAND;
uint8_t EEMEM UITROL_TEMPERATUUR;
uint8_t EEMEM OPROL_TEMPERATUUR;
uint8_t EEMEM UITROL_LICHT;
uint8_t EEMEM OPROL_LICHT;
uint8_t EEMEM MODUS;		//0=Automatisch, 1=Handmatig

// Metingen
uint8_t EEMEM TEMPERATUUR;
uint8_t EEMEM LICHT;
uint16_t EEMEM AFSTAND;

/************************************************************************/
/* Ultrasoon variables                                                  */
/************************************************************************/

volatile uint32_t overFlowCounter = 0;
volatile uint32_t trig_counter = 0;
volatile uint32_t no_of_ticks = 0;

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

void init_afstandssensor() {
	TRIG_OUTPUT_MODE();     // Set Trigger pin as output
	ECHO_INPUT_MODE();      // Set Echo pin as input
}

void trigger_sonar(){
	TRIG_LOW();             // Clear pin before setting it high
	_delay_us(2);           // Clear to zero and give time for electronics to set
	TRIG_HIGH();            // Set pin high
	_delay_us(12);          // Send high pulse for minimum 10us
	TRIG_LOW();             // Clear pin
	_delay_us(1);           // Delay not required, but just in case...
}

ISR(TIMER0_OVF_vect){   // Timer0 overflow interrupt
	overFlowCounter++;
	TCNT0=0;
}

uint16_t lees_afstandssensor(){
	uint16_t dist_in_cm = 0;
	trigger_sonar();                    // send a 10us high pulse

	TCNT0=0;                            // reset timer
	TCCR0B |= (1<<CS10);              // start 16 bit timer with no prescaler

	TIMSK0 = 1<<TOIE0; // enable overflow interrupt on timer0
	overFlowCounter=0;                  // reset overflow counter

	while(!(ECHO_PIN & (1<<ECHO_BIT))){   // while echo pin is still low
		trig_counter++;
		uint32_t max_response_time = SONAR_TIMEOUT;
		if (trig_counter > max_response_time){   // SONAR_TIMEOUT
			return TRIG_ERROR;
		}
	}

	TCNT0=0;                            // reset timer
	TCCR0B |= (1<<CS10);              // start 16 bit timer with no prescaler
	TIMSK0 = 1<<TOIE0;					// enable overflow interrupt on timer0
	overFlowCounter=0;                  // reset overflow counter

	while((ECHO_PIN & (1<<ECHO_BIT))){    // while echo pin is still high
		if (((overFlowCounter*TIMER_MAX)+TCNT0) > SONAR_TIMEOUT){
			return ECHO_ERROR;          // No echo within sonar range
		}
	};

	TCCR0B = 0x00;                      // stop 16 bit timer with no prescaler
	TIMSK0=0;
	no_of_ticks = ((overFlowCounter*TIMER_MAX)+TCNT0);  // counter count
	dist_in_cm = (no_of_ticks/(CONVERT_TO_CM*CYCLES_PER_US));   // distance in cm
	return (dist_in_cm);
}

void meetafstand() {
	uint16_t afstand = lees_afstandssensor();
	if (afstand > 20) {
		return;
	}
	afstand = (afstand * 10) / 15;

	uint8_t proces = 0;

	if (TEMPERATUUR > 16 || LICHT > 8) {
		proces = 1; // Moet uitrollen
	}
	if (TEMPERATUUR < 12 || LICHT < 4) {
		proces = 0; // Moet oprollen
	}

	if (proces == 1)
	{
		if (afstand > 8){
			roodLampje();
		}
		else{
			geelLampje();
		}
	}else{
		if (afstand <= 2) {
			groenLampje();
		}
		else {
			geelLampje();
		}


	}

	eeprom_update_word(&AFSTAND, afstand); // Ipv random, sensor uitlezen
}


/************************************************************************/
/* Ledjes                                                               */
/************************************************************************/

void roodLampje(){
	PORTD |= (1 << PD4);	// Rood aan
	PORTD &= ~(1 << PD3);	// Geel uit
	PORTD &= ~(1 << PD2);	// Groen uit
}
void groenLampje(){
	PORTD |= (1 << PD2);	// Groen aan
	PORTD &= ~(1 << PD3);	// Geel uit
	PORTD &= ~(1 << PD4);	// Rood uit
}
void geelLampje(){
	PORTD ^= (1 << PD3);	// Geel aan
	PORTD &= ~(1 << PD4);	// Rood uit
	PORTD &= ~(1 << PD2);	// Groen uit
}




/************************************************************************/
/* MAIN                                                                 */
/************************************************************************/
int main(void)
{

	DDRB=0;
	DDRD=0xFF;
	uart_init();
	init_adc();

	SCH_Init_T1();
	init_afstandssensor();
	//sei();
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
	SCH_Add_Task(meetafstand, 0, 100);
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
			uint16_t data = eeprom_read_byte(&AFSTAND); // Uitlezen van UltrasonoorSensor
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
			ok = 1;
		}

		if (!strcmp(command, "setTemp")) {
			uint8_t StringOfData[20];
			ser_readln(StringOfData, 20);
			eeprom_update_byte(&UITROL_TEMPERATUUR, StringOfData);
			ser_readln(StringOfData, 20);
			eeprom_update_byte(&OPROL_TEMPERATUUR, StringOfData);
			ok = 1;
		}

		if (!strcmp(command, "setLicht")) {
			uint8_t StringOfData[20];
			ser_readln(StringOfData, 20);
			eeprom_update_byte(&UITROL_LICHT, StringOfData);
			ser_readln(StringOfData, 20);
			eeprom_update_byte(&OPROL_LICHT, StringOfData);
			ok = 1;
		}

		if (!strcmp(command, "setUitrolstand")) {
			uint8_t StringOfData[20];
			ser_readln(StringOfData, 20);
			eeprom_update_byte(&MIN_UITROLSTAND, StringOfData);
			ser_readln(StringOfData, 20);
			eeprom_update_byte(&MAX_UITROLSTAND, StringOfData);
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