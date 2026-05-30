ORG     $8000           *DIR DE INICIO
        LDS     #$03FF          *APUNTADOR DE STAK

*Definición de registros y direcciones de E/S
DDRA    EQU $1000
DDRG    EQU $1008
PORTG   EQU $100A
BAUD    EQU $102B
SCCR2   EQU $102D
SCCR1   EQU $102C
DDRD    EQU $1009

        LDAA    #$00            *CONFIG TODO EL PUERTO A COMO ENTRADAS
        STAA    DDRA            *EL PUERTO A

        LDAA    #$FF            *CONFIG TODO EL PUERTO G COMO ENTRADAS
        STAA    DDRG            *EL PUERTO G

        LDAA    #$00            *SE PONE PUERTO G EN CEROS
        STAA    PORTG

        LDD     #$302C          *CONFIGURA PUERTO SERIAL
        STAA    BAUD            *BAUD 9600 para cristal de 8MHz
        STAB    SCCR2           *HABILITA RX Y TX PERO INTERRUPCN SOLO RX
        LDAA    #$00
        STAA    SCCR1           *8 BITS

        LDAA    #$FE            *CONFIG PUERTO D COMO SALIDAS (EXCEPTO PD0)
        STAA    DDRD            *SEA ENABLE DEL DISPLAY PD4 Y RS PD3

        END