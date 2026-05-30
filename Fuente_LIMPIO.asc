      ORG    $8000          *DIRECCION DE INICIO

*DEFINICION DE VARIABLES
PORTA EQU $1000
PORTB EQU $1002
CONT  EQU $50

      LDS    #$03FF         *INICIALIZA STACK

      LDAA   #$FF           *INMEDIATO: CARGA $FF EN A
      LDAB   #$00           *INMEDIATO: CARGA $00 EN B
      STAA   PORTA          *EXTENDIDO: GUARDA A EN PORTA
      STAB   PORTB          *EXTENDIDO: GUARDA B EN PORTB

      LDAA   #$05           *INMEDIATO: CARGA CONTADOR
      STAA   CONT           *DIRECTO: GUARDA EN $50

      NOP                   *INHERENTE
      INX                   *INHERENTE
      INY                   *INHERENTE
      DEX                   *INHERENTE

CICLO
      NOP                   *INHERENTE
      NOP                   *INHERENTE
      DECA                  *INHERENTE: DECREMENTA A

      END
