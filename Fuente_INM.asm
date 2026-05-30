      *DIRECCIONAMIENTO INMEDIATO

      ORG $8000

      LDAA   #$45           *INMEDIATO: CARGA $45 EN A
      LDAB   #11            *INMEDIATO: CARGA 11 EN B
      LDaA   #'k            *INMEDIATO: CARGA ASCII k EN A
      LDD    #$1789         *INMEDIATO: CARGA $1789 EN D
      ldx    #1531          *INMEDIATO: CARGA 1531 EN X
      addA   #$7C           *INMEDIATO: SUMA $7C A A
      Anda   #$F0           *INMEDIATO: AND $F0 CON A
      LDY    #$ABCD         *INMEDIATO: CARGA $ABCD EN Y

      END
