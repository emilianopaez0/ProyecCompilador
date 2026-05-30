      *DIRECCIONAMIENTO RELATIVO

      ORG $8000

INICIO
      LDX    #1789          *CARGA CONTADOR EN X
CICLO
      NOP                   *INHERENTE
      nop                   *INHERENTE
      NOP                   *INHERENTE
      NoP                   *INHERENTE
      NOP                   *INHERENTE
      Dex                   *DECREMENTA X
      JMP    INICIO         *SALTA A INICIO

      END
