/*
 * Ultrasoon.h
 *
 * Created: 13-11-2017 19:28:42
 *  Author: sanne
 */ 

/*
 * defineultra.c
 *
 * Created: 13-11-2017 19:25:58
 *  Author: sanne
 */ 

/*...- . . .-. --- -... --- -
 * Define Ports and Pins as required
 * Modify Maximum response time and delay as required
 * MAX_RESP_TIME : default: 300
 * DELAY_BETWEEN_TESTS : default: 50
 */
#define TRIG_DDR    DDRB            // Trigger Port
#define TRIG_PORT   PORTB
#define TRIG_PIN    PINB
#define TRIG_BIT    PD0             // Trigger Pin
 
#define ECHO_DDR    DDRB            // Echo Port
#define ECHO_PORT   PORTB
#define ECHO_PIN    PINB
#define ECHO_BIT    PD1             // Echo Pin
 
// Speed of sound
// Default: 343 meters per second in dry air at room temperature (~20C)
#define SPEED_OF_SOUND  343
#define MAX_SONAR_RANGE 10          // This is trigger + echo range (in meters) for SR04
#define DELAY_BETWEEN_TESTS 500     // Echo canceling time between sampling. Default: 500us
#define TIMER_MAX 255             // 65535 for 16 bit timer and 255 for 8 bit timer
 
/* ...- . . .-. --- -... --- -
 * Do not change anything further unless you know what you're doing
 * */
#define TRIG_ERROR -1
#define ECHO_ERROR -2
 
#define CYCLES_PER_US (F_CPU/1000000)// instructions per microsecond
#define CYCLES_PER_MS (F_CPU/1000)      // instructions per millisecond
// Timeout. Decreasing this decreases measuring distance
// but gives faster sampling
#define SONAR_TIMEOUT ((F_CPU*MAX_SONAR_RANGE)/SPEED_OF_SOUND)
 
#define TRIG_INPUT_MODE() TRIG_DDR &= ~(1<<TRIG_BIT)
#define TRIG_OUTPUT_MODE() TRIG_DDR |= (1<<TRIG_BIT)
#define TRIG_LOW() TRIG_PORT &= ~(1<<TRIG_BIT)
#define TRIG_HIGH() TRIG_PORT |=(1<<TRIG_BIT)
 
#define ECHO_INPUT_MODE() ECHO_DDR &= ~(1<<ECHO_BIT)
#define ECHO_OUTPUT_MODE() ECHO_DDR |= (1<<ECHO_BIT)
#define ECHO_LOW() ECHO_PORT &= ~(1<<ECHO_BIT)
#define ECHO_HIGH() ECHO_PORT |=(1<<ECHO_BIT)
 
#define CONVERT_TO_CM ((10000*2)/SPEED_OF_SOUND)    // or simply 58